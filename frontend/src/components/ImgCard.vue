<script lang="ts">
import type {Result} from "../App.vue";

interface Props {
  value: Result;
}
</script>

<script setup lang="ts">
defineProps<Props>();

function copyToClipboard(text: string) {
  navigator.clipboard.writeText(text);
  alert("Copied to clipboard!");
}
</script>

<template>
  <div class="max-w-full w-full md:w-76 md:max-w-76 outline outline-primary hover:outline-2 rounded-lg shadow-sm hover:shadow-lg transition flex flex-col overflow-hidden ">
    <!-- Image preview container -->
    <div class="w-full h-48 bg-gray-100 flex items-center justify-center overflow-hidden">
      <img
        v-if="value.preview"
        :src="value.preview"
        alt=""
        class="object-contain max-h-full max-w-full"
      />
    </div>

    <!-- Alt text + buttons -->
    <div class="p-4 flex flex-col flex-1 justify-between">
      <div class="flex-1">
        <p class="font-semibold text-primary mb-1">Suggested Alt Text:</p>
        <p class="break-words min-h-[3rem]">
          {{ value.alt_text }}
        </p>
      </div>
      <div class="mt-3 flex justify-between items-center">
        <button
          @click="copyToClipboard(value.alt_text)"
          class="px-3 py-1 bg-blue-500 text-white rounded hover:bg-blue-600 transition"
        >
          Copy
        </button>
      </div>
    </div>
  </div>
</template>