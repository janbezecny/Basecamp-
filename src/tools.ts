// MCP tools that expose Basecamp to Claude.
import { McpServer } from "@modelcontextprotocol/server";
import { z } from "zod";
import { BasecampApiError, BasecampClient, type Props } from "./basecamp";

type Result = { content: { type: "text"; text: string }[]; isError?: boolean };

const text = (value: unknown): Result => ({
  content: [{ type: "text", text: typeof value === "string" ? value : JSON.stringify(value, null, 2) }],
});

const person = (p: any) => (p ? { id: p.id, name: p.name, email: p.email_address } : undefined);

const slim = {
  project: (p: any) => ({
    id: p.id,
    name: p.name,
    description: p.description || undefined,
    status: p.status,
    updated_at: p.updated_at,
    app_url: p.app_url,
  }),
  todolist: (l: any) => ({
    id: l.id,
    name: l.name,
    description: l.description || undefined,
    completed: l.completed,
    completed_ratio: l.completed_ratio,
    app_url: l.app_url,
  }),
  todo: (t: any) => ({
    id: t.id,
    content: t.content,
    description: t.description || undefined,
    completed: t.completed,
    due_on: t.due_on ?? undefined,
    starts_on: t.starts_on ?? undefined,
    assignees: t.assignees?.map(person),
    creator: person(t.creator),
    comments_count: t.comments_count,
    todolist: t.parent?.title,
    app_url: t.app_url,
  }),
  message: (m: any) => ({
    id: m.id,
    subject: m.subject,
    content: m.content,
    creator: person(m.creator),
    created_at: m.created_at,
    comments_count: m.comments_count,
    app_url: m.app_url,
  }),
  comment: (c: any) => ({ id: c.id, content: c.content, creator: person(c.creator), created_at: c.created_at }),
  entry: (e: any) => ({
    id: e.id,
    summary: e.summary,
    description: e.description || undefined,
    starts_at: e.starts_at,
    ends_at: e.ends_at,
    all_day: e.all_day,
    participants: e.participants?.map(person),
    app_url: e.app_url,
  }),
  document: (d: any, withContent = false) => ({
    id: d.id,
    title: d.title,
    ...(withContent ? { content: d.content } : {}),
    creator: person(d.creator),
    updated_at: d.updated_at,
    app_url: d.app_url,
  }),
  line: (l: any) => ({ id: l.id, content: l.content, creator: person(l.creator), created_at: l.created_at }),
  recording: (r: any) => ({
    id: r.id,
    type: r.type,
    title: r.title,
    project: r.bucket?.name,
    project_id: r.bucket?.id,
    creator: person(r.creator),
    updated_at: r.updated_at,
    app_url: r.app_url,
  }),
};

const ids = {
  account_id: z
    .number()
    .int()
    .optional()
    .describe("ID Basecamp účtu. Vynech, pokud má uživatel jen jeden účet (použije se první)."),
  project_id: z.number().int().describe("ID projektu (bucketu) z list_projects."),
};
const html = (what: string) => z.string().describe(`${what}. Basecamp přijímá jednoduché HTML (<div>, <strong>, <em>, <a>, <ul>, <ol>, <li>, <br>).`);

export function createServer(props: Props): McpServer {
  const server = new McpServer({ name: "basecamp", version: "1.0.0" });

  const client = (accountId?: number) => {
    const account = accountId ? props.accounts.find((a) => a.id === accountId) : props.accounts[0];
    if (!account) throw new Error(`Účet ${accountId} není dostupný. Dostupné účty: ${props.accounts.map((a) => `${a.id} (${a.name})`).join(", ")}`);
    return new BasecampClient(props.accessToken, account);
  };

  // Every tool turns Basecamp errors into a readable tool error instead of a protocol failure.
  const tool = <S extends z.ZodRawShape>(
    name: string,
    description: string,
    shape: S,
    run: (args: z.infer<z.ZodObject<S>>) => Promise<unknown>,
    readOnly = true,
  ) =>
    server.registerTool(
      name,
      {
        description,
        inputSchema: z.object(shape),
        annotations: { readOnlyHint: readOnly, destructiveHint: false, openWorldHint: true },
      },
      (async (args: z.infer<z.ZodObject<S>>) => {
        try {
          return text(await run(args));
        } catch (error) {
          const message =
            error instanceof BasecampApiError && error.status === 401
              ? "Platnost přihlášení do Basecampu vypršela. Odpoj a znovu připoj konektor."
              : error instanceof Error
                ? error.message
                : String(error);
          return { ...text(message), isError: true };
        }
      }) as any,
    );

  tool("whoami", "Vrátí přihlášeného uživatele Basecampu a účty, ke kterým má přístup.", {}, async () => ({
    name: props.userName,
    email: props.email,
    accounts: props.accounts.map(({ id, name }) => ({ id, name })),
  }));

  // Projects
  tool(
    "list_projects",
    "Vypíše projekty v Basecampu.",
    {
      account_id: ids.account_id,
      status: z.enum(["active", "archived", "trashed"]).optional().describe("Výchozí: active"),
    },
    async ({ account_id, status }) => (await client(account_id).list("/projects.json", { status })).map(slim.project),
  );

  tool(
    "get_project",
    "Detail projektu včetně zapnutých nástrojů (to-do, message board, kalendář, dokumenty, Campfire) a jejich ID.",
    { account_id: ids.account_id, project_id: ids.project_id },
    async ({ account_id, project_id }) => {
      const p = await client(account_id).get(`/projects/${project_id}.json`);
      return {
        ...slim.project(p),
        tools: p.dock.filter((d: any) => d.enabled).map((d: any) => ({ name: d.name, title: d.title, id: d.id })),
      };
    },
  );

  tool(
    "list_people",
    "Vypíše lidi v projektu, nebo všechny lidi v účtu, když chybí project_id. Hodí se pro zjištění ID pro přiřazení úkolu.",
    { account_id: ids.account_id, project_id: ids.project_id.optional() },
    async ({ account_id, project_id }) =>
      (await client(account_id).list(project_id ? `/projects/${project_id}/people.json` : "/people.json")).map((p: any) => ({
        ...person(p),
        title: p.title || undefined,
        company: p.company?.name,
      })),
  );

  tool(
    "list_recent_activity",
    "Nedávno změněné položky napříč projekty (úkoly, zprávy, dokumenty, …).",
    {
      account_id: ids.account_id,
      type: z.enum(["Todo", "Todolist", "Message", "Comment", "Document", "Schedule::Entry", "Upload", "Question::Answer"]),
      project_ids: z.array(z.number().int()).optional().describe("Omezit na tyto projekty. Výchozí: všechny aktivní."),
    },
    async ({ account_id, type, project_ids }) =>
      (
        await client(account_id).list(
          "/projects/recordings.json",
          { type, bucket: project_ids?.join(","), sort: "updated_at", direction: "desc" },
          1,
        )
      ).map(slim.recording),
  );

  // To-dos
  tool(
    "list_todolists",
    "Vypíše to-do listy v projektu.",
    { account_id: ids.account_id, project_id: ids.project_id },
    async ({ account_id, project_id }) => {
      const c = client(account_id);
      const todoset = await c.dockTool(project_id, "todoset");
      return (await c.list(`/buckets/${project_id}/todosets/${todoset.id}/todolists.json`)).map(slim.todolist);
    },
  );

  tool(
    "list_todos",
    "Vypíše úkoly v to-do listu.",
    {
      account_id: ids.account_id,
      project_id: ids.project_id,
      todolist_id: z.number().int(),
      completed: z.boolean().optional().describe("true = jen hotové úkoly; výchozí jsou nedokončené."),
    },
    async ({ account_id, project_id, todolist_id, completed }) =>
      (await client(account_id).list(`/buckets/${project_id}/todolists/${todolist_id}/todos.json`, { completed: completed || undefined })).map(
        slim.todo,
      ),
  );

  tool(
    "get_todo",
    "Detail úkolu.",
    { account_id: ids.account_id, project_id: ids.project_id, todo_id: z.number().int() },
    async ({ account_id, project_id, todo_id }) => slim.todo(await client(account_id).get(`/buckets/${project_id}/todos/${todo_id}.json`)),
  );

  tool(
    "create_todolist",
    "Vytvoří nový to-do list v projektu.",
    { account_id: ids.account_id, project_id: ids.project_id, name: z.string(), description: html("Popis").optional() },
    async ({ account_id, project_id, name, description }) => {
      const c = client(account_id);
      const todoset = await c.dockTool(project_id, "todoset");
      return slim.todolist(await c.post(`/buckets/${project_id}/todosets/${todoset.id}/todolists.json`, { name, description }));
    },
    false,
  );

  const todoFields = {
    description: html("Poznámky k úkolu").optional(),
    assignee_ids: z.array(z.number().int()).optional().describe("ID lidí z list_people"),
    due_on: z.string().optional().describe("Termín ve formátu YYYY-MM-DD"),
    starts_on: z.string().optional().describe("Začátek ve formátu YYYY-MM-DD"),
    notify: z.boolean().optional().describe("Upozornit přiřazené lidi"),
  };

  tool(
    "create_todo",
    "Vytvoří úkol v to-do listu.",
    { account_id: ids.account_id, project_id: ids.project_id, todolist_id: z.number().int(), content: z.string().describe("Název úkolu"), ...todoFields },
    async ({ account_id, project_id, todolist_id, ...body }) =>
      slim.todo(await client(account_id).post(`/buckets/${project_id}/todolists/${todolist_id}/todos.json`, body)),
    false,
  );

  tool(
    "update_todo",
    "Upraví úkol. Vyplň jen pole, která se mají změnit; ostatní zůstanou beze změny.",
    { account_id: ids.account_id, project_id: ids.project_id, todo_id: z.number().int(), content: z.string().optional(), ...todoFields },
    async ({ account_id, project_id, todo_id, ...changes }) => {
      const c = client(account_id);
      const path = `/buckets/${project_id}/todos/${todo_id}.json`;
      // Basecamp clears any field left out of a to-do PUT, so send the current values too.
      const current = await c.get(path);
      const body = {
        content: current.content,
        description: current.description,
        assignee_ids: current.assignees?.map((p: any) => p.id),
        completion_subscriber_ids: current.completion_subscribers?.map((p: any) => p.id),
        due_on: current.due_on,
        starts_on: current.starts_on,
        ...Object.fromEntries(Object.entries(changes).filter(([, value]) => value !== undefined)),
      };
      return slim.todo(await c.put(path, body));
    },
    false,
  );

  tool(
    "set_todo_completed",
    "Označí úkol jako hotový, nebo ho vrátí mezi nedokončené.",
    { account_id: ids.account_id, project_id: ids.project_id, todo_id: z.number().int(), completed: z.boolean() },
    async ({ account_id, project_id, todo_id, completed }) => {
      const c = client(account_id);
      const path = `/buckets/${project_id}/todos/${todo_id}/completion.json`;
      if (completed) await c.post(path);
      else await c.delete(path);
      return completed ? "Úkol je hotový." : "Úkol je znovu otevřený.";
    },
    false,
  );

  // Message board
  tool(
    "list_messages",
    "Vypíše zprávy z Message Boardu projektu.",
    { account_id: ids.account_id, project_id: ids.project_id },
    async ({ account_id, project_id }) => {
      const c = client(account_id);
      const board = await c.dockTool(project_id, "message_board");
      return (await c.list(`/buckets/${project_id}/message_boards/${board.id}/messages.json`, undefined, 2)).map(slim.message);
    },
  );

  tool(
    "get_message",
    "Detail zprávy včetně obsahu.",
    { account_id: ids.account_id, project_id: ids.project_id, message_id: z.number().int() },
    async ({ account_id, project_id, message_id }) => slim.message(await client(account_id).get(`/buckets/${project_id}/messages/${message_id}.json`)),
  );

  tool(
    "create_message",
    "Zveřejní novou zprávu na Message Boardu projektu.",
    { account_id: ids.account_id, project_id: ids.project_id, subject: z.string(), content: html("Text zprávy") },
    async ({ account_id, project_id, subject, content }) => {
      const c = client(account_id);
      const board = await c.dockTool(project_id, "message_board");
      return slim.message(await c.post(`/buckets/${project_id}/message_boards/${board.id}/messages.json`, { subject, content, status: "active" }));
    },
    false,
  );

  // Comments work on any recording: to-dos, messages, documents, schedule entries, …
  tool(
    "list_comments",
    "Vypíše komentáře k libovolné položce (úkol, zpráva, dokument, událost…).",
    { account_id: ids.account_id, project_id: ids.project_id, recording_id: z.number().int().describe("ID úkolu, zprávy, dokumentu apod.") },
    async ({ account_id, project_id, recording_id }) =>
      (await client(account_id).list(`/buckets/${project_id}/recordings/${recording_id}/comments.json`)).map(slim.comment),
  );

  tool(
    "create_comment",
    "Přidá komentář k libovolné položce (úkol, zpráva, dokument, událost…).",
    { account_id: ids.account_id, project_id: ids.project_id, recording_id: z.number().int(), content: html("Text komentáře") },
    async ({ account_id, project_id, recording_id, content }) =>
      slim.comment(await client(account_id).post(`/buckets/${project_id}/recordings/${recording_id}/comments.json`, { content })),
    false,
  );

  // Schedule
  tool(
    "list_schedule_entries",
    "Vypíše události z kalendáře (Schedule) projektu.",
    { account_id: ids.account_id, project_id: ids.project_id, status: z.enum(["upcoming", "past"]).optional().describe("Výchozí: upcoming") },
    async ({ account_id, project_id, status }) => {
      const c = client(account_id);
      const schedule = await c.dockTool(project_id, "schedule");
      return (await c.list(`/buckets/${project_id}/schedules/${schedule.id}/entries.json`, { status })).map(slim.entry);
    },
  );

  tool(
    "create_schedule_entry",
    "Vytvoří událost v kalendáři projektu.",
    {
      account_id: ids.account_id,
      project_id: ids.project_id,
      summary: z.string().describe("Název události"),
      starts_at: z.string().describe("Začátek v ISO 8601, např. 2026-10-08T09:00:00+02:00"),
      ends_at: z.string().describe("Konec v ISO 8601"),
      description: html("Popis").optional(),
      all_day: z.boolean().optional(),
      participant_ids: z.array(z.number().int()).optional(),
      notify: z.boolean().optional(),
    },
    async ({ account_id, project_id, ...body }) => {
      const c = client(account_id);
      const schedule = await c.dockTool(project_id, "schedule");
      return slim.entry(await c.post(`/buckets/${project_id}/schedules/${schedule.id}/entries.json`, body));
    },
    false,
  );

  // Docs & Files
  tool(
    "list_documents",
    "Vypíše dokumenty v hlavní složce Docs & Files projektu.",
    { account_id: ids.account_id, project_id: ids.project_id },
    async ({ account_id, project_id }) => {
      const c = client(account_id);
      const vault = await c.dockTool(project_id, "vault");
      return (await c.list(`/buckets/${project_id}/vaults/${vault.id}/documents.json`)).map((d: any) => slim.document(d));
    },
  );

  tool(
    "get_document",
    "Vrátí dokument včetně obsahu.",
    { account_id: ids.account_id, project_id: ids.project_id, document_id: z.number().int() },
    async ({ account_id, project_id, document_id }) =>
      slim.document(await client(account_id).get(`/buckets/${project_id}/documents/${document_id}.json`), true),
  );

  tool(
    "create_document",
    "Vytvoří dokument v hlavní složce Docs & Files projektu.",
    { account_id: ids.account_id, project_id: ids.project_id, title: z.string(), content: html("Obsah dokumentu") },
    async ({ account_id, project_id, title, content }) => {
      const c = client(account_id);
      const vault = await c.dockTool(project_id, "vault");
      return slim.document(await c.post(`/buckets/${project_id}/vaults/${vault.id}/documents.json`, { title, content, status: "active" }), true);
    },
    false,
  );

  // Campfire (chat)
  tool(
    "list_campfire_lines",
    "Vypíše poslední zprávy z Campfire (chatu) projektu.",
    { account_id: ids.account_id, project_id: ids.project_id },
    async ({ account_id, project_id }) => {
      const c = client(account_id);
      const chat = await c.dockTool(project_id, "chat");
      return (await c.list(`/buckets/${project_id}/chats/${chat.id}/lines.json`, undefined, 1)).map(slim.line);
    },
  );

  tool(
    "send_campfire_line",
    "Pošle zprávu do Campfire (chatu) projektu.",
    { account_id: ids.account_id, project_id: ids.project_id, content: z.string() },
    async ({ account_id, project_id, content }) => {
      const c = client(account_id);
      const chat = await c.dockTool(project_id, "chat");
      return slim.line(await c.post(`/buckets/${project_id}/chats/${chat.id}/lines.json`, { content }));
    },
    false,
  );

  return server;
}
