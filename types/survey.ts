export interface Survey {
  id: string
  title: string
  description: string
  questions: Question[]
  createdAt: Date
  updatedAt: Date
}

export interface Question {
  id: string
  text: string
  type: 'multiple_choice' | 'text' | 'rating'
  options?: string[]
  required: boolean
}

export interface SurveyResponse {
  id: string
  surveyId: string
  answers: Answer[]
  submittedAt: Date
}

export interface Answer {
  questionId: string
  value: string | number
} 