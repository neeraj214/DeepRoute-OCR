import axios from "axios";

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

export function getToken(): string | null {
  return localStorage.getItem("token");
}

export function setToken(token: string | null) {
  if (token) localStorage.setItem("token", token);
  else localStorage.removeItem("token");
}

export function parseJwt(token: string): any | null {
  try {
    const [, payload] = token.split(".");
    const json = JSON.parse(atob(payload.replace(/-/g, "+").replace(/_/g, "/")));
    return json;
  } catch {
    return null;
  }
}

export function isTokenExpired(token: string): boolean {
  const payload = parseJwt(token);
  if (!payload?.exp) return true;
  const expMs = payload.exp * 1000;
  return Date.now() > expMs;
}

export const api = axios.create({
  baseURL: API_BASE,
});

api.interceptors.request.use((config) => {
  const token = getToken();
  if (token && !isTokenExpired(token)) {
    config.headers = {
      ...(config.headers || {}),
      Authorization: `Bearer ${token}`,
    };
  }
  return config;
});

export async function login(email: string, password: string) {
  const params = new URLSearchParams();
  params.append("username", email);
  params.append("password", password);
  const res = await api.post("/auth/login", params, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });
  const token = res.data?.access_token as string;
  setToken(token);
  return res.data;
}

export async function register(payload: { email: string; password: string; full_name?: string }) {
  const res = await api.post("/auth/register", payload);
  return res.data;
}

export function logout() {
  const token = getToken();
  if (token) {
    return api.post("/auth/logout").finally(() => setToken(null));
  }
  setToken(null);
  return Promise.resolve();
}

