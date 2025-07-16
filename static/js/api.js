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

export async function register(username, password) {
  const errorDiv = document.getElementById("registerError");
  if (!username || !password) {
    errorDiv.innerText = "Please fill in all fields.";
    return false;
  }

  try {
    const res = await fetch("http://localhost:8000/auth/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });

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
