<script setup>
import {ref, onMounted, computed} from 'vue'
import emitter from '@/eventBus.js'
import apiUtils from '@/services/api_utils.js'
import powerDataManagement from '@/services/utils.js'

const statesData = ref([])
const sortBy = ref('activePower') // 'name', 'activePower', 'percentage'
const sortOrder = ref('desc') // 'asc' or 'desc'

const sortedStates = computed(() => {
  const sorted = [...statesData.value]

  sorted.sort((a, b) => {
    let aVal, bVal

    switch (sortBy.value) {
      case 'name':
        aVal = a.name
        bVal = b.name
        break
      case 'activePower':
        aVal = a.activePower
        bVal = b.activePower
        break
      case 'percentage':
        aVal = a.activePowerRate
        bVal = b.activePowerRate
        break
      default:
        return 0
    }

    if (typeof aVal === 'string') {
      return sortOrder.value === 'asc'
          ? aVal.localeCompare(bVal)
          : bVal.localeCompare(aVal)
    } else {
      return sortOrder.value === 'asc'
          ? aVal - bVal
          : bVal - aVal
    }
  })

  return sorted
})

function setSortBy(column) {
  if (sortBy.value === column) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortBy.value = column
    sortOrder.value = 'desc'
  }
}

onMounted(() => {
  emitter.on('api-data', (response) => {
    statesData.value = apiUtils.dataProcessMap(response)
  })
})
</script>

<template>
  <div class="state-table-container">
    <h2>Potência por Estado</h2>
    <div class="table-wrapper">
      <table class="state-table">
        <thead>
        <tr>
          <th @click="setSortBy('name')" class="sortable">
            <span class="sort-indicator" v-if="sortBy === 'name'">
              {{ sortOrder === 'asc' ? '▲' : '▼' }}
            </span>
            Estado
          </th>
          <th @click="setSortBy('activePower')" class="sortable">
            <span class="sort-indicator" v-if="sortBy === 'activePower'">
              {{ sortOrder === 'asc' ? '▲' : '▼' }}
            </span>
            Potência Ativa
          </th>
          <th @click="setSortBy('percentage')" class="sortable">
            <span class="sort-indicator" v-if="sortBy === 'percentage'">
              {{ sortOrder === 'asc' ? '▲' : '▼' }}
            </span>
            % do Total
          </th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="state in sortedStates" :key="state.name">
          <td class="state-name">{{ state.name }}</td>
          <td class="power-value">{{ powerDataManagement.formatPower(state.activePower) }}</td>
          <td class="percentage-value">
            <div class="percentage-bar-container">
              <div class="percentage-bar" :style="{ width: state.activePowerRate + '%' }"></div>
              <span class="percentage-text">{{ state.activePowerRate.toFixed(2) }}%</span>
            </div>
          </td>
        </tr>
        </tbody>
      </table>
      <div v-if="statesData.length === 0" class="no-data">
        Nenhum dado disponível. Clique em "Carregar Dados da API" para carregar.
      </div>
    </div>
  </div>
</template>

<style scoped>
.state-table-container {
  background-color: var(--color-background-soft);
  border-radius: 1.5%;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 100%;
}

h2 {
  margin-top: 0;
  margin-bottom: 1rem;
  color: var(--color-heading);
  font-size: clamp(1.2rem, 3vw, 1.5rem);
}

.table-wrapper {
  overflow-x: auto;
  border-radius: 6px;
  border: 1px solid var(--color-border);
}

.state-table {
  width: 100%;
  border-collapse: collapse;
  background-color: var(--color-background);
  font-size: clamp(0.8rem, 2vw, 0.95rem);
}

thead {
  background-color: var(--color-background-mute);
  position: sticky;
  top: 0;
  z-index: 10;
}

th {
  padding: 0.75rem 1rem;
  text-align: left;
  font-weight: 600;
  border-bottom: 2px solid var(--color-border);
  white-space: nowrap;
}

th.sortable {
  cursor: pointer;
  user-select: none;
  transition: background-color 0.2s;
}

th.sortable:hover {
  background-color: var(--color-background-soft);
}

.sort-indicator {
  margin-left: 0.5rem;
  font-size: 0.8em;
  color: var(--color-text);
}

tbody tr {
  border-bottom: 1px solid var(--color-border);
  transition: background-color 0.2s;
}

tbody tr:hover {
  background-color: var(--color-background-soft);
}

tbody tr:last-child {
  border-bottom: none;
}

td {
  padding: 0.75rem 1rem;
}

.state-name {
  font-weight: 500;
  color: var(--color-text);
}

.power-value {
  font-weight: 600;
  color: var(--color-text-highlight);
  text-align: right;
}

.percentage-value {
  min-width: 200px;
}

.percentage-bar-container {
  position: relative;
  width: 100%;
  height: 24px;
  background-color: var(--color-background);
  border-radius: 4px;
  overflow: hidden;
}

.percentage-bar {
  position: absolute;
  left: 0;
  top: 0;
  height: 100%;
  background: linear-gradient(90deg, #42b983 0%, #35a372 100%);
  transition: width 0.3s ease;
  border-radius: 4px;
}

.percentage-text {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  font-weight: 600;
  color: var(--color-text);
  z-index: 1;
  text-shadow: 0 0 3px rgba(255, 255, 255, 0.5);
  font-size: 0.85em;
}

.no-data {
  padding: 2rem;
  text-align: center;
  color: var(--color-text);
  opacity: 0.6;
  font-style: italic;
}

/* Responsividade para telas pequenas */
@media (max-width: 768px) {
  .state-table-container {
    padding: 1rem;
  }

  th, td {
    padding: 0.5rem 0.75rem;
  }

  .percentage-value {
    min-width: 150px;
  }

  .percentage-bar-container {
    height: 20px;
  }
}

.table-wrapper {
  max-height: 600px;
  overflow-y: auto;
}

.table-wrapper::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

.table-wrapper::-webkit-scrollbar-track {
  background: var(--color-background-mute);
  border-radius: 4px;
}

.table-wrapper::-webkit-scrollbar-thumb {
  background: var(--color-border);
  border-radius: 4px;
}

.table-wrapper::-webkit-scrollbar-thumb:hover {
  background: var(--color-border-hover);
}
</style>