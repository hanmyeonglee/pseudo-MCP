import { init, generate, call } from "./mcp_client.js";
import { reload } from "./utils.js";

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

window.sendMessage = async () => {
  const text = userInput.value.trim();
  if (!text) return;

  appendMessage(text, "user");
  userInput.value = "";

  try {
    let params = await generate({
      addr: CONFIG.chatbot_addr,
      id: CONFIG.id,
      tools_list: CONFIG.tools,
      user_input: text,
    });
    if (!params) throw new Error("Invalid Params");

    let result =
      (await call({
        addr: CONFIG.server_addr,
        config: CONFIG,
        params,
      })) ?? "AI is broken, retry plz.";
    appendMessage(result, "ai");
  } catch {
    appendMessage("AI is broken, retry plz.", "ai");
  }
};

userInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") sendMessage();
});

window.onload = async () => {
  let config = await init();
  console.log("config", config);
  if (!config) reload();

  CONFIG = config;
};
