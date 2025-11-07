<script setup>
import {onMounted} from "vue";
import emitter from "@/eventBus.js";
import api_utils from "@/services/api_utils.js";

onMounted(() => {
  emitter.on('api-data', (response) => {
    api_utils.dataProcessSum(response)
  })
})

</script>

<template>
  <div>
    <h2>Total de Potência Ativa: {{ api_utils.totalActivePowerGW.toFixed(2) }} GW</h2>
    <h2>Total de Potência Instalada: {{ api_utils.totalInstalledPowerGW.toFixed(2) }} GW</h2>
  </div>
</template>

<style scoped>

</style>