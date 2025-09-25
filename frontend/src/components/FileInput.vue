<script lang="ts">
import type {Result} from "../App.vue";

interface Props {
  disabled?: boolean;
  selectedModel?: string;
}
</script>

<script setup lang="ts">
import {useTemplateRef} from "vue";
import axios from "axios";

const props = defineProps<Props>()

const fileInput = useTemplateRef('fileInput');

const model = defineModel<Result[]>({required: true});
const emit = defineEmits<{
  'model-loading': [message: string]
}>();

async function uploadImages(event: Event) {
  const files = (event.target as HTMLInputElement).files || [];
  if (!files) return;

  const startIndex = model.value.length;

  for (let i = 0; i < files.length; i++) {
    const formData = new FormData();
    formData.append("file", files[i]!);
    formData.append("model", props.selectedModel || "blip");

    // Create preview
    const preview = URL.createObjectURL(files[i]!);

    model.value.push({ alt_text: "Processing...", preview });

    try {
      // Show loading message for first-time model loads
      if (i === 0 && props.selectedModel !== 'blip') {
        emit('model-loading', `Loading ${props.selectedModel?.toUpperCase()} model (first-time download may take 2-5 minutes)...`);
      }

      const res = await axios.post("http://localhost:8000/describe", formData, {
        timeout: 300000 // 5 minute timeout for model download
      });
      model.value[startIndex + i]!.alt_text = res.data.alt_text;

      // Clear loading message after first successful response
      if (i === 0) {
        emit('model-loading', '');
      }
    } catch (error: any) {
      if (error.code === 'ECONNABORTED') {
        model.value[startIndex + i]!.alt_text = "Timeout - Model may be downloading, please try again";
      } else {
        model.value[startIndex + i]!.alt_text = "Error generating description";
      }
      emit('model-loading', '');
    }
  }
}

function handleDrop(event: DragEvent) {
  const files = event.dataTransfer?.files;
  if (!files) return;
  fileInput.value!.files = files;
  uploadImages(event as unknown as Event);
}
</script>

<template>
  <div
    :data-disabled="disabled"
    class="border-2 border-dashed border-gray-400 rounded-lg p-5 text-center cursor-pointer hover:border-blue-500 transition relative data-[disabled=true]:opacity-50 data-[disabled=true]:pointer-events-none data-[disabled=true]:cursor-not-allowed"
    @drop.prevent="handleDrop"
    @dragover.prevent
    @click="fileInput?.click()"
  >
    <p class="text-gray-500 text-lg">
      Drag & drop images here or click to select files
    </p>
    <input
      ref="fileInput"
      type="file"
      class="hidden"
      multiple
      :disabled="disabled"
      @change="uploadImages"
    />
  </div>
</template>