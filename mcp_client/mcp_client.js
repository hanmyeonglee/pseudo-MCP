import { get_random_id } from "./utils";

function jsonrpc(
    { id, method, version="2.0", params=undefined }
) {
    return {
        id,
        jsonrpc: version,
        method,
        params: params ?? null
    }
}

async function post(
    { addr, data }
) {
    return await fetch(
        addr,
        {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data ?? {})
        }
    )
    .then(response => response.json())
    .catch(() => {});
}

async function initialize(config) {
    let data = jsonrpc({ id: config.id, method: "initialize", params: { clientInfo: { name: config.name, version: config.version }}});
    let { id } = await post({ addr: config.server_addr + "/initialize", data });

    if (id !== config.id) return false;

    await post({
        addr: config.server_addr + "/initialized",
        data: jsonrpc({ id: config.id, method: "notifications/initialized" })
    });

    return true;
}

async function get_tools(config) {
    let data = jsonrpc({ id: config.id, method: "tools/list" });
    let { id, result: { tools } } = await post({ addr: config.server_addr + "/tools/list", data: data });

    if (id !== config.id || !tools ) return { fail: true };
    tools.fail = false;
    return tools;
}

export async function init() {
    let server_addr = prompt("MCP server 서버 주소는?") ?? "http://localhost:5000";
    let chatbot_addr = prompt("LLM Agent 서버 주소는?") ?? "http://localhost:5000";
    
    let config = {
        server_addr, chatbot_addr, id: get_random_id(), name: "mcp_client", version: "0.1.0"
    };
    
    if (!initialize(config)) return undefined;

    let tools = await get_tools(config);
    if (tools.fail) return undefined;

    config.tools = tools;
    return config;
}

export async function call(text) {
    
}