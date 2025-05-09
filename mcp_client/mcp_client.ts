import { get_random_id } from "./utils";

function jsonrpc(
    { id, method, version="2.0", params=undefined}:
    { 
        id: number | string,
        method: string,
        version?: string,
        params?: object | undefined
    }
): object {
    return {
        id,
        jsonrpc: version,
        method,
        params: params ?? {}
    }
}

async function post(
    { addr, data }: { addr: string | URL, data: object | undefined }
): Promise<object> {
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

async function init() {
    const name = "mcp_client";
    let server_addr: string = prompt("MCP server 서버 주소는?") ?? "localhost:5000";
    let chatbot_addr: string = prompt("LLM Agent 서버 주소는?") ?? "localhost:5000";
    
    let config = {
        server_addr, chatbot_addr, id: get_random_id(), name, version: "0.1.0"
    };
    let data = jsonrpc({ id: config.id, method: "initialize", params: { clientInfo: { name: config.name, version: config.version }}});
    let response_json: object = await post({ addr: server_addr, data });
}