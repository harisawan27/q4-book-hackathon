/**
 * Authentication API client for the Docusaurus book.
 * Handles signup, signin, signout, and session management.
 */

// API URL - defaults to localhost for development
// In production, set this via your hosting platform's environment variables
const getApiUrl = (): string => {
  // Check if we're in the browser
  if (typeof window !== 'undefined') {
    // Allow runtime configuration via window object (can be set in index.html)
    if ((window as any).__API_URL__) {
      return (window as any).__API_URL__;
    }
    // Default to same origin /api/v1 in production, localhost in development
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
      return 'http://localhost:8000/api/v1';
    }
    // In production, assume API is at same origin
    return `https://q4-book-hackathon-backend.vercel.app/api/v1`;
  }
  // Server-side rendering fallback
  return 'https://q4-book-hackathon-backend.vercel.app/api/v1';
};

const API_URL = getApiUrl();

// Types
export interface UserBackground {
  software_skills: 'none' | 'beginner' | 'intermediate' | 'advanced';
  hardware_skills: 'none' | 'beginner' | 'intermediate' | 'advanced';
  experience_level: 'student' | 'professional' | 'hobbyist' | 'researcher';
}

export interface User {
  id: string;
  email: string;
  name?: string;
  email_verified?: string;
  created_at: string;
}

export interface UserProfile extends User {
  background?: UserBackgroundResponse;
}

export interface UserBackgroundResponse extends UserBackground {
  id: string;
  user_id: string;
  created_at: string;
  updated_at: string;
}

export interface AuthResponse {
  user: User;
  token: string;
  expires_at: string;
}

export interface SessionResponse {
  user: User;
  expires_at: string;
  has_background: boolean;
}

// Token storage
let authToken: string | null = null;

export function getToken(): string | null {
  if (typeof window === 'undefined') return null;
  if (authToken) return authToken;
  return localStorage.getItem('auth_token');
}

export function setToken(token: string): void {
  authToken = token;
  if (typeof window !== 'undefined') {
    localStorage.setItem('auth_token', token);
  }
}

export function clearToken(): void {
  authToken = null;
  if (typeof window !== 'undefined') {
    localStorage.removeItem('auth_token');
  }
}

// API helpers
async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = getToken();
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...(options.headers || {}),
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ message: 'Request failed' }));
    throw new Error(error.message || error.detail || 'Request failed');
  }

  return response.json();
}

// Auth API functions
export async function signUp(
  email: string,
  password: string,
  name?: string,
  background?: UserBackground
): Promise<AuthResponse> {
  const response = await apiRequest<AuthResponse>('/auth/signup', {
    method: 'POST',
    body: JSON.stringify({ email, password, name, background }),
  });

  setToken(response.token);
  return response;
}

export async function signIn(email: string, password: string): Promise<AuthResponse> {
  const response = await apiRequest<AuthResponse>('/auth/signin', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  });

  setToken(response.token);
  return response;
}

export async function signOut(): Promise<void> {
  try {
    await apiRequest('/auth/signout', { method: 'POST' });
  } finally {
    clearToken();
  }
}

export async function getSession(): Promise<SessionResponse | null> {
  try {
    return await apiRequest<SessionResponse>('/auth/session');
  } catch {
    clearToken();
    return null;
  }
}

// Profile API functions
export async function getProfile(): Promise<UserProfile> {
  return apiRequest<UserProfile>('/profile');
}

export async function getBackground(): Promise<UserBackgroundResponse> {
  return apiRequest<UserBackgroundResponse>('/profile/background');
}

export async function updateBackground(background: UserBackground): Promise<UserBackgroundResponse> {
  return apiRequest<UserBackgroundResponse>('/profile/background', {
    method: 'PUT',
    body: JSON.stringify(background),
  });
}

// Content transformation API functions
export interface TransformationResponse {
  content: string;
  original_length: number;
  transformed_length: number;
  duration_ms: number;
  transformation_type: 'personalization' | 'translation';
}

export async function personalizeContent(
  chapterSlug: string,
  content: string
): Promise<TransformationResponse> {
  return apiRequest<TransformationResponse>('/content/personalize', {
    method: 'POST',
    body: JSON.stringify({ chapter_slug: chapterSlug, content }),
  });
}

export async function translateContent(
  chapterSlug: string,
  content: string
): Promise<TransformationResponse> {
  return apiRequest<TransformationResponse>('/content/translate', {
    method: 'POST',
    body: JSON.stringify({ chapter_slug: chapterSlug, content }),
  });
}

export interface TransformationLog {
  id: string;
  chapter_slug: string;
  transformation_type: string;
  input_length: number;
  output_length: number;
  duration_ms: number;
  success: boolean;
  error_message?: string;
  created_at: string;
}

export interface TransformationLogsResponse {
  logs: TransformationLog[];
  total: number;
  limit: number;
  offset: number;
}

export async function getTransformationLogs(
  limit = 20,
  offset = 0,
  type?: 'personalization' | 'translation'
): Promise<TransformationLogsResponse> {
  const params = new URLSearchParams({ limit: String(limit), offset: String(offset) });
  if (type) params.append('type', type);
  return apiRequest<TransformationLogsResponse>(`/content/logs?${params}`);
}
