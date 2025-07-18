import { login, register } from './api.js';
import { clearErrors } from './utils.js';
import { showError } from './utils.js';
import { ChatBot } from './chat.js';

export function initAuth({ onLoginSuccess, onLogout }) {
  console.log("initAuth called");
  document.getElementById("loginButton").addEventListener("click", async () => {
    await handleLogin(onLoginSuccess);
  });

  document.getElementById("registerButton").addEventListener("click", async () => {
    await handleRegister();
  });

  document.getElementById("loginForm").addEventListener("submit", async e => {
    e.preventDefault();
    await handleLogin(onLoginSuccess);
  });

  document.getElementById("registerForm").addEventListener("submit", async e => {
    e.preventDefault();
    await handleRegister();
  });

  document.getElementById("showRegister").addEventListener("click", () => {
    toggleForms("register");
  });

  document.getElementById("showLogin").addEventListener("click", () => {
    toggleForms("login");
  });
}

function toggleForms(formToShow) {
  const loginForm = document.getElementById("loginForm");
  const registerForm = document.getElementById("registerForm");

  if (formToShow === "register") {
    loginForm.style.display = "none";
    registerForm.style.display = "block";
  } else {
    loginForm.style.display = "block";
    registerForm.style.display = "none";
  }
}

async function handleLogin(onLoginSuccess) {
  clearErrors("loginError");
  const username = document.getElementById("loginUsername").value.trim();
  const password = document.getElementById("loginPassword").value.trim();
  const errorDiv = document.getElementById("loginError");
  errorDiv.innerText = "";

  if (!username || !password) {
    errorDiv.innerText = "Please fill in all fields.";
    return;
  }

  const token = await login(username, password);
  if (token) {
    onLoginSuccess(token);
  } else {
    errorDiv.innerText = "Login failed. Please check your credentials.";
  }
}

async function handleRegister() {
  clearErrors("registerError");
  const username = document.getElementById("registerUsername").value.trim();
  const plain_password = document.getElementById("registerPassword").value.trim();
  const success = await register(username, plain_password);
  if (success) {
    toggleForms("login");
    alert("Registration successful! Please login.");
  } else {
    showError("registerError", "Registration failed. Try a different username.");
  }
}
