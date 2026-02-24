<script setup lang="ts">
import { computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useRouteStore } from '../stores/routes';
import { useUserStore } from '../stores/user';
import NavBar from '../components/NavBar.vue';

const route = useRoute();
const router = useRouter();
const routeStore = useRouteStore();
const userStore = useUserStore();

const routeId = route.params.id as string;
const currentRoute = computed(() => routeStore.getRouteById(routeId));

const isPassenger = computed(() => userStore.user?.type === 'passenger');
const isDriver = computed(() => userStore.user?.type === 'driver');
const isMyRoute = computed(() => currentRoute.value?.driverId === userStore.user?.id);
const isBooked = computed(() => currentRoute.value?.passengers.includes(userStore.user?.id || ''));
const isFull = computed(() => (currentRoute.value?.availableSeats || 0) <= 0);

async function handleBook() {
  if (!userStore.isAuthenticated) {
    router.push('/auth');
    return;
  }
  try {
    await routeStore.bookRoute(routeId);
    alert('Booked successfully!');
  } catch (e: any) {
    alert(e.message);
  }
}

async function handleCancel() {
  try {
    await routeStore.cancelBooking(routeId);
    alert('Cancelled successfully!');
  } catch (e: any) {
    alert(e.message);
  }
}

function getPassengerName(userId: string) {
  const user = userStore.getUserById(userId);
  return user ? user.nickname : 'Unknown User';
}

onMounted(async () => {
    if (!currentRoute.value) {
        await routeStore.fetchRouteById(routeId);
    }
});
</script>

<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">
    <NavBar />
    
    <main class="flex-grow py-10">
      <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
        
        <div v-if="!currentRoute" class="text-center py-12">
            <h3 class="mt-2 text-sm font-medium text-gray-900">Route not found</h3>
            <div class="mt-6">
                <router-link to="/" class="text-primary hover:text-blue-600">Go back home</router-link>
            </div>
        </div>
        
        <div v-else class="bg-white shadow overflow-hidden sm:rounded-lg">
          <div class="px-4 py-5 sm:px-6 flex justify-between items-center">
            <div>
              <h3 class="text-lg leading-6 font-medium text-gray-900">Route Details</h3>
              <p class="mt-1 max-w-2xl text-sm text-gray-500">Full information about the trip.</p>
            </div>
            <div v-if="isPassenger">
                <span v-if="isBooked" class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                  Booked
                </span>
                <span v-else-if="isFull" class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-red-100 text-red-800">
                  Full
                </span>
                <span v-else class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-blue-100 text-blue-800">
                  Available
                </span>
            </div>
          </div>
          
          <div class="border-t border-gray-200 px-4 py-5 sm:p-0">
            <dl class="sm:divide-y sm:divide-gray-200">
              
              <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-gray-500">Driver</dt>
                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2 flex items-center">
                    <img class="h-8 w-8 rounded-full mr-3" :src="currentRoute.driverAvatar || `https://i.pravatar.cc/150?u=${currentRoute.driverId}`" alt="">
                    <span>{{ currentRoute.driverName }}</span>
                </dd>
              </div>

              <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-gray-500">From</dt>
                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{{ currentRoute.startLocation }}</dd>
              </div>

              <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-gray-500">To</dt>
                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{{ currentRoute.destination }}</dd>
              </div>

              <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-gray-500">Date & Time</dt>
                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{{ currentRoute.date }} at {{ currentRoute.time }}</dd>
              </div>

              <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-gray-500">Car Model</dt>
                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{{ currentRoute.carModel }}</dd>
              </div>

              <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-gray-500">Seats</dt>
                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                    {{ currentRoute.availableSeats }} available / {{ currentRoute.totalSeats }} total
                </dd>
              </div>

              <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-gray-500">Description</dt>
                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{{ currentRoute.description || 'No description provided.' }}</dd>
              </div>
              
              <!-- Driver Only: Passenger List -->
              <div v-if="isDriver && isMyRoute" class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6 bg-gray-50">
                <dt class="text-sm font-medium text-gray-500">Passengers</dt>
                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                    <ul v-if="currentRoute.passengerDetails ? currentRoute.passengerDetails.length > 0 : currentRoute.passengers.length > 0" class="border border-gray-200 rounded-md divide-y divide-gray-200">
                        <li v-for="passenger in currentRoute.passengerDetails || []" :key="passenger.id" class="pl-3 pr-4 py-3 flex items-center justify-between text-sm">
                            <div class="w-0 flex-1 flex items-center">
                                <span class="ml-2 flex-1 w-0 truncate">{{ passenger.nickname }}</span>
                            </div>
                        </li>
                        <li v-for="passengerId in currentRoute.passengerDetails ? [] : currentRoute.passengers" :key="passengerId" class="pl-3 pr-4 py-3 flex items-center justify-between text-sm">
                            <div class="w-0 flex-1 flex items-center">
                                <span class="ml-2 flex-1 w-0 truncate">{{ getPassengerName(passengerId) }}</span>
                            </div>
                        </li>
                    </ul>
                    <span v-else class="text-gray-500 italic">No passengers yet.</span>
                </dd>
              </div>

            </dl>
          </div>
          
          <div class="bg-gray-50 px-4 py-4 sm:px-6 flex justify-end gap-4">
            <button @click="router.back()" type="button" class="bg-white py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary">
              Back
            </button>
            
            <template v-if="isPassenger">
                <button v-if="!isBooked && !isFull" @click="handleBook" type="button" class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary">
                  Book Seat
                </button>
                <button v-else-if="isBooked" @click="handleCancel" type="button" class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500">
                  Cancel Booking
                </button>
            </template>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>
