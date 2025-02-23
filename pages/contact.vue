<template>
  <div class="space-y-8">
    <div class="text-center">
      <h1 class="text-4xl font-bold text-gray-900 mb-4">Contact Us</h1>
      <p class="text-xl text-gray-600">Get in touch with our team</p>
    </div>

    <div class="max-w-2xl mx-auto bg-white p-8 rounded-lg shadow-md">
      <form @submit.prevent="handleSubmit" class="space-y-6">
        <div>
          <label for="name" class="block text-sm font-medium text-gray-700">Name</label>
          <input type="text" id="name" v-model="form.name" 
                 class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
        </div>

        <div>
          <label for="email" class="block text-sm font-medium text-gray-700">Email</label>
          <input type="email" id="email" v-model="form.email" 
                 class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
        </div>

        <div>
          <label for="message" class="block text-sm font-medium text-gray-700">Message</label>
          <textarea id="message" v-model="form.message" rows="4" 
                    class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"></textarea>
        </div>

        <button type="submit" 
                class="w-full bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700">
          Send Message
        </button>
      </form>
    </div>
  </div>
</template>

<script lang="ts" setup>
const form = reactive({
  name: '',
  email: '',
  message: ''
})

const handleSubmit = () => {
  console.log('Form submitted:', form)
}
</script>

<style>

</style>