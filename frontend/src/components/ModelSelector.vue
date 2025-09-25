<script lang="ts">
export interface Model {
  id: string;
  name: string;
  description: string;
}
</script>

<script setup lang="ts">
import {onMounted, ref} from "vue";
import axios from "axios";

const model = defineModel<string>({required: true})
const availableModels = ref<Model[]>([]);

onMounted(async () => {
  try {
    const response = await axios.get('http://localhost:8000/models');
    availableModels.value = response.data.models;
  } catch (error) {
    console.error('Failed to fetch models:', error);
    // Fallback models if API fails
    availableModels.value = [
      {id: 'blip', name: 'BLIP', description: 'Salesforce BLIP base model'}
    ];
  }
});
</script>

<template>
  <div class="flex flex-col">
    <label for="model-select" class="block text-sm font-medium text-gray-700 mb-2 text-nowrap">
      Select AI Model
    </label>
    <select
      id="model-select"
      v-model="model"
      class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
    >
      <option v-for="model in availableModels" :key="model.id" :value="model.id">
        {{ model.name }}
      </option>
    </select>
  </div>
</template>