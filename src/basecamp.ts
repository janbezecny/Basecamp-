// Minimal client for Basecamp's OAuth (Launchpad) and the Basecamp 4 API (bc3 product).
// API reference: https://github.com/basecamp/bc3-api

const LAUNCHPAD = "https://launchpad.37signals.com";
const USER_AGENT = "Claude Basecamp Connector (https://github.com/janbezecny/Basecamp-)";

export interface BasecampAccount {
  id: number;
  name: string;
  href: string;
}

/** What the OAuth grant stores; handed to every MCP request as encrypted props. */
export interface Props {
  accessToken: string;
  refreshToken: string;
  /** Unix seconds when the Basecamp access token expires. */
  expiresAt: number;
  userName: string;
  email: string;
  accounts: BasecampAccount[];
}

export interface TokenResponse {
  access_token: string;
  refresh_token?: string;
  expires_in?: number;
}

export class BasecampAuthError extends Error {
  constructor(
    message: string,
    readonly status: number,
  ) {
    super(message);
  }
}

export function authorizeUrl(clientId: string, redirectUri: string, state: string): string {
  const url = new URL(`${LAUNCHPAD}/authorization/new`);
  url.searchParams.set("type", "web_server");
  url.searchParams.set("client_id", clientId);
  url.searchParams.set("redirect_uri", redirectUri);
  url.searchParams.set("state", state);
  return url.toString();
}

async function tokenRequest(params: Record<string, string>): Promise<TokenResponse> {
  const url = new URL(`${LAUNCHPAD}/authorization/token`);
  for (const [key, value] of Object.entries(params)) url.searchParams.set(key, value);
  const res = await fetch(url, { method: "POST", headers: { "User-Agent": USER_AGENT } });
  if (!res.ok) {
    throw new BasecampAuthError(`Basecamp token request failed: ${res.status} ${await res.text()}`, res.status);
  }
  return res.json();
}

export function exchangeCode(env: Env, code: string, redirectUri: string): Promise<TokenResponse> {
  return tokenRequest({
    type: "web_server",
    client_id: env.BASECAMP_CLIENT_ID,
    client_secret: env.BASECAMP_CLIENT_SECRET,
    redirect_uri: redirectUri,
    code,
  });
}

export function refreshAccessToken(env: Env, refreshToken: string, redirectUri: string): Promise<TokenResponse> {
  return tokenRequest({
    type: "refresh",
    client_id: env.BASECAMP_CLIENT_ID,
    client_secret: env.BASECAMP_CLIENT_SECRET,
    redirect_uri: redirectUri,
    refresh_token: refreshToken,
  });
}

interface AuthorizationInfo {
  expires_at: string;
  identity: { id: number; first_name: string; last_name: string; email_address: string };
  accounts: { product: string; id: number; name: string; href: string }[];
}

export async function fetchAuthorization(accessToken: string): Promise<AuthorizationInfo> {
  const res = await fetch(`${LAUNCHPAD}/authorization.json`, {
    headers: { Authorization: `Bearer ${accessToken}`, "User-Agent": USER_AGENT },
  });
  if (!res.ok) throw new BasecampAuthError(`Basecamp authorization lookup failed: ${res.status}`, res.status);
  return res.json();
}

export class BasecampApiError extends Error {
  constructor(
    readonly status: number,
    readonly body: string,
  ) {
    super(`Basecamp API error ${status}: ${body.slice(0, 500)}`);
  }
}

export class BasecampClient {
  readonly baseUrl: string;

  constructor(
    private readonly accessToken: string,
    readonly account: BasecampAccount,
  ) {
    this.baseUrl = account.href.replace(/\/$/, "");
  }

  private url(path: string, query?: Record<string, string | number | boolean | undefined>): URL {
    const url = new URL(path.startsWith("http") ? path : `${this.baseUrl}${path}`);
    for (const [key, value] of Object.entries(query ?? {})) {
      if (value !== undefined) url.searchParams.set(key, String(value));
    }
    return url;
  }

  private async send(method: string, url: URL | string, body?: unknown): Promise<Response> {
    const res = await fetch(url, {
      method,
      headers: {
        Authorization: `Bearer ${this.accessToken}`,
        "User-Agent": USER_AGENT,
        Accept: "application/json",
        ...(body === undefined ? {} : { "Content-Type": "application/json; charset=utf-8" }),
      },
      body: body === undefined ? undefined : JSON.stringify(body),
    });
    if (!res.ok) throw new BasecampApiError(res.status, await res.text());
    return res;
  }

  async get<T = any>(path: string, query?: Record<string, string | number | boolean | undefined>): Promise<T> {
    return (await this.send("GET", this.url(path, query))).json();
  }

  /** Follows `Link: rel="next"` headers, up to `maxPages` pages. */
  async list<T = any>(
    path: string,
    query?: Record<string, string | number | boolean | undefined>,
    maxPages = 5,
  ): Promise<T[]> {
    const items: T[] = [];
    let next: string | null = this.url(path, query).toString();
    for (let page = 0; next && page < maxPages; page++) {
      const res = await this.send("GET", next);
      items.push(...((await res.json()) as T[]));
      next = res.headers.get("Link")?.match(/<([^>]+)>;\s*rel="next"/)?.[1] ?? null;
    }
    return items;
  }

  async post<T = any>(path: string, body?: unknown): Promise<T | null> {
    const res = await this.send("POST", this.url(path), body);
    return res.status === 204 || res.headers.get("Content-Length") === "0" ? null : res.json();
  }

  async put<T = any>(path: string, body: unknown): Promise<T> {
    return (await this.send("PUT", this.url(path), body)).json();
  }

  async delete(path: string): Promise<void> {
    await this.send("DELETE", this.url(path));
  }

  /** The dock entry (todoset, message_board, schedule, vault, chat, …) of a project. */
  async dockTool(projectId: number, name: string): Promise<{ id: number; url: string }> {
    const project = await this.get(`/projects/${projectId}.json`);
    const tool = (project.dock as { name: string; id: number; url: string; enabled: boolean }[]).find(
      (entry) => entry.name === name && entry.enabled,
    );
    if (!tool) throw new Error(`Projekt ${projectId} nemá zapnutý nástroj „${name}“.`);
    return tool;
  }
}
