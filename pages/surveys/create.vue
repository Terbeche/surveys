<template>
  <div class="space-y-8">
    <div class="text-center">
      <h1 class="text-4xl font-bold text-gray-900 mb-4">Create New Survey</h1>
      <p class="text-xl text-gray-600">Design your survey questions</p>
    </div>

    <form @submit.prevent="handleSubmit" class="max-w-3xl mx-auto space-y-6">
      <div class="bg-white p-6 rounded-lg shadow-md">
        <div class="space-y-4">
          <div>
            <label for="title" class="block text-sm font-medium text-gray-700">Survey Title</label>
            <input type="text" id="title" v-model="surveyForm.title" 
                   class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
          </div>

          <div>
            <label for="description" class="block text-sm font-medium text-gray-700">Description</label>
            <textarea id="description" v-model="surveyForm.description" rows="3"
                      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"></textarea>
          </div>
        </div>
      </div>

      <div class="space-y-4">
        <div v-for="(question, index) in surveyForm.questions" :key="index" 
             class="bg-white p-6 rounded-lg shadow-md">
          <div class="flex justify-between items-start mb-4">
            <h3 class="text-lg font-medium">Question {{ index + 1 }}</h3>
            <button type="button" @click="removeQuestion(index)"
                    class="text-red-600 hover:text-red-800">
              Remove
            </button>
          </div>

          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">Question Text</label>
              <input type="text" v-model="question.text"
                     class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700">Question Type</label>
              <select v-model="question.type"
                      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
                <option value="multiple_choice">Multiple Choice</option>
                <option value="text">Text</option>
                <option value="rating">Rating</option>
              </select>
            </div>

            <div v-if="question.type === 'multiple_choice'">
              <label class="block text-sm font-medium text-gray-700">Options</label>
              <div v-for="(option, optionIndex) in question.options" :key="optionIndex" class="flex mt-2">
                <input type="text" v-model="question.options[optionIndex]"
                       class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
                <button type="button" @click="removeOption(question, optionIndex)"
                        class="ml-2 text-red-600 hover:text-red-800">
                  Remove
                </button>
              </div>
              <button type="button" @click="addOption(question)"
                      class="mt-2 text-indigo-600 hover:text-indigo-800">
                Add Option
              </button>
            </div>

            <div class="flex items-center">
              <input type="checkbox" v-model="question.required" id="required"
                     class="rounded border-gray-300 text-indigo-600 focus:ring-indigo-500">
              <label for="required" class="ml-2 block text-sm text-gray-900">Required</label>
            </div>
          </div>
        </div>
      </div>

      <div class="flex justify-center">
        <button type="button" @click="addQuestion"
                class="mr-4 px-4 py-2 border border-transparent text-sm font-medium rounded-md text-indigo-700 bg-indigo-100 hover:bg-indigo-200">
          Add Question
        </button>
        <button type="submit"
                class="px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700">
          Create Survey
        </button>
      </div>
    </form>
  </div>
</template>

<script lang="ts" setup>
import type { Survey, Question } from '~/types/survey'

const router = useRouter()
const { createSurvey } = useSurveys()

const surveyForm = reactive<Omit<Survey, 'id' | 'createdAt' | 'updatedAt'>>({
  title: '',
  description: '',
  questions: []
})

const addQuestion = () => {
  surveyForm.questions.push({
    id: crypto.randomUUID(),
    text: '',
    type: 'multiple_choice',
    options: [''],
    required: false
  })
}

const removeQuestion = (index: number) => {
  surveyForm.questions.splice(index, 1)
}

const addOption = (question: Question) => {
  if (!question.options) question.options = []
  question.options.push('')
}

const removeOption = (question: Question, index: number) => {
  if (question.options) {
    question.options.splice(index, 1)
  }
}

const handleSubmit = async () => {
  try {
    const newSurvey = await createSurvey(surveyForm)
    router.push('/surveys')
  } catch (error) {
    console.error('Failed to create survey:', error)
  }
}
</script> 