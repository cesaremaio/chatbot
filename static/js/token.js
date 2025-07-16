let accessToken = null;
let refreshToken = null;

export function saveTokens(access, refresh) {
  accessToken = access;
  refreshToken = refresh;
  localStorage.setItem("refreshToken", refresh);
}

export function getAccessToken() {
  return accessToken;
}

export async function authFetch(url, options = {}) {
  options.headers = options.headers || {};
  options.headers["Authorization"] = "Bearer " + accessToken;

  let response = await fetch(url, options);

  if (response.status === 401) {
    const newAccess = await refreshAccessToken();
    if (newAccess) {
      accessToken = newAccess;
      options.headers["Authorization"] = "Bearer " + accessToken;
      return fetch(url, options);  // Retry
    }
  }

  return response;
}

async function refreshAccessToken() {
  const storedRefresh = localStorage.getItem("refreshToken");
  if (!storedRefresh) return null;

  const res = await fetch("/auth/refresh", {
    method: "POST",
    headers: {
      "refresh_token": storedRefresh
    }
  });

  if (res.ok) {
    const data = await res.json();
    accessToken = data.access_token;
    return data.access_token;
  } else {
    console.warn("Refresh token expired");
    return null;
  }
}


export async function testToken(token) {
  try {
    const res = await fetch("/auth/check", {
      headers: { "Authorization": "Bearer " + token }
    });
    return res.ok;
  } catch {
    return false;
  }
}