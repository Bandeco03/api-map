<script setup>
import {ref, onMounted, onBeforeUnmount} from 'vue'
import VChart from 'vue-echarts'
import * as echarts from 'echarts/core'
import {LineChart} from 'echarts/charts'
import {
  GridComponent,
  TooltipComponent,
  TitleComponent
} from 'echarts/components'
import {CanvasRenderer} from 'echarts/renderers'
import apiUtils from '../services/api_utils'
import emitter from "@/eventBus.js";

// Register required ECharts components
echarts.use([
  LineChart,
  GridComponent,
  TooltipComponent,
  TitleComponent,
  CanvasRenderer
])

const chartRef = ref(null)
const loading = ref(true)
const error = ref(null)

const props = defineProps({
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

// Chart option as reactive ref
const option = ref({
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
    data: [],
    axisLabel: {
      rotate: 45,
      interval: 0
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
      data: [],
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
})

/**
 * Load historical data from backend and render chart
 */
const loadChartData = async (historical) => {
  try {
    loading.value = true
    error.value = null

    // Process data using api_utils (only data processing, no chart logic)
    const processedData = apiUtils.dataProcessHistory(historical.data)

    // Update chart option with processed data
    option.value.xAxis.data = processedData.timestamps
    option.value.xAxis.axisLabel.interval = Math.floor(processedData.timestamps.length / 10) || 0
    option.value.series[0].data = processedData.activePower

    // Apply Y-axis resolution settings
    if (props.yAxisMin !== null) {
      option.value.yAxis.min = props.yAxisMin
    }
    if (props.yAxisMax !== null) {
      option.value.yAxis.max = props.yAxisMax
    }
    if (props.yAxisInterval !== null) {
      option.value.yAxis.interval = props.yAxisInterval
    }

    // console.log('Line chart data loaded successfully')
  } catch (err) {
    console.error('Error loading chart data:', err)
    error.value = 'Erro ao carregar dados do gráfico'

    // Show empty chart on error
    option.value.xAxis.data = []
    option.value.series[0].data = []
  } finally {
    loading.value = false
  }
}

const handleHistoryData = (historical) => {
  loadChartData(historical)
}

onMounted(() => {
  emitter.on('api-history', handleHistoryData)
})

onBeforeUnmount(() => {
  emitter.off('api-history', handleHistoryData)
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
    </div>

    <v-chart
        ref="chartRef"
        class="chart"
        :option="option"
        autoresize
    />
  </div>
</template>

<style scoped>
.line-chart-container {
  position: relative;
  width: 100%;
}

.chart {
  width: 100%;
  height: 300px;
  min-height: 300px;
}

.loading-overlay {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  min-height: 300px;
}

.loading-overlay p {
  font-size: clamp(0.875rem, 2vw, 1rem);
}

.error-message {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  min-height: 300px;
  color: #e74c3c;
}

.error-message p {
  margin-bottom: 1rem;
  font-size: clamp(0.9rem, 2.5vw, 1.1rem);
}

/* Tablet */
@media (min-width: 768px) {
  .chart {
    height: 400px;
    min-height: 400px;
  }

  .loading-overlay,
  .error-message {
    padding: 1.5rem;
    min-height: 400px;
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .chart {
    height: 500px;
    min-height: 500px;
  }

  .loading-overlay,
  .error-message {
    padding: 2rem;
    min-height: 500px;
  }
}
</style>