import { showError } from './utils.js';


export async function login(username, password) {
  const errorDiv = document.getElementById("loginError");
  if (!username || !password) {
    errorDiv.innerText = "Please fill in all fields.";
    return null;
  }

  const formData = new URLSearchParams();
  formData.append("username", username);
  formData.append("password", password);

  try {
    const res = await fetch("http://localhost:8000/auth/token", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: formData.toString(),
    });
    if (!res.ok) throw new Error("Invalid credentials");

    const data = await res.json();

    // Redirect to chatbot page ("/")
    window.location.href = "/";

    return data.access_token;
  } catch (err) {
    errorDiv.innerText = "Login failed. Please check your credentials.";
    return null;
  }
}

export async function logout() {
  const errorDiv = document.getElementById("logoutError");
  if (errorDiv) errorDiv.innerText = "";

  try {
    localStorage.removeItem("jwtToken");

    if (window.chatBotInstance) {
      window.chatBotInstance.eventSource.close();
      window.chatBotInstance = null;
    }

    return true;
  } catch (err) {
    if (errorDiv) errorDiv.innerText = "Logout failed.";
    return false;
  }
}


export async function register(username, plain_password) {
  const errorDiv = document.getElementById("registerError");
  if (!username || !plain_password) {
    errorDiv.innerText = "Please fill in all fields.";
    return false;
  }

  console.log("Registering with:", { username, plain_password });

  try {
    const res = await fetch("http://localhost:8000/auth/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, plain_password }),
    });

    console.log("Status:", res.status);
    const data = await res.json();
    console.log("Response:", data);

    if (!res.ok) {
      const errorData = await res.json();
      throw new Error(errorData.detail || "Registration failed");
    }
    return true;
  } catch (err) {
    errorDiv.innerText = err.message;
    return false;
  }
}


export async function update_credentials(new_username, new_password, token){ 
  try {
    const res = await fetch("http://localhost:8000/db/users/update-my-credentials", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`,
      },
      body: JSON.stringify({ username: new_username, plain_password: new_password })
    });

    if (res.ok) {
      return true;
    } else {
      const err = await res.json();
      showError("updateError", err.detail || "Update failed");
      return false;
    }
  } catch (err) {
    console.error(err);
    showError("updateError", "Network error");
    return false;
  }
}
