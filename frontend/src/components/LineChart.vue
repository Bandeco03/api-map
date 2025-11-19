<script setup>
import {ref, onMounted, onBeforeUnmount} from 'vue'
import * as echarts from 'echarts'
import apiService from '../services/api'
import apiUtils from '../services/api_utils'

const chartRef = ref(null)
const loading = ref(true)
const error = ref(null)
const chartInstance = ref(null)

const props = defineProps({
  limit: {
    type: Number,
    default: 100
  },
  height: {
    type: String,
    default: '400px'
  },
  yAxisMin: {
    type: Number,
    default: null
  },
  yAxisMax: {
    type: Number,
    default: null
  },
  yAxisInterval: {
    type: Number,
    default: null
  }
})

/**
 * Create ECharts option for line chart
 * @param {Array} timestamps - Array of timestamp labels
 * @param {Array} activePower - Array of active power values
 * @returns {Object} ECharts option configuration
 */
const createLineChartOption = (timestamps, activePower) => {
  const option = {
    title: {
      text: 'Histórico de Potência Ativa',
      left: 'center',
      textStyle: {
        color: getComputedStyle(document.documentElement).getPropertyValue('--color-text').trim()
      }
    },
    tooltip: {
      trigger: 'axis',
      formatter: (params) => {
        if (params && params.length > 0) {
          const param = params[0]
          return `${param.axisValue}<br/>Potência Ativa: ${param.value} MW`
        }
        return ''
      }
    },
    xAxis: {
      type: 'category',
      data: timestamps,
      axisLabel: {
        rotate: 45,
        interval: Math.floor(timestamps.length / 10) || 0
      }
    },
    yAxis: {
      type: 'value',
      name: 'Potência (MW)',
      axisLabel: {
        formatter: '{value} MW'
      }
    },
    series: [
      {
        name: 'Potência Ativa',
        type: 'line',
        data: activePower,
        smooth: true,
        itemStyle: {
          color: '#ff7700'
        },
        areaStyle: {
          color: 'rgba(255,119,0,0.2)'
        }
      }
    ],
    grid: {
      left: '3%',
      right: '4%',
      bottom: '15%',
      containLabel: true
    }
  }

  // Apply Y-axis resolution settings
  if (props.yAxisMin !== null) {
    option.yAxis.min = props.yAxisMin
  }
  if (props.yAxisMax !== null) {
    option.yAxis.max = props.yAxisMax
  }
  if (props.yAxisInterval !== null) {
    option.yAxis.interval = props.yAxisInterval
  }

  return option
}

/**
 * Load historical data from backend and render chart
 */
const loadChartData = async () => {
  try {
    loading.value = true
    error.value = null

    // Fetch historical data from backend
    const response = await apiService.getPowerDataHistory(props.limit)

    // Process data using api_utils (only data processing, no chart logic)
    const processedData = apiUtils.dataProcessHistory(response.data)

    // Create chart option from processed data
    const chartOption = createLineChartOption(processedData.timestamps, processedData.activePower)

    // Render chart with processed data
    if (chartInstance.value) {
      chartInstance.value.setOption(chartOption)
    }

    console.log('Line chart data loaded successfully')
  } catch (err) {
    console.error('Error loading chart data:', err)
    error.value = 'Erro ao carregar dados do gráfico'

    // Show empty chart on error
    if (chartInstance.value) {
      const emptyOption = createLineChartOption([], [])
      chartInstance.value.setOption(emptyOption)
    }
  } finally {
    loading.value = false
  }
}

/**
 * Initialize ECharts instance
 */
const initChart = () => {
  if (chartRef.value && !chartInstance.value) {
    chartInstance.value = echarts.init(chartRef.value)

    // Handle window resize
    window.addEventListener('resize', () => {
      chartInstance.value?.resize()
    })
  }
}

/**
 * Cleanup chart instance
 */
const destroyChart = () => {
  if (chartInstance.value) {
    chartInstance.value.dispose()
    chartInstance.value = null
  }
  window.removeEventListener('resize', () => {
    chartInstance.value?.resize()
  })
}

onMounted(() => {
  initChart()
  loadChartData()
})

onBeforeUnmount(() => {
  destroyChart()
})

// Expose refresh method
defineExpose({
  refresh: loadChartData
})
</script>

<template>
  <div class="line-chart-container">
    <div v-if="loading" class="loading-overlay">
      <div class="spinner"></div>
      <p>Carregando dados históricos...</p>
    </div>

    <div v-else-if="error" class="error-message">
      <p>{{ error }}</p>
      <button @click="loadChartData" class="retry-button">Tentar Novamente</button>
    </div>

    <div
        ref="chartRef"
        class="chart"
        :style="{ height: props.height }"
    ></div>
  </div>
</template>

<style scoped>
.line-chart-container {
  position: relative;
  width: 100%;
}

.chart {
  width: 100%;
}

.loading-overlay {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  min-height: 400px;
}

.error-message {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  min-height: 400px;
  color: #e74c3c;
}

.error-message p {
  margin-bottom: 1rem;
  font-size: 1.1rem;
}

.retry-button {
  padding: 0.5rem 1rem;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
}

.retry-button:hover {
  background-color: #2980b9;
}
</style>