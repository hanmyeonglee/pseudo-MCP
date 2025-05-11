import { get_random_id } from "./utils.js";

function jsonrpc({ id, method, version = "2.0", params = undefined }) {
  return {
    id,
    jsonrpc: version,
    method,
    params: params ?? null,
  };
}

async function post({ addr, data }) {
  return fetch(addr, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data ?? {}),
  }).then(async (response) => {
    if (!response.ok) {
      console.log(await response.text());
      throw new Error("failed");
    }
    return response.json();
  });
}

async function initialize(config) {
  let data = jsonrpc({
    id: config.id,
    method: "initialize",
    params: { clientInfo: { name: config.name, version: config.version } },
  });
  let { id } = await post({
    addr: config.server_addr + "/initialize",
    data,
  });

  if (id !== config.id) return false;

  await post({
    addr: config.server_addr + "/initialized",
    data: jsonrpc({ id: config.id, method: "notifications/initialized" }),
  });

  return true;
}

async function get_tools(config) {
  let data = jsonrpc({ id: config.id, method: "tools/list" });
  let {
    id,
    result: { tools },
  } = await post({
    addr: config.server_addr + "/tools/list",
    data: data,
  });

  if (id !== config.id || !tools) return { fail: true };
  tools.fail = false;
  return tools;
}

export async function init() {
  let server_addr = prompt("Address of MCP Server") ?? "http://localhost:5000";
  let chatbot_addr = prompt("Address of LLM Server") ?? "http://localhost:5000";

  let config = {
    server_addr,
    chatbot_addr,
    id: get_random_id(),
    name: "mcp_client",
    version: "2.0",
  };

  try {
    let flag = await initialize(config);
    if (!flag) return undefined;

    let tools = await get_tools(config);
    if (tools.fail) return undefined;

    config.tools = tools;
    return config;
  } catch (err) {
    console.log(err);
    return undefined;
  }
}

export async function generate({ addr, id, tools_list, user_input }) {
  let data = { id, tools_list, user_input };
  try {
    let { id, answer } = await post({ addr, data });
    if (id !== id) return undefined;
    return answer;
  } catch {
    return undefined;
  }
}

export async function call({ addr, config, params }) {
  let data = {
    params,
    id: config.id,
    method: "tools/call",
    jsonrpc: config.version,
  };
  try {
    let response4 = await post({
      addr: addr + "/tools/call",
      data,
    });
    let { id, result } = response4;
    if (id !== config.id) return undefined;
    return result;
  } catch {
    return undefined;
  }
}
