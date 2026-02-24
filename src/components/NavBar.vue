<script setup lang="ts">
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '../stores/user';

const router = useRouter();
const userStore = useUserStore();

const isAuthenticated = computed(() => userStore.isAuthenticated);
const user = computed(() => userStore.user);

function handleLogout() {
  userStore.logout();
  router.push('/auth');
}

function navigateTo(path: string) {
  router.push(path);
}
</script>

<template>
  <nav class="bg-white shadow-sm border-b border-gray-100">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <div class="flex">
          <div class="flex-shrink-0 flex items-center cursor-pointer" @click="navigateTo('/')">
            <span class="text-xl font-bold text-primary">RideShare</span>
          </div>
          <div class="hidden sm:ml-6 sm:flex sm:space-x-8">
            <a @click="navigateTo('/')" class="cursor-pointer border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">
              Routes
            </a>
            <a v-if="user?.type === 'driver'" @click="navigateTo('/publish')" class="cursor-pointer border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">
              Publish Route
            </a>
          </div>
        </div>
        <div class="flex items-center">
          <div v-if="!isAuthenticated" class="flex-shrink-0">
            <button @click="navigateTo('/auth')" type="button" class="relative inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary shadow-sm transition-colors duration-200">
              Login / Register
            </button>
          </div>
          <div v-else class="ml-3 relative flex items-center gap-4">
            <div class="flex flex-col items-end">
                <span class="text-sm font-medium text-gray-900">{{ user?.nickname }}</span>
                <span class="text-xs text-gray-500 capitalize">{{ user?.type }}</span>
            </div>
            <div class="relative group">
                <button class="bg-white rounded-full flex text-sm focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary items-center justify-center h-8 w-8 overflow-hidden border border-gray-200">
                  <img v-if="user?.profileImage" class="h-full w-full object-cover" :src="user.profileImage" alt="">
                  <span v-else class="h-full w-full flex items-center justify-center bg-gray-100 text-gray-400">
                    <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M24 20.993V24H0v-2.996A14.977 14.977 0 0112.004 15c4.904 0 9.26 2.354 11.996 5.993zM16.002 8.999a4 4 0 11-8 0 4 4 0 018 0z" />
                    </svg>
                  </span>
                </button>
                <!-- Dropdown -->
                <div class="origin-top-right absolute right-0 top-full pt-1 w-48 hidden group-hover:block z-50">
                    <div class="rounded-md shadow-lg py-1 bg-white ring-1 ring-black ring-opacity-5 focus:outline-none">
                        <a v-if="user?.type === 'passenger'" @click="navigateTo('/my-bookings')" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 cursor-pointer">My Bookings</a>
                        <a v-if="user?.type === 'driver'" @click="navigateTo('/my-routes')" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 cursor-pointer">My Published Routes</a>
                        <a @click="handleLogout" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 cursor-pointer">Sign out</a>
                    </div>
                </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Mobile menu, show/hide based on menu state. -->
    <div class="sm:hidden border-t border-gray-200">
        <div class="pt-2 pb-3 space-y-1">
            <a @click="navigateTo('/')" class="bg-indigo-50 border-primary text-primary block pl-3 pr-4 py-2 border-l-4 text-base font-medium">Routes</a>
            <a v-if="user?.type === 'driver'" @click="navigateTo('/publish')" class="border-transparent text-gray-500 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-700 block pl-3 pr-4 py-2 border-l-4 text-base font-medium">Publish Route</a>
        </div>
    </div>
  </nav>
</template>
