import { initAuth } from "./auth.js";
import { ChatBot } from "./chat.js";
import { testToken } from './token.js';

function showChatUI() {
  console.log("Showing chat UI");
  document.getElementById("authContainer").style.display = "none";
  document.querySelector(".chat-container").style.display = "flex"; // or "block"
}

function showAuthUI() {
  console.log("Showing auth UI");
  document.getElementById("authContainer").style.display = "block";
  document.querySelector(".chat-container").style.display = "none";
}

let chatBotInstance = null;
document.addEventListener("DOMContentLoaded", async () => {
  initAuth({
    onLoginSuccess: (jwtToken) => {
      localStorage.setItem("jwtToken", jwtToken);
      showChatUI();
      chatBotInstance = new ChatBot(jwtToken);
    },
    onLogout: () => {
      localStorage.removeItem("jwtToken");
      showAuthUI();
      if (chatBotInstance) {
        chatBotInstance.eventSource.close();
        chatBotInstance = null;
      }
    }
  });

  const jwtToken = localStorage.getItem("jwtToken");

  if (jwtToken) {
    // 🔁 Prova a verificare che il token sia ancora valido
    const isValid = await testToken(jwtToken);

    if (isValid) {
      showChatUI();
      chatBotInstance = new ChatBot(jwtToken);
    } else {
      localStorage.removeItem("jwtToken");
      showAuthUI();
    }
  } else {
    showAuthUI();
  }
});