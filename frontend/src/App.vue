<script setup>
import MapComponent from './components/MapComponent.vue'
import FetchAPIButton from "@/components/FetchAPIButton.vue";
import LoadingScreen from "@/components/LoadingScreen.vue";
import LineChart from "@/components/LineChart.vue";
</script>

<template>
  <LoadingScreen />
  <main>
    <FetchAPIButton />
    <div>
      <MapComponent />
    </div>
    <div>
      <LineChart :height="'50rem'" :yAxisInterval="300" />
    </div>
  </main>
</template>

<style>
main {
  padding: 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 100vh;
  width: 100%;
  box-sizing: border-box;
}
</style>

<style scoped>
div {
  width: 100%;
}
</style>
