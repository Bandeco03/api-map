<script setup>
import {onMounted, ref} from 'vue'
import apiService from '../services/api.js'
import emitter from "@/eventBus.js";

async function fetchData() {
  emitter.emit('loading-start')
  let data = null
  let historical = null

  try {
    data = await apiService.getPowerData()
    historical = await apiService.getPowerDataHistory()
    console.log('Dados buscados com sucesso')
  } catch (error) {
    console.error('Erro ao buscar dados:', error)
  } finally {
    if (data) {
      emitter.emit('api-data', data)
    }
    if (historical) {
      emitter.emit('api-history', historical)
    }
    emitter.emit('loading-stop')
  }
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
  color: hsl(28, 100%, 50%);
  background-color: hsla(28, 100%, 50%, 0.2);
}

.controls {
  display: flex;
  justify-content: center;
  align-self: center;
  flex-wrap: wrap;
  gap: 10px;
  width: 100%;
  margin-bottom: 15px;
}

@media (min-width: 768px) {
  .controls {
    margin-bottom: 20px;
  }
}
</style>