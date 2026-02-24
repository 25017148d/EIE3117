<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">
    <NavBar />
    
    <div class="container mx-auto px-4 py-8">
      <div class="max-w-7xl mx-auto">
        <h1 class="text-3xl font-bold text-gray-900 mb-8">My Published Routes</h1>
        
        <div v-if="routes.length === 0" class="text-center py-12 bg-white rounded-lg shadow-sm">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
          </svg>
          <h3 class="mt-2 text-sm font-medium text-gray-900">No routes published</h3>
          <p class="mt-1 text-sm text-gray-500">Get started by creating a new route.</p>
          <div class="mt-6">
            <button @click="$router.push('/publish')" type="button" class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary">
              Create Route
            </button>
          </div>
        </div>
        
        <div v-else class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          <div v-for="route in routes" :key="route.id" class="flex flex-col bg-white rounded-lg shadow overflow-hidden border border-gray-100">
             <!-- Route Card (Reusing component for consistent style) -->
             <div class="flex-grow">
                 <RouteCard :route="route" class="h-full shadow-none border-0 rounded-none" />
             </div>

             <!-- Passenger List Section -->
             <div class="px-4 py-4 bg-gray-50 border-t border-gray-100">
                 <div class="flex justify-between items-center mb-3">
                   <h4 class="text-xs font-semibold text-gray-500 uppercase tracking-wider">
                       Passengers ({{ route.passengerDetails ? route.passengerDetails.length : route.passengers.length }})
                   </h4>
                 </div>
                 
                 <ul v-if="route.passengerDetails ? route.passengerDetails.length > 0 : route.passengers.length > 0" class="space-y-3">
                     <li v-for="passenger in route.passengerDetails || []" :key="passenger.id" class="flex items-center justify-between bg-white p-2 rounded border border-gray-200 shadow-sm">
                         <div class="flex items-center min-w-0">
                             <div class="h-8 w-8 rounded-full bg-primary/10 flex items-center justify-center text-xs font-bold text-primary flex-shrink-0">
                                 {{ passenger.nickname.charAt(0).toUpperCase() }}
                             </div>
                             <span class="ml-2 text-sm text-gray-700 truncate font-medium">{{ passenger.nickname }}</span>
                         </div>
                     </li>
                     <li v-for="passengerId in route.passengerDetails ? [] : route.passengers" :key="passengerId" class="flex items-center justify-between bg-white p-2 rounded border border-gray-200 shadow-sm">
                         <div class="flex items-center min-w-0">
                             <div class="h-8 w-8 rounded-full bg-primary/10 flex items-center justify-center text-xs font-bold text-primary flex-shrink-0">
                                 {{ getPassengerName(passengerId).charAt(0).toUpperCase() }}
                             </div>
                             <span class="ml-2 text-sm text-gray-700 truncate font-medium">{{ getPassengerName(passengerId) }}</span>
                         </div>
                     </li>
                 </ul>
                 <p v-else class="text-sm text-gray-400 italic text-center py-2">No bookings yet.</p>
             </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { storeToRefs } from 'pinia';
import { useRouteStore } from '../stores/routes';
import { useUserStore } from '../stores/user';
import NavBar from '../components/NavBar.vue';
import RouteCard from '../components/RouteCard.vue';

const routeStore = useRouteStore();
const userStore = useUserStore();

const { myRoutes: routes } = storeToRefs(routeStore);

function getPassengerName(passengerId: string) {
    const user = userStore.getUserById(passengerId);
    return user ? user.nickname : 'Unknown User';
}

onMounted(() => {
  routeStore.fetchMyRoutes();
});
</script>
