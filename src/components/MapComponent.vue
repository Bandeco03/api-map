<script setup>
import { ref } from 'vue'
import VChart from 'vue-echarts'
import * as echarts from 'echarts/core'
import { MapChart } from 'echarts/charts'
import { TooltipComponent, VisualMapComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import brazilGeoJson from '../../public/brazil.json'
import axios from 'axios'

const realTimePower = ref(true)

// Register required ECharts modules
echarts.use([MapChart, TooltipComponent, VisualMapComponent, CanvasRenderer])

echarts.registerMap('BRA', brazilGeoJson)

// Mapeamento de código para nome do estado
const codeToStateName = {
  '12': 'Acre',
  '27': 'Alagoas',
  '16': 'Amapá',
  '13': 'Amazonas',
  '29': 'Bahia',
  '23': 'Ceará',
  '32': 'Espírito Santo',
  '52': 'Goiás',
  '21': 'Maranhão',
  '51': 'Mato Grosso',
  '50': 'Mato Grosso do Sul',
  '31': 'Minas Gerais',
  '15': 'Pará',
  '25': 'Paraíba',
  '41': 'Paraná',
  '26': 'Pernambuco',
  '22': 'Piauí',
  '33': 'Rio de Janeiro',
  '24': 'Rio Grande do Norte',
  '43': 'Rio Grande do Sul',
  '11': 'Rondônia',
  '14': 'Roraima',
  '42': 'Santa Catarina',
  '35': 'São Paulo',
  '28': 'Sergipe',
  '17': 'Tocantins',
  '53': 'Distrito Federal'
}

const stateData = ref([])

async function fetchData() {
  const url = 'https://gateway.isolarcloud.com.hk/openapi/getPowerStationInfoPowerByCodeList'
  const headers = {
    'Content-Type': 'application/json',
    'x-access-key': '3g1nrc7c59kxygt2i7idana49jpvw01f',
    'sys_code': '901'
  }
  const data = {
    token: '110295_b1f25dda84f640c7acc6456bbbec9a47',
    appkey: '664780B4B466AB6F19DF393D5055D977'
  }

  try {
    const response = await axios.post(url, data, { headers })

    if (response.data && response.data.result_code === '1' && response.data.result_data) {
      stateData.value = response.data.result_data.map(item => {
        const stateName = codeToStateName[item.code] || `Estado ${item.code}`
        if (realTimePower.value) {
          return {
            name: stateName,
            value: item.state_realtime_power, // valor usado para o visualMap
            activePower: item.state_realtime_power,
            totalPower: item.state_installed_power
          }
        } else {
          return {
            name: stateName,
            value: item.state_installed_power, // valor usado para o visualMap
            activePower: item.state_realtime_power,
            totalPower: item.state_installed_power
          }
        }
      })

      // Atualizar opções do mapa
      option.value.series[0].data = stateData.value

      // Atualizar visualMap baseado nos valores reais
      const powers = stateData.value.map(s => s.value)
      option.value.visualMap.min = Math.min(...powers)
      option.value.visualMap.max = Math.max(...powers)

      console.log('Dados carregados com sucesso:', stateData.value.length, 'estados')
    } else {
      console.error('Dados da API inválidos', response.data)
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
          Potência instalada: <b>${(d.totalPower / 1000000).toFixed(2)}</b> MW
        `
      }
      return `<b>${params.name}</b><br/>Sem dados`
    }
  },
  visualMap: {
    min: 0,
    max: 2500,
    left: 'left',
    top: 'bottom',
    text: ['Alto', 'Baixo'],
    inRange: { color: ['#e0f7fa', '#0288d1'] },
    calculable: true
  },
  series: [
    {
      type: 'map',
      map: 'BRA',
      roam: false,
      layoutCenter: ['50%', '50%'],
      layoutSize: '90%',
      aspectScale: 0.9,
      data: stateData.value
    }
  ]
})

import { onMounted } from 'vue'
onMounted(() => {
  fetchData()
})
</script>

<template>
  <div>
    <button @click="fetchData" style="margin: 10px; padding: 10px 20px; cursor: pointer;">
      Carregar Dados da API
    </button>
    <button @click="realTimePower = !realTimePower; fetchData()" style="margin: 10px; padding: 10px 20px; cursor: pointer;">
      Mostrar {{ realTimePower ? 'Potência Instalada' : 'Potência Ativa' }}
    </button>
    <v-chart :option="option" autoresize style="height: 600px; width: 100%;" />
    <header>
      {{ realTimePower }}
    </header>
  </div>
</template>