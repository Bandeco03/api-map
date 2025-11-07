<script setup>
import MapComponent from './components/MapComponent.vue'
import FetchAPIButton from "@/components/FetchAPIButton.vue";
import LoadingScreen from "@/components/LoadingScreen.vue";
</script>

<template>
  <LoadingScreen />
  <main>
    <FetchAPIButton />
    <div>
      <MapComponent />
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
