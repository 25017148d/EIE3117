<script setup lang="ts">
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '../stores/user';
import { useRouteStore } from '../stores/routes';
import type { Route } from '../stores/routes';

const props = defineProps<{
  route: Route;
}>();

const router = useRouter();
const userStore = useUserStore();
const routeStore = useRouteStore();

const isPassenger = computed(() => userStore.user?.type === 'passenger');
const isDriver = computed(() => userStore.user?.type === 'driver');
const isMyRoute = computed(() => props.route.driverId === userStore.user?.id);
const isBooked = computed(() => props.route.passengers.includes(userStore.user?.id || ''));
const isFull = computed(() => props.route.availableSeats <= 0);

async function handleBook() {
  if (!userStore.isAuthenticated) {
    router.push('/auth');
    return;
  }
  try {
    await routeStore.bookRoute(props.route.id);
    alert('Booked successfully!');
  } catch (e: any) {
    alert(e.message);
  }
}

async function handleCancel() {
  try {
    await routeStore.cancelBooking(props.route.id);
    alert('Cancelled successfully!');
  } catch (e: any) {
    alert(e.message);
  }
}

function handleView() {
  router.push(`/routes/${props.route.id}`);
}
</script>

<template>
  <div class="bg-white overflow-hidden shadow rounded-lg hover:shadow-md transition-shadow duration-200 border border-gray-100 flex flex-col h-full">
    <div class="px-4 py-5 sm:p-6 flex-grow">
      <div class="flex items-center justify-between mb-4">
        <div class="flex items-center space-x-3">
          <img class="h-10 w-10 rounded-full object-cover border border-gray-200" :src="route.driverAvatar || `https://i.pravatar.cc/150?u=${route.driverId}`" alt="" />
          <div>
            <p class="text-sm font-medium text-gray-900 truncate">{{ route.driverName }}</p>
            <p class="text-xs text-gray-500 truncate">Driver</p>
          </div>
        </div>
        <div class="bg-blue-50 text-blue-700 text-xs px-2 py-1 rounded-full font-medium">
            {{ route.availableSeats }} seats left
        </div>
      </div>
      
      <div class="space-y-3">
        <div class="flex justify-between items-start">
            <div>
                <p class="text-xs text-gray-500 uppercase tracking-wide font-semibold">From</p>
                <p class="text-lg font-medium text-gray-900">{{ route.startLocation }}</p>
            </div>
            <div class="text-gray-400">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"></path></svg>
            </div>
            <div class="text-right">
                <p class="text-xs text-gray-500 uppercase tracking-wide font-semibold">To</p>
                <p class="text-lg font-medium text-gray-900">{{ route.destination }}</p>
            </div>
        </div>

        <div class="border-t border-gray-100 pt-3 flex justify-between text-sm">
            <div class="flex items-center text-gray-500">
                <svg class="mr-1.5 h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
                {{ route.date }}
            </div>
            <div class="flex items-center text-gray-500">
                <svg class="mr-1.5 h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                {{ route.time }}
            </div>
        </div>
        
        <p class="text-sm text-gray-600 mt-2 line-clamp-2">{{ route.description }}</p>
      </div>
    </div>
    
    <div class="bg-gray-50 px-4 py-4 sm:px-6 flex justify-between items-center border-t border-gray-100">
      <button @click="handleView" class="text-sm font-medium text-primary hover:text-blue-600 transition-colors">
        View Details
      </button>
      
      <div v-if="isPassenger">
          <button v-if="!isBooked && !isFull" @click="handleBook" class="inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded text-white bg-primary hover:bg-blue-600 shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary transition-colors">
            Book Seat
          </button>
          <button v-else-if="isBooked" @click="handleCancel" class="inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded text-red-700 bg-red-100 hover:bg-red-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition-colors">
            Cancel
          </button>
          <span v-else class="text-xs font-medium text-gray-400 bg-gray-100 px-2 py-1 rounded">Full</span>
      </div>
      <div v-else-if="isDriver && isMyRoute">
          <span class="text-xs font-medium text-green-600 bg-green-100 px-2 py-1 rounded">My Route</span>
      </div>
    </div>
  </div>
</template>
