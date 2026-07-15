// Use environment variable or fallback to default development URL
const API = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export async function apiRequest(path, method = "GET", body = null, isForm = false) {

  // console.log(`API Request: ${method} ${API}${path}`);

  const options = {
    method,
    credentials: "include", // sends cookies for admin auth
    headers: {},  
  };

  // Add Authorization header as fallback from localStorage
  // This ensures API calls work even if cookies fail
  const storedToken = localStorage.getItem("access_token");
  if (storedToken) {
    console.log("Using stored token from localStorage");
    options.headers = {
      ...options.headers,
      "Authorization": `Bearer ${storedToken}`
    };
  } else {
    console.log("No stored token found in localStorage");
  }

  if (body) {
    if (isForm) {
      options.body = body; // FormData
    } else {
      options.headers = { 
        "Content-Type": "application/json",
        ...options.headers 
      };
      options.body = JSON.stringify(body);
    }
  }

  const res = await fetch(`${API}${path}`, options);

  let data;
  try {
    data = await res.json();
  } catch {
    data = null;
  }

  console.log(`Response status: ${res.status}`);

  if (!res.ok) {
    throw new Error(data?.detail || `Request failed with status ${res.status}`);
  }

  return data;
}

