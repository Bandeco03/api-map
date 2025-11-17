<script setup>
import {onMounted, ref} from "vue";
import apiUtils from '../services/api_utils.js'
import emitter from "@/eventBus.js"

let totalActivePower = ref(0)
let totalInstalledPower = ref(0)

async function updateTotals(data) {
  const totals = apiUtils.dataProcessSum(data)
  if (totals) {
    totalActivePower.value = totals.totalActivePower / 1000000000 // Convert to GW
    totalInstalledPower.value = totals.totalInstalledPower / 1000000000 // Convert to GW
  }
}

onMounted(() => {
  emitter.on('api-data', (response) => {
    updateTotals(response)
  })
})
</script>

<template>
  <div class="total-sum">
    {{ totalActivePower.toFixed(2) }} GW de potência total ativa
    <br>
    {{ totalInstalledPower.toFixed(2) }} GW de potência total instalada
  </div>
</template>

<style scoped>
div {
  border: 1px solid gray;
  border-radius: 5px;
  position: fixed;
  background-color: var(--color-background);
  z-index: 1000;
  padding: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.total-sum {
  text-align: center;
  width: 20%;
}
</style>