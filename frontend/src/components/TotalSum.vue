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

</template>

<style scoped>

</style>