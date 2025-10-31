<script setup>
import MapComponent from './components/MapComponent.vue'
import FetchAPIButton from "@/components/FetchAPIButton.vue";
</script>

<template>
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

button {
  border: none;
  border-radius: 15px;
  font-size: 16px;
  margin: 0 10px;
  padding: 10px 20px;
  cursor: pointer;
}
</style>

<style scoped>
div {
  width: 100%;
}
</style>
