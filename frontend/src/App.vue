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
  padding: clamp(0.5rem, 2vw, 2rem);
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 100vh;
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
  flex-direction: column;
  gap: 20px;
  width: 100%;
}

.map-info-container > :first-child {
  min-width: 0;
}

.map-info-container > :last-child {
  min-width: 0;
}

/* Desktop: layout lado a lado */
@media (min-width: 768px) {
  .map-info-container {
    flex-direction: row;
  }

  .map-info-container > :first-child {
    flex: 2;
  }

  .map-info-container > :last-child {
    flex: 1;
    min-width: 300px;
  }
}
</style>
