<script setup>
import {onMounted, ref} from "vue";
import apiUtils from '../services/api_utils.js'
import emitter from "@/eventBus.js"
import powerDataManagement from '@/services/utils.js'
import energyImg from '../assets/energy.png'

let totalActivePower = ref(0)
let totalInstalledPower = ref(0)
let isOpen = ref(false) // Menu boolean state (visible/hidden)

async function updateTotals(data) {
  const totals = apiUtils.dataProcessSum(data)
  if (totals) {
    totalActivePower.value = powerDataManagement.formatPower(totals.totalActivePower)
    totalInstalledPower.value = powerDataManagement.formatPower(totals.totalInstalledPower)
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
      <span class="power-value">{{ totalActivePower }}</span> de potência total ativa
      <br>
      <span class="power-value">{{ totalInstalledPower }}</span> de potência total instalada
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
  padding: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  text-align: center;
  width: 70%;
  max-width: 300px;
  min-height: 60px;
  display: grid;
  grid-template-columns: 1fr;
  left: 0;
  top: 10px;
  transform: translateX(0);
  transition: transform 0.35s ease-in-out, box-shadow 0.3s ease-in-out;
  overflow: visible;
  font-size: clamp(0.75rem, 2vw, 0.95rem);
}

.total-sum.closed {
  transform: translateX(calc(-100% + 44px));
}

.content {
  padding-right: 10px;
}

.power-value {
  font-weight: bold;
  color: var(--color-text-highlight);
  font-size: clamp(0.85rem, 2.5vw, 1.1rem);
}

.toggle-btn {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-background-soft);
  border: 1px solid var(--color-border);
  border-left: none;
  cursor: pointer;
  position: absolute;
  top: 8px;
  right: -40px;
  padding: 0;
  border-radius: 0 8px 8px 0;
}

.total-sum.closed .toggle-btn {
  right: 0;
}

.icon {
  width: 24px;
  height: 24px;
  object-fit: contain;
  display: block;
}

/* Tablet */
@media (min-width: 768px) {
  .total-sum {
    width: 50%;
    max-width: 350px;
    padding: 10px;
    top: 15px;
  }

  .toggle-btn {
    width: 44px;
    height: 44px;
    right: -44px;
  }

  .total-sum.closed .toggle-btn {
    right: 0;
  }

  .icon {
    width: 28px;
    height: 28px;
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .total-sum {
    width: 25%;
    max-width: 400px;
    top: 20px;
  }
}
</style>