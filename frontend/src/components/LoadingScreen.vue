<script setup>

import {onMounted, ref} from "vue";
import emitter from "@/eventBus.js";

const loading = ref(false)

onMounted(() => {
  emitter.on('loading-start', () => {
    loading.value = true
  })
  emitter.on('loading-stop', () => {
    loading.value = false
  })
})
</script>

<template>
  <div v-if="loading" class="spinner-overlay">
    <div class="spinner"></div>
    <p class="loading-text">Carregando dados...</p>
  </div>
</template>

<style scoped>
.spinner-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.8);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.spinner {
  width: 6vmin;
  height: 6vmin;
  border: 0.8vmin solid #f3f3f3;
  border-top: 0.8vmin solid #0288d1;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.loading-text {
  margin-top: 20px;
  font-size: 18px;
  color: #0288d1;
  font-weight: 600;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(361deg);
  }
}
</style>