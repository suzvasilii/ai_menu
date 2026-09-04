<template>
  <div class="auth-modal-overlay">
    <div class="auth-modal">
      <p><h2>Для входа в сервис необходима авторизация</h2></p>
      <p><h3><a href="https://t.me/hypervotrsbot">Напишите нашему боту</a> команду /token</h3></p>
      <p><h3><a href="https://t.me/hypervotrsbot">Если бот вас распознает, то вы сможете воспользоваться меню</a></h3></p>
    </div>
  </div>
</template>
<style scoped>
.auth-modal-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}
.auth-modal {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  width: 360px;
  position: relative;
}
</style>
<script setup lang="ts">
</script>