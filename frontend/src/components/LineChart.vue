<script setup>
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'
import apiService from '../services/api'
import apiUtils from '../services/api_utils'
import echartsHandler from '../services/echart_handler'

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
  }
})

/**
 * Load historical data from backend and render chart
 */
const loadChartData = async () => {
  try {
    loading.value = true
    error.value = null

    // Fetch historical data from backend
    const response = await apiService.getPowerDataHistory(props.limit)

    // Process data using api_utils
    const processedData = apiUtils.dataProcessHistoryForChart(response.data)

    // Render chart with processed data
    if (chartInstance.value) {
      chartInstance.value.setOption(processedData.chartOption)
    }

    console.log('Line chart data loaded successfully')
  } catch (err) {
    console.error('Error loading chart data:', err)
    error.value = 'Erro ao carregar dados do gráfico'

    // Show empty chart on error
    if (chartInstance.value) {
      chartInstance.value.setOption(echartsHandler.createEmptyChartOption())
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

// Cleanup on unmount
import { onBeforeUnmount } from 'vue'
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