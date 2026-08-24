<template>
<div class="form-wrapper">
<h2 class = "pageTitle">{{ pageTitle }}</h2>
<NewForm/>
</div>
</template>
<script setup lang="ts">
import NewForm from './NewForm.vue'
const pageTitle: string = 'Добавление нового блюда в меню'
</script>

<style scoped>
.form-wrapper {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  padding: 0 20px;
  box-sizing: border-box;
}
.pageTitle {
    margin: 20px;
}

@media (max-width: 600px) {
  .pageTitle {
    font-size: 1.2rem;
  }
}
</style>