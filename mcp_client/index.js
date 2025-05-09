import { init } from "./mcp_client";

const messages = document.getElementById('messages');
const userInput = document.getElementById('userInput');
let CONFIG = undefined;

function appendMessage(text, sender) {
  const div = document.createElement('div');
  div.className = `message ${sender}`;
  div.textContent = text;
  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
}

function sendMessage() {
  const text = userInput.value.trim();
  if (!text) return;

  appendMessage(text, 'user');
  userInput.value = '';

  // 모의 AI 응답
  setTimeout(() => {
    const aiReply = `Hello, World!`;
    appendMessage(aiReply, 'ai');
  }, 500);
}

userInput.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') sendMessage();
});

window.onload = async () => {
  let config = await init();
  if (!config) {
    alert("Server Error... Reload");
    location.href = '/';
  }

  CONFIG = config;
}