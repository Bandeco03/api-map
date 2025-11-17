<script setup>
import MapComponent from './components/MapComponent.vue'
import FetchAPIButton from "@/components/FetchAPIButton.vue";
import LoadingScreen from "@/components/LoadingScreen.vue";
import LineChart from "@/components/LineChart.vue";
import StateCompare from "@/components/StateCompare.vue";
import InfoViewer from "@/components/InfoViewer.vue";
</script>

<template>
  <LoadingScreen />
  <InfoViewer />
  <main>
    <FetchAPIButton />
    <div class="map-info-container">
      <MapComponent />
      <StateCompare />
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

.map-info-container {
  display: flex;
  gap: 20px;
}

.map-info-container > :first-child {
  flex: 2;
  min-width: 0;
}

.map-info-container > :last-child {
  flex: 1;
  min-width: 300px;
}
</style>
