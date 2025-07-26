import { login, logout, register, update_credentials } from './api.js';
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

  document.getElementById("logoutButton").addEventListener("click", async () => {
    if (confirm("Are you sure you want to log out?")) {
      await handleLogout(onLogout);
    }
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

  document.getElementById("updateCredentialsButton").addEventListener("click", () => {
    toggleForms("update");
    document.querySelector(".chat-container").style.display = "none";
    document.getElementById("authContainer").style.display = "block";
  });

  document.getElementById("updateForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    await handleUpdateCredentials();
  });

  document.getElementById("backToChat").addEventListener("click", (e) => {
    e.preventDefault();
    document.getElementById("authContainer").style.display = "none";
    document.querySelector(".chat-container").style.display = "flex";
});

}

function toggleForms(formToShow) {
  const loginForm = document.getElementById("loginForm");
  const registerForm = document.getElementById("registerForm");
  const updateForm = document.getElementById("updateForm");

  loginForm.style.display = "none";
  registerForm.style.display = "none";
  updateForm.style.display = "none";

  if (formToShow === "login") {
    loginForm.style.display = "block";
  } else if (formToShow === "register") {
    registerForm.style.display = "block";
  } else if (formToShow === "update") {
    updateForm.style.display = "block";
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

async function handleLogout(onLogout) {
  const success = await logout();
  if (success ) {
    onLogout();
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

async function handleUpdateCredentials() {
  const newUsername = document.getElementById("updateUsername").value.trim();
  const newPassword = document.getElementById("updatePassword").value.trim();

  if (!newUsername || !newPassword) {
    showError("updateError", "Username and password required.");
    return;
  }

  const token = localStorage.getItem("jwtToken");
  const success = await update_credentials(newUsername, newPassword, token);

  if (success) {
    toggleForms("login");
    alert("Credentials updated.");
    document.getElementById("updateUsername").value = "";
    document.getElementById("updatePassword").value = "";
  }
}


