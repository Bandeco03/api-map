<script setup>
import {onMounted, ref} from 'vue'
import apiService from '../services/api.js'
import emitter from "@/eventBus.js";

const loading = ref(false)

async function fetchData() {
  emitter.emit('loading-start')
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

  emitter.emit('loading-stop')
}

onMounted(() => {
  fetchData()
})

</script>

<template>
  <div class="controls">
    <button @click="fetchData" class="update-btn">
      Carregar Dados da API
    </button>
  </div>

</template>

<style scoped>
.update-btn {
  color: hsla(160, 100%, 37%, 1);
  background-color: hsla(160, 100%, 37%, 0.2);
}

.controls {
  display: flex;
  justify-content: center;
  align-self: center;
}
</style>