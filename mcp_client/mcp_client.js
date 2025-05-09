var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
import { get_random_id } from "./utils";
function jsonrpc({ id, method, version = "2.0", params = undefined }) {
    return {
        id,
        jsonrpc: version,
        method,
        params: params !== null && params !== void 0 ? params : {}
    };
}
function post(_a) {
    return __awaiter(this, arguments, void 0, function* ({ addr, data }) {
        return yield fetch(addr, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data !== null && data !== void 0 ? data : {})
        })
            .then(response => response.json())
            .catch(() => { });
    });
}
function init() {
    return __awaiter(this, void 0, void 0, function* () {
        var _a, _b;
        const name = "mcp_client";
        let server_addr = (_a = prompt("MCP server 서버 주소는?")) !== null && _a !== void 0 ? _a : "localhost:5000";
        let chatbot_addr = (_b = prompt("LLM Agent 서버 주소는?")) !== null && _b !== void 0 ? _b : "localhost:5000";
        let config = {
            server_addr, chatbot_addr, id: get_random_id(), name, version: "0.1.0"
        };
        let data = jsonrpc({ id: config.id, method: "initialize", params: { clientInfo: { name: config.name, version: config.version } } });
        let response_json = yield post({ addr: server_addr, data });
    });
}
