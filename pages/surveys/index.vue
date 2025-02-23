<template>
  <div class="space-y-8">
    <div class="flex justify-between items-center">
      <h1 class="text-3xl font-bold text-gray-900">My Surveys</h1>
      <NuxtLink 
        to="/surveys/create"
        class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
      >
        Create New Survey
      </NuxtLink>
    </div>

    <div v-if="loading" class="text-center py-8">
      <div class="text-gray-600">Loading surveys...</div>
    </div>

    <div v-else-if="error" class="text-center py-8">
      <div class="text-red-600">{{ error }}</div>
    </div>

    <div v-else-if="surveys.length === 0" class="text-center py-8">
      <div class="text-gray-600">No surveys found. Create your first survey!</div>
    </div>

    <div v-else class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
      <div v-for="survey in surveys" :key="survey.id" 
           class="bg-white rounded-lg shadow-md overflow-hidden">
        <div class="p-6">
          <h3 class="text-lg font-semibold text-gray-900">{{ survey.title }}</h3>
          <p class="mt-2 text-gray-600">{{ survey.description }}</p>
          <div class="mt-4 flex space-x-4">
            <NuxtLink 
              :to="`/surveys/${survey.id}`"
              class="inline-flex items-center px-3 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
            >
              View Survey
            </NuxtLink>
            <button
              @click="deleteSurvey(survey.id)"
              class="inline-flex items-center px-3 py-2 border border-gray-300 text-sm font-medium rounded-md text-red-600 bg-white hover:bg-red-50"
            >
              Delete
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useSurveys } from '~/composables/useSurveys'

definePageMeta({
  middleware: ['auth']
})

const { surveys, loading, error, fetchSurveys } = useSurveys()

const deleteSurvey = async (id: string) => {
  // TODO: Implement delete functionality
  console.log('Delete survey:', id)
}

onMounted(() => {
  fetchSurveys()
})
</script> 