<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-white shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <NuxtLink to="/" class="text-2xl font-bold text-indigo-600">SurveyPro</NuxtLink>
          </div>
          <div class="flex space-x-8">
            <NuxtLink to="/" class="inline-flex items-center px-1 pt-1 text-gray-700 hover:text-indigo-600">Home</NuxtLink>
            <NuxtLink to="/surveys" class="inline-flex items-center px-1 pt-1 text-gray-700 hover:text-indigo-600">Surveys</NuxtLink>
            <NuxtLink to="/about" class="inline-flex items-center px-1 pt-1 text-gray-700 hover:text-indigo-600">About</NuxtLink>
            <NuxtLink to="/contact" class="inline-flex items-center px-1 pt-1 text-gray-700 hover:text-indigo-600">Contact</NuxtLink>
            
            <!-- Auth Navigation -->
            <template v-if="isAuthenticated">
              <button @click="handleLogout" 
                      class="inline-flex items-center px-1 pt-1 text-gray-700 hover:text-indigo-600">
                Logout
              </button>
            </template>
            <template v-else>
              <NuxtLink to="/login" class="inline-flex items-center px-1 pt-1 text-gray-700 hover:text-indigo-600">Login</NuxtLink>
              <NuxtLink to="/register" class="inline-flex items-center px-3 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700">
                Register
              </NuxtLink>
            </template>
          </div>
        </div>
      </div>
    </nav>
    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <NuxtPage />
    </main>
  </div>
</template>

<script setup lang="ts">
import { useAuth } from '~/composables/useAuth'
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const { token, logout } = useAuth()

const isAuthenticated = computed(() => !!token.value)

const handleLogout = () => {
  logout()
  router.push('/login')
}
</script>
