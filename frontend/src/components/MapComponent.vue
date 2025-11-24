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

const activePowerRate = ref(0)

// Register required ECharts modules
echarts.use([MapChart, TooltipComponent, VisualMapComponent, CanvasRenderer])

echarts.registerMap('BRA', brazilGeoJson)

const stateData = ref([])

async function fetchData(response) {
  activePowerRate.value = 0

  try {
    // Process the data using apiUtils
    const processedData = apiUtils.dataProcessMap(response)

    if (processedData && processedData.length > 0) {
      stateData.value = processedData

      // Calculate totals
      activePowerRate.value = stateData.value.reduce((sum, state) => sum + state.activePowerRate, 0)

      // Atualizar opções do mapa
      option.value.series[0].data = stateData.value

      // Atualizar visualMap baseado nos valores reais
      const powers = stateData.value.map(s => s.value)
      option.value.visualMap.min = Math.min(...powers)
      option.value.visualMap.max = Math.max(...powers)

      // console.log('Dados carregados com sucesso:', stateData.value.length, 'estados')
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
    inRange: {color: ['#ECECEC', '#FF7900']},
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
              return `${sigla}\n${rate} %`
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
          textBorderWidth: 3,
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
    if (stateInfo) {
      emitter.emit('state-clicked', stateInfo)
    }
  }
}

// Função para atualizar a visualização dos estados selecionados no mapa
const updateMapSelection = (selectedStates) => {
  option.value.series[0].data = stateData.value.map(state => {
    const isSelected = selectedStates.some(s => s.name === state.name)
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

  // Ouvir mudanças na seleção de estados
  emitter.on('state-selection-changed', (selectedStates) => {
    updateMapSelection(selectedStates)
  })
})
</script>

<template>
  <div class="main-container">
    <div class="content-wrapper">
      <!-- Mapa -->
      <div class="map-container">
        <v-chart
            :option="option"
            autoresize
            class="map-chart"
            @click="handleMapClick"
        />
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
  width: 100%;
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
  padding: 10px;
  overflow: hidden;
}

.map-container {
  flex: 1;
  position: relative;
  width: 100%;
}

.map-chart {
  height: 400px;
  width: 100%;
}

/* Tablet */
@media (min-width: 768px) {
  .content-wrapper {
    padding: 15px;
  }

  .map-chart {
    height: 500px;
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .content-wrapper {
    padding: 20px;
  }

  .map-chart {
    height: 600px;
  }
}
</style>
