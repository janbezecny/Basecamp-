# Basecamp konektor pro Claude

Vzdálený MCP server, který Claude trvale propojí s Basecampem (3 i 4). Běží na Cloudflare Workers a do Claude se přidá jako **vlastní konektor**. Pak je k dispozici ve všech konverzacích na claude.ai, v desktopové i mobilní aplikaci a v Claude Code.

Přihlášení probíhá přes Basecamp (OAuth). Konektor se připojuje jednou a pak zůstává připojený: tokeny se obnovují samy, dokud konektor používáš (bez použití vyprší po 90 dnech).

## Co Claude v Basecampu umí

| Oblast | Nástroje |
| --- | --- |
| Účet a lidé | `whoami`, `list_people` |
| Projekty | `list_projects`, `get_project`, `list_recent_activity` |
| Úkoly (To-dos) | `list_todolists`, `create_todolist`, `list_todos`, `get_todo`, `create_todo`, `update_todo`, `set_todo_completed` |
| Message Board | `list_messages`, `get_message`, `create_message` |
| Komentáře | `list_comments`, `create_comment` (u úkolů, zpráv, dokumentů, událostí…) |
| Kalendář (Schedule) | `list_schedule_entries`, `create_schedule_entry` |
| Docs & Files | `list_documents`, `get_document`, `create_document` |
| Campfire | `list_campfire_lines`, `send_campfire_line` |

Pokud máš víc Basecamp účtů, každý nástroj přijímá volitelné `account_id`. Bez něj se použije první účet.

## Nasazení (jednorázově, asi 15 minut)

Potřebuješ zdarma účet na [Cloudflare](https://dash.cloudflare.com/sign-up) a Node.js 20+.

### 1. Nasaď Worker

```sh
git clone https://github.com/janbezecny/Basecamp-.git
cd Basecamp-
npm install
npx wrangler login
npx wrangler kv namespace create OAUTH_KV
```

Vrácené `id` vlož do `wrangler.jsonc` místo `REPLACE_WITH_KV_NAMESPACE_ID` a nasaď:

```sh
npx wrangler deploy
```

Wrangler vypíše adresu, například `https://basecamp-mcp.TVUJ-UCET.workers.dev`. Dál jí říkáme **URL konektoru**.

### 2. Zaregistruj aplikaci v Basecampu

1. Otevři <https://launchpad.37signals.com/integrations> a zaregistruj novou aplikaci.
2. Jméno a firmu vyplň libovolně, jako Website zadej URL konektoru.
3. **Redirect URI** nastav na `URL konektoru/callback`, například `https://basecamp-mcp.TVUJ-UCET.workers.dev/callback`.
4. Po uložení si opiš **Client ID** a **Client Secret**.

### 3. Ulož tajné klíče do Workeru

```sh
npx wrangler secret put BASECAMP_CLIENT_ID
npx wrangler secret put BASECAMP_CLIENT_SECRET
```

Hodnoty se zadávají interaktivně a nikam do repozitáře se neukládají.

### 4. Přidej konektor do Claude

1. Otevři <https://claude.ai/customize/connectors>, zvol **Add custom connector**.
2. Název: `Basecamp`. URL: `URL konektoru/mcp`, například `https://basecamp-mcp.TVUJ-UCET.workers.dev/mcp`.
3. Klikni na **Connect**. Potvrdíš přístup, přihlásíš se do Basecampu a hotovo.

V Team/Enterprise plánu musí vlastní konektor nejdřív přidat administrátor organizace.

Konektor pak zapneš v kterékoli konverzaci v menu nástrojů. Zkus třeba: *„Jaké úkoly mám v Basecampu po termínu?“*

## Bez příkazové řádky

Worker jde nasadit i přímo z Cloudflare dashboardu: **Workers & Pages → Create → Import a repository**, vyber tento repozitář. KV namespace (`OAUTH_KV`) vytvoříš v **Storage & Databases → KV**, jeho id zapíšeš do `wrangler.jsonc`. Tajné klíče přidáš ve Workeru přes **Settings → Variables and Secrets** (typ *Secret*).

## Lokální vývoj

```sh
cp .dev.vars.example .dev.vars   # doplň Client ID a Secret
npm run dev                      # http://localhost:8787
npm run typecheck
```

Pro lokální test přidej v Basecamp aplikaci i Redirect URI `http://localhost:8787/callback`.

## Jak to funguje

- `src/index.ts`: OAuth 2.1 server ([`@cloudflare/workers-oauth-provider`](https://github.com/cloudflare/workers-oauth-provider)) chrání endpoint `/mcp`. Claude se registruje sám (DCR nebo CIMD).
- `src/auth.ts`: stránka se souhlasem a předání přihlášení do Basecampu (Launchpad) a zpět.
- `src/basecamp.ts`: klient pro Basecamp API. Basecamp tokeny jsou zašifrované v KV, Claude je nikdy nevidí.
- `src/tools.ts`: MCP nástroje.

Basecamp access token platí dva týdny. Konektor ho obnoví sám, když Claude obnovuje svůj token a do vypršení zbývají méně než dva dny.

## Odpojení

Konektor odebereš v nastavení Claude. Přístup úplně zrušíš v Basecampu na <https://launchpad.37signals.com/> v sekci autorizovaných aplikací.
