<script lang="ts">
export interface Result {
  alt_text: string;
  preview: string;
}
</script>

<script setup lang="ts">
import {ref} from "vue";
import FileInput from "@/components/FileInput.vue";
import ImgCard from "@/components/ImgCard.vue";
import ModelSelector from "@/components/ModelSelector.vue";
import ModelLoadingAlert from "@/components/ModelLoadingAlert.vue";

const results = ref<Result[]>([]);
const selectedModel = ref('blip');
const modelLoadingMessage = ref<string>('');
</script>

<template>
  <main class="flex flex-col items-center justify-center gap-10 max-w-5xl mx-auto p-6">
    <img
      src="./assets/logo.svg"
      alt="Alt Text Generator Logo"
      class="flex-0 mx-auto max-h-48 object-contain"
    />

    <h1 class="sr-only">Alt Text Generator</h1>

    <ModelSelector v-model="selectedModel" />

    <FileInput
      v-model="results"
      :disabled="results.length >= 3"
      :selected-model="selectedModel"
      @model-loading="modelLoadingMessage = $event"
    />

    <ModelLoadingAlert v-if="modelLoadingMessage" v-model="modelLoadingMessage" />

    <div v-if="results.length" class="flex flex-col md:flex-row gap-6 justify-center self-stretch flex-wrap">
      <ImgCard v-for="res in results" :key="res.preview" :value="res" />
    </div>
  </main>
</template>
