/**
 * Backend API base URL from .env. All API calls should use this.
 * Vite exposes env vars prefixed with VITE_.
 */
export const API_BASE_URL =
  (typeof import.meta !== 'undefined' && import.meta.env?.VITE_API_BASE_URL) ||
  'http://localhost:8000'

/** Build full API URL from a path (path should start with /). */
export function apiUrl(path) {
  const base = API_BASE_URL.replace(/\/$/, '')
  const p = path.startsWith('/') ? path : `/${path}`
  return `${base}${p}`
}
