import { browser } from '$app/environment';
import type {
  Issue,
  IssueCreate,
  IssueUpdate,
  UserCreate,
  UserLogin,
  Token,
  DailyStats,
  AnalyticsStats
} from './types';

const API_BASE = 'http://localhost:8000/api';

// Helper for JSON Auth headers
function getAuthHeaders(): HeadersInit {
  let token = null;
  if (browser) {
    token = localStorage.getItem('token');
  }
  return {
    'Content-Type': 'application/json',
    ...(token && { 'Authorization': `Bearer ${token}` })
  };
}

// Helper for Bearer headers (no content-type — for file upload)
function getBearerHeaders(): HeadersInit {
  const headers: HeadersInit = {};
  const token = browser ? localStorage.getItem('token') : null;
  if (token) headers['Authorization'] = `Bearer ${token}`;
  return headers;
}

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const error = await response.text();
    throw new Error(error || `HTTP ${response.status}`);
  }
  return response.json();
}

// ─────────────────────────────────────────
// Auth endpoints
// ─────────────────────────────────────────
export async function register(userData: UserCreate): Promise<Token> {
  const response = await fetch(`${API_BASE}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(userData)
  });
  return handleResponse<Token>(response);
}

export async function login(credentials: UserLogin): Promise<Token> {
  const response = await fetch(`${API_BASE}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(credentials)
  });
  return handleResponse<Token>(response);
}

// ─────────────────────────────────────────
// Issues endpoints
// ─────────────────────────────────────────
export async function fetchIssues(): Promise<Issue[]> {
  const response = await fetch(`${API_BASE}/issues`, {
    headers: getAuthHeaders()
  });
  return handleResponse<Issue[]>(response);
}

export async function fetchIssue(id: number): Promise<Issue> {
  const response = await fetch(`${API_BASE}/issues/${id}`, {
    headers: getAuthHeaders()
  });
  return handleResponse<Issue>(response);
}

export async function createIssue(data: FormData): Promise<Issue> {
  let token = null;
  if (browser) {
    token = localStorage.getItem('token');
  }

  const response = await fetch(`${API_BASE}/issues`, {
    method: 'POST',
    headers: {
      // ✅ Don't set Content-Type here
      ...(token && { Authorization: `Bearer ${token}` })
    },
    body: data // FormData auto sets content-type with boundary
  });

  return handleResponse<Issue>(response);
}

export async function updateIssue(id: number, update: IssueUpdate): Promise<Issue> {
  const response = await fetch(`${API_BASE}/issues/${id}`, {
    method: 'PATCH',
    headers: getAuthHeaders(),
    body: JSON.stringify(update)
  });
  return handleResponse<Issue>(response);
}

// ─────────────────────────────────────────
// Stats endpoints
// ─────────────────────────────────────────
export async function fetchDailyStats(): Promise<DailyStats[]> {
  const response = await fetch(`${API_BASE}/stats/daily`, {
    headers: getAuthHeaders()
  });
  return handleResponse<DailyStats[]>(response);
}

export async function fetchSeverityStats(): Promise<Record<string, number>> {
  const response = await fetch(`${API_BASE}/stats/severity`, {
    headers: getAuthHeaders()
  });
  return handleResponse<Record<string, number>>(response);
}

// ─────────────────────────────────────────
// Analytics endpoint (alternative solution)
// ─────────────────────────────────────────
export async function fetchAnalytics(): Promise<AnalyticsStats> {
  const response = await fetch(`${API_BASE}/stats/analytics`, {
    headers: getAuthHeaders()
  });
  return handleResponse<AnalyticsStats>(response);
}

// ─────────────────────────────────────────
// WebSocket connection
// ─────────────────────────────────────────
export function createWebSocketConnection() {
  if (!browser) return null;

  const ws = new WebSocket('ws://localhost:8000/ws/issues');

  ws.onopen = () => {
    console.log('✅ WebSocket connected');
  };

  ws.onerror = (error) => {
    console.error('❌ WebSocket error:', error);
  };

  return ws;
}
