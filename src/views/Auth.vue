<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '../stores/user';
import NavBar from '../components/NavBar.vue';

const router = useRouter();
const userStore = useUserStore();

const activeTab = ref<'login' | 'register'>('login');

// Login Form Data
const loginForm = ref({
  loginId: '',
  password: '',
  rememberMe: false
});

// Register Form Data
const registerForm = ref({
  loginId: '',
  nickname: '',
  email: '',
  password: '',
  passwordConfirm: '',
  type: 'passenger' as 'passenger' | 'driver',
  profileImage: null as File | null
});

const errorMsg = ref('');

async function handleLogin() {
  errorMsg.value = '';
  try {
    await userStore.login(loginForm.value.loginId, loginForm.value.password, loginForm.value.rememberMe);
    router.push('/');
  } catch (e: any) {
    errorMsg.value = e.message;
  }
}

async function handleRegister() {
  errorMsg.value = '';
  try {
    if (registerForm.value.password !== registerForm.value.passwordConfirm) {
      errorMsg.value = 'Passwords do not match';
      return;
    }
    // Mock image upload handling (convert to base64 for preview/storage)
    let profileImageUrl = '';
    if (registerForm.value.profileImage) {
        const reader = new FileReader();
        reader.readAsDataURL(registerForm.value.profileImage);
        await new Promise((resolve) => {
            reader.onload = () => {
                profileImageUrl = reader.result as string;
                resolve(null);
            };
        });
    }

    await userStore.register({
        loginId: registerForm.value.loginId,
        nickname: registerForm.value.nickname,
        email: registerForm.value.email,
        type: registerForm.value.type,
        profileImage: profileImageUrl || null,
        password: registerForm.value.password,
        passwordConfirm: registerForm.value.passwordConfirm
    });
    router.push('/');
  } catch (e: any) {
    errorMsg.value = e.message;
  }
}

function onFileChange(e: Event) {
    const target = e.target as HTMLInputElement;
    if (target.files && target.files[0]) {
        registerForm.value.profileImage = target.files[0];
    }
}
</script>

<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">
    <NavBar />
    
    <div class="flex-grow flex flex-col justify-center py-12 sm:px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
        {{ activeTab === 'login' ? 'Sign in to your account' : 'Create a new account' }}
      </h2>
    </div>

    <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
      <div class="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
        
        <!-- Tabs -->
        <div class="flex border-b border-gray-200 mb-6">
            <button 
                class="flex-1 py-2 text-center text-sm font-medium focus:outline-none"
                :class="activeTab === 'login' ? 'text-primary border-b-2 border-primary' : 'text-gray-500 hover:text-gray-700'"
                @click="activeTab = 'login'"
            >
                Login
            </button>
            <button 
                class="flex-1 py-2 text-center text-sm font-medium focus:outline-none"
                :class="activeTab === 'register' ? 'text-primary border-b-2 border-primary' : 'text-gray-500 hover:text-gray-700'"
                @click="activeTab = 'register'"
            >
                Register
            </button>
        </div>

        <!-- Error Message -->
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

        <!-- Login Form -->
        <form v-if="activeTab === 'login'" class="space-y-6" @submit.prevent="handleLogin">
          <div>
            <label for="loginId" class="block text-sm font-medium text-gray-700"> Login ID </label>
            <div class="mt-1">
              <input v-model="loginForm.loginId" id="loginId" name="loginId" type="text" required class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-primary focus:border-primary sm:text-sm">
            </div>
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-gray-700"> Password </label>
            <div class="mt-1">
              <input v-model="loginForm.password" id="password" name="password" type="password" required class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-primary focus:border-primary sm:text-sm">
            </div>
          </div>

          <div class="flex items-center justify-between">
            <div class="flex items-center">
              <input v-model="loginForm.rememberMe" id="remember-me" name="remember-me" type="checkbox" class="h-4 w-4 text-primary focus:ring-primary border-gray-300 rounded">
              <label for="remember-me" class="ml-2 block text-sm text-gray-900"> Remember me </label>
            </div>
          </div>

          <div>
            <button type="submit" class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary">
              Sign in
            </button>
          </div>
        </form>

        <!-- Register Form -->
        <form v-else class="space-y-6" @submit.prevent="handleRegister">
          <div>
            <label for="reg-loginId" class="block text-sm font-medium text-gray-700"> Login ID </label>
            <div class="mt-1">
              <input v-model="registerForm.loginId" id="reg-loginId" name="loginId" type="text" required class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-primary focus:border-primary sm:text-sm">
            </div>
          </div>

          <div>
            <label for="nickname" class="block text-sm font-medium text-gray-700"> Nickname </label>
            <div class="mt-1">
              <input v-model="registerForm.nickname" id="nickname" name="nickname" type="text" required class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-primary focus:border-primary sm:text-sm">
            </div>
          </div>

          <div>
            <label for="email" class="block text-sm font-medium text-gray-700"> Email address </label>
            <div class="mt-1">
              <input v-model="registerForm.email" id="email" name="email" type="email" required class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-primary focus:border-primary sm:text-sm">
            </div>
          </div>
          
          <div>
            <label for="reg-password" class="block text-sm font-medium text-gray-700"> Password </label>
            <div class="mt-1">
              <input v-model="registerForm.password" id="reg-password" name="password" type="password" required class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-primary focus:border-primary sm:text-sm">
            </div>
          </div>

          <div>
            <label for="reg-password-confirm" class="block text-sm font-medium text-gray-700"> Confirm Password </label>
            <div class="mt-1">
              <input v-model="registerForm.passwordConfirm" id="reg-password-confirm" name="passwordConfirm" type="password" required class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-primary focus:border-primary sm:text-sm">
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700"> I am a... </label>
            <div class="mt-2 space-y-2">
                <div class="flex items-center">
                    <input v-model="registerForm.type" id="passenger" name="type" type="radio" value="passenger" class="focus:ring-primary h-4 w-4 text-primary border-gray-300">
                    <label for="passenger" class="ml-3 block text-sm font-medium text-gray-700"> Passenger </label>
                </div>
                <div class="flex items-center">
                    <input v-model="registerForm.type" id="driver" name="type" type="radio" value="driver" class="focus:ring-primary h-4 w-4 text-primary border-gray-300">
                    <label for="driver" class="ml-3 block text-sm font-medium text-gray-700"> Driver </label>
                </div>
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700"> Profile Image </label>
            <div class="mt-1 flex items-center">
                <span class="inline-block h-12 w-12 rounded-full overflow-hidden bg-gray-100">
                    <svg class="h-full w-full text-gray-300" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M24 20.993V24H0v-2.996A14.977 14.977 0 0112.004 15c4.904 0 9.26 2.354 11.996 5.993zM16.002 8.999a4 4 0 11-8 0 4 4 0 018 0z" />
                    </svg>
                </span>
                <input type="file" @change="onFileChange" accept="image/*" class="ml-5 bg-white py-2 px-3 border border-gray-300 rounded-md shadow-sm text-sm leading-4 font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary">
            </div>
          </div>

          <div>
            <button type="submit" class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary">
              Create Account
            </button>
          </div>
        </form>
      </div>
    </div>
    </div>
  </div>
</template>
