import { ref } from 'vue'
import { useAuth } from './useAuth'
import type { Survey, SurveyResponse } from '~/types/survey'

export const useSurveys = () => {
  const surveys = ref<Survey[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  const { token } = useAuth()

  const fetchSurveys = async () => {
    loading.value = true
    error.value = null
    
    try {
      const response = await fetch('http://localhost:8000/surveys/', {
        headers: {
          'Authorization': `Bearer ${token.value}`
        }
      })

      if (!response.ok) {
        throw new Error('Failed to fetch surveys')
      }

      surveys.value = await response.json()
    } catch (err) {
      error.value = 'Failed to fetch surveys'
      console.error('Error fetching surveys:', err)
    } finally {
      loading.value = false
    }
  }

  const createSurvey = async (survey: Omit<Survey, 'id' | 'createdAt' | 'updatedAt'>) => {
    loading.value = true
    error.value = null

    try {
      const response = await fetch('http://localhost:8000/surveys/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token.value}`
        },
        body: JSON.stringify(survey)
      })

      if (!response.ok) {
        throw new Error('Failed to create survey')
      }

      const newSurvey = await response.json()
      surveys.value.push(newSurvey)
      return newSurvey
    } catch (err) {
      error.value = 'Failed to create survey'
      throw err
    } finally {
      loading.value = false
    }
  }

  const submitSurveyResponse = async (response: Omit<SurveyResponse, 'id' | 'submittedAt'>) => {
    loading.value = true
    error.value = null

    try {
      const apiResponse = await fetch(`http://localhost:8000/surveys/${response.surveyId}/respond`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token.value}`
        },
        body: JSON.stringify(response)
      })

      if (!apiResponse.ok) {
        throw new Error('Failed to submit survey response')
      }

      return await apiResponse.json()
    } catch (err) {
      error.value = 'Failed to submit survey response'
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    surveys,
    loading,
    error,
    fetchSurveys,
    createSurvey,
    submitSurveyResponse
  }
} 