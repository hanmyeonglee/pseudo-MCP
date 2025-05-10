import { init, generate, call } from "./mcp_client";
import { reload } from "./utils";

const messages = document.getElementById("messages");
const userInput = document.getElementById("userInput");
let CONFIG = undefined;

function appendMessage(text, sender) {
  const div = document.createElement("div");
  div.className = `message ${sender}`;
  div.textContent = text;
  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
}

function sendMessage() {
  const text = userInput.value.trim();
  if (!text) return;

  appendMessage(text, "user");
  userInput.value = "";

  let params = generate({
    addr: CONFIG.chatbot_addr,
    id: CONFIG.id,
    tools_list: CONFIG.tools,
    user_input: text,
  });
  if (!params) reload();

  let result = call({
    addr: CONFIG.server_addr,
    config: CONFIG,
    params,
  });
  if (!result) reload();

  appendMessage(result, "ai");
}

userInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") sendMessage();
});

window.onload = async () => {
  let config = await init();
  if (!config) reload();

  CONFIG = config;
};
