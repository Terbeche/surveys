<template>
  <div class="space-y-8">
    <div class="text-center">
      <h1 class="text-4xl font-bold text-gray-900 mb-4">Welcome to SurveyPro</h1>
      <p class="text-xl text-gray-600">Create and manage surveys with ease</p>
    </div>

    <div v-if="loading" class="text-center">
      Loading surveys...
    </div>

    <div v-else-if="error" class="text-center text-red-600">
      {{ error }}
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="survey in surveys" :key="survey.id" 
           class="bg-white rounded-lg shadow-md p-6">
        <h3 class="text-lg font-semibold text-gray-900">{{ survey.title }}</h3>
        <p class="mt-2 text-gray-600">{{ survey.description }}</p>
        <div class="mt-4">
          <NuxtLink :to="`/surveys/${survey.id}`"
                    class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700">
            Take Survey
          </NuxtLink>
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

onMounted(() => {
  fetchSurveys()
})
</script>

<style>

</style>