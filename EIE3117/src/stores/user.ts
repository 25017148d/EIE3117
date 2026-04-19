import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import axios from 'axios';

export interface User {
  id: string;
  loginId: string;
  nickname: string;
  email: string;
  type: 'passenger' | 'driver';
  profileImage: string | null;
}

const API_BASE = 'http://localhost:8000/api';
const AUTH_KEY = 'authTokens';

function readTokens() {
  const session = sessionStorage.getItem(AUTH_KEY);
  if (session) return { tokens: JSON.parse(session), storage: sessionStorage };
  return { tokens: null, storage: null };
}

// Store only the short-lived access token in sessionStorage by default.
function writeTokens(tokens: { access?: string }, rememberMe: boolean) {
  // For security, avoid persistent localStorage by default. If rememberMe is true
  // you may implement a more explicit opt-in flow; keep here using sessionStorage.
  if (tokens && tokens.access) {
    sessionStorage.setItem(AUTH_KEY, JSON.stringify(tokens));
  }
}

function clearTokens() {
  sessionStorage.removeItem(AUTH_KEY);
}

function setAxiosAuth(token: string | null) {
  if (token) {
    axios.defaults.headers.common.Authorization = `Bearer ${token}`;
  } else {
    delete axios.defaults.headers.common.Authorization;
  }
}

function normalizeUser(user: User): User {
  return {
    ...user,
    id: String(user.id),
    profileImage: user.profileImage || null
  };
}

export const useUserStore = defineStore('user', () => {
  localStorage.removeItem('allUsers');
  localStorage.removeItem('currentUser');
  sessionStorage.removeItem('currentUser');
  const user = ref<User | null>(null);
  const userCache = ref<Record<string, User>>({});
  const isAuthenticated = computed(() => !!user.value);

  async function register(userData: Omit<User, 'id'> & { password: string; passwordConfirm: string }) {
    const payload = {
      loginId: userData.loginId,
      nickname: userData.nickname,
      email: userData.email,
      type: userData.type,
      profileImage: userData.profileImage,
      password: userData.password,
      password2: userData.passwordConfirm
    };
    await axios.post(`${API_BASE}/auth/register/`, payload);
    await login(userData.loginId, userData.password, true);
  }

  async function login(loginId: string, password: string, rememberMe: boolean) {
    const tokenResp = await axios.post(`${API_BASE}/auth/token/`, {
      username: loginId,
      password
    });
    // Backend now sets refresh token in an HttpOnly cookie; response contains access.
    writeTokens(tokenResp.data, rememberMe);
    setAxiosAuth(tokenResp.data.access || null);
    await fetchMe();
  }

  async function fetchMe() {
    const { tokens } = readTokens();
    if (!tokens?.access) throw new Error('No token');
    setAxiosAuth(tokens.access);
    const meResp = await axios.get(`${API_BASE}/auth/me/`);
    user.value = normalizeUser(meResp.data);
    cacheUsers([user.value]);
  }

  async function checkAuth() {
    const { tokens } = readTokens();
    if (!tokens?.access) {
      user.value = null;
      setAxiosAuth(null);
      return;
    }
    try {
      await fetchMe();
    } catch {
      clearTokens();
      setAxiosAuth(null);
      user.value = null;
    }
  }

  function logout() {
    user.value = null;
    clearTokens();
    setAxiosAuth(null);
  }

  function cacheUsers(users: User[]) {
    const map = { ...userCache.value };
    users.forEach(u => {
      const normalized = normalizeUser(u);
      map[normalized.id] = normalized;
    });
    userCache.value = map;
  }

  function getUserById(id: string) {
    return userCache.value[id];
  }

  return {
    user,
    isAuthenticated,
    register,
    login,
    logout,
    checkAuth,
    getUserById,
    cacheUsers
  };
});
