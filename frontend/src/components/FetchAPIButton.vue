<script setup>
import {onBeforeMount, onMounted, ref} from 'vue'
import apiService from '../services/api.js'
import emitter from "@/eventBus.js";

const loading = ref(false)

async function fetchData() {
  loading.value = true
  let data = null

  try {
    data = await apiService.getPowerData()
    console.log('Dados buscados com sucesso:', data)
  } catch (error) {
    console.error('Erro ao buscar dados:', error)
  } finally {
    if (data) {
      emitter.emit('api-data', data)
    }
    loading.value = false
  }
}

onBeforeMount(() => {
  fetchData()
})

onMounted(() => {
  emitter.on('update-data', fetchData)
})
</script>

<template>
  <div class="controls">
    <button @click="fetchData" class="update-btn">
      Carregar Dados da API
    </button>
  </div>

  <!-- Spinner de carregamento -->
  <div v-if="loading" class="spinner-overlay">
    <div class="spinner"></div>
    <p class="loading-text">Carregando dados...</p>
  </div>
</template>

<style scoped>
.update-btn {
  color: hsla(160, 100%, 37%, 1);
  background-color: hsla(160, 100%, 37%, 0.2);
}

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
  width: 50px;
  height: 50px;
  border: 5px solid #f3f3f3;
  border-top: 5px solid #0288d1;
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
    transform: rotate(360deg);
  }
}
</style>