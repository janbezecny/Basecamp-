// Entry point: an OAuth-protected remote MCP server that Claude adds as a custom connector.
import { GrantType, OAuthError, OAuthProvider } from "@cloudflare/workers-oauth-provider";
import { createMcpHandler } from "agents/mcp/server";
import { BasecampAuthError, refreshAccessToken, type Props } from "./basecamp";
import { authHandler } from "./auth";
import { createServer } from "./tools";

const DAY = 24 * 60 * 60;

const mcpHandler = {
  fetch(request: Request, env: Env, ctx: ExecutionContext<Props>): Promise<Response> {
    const props = ctx.props;
    return createMcpHandler(() => createServer(props), {
      route: "/mcp",
      // Every request here already carries a valid bearer token, so accept whichever
      // hostname the Worker is served on (workers.dev or a custom domain).
      allowedHostnames: [new URL(request.url).hostname],
    })(request, env, ctx);
  },
};

// The provider needs its own public URL as the token audience; build one per origin.
const providers = new Map<string, OAuthProvider<Env>>();

function provider(origin: string): OAuthProvider<Env> {
  let instance = providers.get(origin);
  if (!instance) {
    instance = new OAuthProvider<Env>({
      apiRoute: "/mcp",
      apiHandler: mcpHandler as any,
      defaultHandler: authHandler as any,
      authorizeEndpoint: "/authorize",
      tokenEndpoint: "/oauth/token",
      clientRegistrationEndpoint: "/oauth/register",
      clientIdMetadataDocumentEnabled: true,
      resourceMetadata: { resource: `${origin}/mcp`, authorization_servers: [origin], resource_name: "Basecamp" },
      accessTokenTTL: 60 * 60,
      // Keep the connection for as long as Claude keeps using it.
      refreshTokenTTL: 90 * DAY,
      refreshTokenIdleTTL: 90 * DAY,
      tokenExchangeCallback: async ({ grantType, props, env }) => {
        if (grantType !== GrantType.REFRESH_TOKEN) return;
        const current = props as Props;
        // Basecamp access tokens last two weeks; renew them once fewer than two days remain.
        if (current.expiresAt - Date.now() / 1000 > 2 * DAY) return;
        try {
          const token = await refreshAccessToken(env, current.refreshToken, `${origin}/callback`);
          const next: Props = {
            ...current,
            accessToken: token.access_token,
            refreshToken: token.refresh_token ?? current.refreshToken,
            expiresAt: Math.floor(Date.now() / 1000) + (token.expires_in ?? 14 * DAY),
          };
          return { accessTokenProps: next, newProps: next };
        } catch (error) {
          if (error instanceof BasecampAuthError && error.status >= 400 && error.status < 500) {
            throw new OAuthError("invalid_grant", { description: "Přístup do Basecampu byl odvolán." });
          }
          throw new OAuthError("temporarily_unavailable", { description: "Basecamp je nedostupný.", statusCode: 503 });
        }
      },
    });
    providers.set(origin, instance);
  }
  return instance;
}

export default {
  fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    return provider(new URL(request.url).origin).fetch(request, env, ctx);
  },
} satisfies ExportedHandler<Env>;
