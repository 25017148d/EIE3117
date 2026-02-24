<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '../stores/user';
import { useRouteStore } from '../stores/routes';
import NavBar from '../components/NavBar.vue';

const router = useRouter();
const userStore = useUserStore();
const routeStore = useRouteStore();

// Form Data
const routeForm = ref({
  date: '',
  time: '',
  startLocation: '',
  destination: '',
  carModel: '',
  totalSeats: 1,
  description: ''
});

const errorMsg = ref('');
const successMsg = ref('');

async function handleSubmit() {
  errorMsg.value = '';
  successMsg.value = '';

  try {
    if (!userStore.user || userStore.user.type !== 'driver') {
      throw new Error('Unauthorized');
    }

    await routeStore.addRoute({
      date: routeForm.value.date,
      time: routeForm.value.time,
      startLocation: routeForm.value.startLocation,
      destination: routeForm.value.destination,
      carModel: routeForm.value.carModel,
      totalSeats: routeForm.value.totalSeats,
      description: routeForm.value.description
    });

    successMsg.value = 'Route published successfully!';
    
    // Redirect after a short delay
    setTimeout(() => {
      router.push('/');
    }, 1500);
    
  } catch (e: any) {
    errorMsg.value = e.message;
  }
}
</script>

<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">
    <NavBar />
    
    <header class="bg-white shadow">
      <div class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <h1 class="text-3xl font-bold text-gray-900">Publish a Route</h1>
      </div>
    </header>

    <main class="flex-grow">
      <div class="max-w-3xl mx-auto py-6 sm:px-6 lg:px-8">
        <div class="bg-white shadow px-4 py-5 sm:rounded-lg sm:p-6">
          
          <div v-if="errorMsg" class="mb-4 bg-red-50 border-l-4 border-red-400 p-4">
            <div class="flex">
              <div class="flex-shrink-0">
                <svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
                </svg>
              </div>
              <div class="ml-3">
                <p class="text-sm text-red-700">{{ errorMsg }}</p>
              </div>
            </div>
          </div>

          <div v-if="successMsg" class="mb-4 bg-green-50 border-l-4 border-green-400 p-4">
            <div class="flex">
              <div class="flex-shrink-0">
                <svg class="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
                </svg>
              </div>
              <div class="ml-3">
                <p class="text-sm text-green-700">{{ successMsg }}</p>
              </div>
            </div>
          </div>

          <form @submit.prevent="handleSubmit" class="space-y-6">
            <div class="grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-6">
              
              <div class="sm:col-span-3">
                <label for="date" class="block text-sm font-medium text-gray-700">Date</label>
                <div class="mt-1">
                  <input type="date" name="date" id="date" v-model="routeForm.date" required class="shadow-sm focus:ring-primary focus:border-primary block w-full sm:text-sm border-gray-300 rounded-md">
                </div>
              </div>

              <div class="sm:col-span-3">
                <label for="time" class="block text-sm font-medium text-gray-700">Time</label>
                <div class="mt-1">
                  <input type="time" name="time" id="time" v-model="routeForm.time" required class="shadow-sm focus:ring-primary focus:border-primary block w-full sm:text-sm border-gray-300 rounded-md">
                </div>
              </div>

              <div class="sm:col-span-3">
                <label for="startLocation" class="block text-sm font-medium text-gray-700">From</label>
                <div class="mt-1">
                  <input type="text" name="startLocation" id="startLocation" v-model="routeForm.startLocation" required class="shadow-sm focus:ring-primary focus:border-primary block w-full sm:text-sm border-gray-300 rounded-md" placeholder="City or location">
                </div>
              </div>

              <div class="sm:col-span-3">
                <label for="destination" class="block text-sm font-medium text-gray-700">To</label>
                <div class="mt-1">
                  <input type="text" name="destination" id="destination" v-model="routeForm.destination" required class="shadow-sm focus:ring-primary focus:border-primary block w-full sm:text-sm border-gray-300 rounded-md" placeholder="City or location">
                </div>
              </div>

              <div class="sm:col-span-3">
                <label for="carModel" class="block text-sm font-medium text-gray-700">Car Model</label>
                <div class="mt-1">
                  <input type="text" name="carModel" id="carModel" v-model="routeForm.carModel" required class="shadow-sm focus:ring-primary focus:border-primary block w-full sm:text-sm border-gray-300 rounded-md" placeholder="e.g. Toyota Camry">
                </div>
              </div>

              <div class="sm:col-span-3">
                <label for="totalSeats" class="block text-sm font-medium text-gray-700">Available Seats</label>
                <div class="mt-1">
                  <input type="number" name="totalSeats" id="totalSeats" v-model="routeForm.totalSeats" min="1" max="8" required class="shadow-sm focus:ring-primary focus:border-primary block w-full sm:text-sm border-gray-300 rounded-md">
                </div>
              </div>

              <div class="sm:col-span-6">
                <label for="description" class="block text-sm font-medium text-gray-700">Description (Optional)</label>
                <div class="mt-1">
                  <textarea id="description" name="description" rows="3" v-model="routeForm.description" class="shadow-sm focus:ring-primary focus:border-primary block w-full sm:text-sm border border-gray-300 rounded-md" placeholder="Any additional details about the trip..."></textarea>
                </div>
              </div>
            </div>

            <div class="pt-5">
              <div class="flex justify-end">
                <button type="button" @click="router.back()" class="bg-white py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary">
                  Cancel
                </button>
                <button type="submit" class="ml-3 inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary">
                  Publish Route
                </button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </main>
  </div>
</template>
