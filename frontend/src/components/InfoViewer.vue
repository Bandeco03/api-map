<script setup>
import {onMounted, ref} from "vue";
import apiUtils from '../services/api_utils.js'
import emitter from "@/eventBus.js"
import energyImg from '../assets/energy.png'

let totalActivePower = ref(0)
let totalInstalledPower = ref(0)
let isOpen = ref(false) // Estado do menu (aberto/fechado)

async function updateTotals(data) {
  const totals = apiUtils.dataProcessSum(data)
  if (totals) {
    totalActivePower.value = totals.totalActivePower / 1000000000 // Convert to GW
    totalInstalledPower.value = totals.totalInstalledPower / 1000000000 // Convert to GW
  }
}

function toggleMenu() {
  isOpen.value = !isOpen.value
}

onMounted(() => {
  emitter.on('api-data', (response) => {
    updateTotals(response)
  })
})
</script>

<template>
  <div class="total-sum" :class="{ 'closed': !isOpen }" :aria-expanded="isOpen">
    <div class="content" v-show="isOpen">
      <span class="power-value">{{ totalActivePower.toFixed(2) }} GW</span> de potência total ativa
      <br>
      <span class="power-value">{{ totalInstalledPower.toFixed(2) }} GW</span> de potência total instalada
    </div>
    <button @click="toggleMenu" class="toggle-btn" :aria-label="isOpen ? 'Ocultar painel' : 'Mostrar painel'">
      <img :src="energyImg" alt="" class="icon"/>
    </button>
  </div>
</template>

<style scoped>
.total-sum {
  border: var(--color-border);
  border-radius: 5px;
  position: fixed;
  background-color: var(--color-background-soft);
  z-index: 1000;
  padding: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  text-align: center;
  width: 20%;
  min-height: 60px;
  display: grid;
  grid-template-columns: 1fr;
  left: 0;
  top: 20px;
  transform: translateX(0);
  transition: transform 0.35s ease-in-out, box-shadow 0.3s ease-in-out;
  overflow: visible;
}

.total-sum.closed {
  transform: translateX(calc(-100% + 44px));
}

.power-value {
  font-weight: bold;
  color: var(--color-text-highlight);
}

.toggle-btn {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-background-soft);
  border: 1px solid var(--color-border);
  border-left: none;
  cursor: pointer;
  position: absolute;
  top: 8px;
  right: -44px;
  padding: 0;
  border-radius: 0 8px 8px 0;
}

.total-sum.closed .toggle-btn {
  right: 0; /* encosta na borda visível quando fechado */
}

.icon {
  width: 28px;
  height: 28px;
  object-fit: contain;
  display: block;
}
</style>