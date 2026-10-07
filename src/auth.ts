// The connector's own sign-in pages: consent, then the hand-off to Basecamp and back.
import {
  AuthorizationError,
  CimdFetchError,
  authorizationErrorRedirect,
  type ConsentDescription,
  type OAuthHelpers,
} from "@cloudflare/workers-oauth-provider";
import { authorizeUrl, exchangeCode, fetchAuthorization, type Props } from "./basecamp";

type AuthEnv = Env & { OAUTH_PROVIDER: OAuthHelpers };

const escape = (value: string) => value.replace(/[&<>"']/g, (char) => `&#${char.charCodeAt(0)};`);

export const callbackUrl = (request: Request) => new URL("/callback", request.url).toString();

function page(title: string, body: string, status = 200, headers = new Headers()): Response {
  headers.set("Content-Type", "text/html; charset=utf-8");
  const html = `<!doctype html>
<html lang="cs">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${escape(title)}</title>
<style>
  :root { color-scheme: light dark; }
  body { font: 16px/1.5 system-ui, sans-serif; max-width: 34rem; margin: 3rem auto; padding: 0 1rem; }
  .card { border: 1px solid #8884; border-radius: 12px; padding: 1.5rem; }
  .warn { background: #f5a62322; border-left: 4px solid #f5a623; padding: .5rem .75rem; }
  button { font: inherit; padding: .6rem 1.2rem; border-radius: 8px; border: 1px solid #8886; cursor: pointer; }
  button.primary { background: #1d6b3a; color: #fff; border-color: #1d6b3a; }
</style>
</head>
<body><div class="card">${body}</div></body>
</html>`;
  return new Response(html, { status, headers });
}

function consentPage(details: ConsentDescription, handle: string, headers: Headers): Response {
  const name = escape(details.clientName);
  const origin = details.clientDomain
    ? `Aplikaci vydává <strong>${escape(details.clientDomain)}</strong>.`
    : "Aplikace se zaregistrovala sama, její název není ověřený.";
  return page(
    `Povolit ${details.clientName}`,
    `<h1>Povolit přístup k Basecampu?</h1>
<p><strong>${name}</strong> chce číst a upravovat tvůj Basecamp tvým jménem. ${origin}</p>
<p>Přístup bude předán na <strong>${escape(details.redirectHost)}</strong>.</p>
${details.redirectIsLoopback ? '<p class="warn"><strong>Přístup míří do aplikace na tomto počítači.</strong> Pokračuj, jen pokud jsi přihlášení právě spustil(a) z ní.</p>' : ""}
<form method="post" action="/authorize">
  <input type="hidden" name="handle" value="${escape(handle)}">
  <p><button class="primary" name="decision" value="approve">Pokračovat do Basecampu</button>
  <button name="decision" value="deny">Zamítnout</button></p>
</form>`,
    200,
    headers,
  );
}

async function authorize(request: Request, env: AuthEnv): Promise<Response> {
  const oauth = env.OAUTH_PROVIDER;

  if (request.method === "GET") {
    const authRequest = await oauth.parseAuthRequest(request);
    const details = await oauth.describeConsent(authRequest);
    const consent = await oauth.beginConsent(authRequest);
    return consentPage(details, consent.handle, consent.headers);
  }

  if (request.method !== "POST") return new Response("Method Not Allowed", { status: 405 });

  const form = await request.formData();
  const handle = String(form.get("handle"));
  if (form.get("decision") !== "approve") {
    const denied = await oauth.denyConsent(request, handle);
    return new Response(null, { status: 302, headers: denied.headers });
  }
  const approved = await oauth.approveConsent(request, handle);
  const { state, headers } = await oauth.beginUpstream(approved.request, { headers: approved.headers });
  headers.set("Location", authorizeUrl(env.BASECAMP_CLIENT_ID, callbackUrl(request), state));
  return new Response(null, { status: 302, headers });
}

async function callback(request: Request, env: AuthEnv): Promise<Response> {
  const oauth = env.OAUTH_PROVIDER;
  const { request: original, headers } = await oauth.finishUpstream(request);

  const code = new URL(request.url).searchParams.get("code");
  if (!code) {
    headers.set("Location", authorizationErrorRedirect(original, "access_denied"));
    return new Response(null, { status: 302, headers });
  }

  const token = await exchangeCode(env, code, callbackUrl(request));
  const info = await fetchAuthorization(token.access_token);
  const accounts = info.accounts
    .filter((account) => account.product === "bc3")
    .map(({ id, name, href }) => ({ id, name, href }));
  if (accounts.length === 0) {
    return page("Žádný Basecamp účet", "<h1>Nenašel jsem žádný účet Basecamp 3/4</h1><p>Tento 37signals účet nemá přístup k Basecampu 3 ani 4.</p>", 400, headers);
  }

  const props: Props = {
    accessToken: token.access_token,
    refreshToken: token.refresh_token ?? "",
    expiresAt: Math.floor(Date.parse(info.expires_at) / 1000) || Math.floor(Date.now() / 1000) + (token.expires_in ?? 0),
    userName: `${info.identity.first_name} ${info.identity.last_name}`.trim(),
    email: info.identity.email_address,
    accounts,
  };
  const { redirectTo } = await oauth.completeAuthorization({
    request: original,
    userId: String(info.identity.id),
    metadata: { label: props.userName },
    scope: original.scope,
    props,
  });
  headers.set("Location", redirectTo);
  return new Response(null, { status: 302, headers });
}

export const authHandler = {
  async fetch(request: Request, env: AuthEnv): Promise<Response> {
    const { pathname } = new URL(request.url);
    try {
      if (pathname === "/authorize") return await authorize(request, env);
      if (pathname === "/callback") return await callback(request, env);
    } catch (error) {
      if (error instanceof AuthorizationError && error.redirectTo) return Response.redirect(error.redirectTo, 302);
      if (error instanceof AuthorizationError || error instanceof CimdFetchError) {
        const message = error instanceof AuthorizationError ? error.description : "Aplikaci se nepodařilo ověřit.";
        return page("Chyba přihlášení", `<h1>Přihlášení se nepovedlo</h1><p>${escape(message ?? "")}</p><p>Zkus připojení spustit znovu.</p>`, 400);
      }
      throw error;
    }
    if (pathname === "/") {
      const mcpUrl = new URL("/mcp", request.url).toString();
      return page(
        "Basecamp MCP",
        `<h1>Basecamp konektor pro Claude</h1><p>V Claude přidej vlastní konektor s touto adresou:</p><p><code>${escape(mcpUrl)}</code></p>`,
      );
    }
    return new Response("Not Found", { status: 404 });
  },
};
