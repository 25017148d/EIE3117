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
  const local = localStorage.getItem(AUTH_KEY);
  if (local) return { tokens: JSON.parse(local), storage: localStorage };
  const session = sessionStorage.getItem(AUTH_KEY);
  if (session) return { tokens: JSON.parse(session), storage: sessionStorage };
  return { tokens: null, storage: null };
}

function writeTokens(tokens: { access: string; refresh: string }, rememberMe: boolean) {
  const storage = rememberMe ? localStorage : sessionStorage;
  storage.setItem(AUTH_KEY, JSON.stringify(tokens));
  if (!rememberMe) {
    localStorage.removeItem(AUTH_KEY);
  }
  if (rememberMe) {
    sessionStorage.removeItem(AUTH_KEY);
  }
}

function clearTokens() {
  localStorage.removeItem(AUTH_KEY);
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
    writeTokens(tokenResp.data, rememberMe);
    setAxiosAuth(tokenResp.data.access);
    await fetchMe();
  }

  async function fetchMe() {
    const { tokens } = readTokens();
    if (!tokens?.access) throw new Error('No token');
    setAxiosAuth(tokens.access);
    const meResp = await axios.get(`${API_BASE}/auth/me/`, {
      headers: { Authorization: `Bearer ${tokens.access}` }
    });
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
