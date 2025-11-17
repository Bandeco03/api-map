<script setup>
import {onMounted, ref} from 'vue'
import VChart from 'vue-echarts'
import * as echarts from 'echarts/core'
import {MapChart} from 'echarts/charts'
import {TooltipComponent, VisualMapComponent} from 'echarts/components'
import {CanvasRenderer} from 'echarts/renderers'
import brazilGeoJson from '../brazil-states.json'
import apiUtils from '../services/api_utils.js'
import emitter from "@/eventBus.js";

const selectedStates = ref([])
const totalActivePower = ref(0)
const totalInstalledPower = ref(0)
const activePowerRate = ref(0)

// Register required ECharts modules
echarts.use([MapChart, TooltipComponent, VisualMapComponent, CanvasRenderer])

echarts.registerMap('BRA', brazilGeoJson)

const stateData = ref([])

async function fetchData(response) {
  totalActivePower.value = 0
  totalInstalledPower.value = 0
  activePowerRate.value = 0

  try {
    // Process the data using apiUtils
    const processedData = apiUtils.dataProcessMap(response)

    if (processedData && processedData.length > 0) {
      stateData.value = processedData

      // Calculate totals
      totalActivePower.value = stateData.value.reduce((sum, state) => sum + state.activePower, 0) / 1000000000 // Convert to GW
      totalInstalledPower.value = stateData.value.reduce((sum, state) => sum + state.totalPower, 0) / 1000000000 // Convert to GW
      activePowerRate.value = stateData.value.reduce((sum, state) => sum + state.activePowerRate, 0)

      // Atualizar opções do mapa
      option.value.series[0].data = stateData.value

      // Atualizar visualMap baseado nos valores reais
      const powers = stateData.value.map(s => s.value)
      option.value.visualMap.min = Math.min(...powers)
      option.value.visualMap.max = Math.max(...powers)

      console.log('Dados carregados com sucesso:', stateData.value.length, 'estados')
    } else {
      console.error('Dados da API inválidos', response)
    }
  } catch (error) {
    console.error('Erro ao buscar dados:', error)
  }
}


const option = ref({
  tooltip: {
    trigger: 'item',
    formatter: params => {
      const d = stateData.value.find(s => s.name === params.name)
      if (d) {
        return `
          <b>${params.name}</b><br/>
          Potência ativa: <b>${(d.activePower / 1000000).toFixed(2)}</b> MW<br/>
          Potência instalada: <b>${(d.totalPower / 1000000).toFixed(2)}</b> MW <br/>
          Representação total: <b>${(d.activePowerRate).toFixed(2)}</b>%
        `
      }
      return `<b>${params.name}</b><br/>Sem dados`
    }
  },
  visualMap: {
    type: 'continuous',
    min: 0,
    max: 2500,
    left: 'left',
    top: 'bottom',
    text: ['Alto', 'Baixo'],
    title: ['Potência (MW)'],
    inRange: {color: ['#e0f7fa', '#0288d1']},
    calculable: true,
    show: true
  },
  series: [
    {
      type: 'map',
      map: 'BRA',
      roam: 'scale',
      scaleLimit: {min: 0.8, max: 10},
      layoutCenter: ['50%', '50%'],
      layoutSize: '100%',
      aspectScale: 0.95,
      data: stateData.value,
      label: {
        show: true,
        fontSize: 10,
        fontWeight: 'bold',
        color: '#000000',
        formatter: (params) => {
          const geoData = brazilGeoJson.features.find(f => f.properties.name === params.name)
          const stateInfo = stateData.value.find(s => s.name === params.name)

          if (geoData) {
            const sigla = geoData.properties.sigla
            if (stateInfo) {
              const powerMW = (stateInfo.activePower / 1000000).toFixed(0)
              const rate = (stateInfo.activePowerRate).toFixed(1)
              return `${sigla}\n${powerMW} MW\n${rate} %`
            }
            return sigla
          }
          return params.name
        }
      },
      emphasis: {
        label: {
          show: true,
          fontSize: 16,
          fontWeight: 'bold',
          color: '#000000',
          textBorderColor: '#ffffff',
          textShadowColor: 'rgba(0, 0, 0, 0.3)',
          textShadowBlur: 2,
          textShadowOffsetX: 3,
          textShadowOffsetY: 3,
          textBorderWidth: 3
        },
        itemStyle: {
          borderWidth: 2
        }
      }
    }
  ]
})

// Função para lidar com cliques no mapa
const handleMapClick = (params) => {
  if (params.componentType === 'series' && params.seriesType === 'map') {
    const stateName = params.name
    const stateInfo = stateData.value.find(s => s.name === stateName)
  }
}


// Função para remover estado da lista
const removeState = (stateName) => {
  const index = selectedStates.value.findIndex(s => s.name === stateName)
  if (index !== -1) {
    selectedStates.value.splice(index, 1)
    updateMapSelection()
  }
}

// Função para limpar todos os estados selecionados
const clearSelection = () => {
  selectedStates.value = []
  // Forçar atualização imediata do mapa
  option.value.series[0].data = stateData.value.map(state => ({
    ...state,
    itemStyle: undefined
  }))
}

// Função para atualizar a visualização dos estados selecionados no mapa
const updateMapSelection = () => {
  option.value.series[0].data = stateData.value.map(state => {
    const isSelected = selectedStates.value.some(s => s.name === state.name)
    return {
      ...state,
      itemStyle: isSelected ? {
        areaColor: '#ff6b6b',
        borderColor: '#c92a2a',
        borderWidth: 2
      } : undefined
    }
  })
}

onMounted(() => {
  emitter.on('api-data', (data) => {
    fetchData(data)
  })
})
</script>

<template>
  <div class="main-container">
    <header>
      {{ totalActivePower.toFixed(2) }} GW de potência total ativa |
      {{ totalInstalledPower.toFixed(2) }} GW de potência total instalada
    </header>


    <div class="content-wrapper">
      <!-- Mapa -->
      <div class="map-container">
        <v-chart
            :option="option"
            autoresize
            style="height: 600px; width: 100%;"
            @click="handleMapClick"
        />
      </div>

      <!-- Painel de comparação -->
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
    </div>
  </div>
</template>

<style scoped>
h3 {
  color: #0288d1;
}

.main-container {
  display: flex;
  flex-direction: column;
  height: 100%;
}

button {

  border: none;
  border-radius: 15px;
  font-size: 16px;
  margin: 0 10px;
  padding: 10px 20px;
  cursor: pointer;
}

.content-wrapper {
  display: flex;
  flex: 1;
  justify-content: center;
  align-items: flex-start;
  padding: 20px;
  overflow: hidden;
}

.map-container {
  flex: 2;
  position: relative;
}

.comparison-panel {
  flex: 1;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  margin-left: 20px;
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
  background-color: #ff6b6b;
  color: white;
  border: none;
  border-radius: 15px;
  padding: 5px 10px;
  cursor: pointer;
}

.empty-state {
  text-align: center;
  color: #888;
}

.states-list {
  margin-top: 10px;
}

.state-card {
  background-color: white;
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

.remove-btn {
  background: none;
  border: none;
  color: #ff6b6b;
  font-size: 18px;
  cursor: pointer;
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
  color: #333;
}

.value {
  font-weight: 600;
  color: #0288d1;
}
</style>
