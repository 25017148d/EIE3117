<script setup lang="ts">
import { computed, ref, onMounted } from 'vue';
import { storeToRefs } from 'pinia';
import { useRouteStore } from '../stores/routes';
import { useUserStore } from '../stores/user';
import RouteCard from '../components/RouteCard.vue';
import NavBar from '../components/NavBar.vue';

const routeStore = useRouteStore();
const userStore = useUserStore();
const { availableRoutes: routes } = storeToRefs(routeStore);

const filterDate = ref('');
const filterStart = ref('');
const filterDest = ref('');

const filteredRoutes = computed(() => {
  return routes.value.filter(route => {
    // Filter by user role - hide own routes for drivers
    if (userStore.user && route.driverId === userStore.user.id) return false;

    if (filterDate.value && route.date !== filterDate.value) return false;
    if (filterStart.value && !route.startLocation.toLowerCase().includes(filterStart.value.toLowerCase())) return false;
    if (filterDest.value && !route.destination.toLowerCase().includes(filterDest.value.toLowerCase())) return false;
    return true;
  });
});

onMounted(() => {
  routeStore.fetchRoutes();
});
</script>

<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">
    <NavBar />
    
    <header class="bg-white shadow">
      <div class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <h1 class="text-3xl font-bold text-gray-900">Available Routes</h1>
        <p class="mt-2 text-sm text-gray-500">Find a ride that matches your schedule and destination.</p>
      </div>
    </header>
    
    <main class="flex-grow">
      <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <!-- Filter Section -->
        <div class="bg-white shadow px-4 py-5 sm:rounded-lg sm:p-6 mb-8">
            <div class="grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-6">
                <div class="sm:col-span-2">
                    <label for="start" class="block text-sm font-medium text-gray-700">From</label>
                    <div class="mt-1">
                        <input type="text" v-model="filterStart" name="start" id="start" class="shadow-sm focus:ring-primary focus:border-primary block w-full sm:text-sm border-gray-300 rounded-md" placeholder="City or location">
                    </div>
                </div>

                <div class="sm:col-span-2">
                    <label for="destination" class="block text-sm font-medium text-gray-700">To</label>
                    <div class="mt-1">
                        <input type="text" v-model="filterDest" name="destination" id="destination" class="shadow-sm focus:ring-primary focus:border-primary block w-full sm:text-sm border-gray-300 rounded-md" placeholder="City or location">
                    </div>
                </div>

                <div class="sm:col-span-2">
                    <label for="date" class="block text-sm font-medium text-gray-700">Date</label>
                    <div class="mt-1">
                        <input type="date" v-model="filterDate" name="date" id="date" class="shadow-sm focus:ring-primary focus:border-primary block w-full sm:text-sm border-gray-300 rounded-md">
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Route Grid -->
        <div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          <div v-for="route in filteredRoutes" :key="route.id" class="col-span-1">
            <RouteCard :route="route" />
          </div>
        </div>
        
        <div v-if="filteredRoutes.length === 0" class="text-center py-12">
            <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                <path vector-effect="non-scaling-stroke" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 13h6m-3-3v6m-9 1V7a2 2 0 012-2h6l2 2h6a2 2 0 012 2v8a2 2 0 01-2 2H5a2 2 0 01-2-2z" />
            </svg>
            <h3 class="mt-2 text-sm font-medium text-gray-900">No routes found</h3>
            <p class="mt-1 text-sm text-gray-500">Try adjusting your search criteria.</p>
        </div>
      </div>
    </main>
    
    <footer class="bg-white border-t border-gray-200 mt-auto">
        <div class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
            <p class="text-center text-sm text-gray-500">&copy; 2026 RideShare. All rights reserved.</p>
        </div>
    </footer>
  </div>
</template>
