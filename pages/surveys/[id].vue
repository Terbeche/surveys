<template>
  <div class="max-w-3xl mx-auto space-y-8">
    <div v-if="loading" class="text-center py-8">
      <div class="text-gray-600">Loading survey...</div>
    </div>

    <div v-else-if="error" class="text-center py-8">
      <div class="text-red-600">{{ error }}</div>
    </div>

    <template v-else>
      <div class="bg-white shadow-md rounded-lg p-6">
        <h1 class="text-3xl font-bold text-gray-900 mb-4">{{ survey?.title }}</h1>
        <p class="text-gray-600 mb-8">{{ survey?.description }}</p>

        <form @submit.prevent="handleSubmit" class="space-y-6">
          <div v-for="question in survey?.questions" :key="question.id" class="bg-gray-50 p-6 rounded-lg">
            <h3 class="text-lg font-medium text-gray-900 mb-4">{{ question.text }}</h3>

            <!-- Multiple Choice Question -->
            <div v-if="question.type === 'multiple_choice'" class="space-y-4">
              <div v-for="option in question.options" :key="option" class="flex items-center">
                <input
                  type="radio"
                  :id="option"
                  :name="question.id"
                  :value="option"
                  v-model="answers[question.id]"
                  class="h-4 w-4 text-indigo-600 focus:ring-indigo-500"
                >
                <label :for="option" class="ml-3 text-gray-700">{{ option }}</label>
              </div>
            </div>

            <!-- Text Question -->
            <div v-else-if="question.type === 'text'">
              <textarea
                v-model="answers[question.id]"
                rows="3"
                class="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md"
              ></textarea>
            </div>

            <!-- Rating Question -->
            <div v-else-if="question.type === 'rating'" class="flex space-x-4">
              <template v-for="n in 5" :key="n">
                <button
                  type="button"
                  @click="answers[question.id] = n"
                  :class="[
                    'px-4 py-2 rounded-md',
                    answers[question.id] === n 
                      ? 'bg-indigo-600 text-white' 
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  ]"
                >
                  {{ n }}
                </button>
              </template>
            </div>
          </div>

          <div class="flex justify-center">
            <button
              type="submit"
              :disabled="submitting"
              class="px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50"
            >
              {{ submitting ? 'Submitting...' : 'Submit Survey' }}
            </button>
          </div>
        </form>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useSurveys } from '~/composables/useSurveys'
import type { Survey } from '~/types/survey'

definePageMeta({
  middleware: ['auth']
})

const route = useRoute()
const router = useRouter()
const { submitSurveyResponse } = useSurveys()

const survey = ref<Survey | null>(null)
const loading = ref(false)
const error = ref<string | null>(null)
const submitting = ref(false)
const answers = ref<Record<string, any>>({})

const fetchSurvey = async () => {
  loading.value = true
  try {
    const response = await fetch(`http://localhost:8000/surveys/${route.params.id}`)
    if (!response.ok) throw new Error('Failed to fetch survey')
    survey.value = await response.json()
  } catch (err) {
    error.value = 'Failed to load survey'
    console.error(err)
  } finally {
    loading.value = false
  }
}

const handleSubmit = async () => {
  if (!survey.value) return

  submitting.value = true
  try {
    await submitSurveyResponse({
      surveyId: survey.value.id,
      answers: Object.entries(answers.value).map(([questionId, value]) => ({
        questionId,
        value
      }))
    })
    router.push('/surveys/thank-you')
  } catch (err) {
    error.value = 'Failed to submit survey'
    console.error(err)
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  fetchSurvey()
})
</script> 