<script setup>
import { ref, onMounted } from 'vue'
import emitter from "@/eventBus.js"

const selectedStates = ref([])

// Adicionar estado à lista
const addState = (stateInfo) => {
  const exists = selectedStates.value.some(s => s.name === stateInfo.name)
  if (!exists) {
    selectedStates.value.push(stateInfo)
    emitter.emit('state-selection-changed', selectedStates.value)
  }
}

// Remover estado da lista
const removeState = (stateName) => {
  const index = selectedStates.value.findIndex(s => s.name === stateName)
  if (index !== -1) {
    selectedStates.value.splice(index, 1)
    emitter.emit('state-selection-changed', selectedStates.value)
  }
}

// Limpar todos os estados selecionados
const clearSelection = () => {
  selectedStates.value = []
  emitter.emit('state-selection-changed', selectedStates.value)
}

onMounted(() => {
  emitter.on('state-clicked', (stateInfo) => {
    addState(stateInfo)
  })
})
</script>

<template>
  <div class="comparison-panel">
    <div class="panel-header">
      <h3>Estados Selecionados</h3>
      <button v-if="selectedStates.length > 0" @click="clearSelection" class="clear-btn">
        Limpar Tudo
      </button>
    </div>

    <div v-if="selectedStates.length === 0" class="empty-state">
      <p>Clique nos estados no mapa para compará-los</p>
    </div>

    <div v-else class="states-list">
      <div
          v-for="state in selectedStates"
          :key="state.name"
          class="state-card"
      >
        <div class="state-header">
          <h4>{{ state.name }}</h4>
          <button @click="removeState(state.name)" class="remove-btn">×</button>
        </div>
        <div class="state-data">
          <div class="data-row">
            <span class="label">Potência Ativa:</span>
            <span class="value">{{ (state.activePower / 1000000).toFixed(2) }} MW</span>
          </div>
          <div class="data-row">
            <span class="label">Potência Instalada:</span>
            <span class="value">{{ (state.totalPower / 1000000).toFixed(2) }} MW</span>
          </div>
          <div class="data-row">
            <span class="label">Utilização:</span>
            <span class="value">{{ ((state.activePower / state.totalPower) * 100).toFixed(1) }}%</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
h3 {
  color: var(--color-heading);
}

.comparison-panel {
  flex: 1;
  width: 100%;
  background-color: var(--color-background-mute);
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
  max-height: 600px;
  overflow-y: auto;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.clear-btn {
  background-color: rgba(255, 82, 82, 0.2);
  color: rgb(255, 82, 82);
  border: none;
  border-radius: 15px;
  padding: 5px 10px;
  cursor: pointer;
}

.empty-state {
  text-align: center;
  color: var(--color-text);
  padding: 20px;
}

.states-list {
  margin-top: 10px;
}

.state-card {
  background-color: var(--color-background-soft);
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 10px;
  padding: 10px;
}

.state-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.state-header h4 {
  margin: 0;
  color: var(--color-text);
}

.remove-btn {
  background: none;
  border: none;
  color: #ff6b6b;
  font-size: 24px;
  cursor: pointer;
  padding: 0;
  margin: 0;
  line-height: 1;
}

.remove-btn:hover {
  color: #ff5252;
}

.state-data {
  margin-top: 10px;
}

.data-row {
  display: flex;
  justify-content: space-between;
  margin: 5px 0;
}

.label {
  font-weight: 500;
  color: var(--color-text);
}

.value {
  font-weight: 600;
  color: var(--color-text-highlight);
}
</style>