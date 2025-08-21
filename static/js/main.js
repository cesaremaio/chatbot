import { initAuth } from "./auth.js";
import { ChatBot } from "./chat.js";
import { testToken } from './token.js';

function showChatUI() {
  console.log("Showing chat UI");
  document.getElementById("authContainer").style.display = "none";
  document.querySelector(".chat-container").style.display = "flex"; // or "block"
  initializeUploader(); // Initialize drag & drop functionality

}

function showAuthUI() {
  console.log("Showing auth UI");
  document.getElementById("authContainer").style.display = "block";
  document.querySelector(".chat-container").style.display = "none";
}

let chatBotInstance = null;


export async function onLoginSuccess(jwtToken) {
  localStorage.setItem("jwtToken", jwtToken);
  showChatUI();
  chatBotInstance = new ChatBot(jwtToken);
}

export async function onLogout() {
  console.log("onLogout is being executed")
  // Redirect to login screen
  window.location.href = "/";
  showAuthUI();
  if (chatBotInstance) {
    chatBotInstance.eventSource.close();
    chatBotInstance = null;
  }
}


document.addEventListener("DOMContentLoaded", async () => {
  initAuth({
    onLoginSuccess: onLoginSuccess,
    onLogout: onLogout
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