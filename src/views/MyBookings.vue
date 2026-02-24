<script setup lang="ts">
import { onMounted } from 'vue';
import { storeToRefs } from 'pinia';
import { useRouteStore } from '../stores/routes';
import RouteCard from '../components/RouteCard.vue';
import NavBar from '../components/NavBar.vue';

const routeStore = useRouteStore();
const { myBookings } = storeToRefs(routeStore);

onMounted(() => {
  routeStore.fetchMyBookings();
});
</script>

<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">
    <NavBar />
    
    <header class="bg-white shadow">
      <div class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <h1 class="text-3xl font-bold text-gray-900">My Bookings</h1>
      </div>
    </header>
    
    <main class="flex-grow">
      <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        
        <div v-if="myBookings.length > 0" class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          <div v-for="route in myBookings" :key="route.id" class="col-span-1">
            <RouteCard :route="route" />
          </div>
        </div>
        
        <div v-else class="text-center py-12 bg-white shadow rounded-lg">
            <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                <path vector-effect="non-scaling-stroke" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <h3 class="mt-2 text-sm font-medium text-gray-900">No bookings yet</h3>
            <p class="mt-1 text-sm text-gray-500">You haven't booked any rides yet.</p>
            <div class="mt-6">
                <router-link to="/" class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary">
                    Browse Routes
                </router-link>
            </div>
        </div>
      </div>
    </main>
  </div>
</template>
