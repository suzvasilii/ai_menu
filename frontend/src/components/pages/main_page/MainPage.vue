<template>
  <div class="home-wrapper">
      <h6 class="main_title">Приветствуем в нашем ресторане, меня зовут Арсений и я буду вашим официантом! Вы можете сделать заказ из готовых блюд или же добавить свое блюдо. Или можете просто посмотреть на мои фотки </h6>
    <Slider />
  </div>
</template>

<script setup lang="ts">
import Slider from "@/components/pages/main_page/Slider.vue";
</script>

<style scoped>
.home-wrapper {
  padding: 0 10px;
  max-width: 1200px;
  margin: 0 auto;
}
</style>