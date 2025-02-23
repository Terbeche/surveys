import { ref } from 'vue'
import { useCookie } from '#app'

interface LoginCredentials {
  email: string
  password: string
}

interface RegisterCredentials extends LoginCredentials {
  // Add any additional registration fields here
}

export const useAuth = () => {
  // Use useCookie for token persistence
  const token = useCookie('auth_token', {
    maxAge: 60 * 60 * 24 * 7, // 7 days
    secure: true
  })
  const error = ref<string | null>(null)

  const login = async (credentials: LoginCredentials) => {
    try {
      const formData = new FormData()
      formData.append('username', credentials.email)  // FastAPI OAuth expects 'username'
      formData.append('password', credentials.password)

      const response = await fetch('http://localhost:8000/token', {
        method: 'POST',
        body: formData
      })

      if (!response.ok) {
        throw new Error('Login failed')
      }

      const data = await response.json()
      token.value = data.access_token
      return data
    } catch (err) {
      error.value = 'Failed to login'
      throw err
    }
  }

  const register = async (credentials: RegisterCredentials) => {
    try {
      const response = await fetch('http://localhost:8000/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(credentials)
      })

      if (!response.ok) {
        throw new Error('Registration failed')
      }

      return await response.json()
    } catch (err) {
      error.value = 'Failed to register'
      throw err
    }
  }

  const logout = () => {
    token.value = null
  }

  return {
    token,
    error,
    login,
    register,
    logout
  }
} 