import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import axios from 'axios';
import { useUserStore } from './user';

export interface PassengerDetail {
  id: string;
  nickname: string;
  profileImage: string | null;
}

export interface Route {
  id: string;
  driverId: string;
  driverName: string;
  driverAvatar: string | null;
  date: string;
  time: string;
  startLocation: string;
  destination: string;
  carModel: string;
  totalSeats: number;
  availableSeats: number;
  description: string;
  passengers: string[];
  passengerDetails?: PassengerDetail[];
}

const API_BASE = 'http://localhost:8000/api';
const AUTH_KEY = 'authTokens';

function readAccessToken() {
  const local = localStorage.getItem(AUTH_KEY);
  if (local) return JSON.parse(local).access;
  const session = sessionStorage.getItem(AUTH_KEY);
  if (session) return JSON.parse(session).access;
  return null;
}

export const useRouteStore = defineStore('route', () => {
  localStorage.removeItem('allRoutes');
  const routes = ref<Route[]>([]);
  const myBookings = ref<Route[]>([]);
  const myRoutes = ref<Route[]>([]);
  const userStore = useUserStore();

  const availableRoutes = computed(() => routes.value);

  function authHeaders() {
    const token = readAccessToken();
    return token ? { Authorization: `Bearer ${token}` } : {};
  }

  function normalizeRoute(route: Route) {
    const passengers = (route.passengers || []).map(p => String(p));
    const passengerDetails = (route.passengerDetails || []).map(p => ({
      ...p,
      id: String(p.id),
      profileImage: p.profileImage || null
    }));
    return {
      ...route,
      id: String(route.id),
      driverId: String(route.driverId),
      driverAvatar: route.driverAvatar || null,
      passengers,
      passengerDetails
    };
  }

  function mergeRoute(route: Route) {
    const normalized = normalizeRoute(route);
    const index = routes.value.findIndex(r => r.id === normalized.id);
    if (index >= 0) {
      routes.value[index] = normalized;
    } else {
      routes.value.unshift(normalized);
    }
  }

  function getRouteById(id: string) {
    const targetId = String(id);
    return (
      routes.value.find(r => r.id === targetId) ||
      myRoutes.value.find(r => r.id === targetId) ||
      myBookings.value.find(r => r.id === targetId)
    );
  }

  function cacheFromRoutes(list: Route[]) {
    const users = list.flatMap(route => {
      const driver = {
        id: route.driverId,
        loginId: '',
        nickname: route.driverName,
        email: '',
        type: 'driver' as const,
        profileImage: route.driverAvatar
      };
      const passengers = (route.passengerDetails || []).map(p => ({
        id: p.id,
        loginId: '',
        nickname: p.nickname,
        email: '',
        type: 'passenger' as const,
        profileImage: p.profileImage || null
      }));
      return [driver, ...passengers];
    });
    userStore.cacheUsers(users);
  }

  async function fetchRoutes() {
    const resp = await axios.get(`${API_BASE}/routes/`);
    routes.value = resp.data.map((route: Route) => normalizeRoute(route));
    cacheFromRoutes(routes.value);
  }

  async function fetchRouteById(id: string) {
    const resp = await axios.get(`${API_BASE}/routes/${id}/`);
    const normalized = normalizeRoute(resp.data);
    mergeRoute(normalized);
    cacheFromRoutes([normalized]);
    return normalized as Route;
  }

  async function fetchMyBookings() {
    const resp = await axios.get(`${API_BASE}/routes/my-bookings/`, { headers: authHeaders() });
    myBookings.value = resp.data.map((route: Route) => normalizeRoute(route));
    cacheFromRoutes(myBookings.value);
  }

  async function fetchMyRoutes() {
    const resp = await axios.get(`${API_BASE}/routes/my-routes/`, { headers: authHeaders() });
    myRoutes.value = resp.data.map((route: Route) => normalizeRoute(route));
    cacheFromRoutes(myRoutes.value);
  }

  async function addRoute(routeData: Omit<Route, 'id' | 'driverId' | 'driverName' | 'driverAvatar' | 'availableSeats' | 'passengers' | 'passengerDetails'>) {
    const resp = await axios.post(`${API_BASE}/routes/`, routeData, { headers: authHeaders() });
    const normalized = normalizeRoute(resp.data);
    mergeRoute(normalized);
    myRoutes.value = [normalized, ...myRoutes.value];
    return normalized as Route;
  }

  async function bookRoute(routeId: string) {
    const resp = await axios.post(`${API_BASE}/routes/${routeId}/book/`, {}, { headers: authHeaders() });
    mergeRoute(resp.data);
    await fetchMyBookings();
    return resp.data as Route;
  }

  async function cancelBooking(routeId: string) {
    const resp = await axios.delete(`${API_BASE}/routes/${routeId}/book/`, { headers: authHeaders() });
    mergeRoute(resp.data);
    await fetchMyBookings();
    return resp.data as Route;
  }

  return {
    routes,
    myBookings,
    myRoutes,
    availableRoutes,
    getRouteById,
    fetchRoutes,
    fetchRouteById,
    fetchMyBookings,
    fetchMyRoutes,
    addRoute,
    bookRoute,
    cancelBooking
  };
});
