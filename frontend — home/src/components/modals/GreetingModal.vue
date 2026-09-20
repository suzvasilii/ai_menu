<template>
  <Teleport to="body">
    <div
      v-if="isOpen"
      class="modal fade show d-block"
      tabindex="-1"
      role="dialog"
      @click.self="close"
    >
      <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content greeting-modal">
          <div class="modal-body greeting-body">
            <img
              :src="greetingImage"
              alt="officiant"
              class="greeting-image"
            />
            <h4 class="greeting-title">Добро пожаловать!</h4>
            <p class="greeting-text">
              Приветствуем в нашем ресторане, меня зовут Арсений и я буду вашим
              официантом! Вы можете сделать заказ из готовых блюд или же добавить
              свое блюдо. Или можете просто посмотреть на мои фотки.
            </p>
            <button class="btn btn-success greeting-btn" @click="close">
              Понятно
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="isOpen" class="modal-backdrop fade show"></div>
  </Teleport>
</template>

<script setup lang="ts">
import greetingImage from '@/assets/arsenij.jpg'

defineProps<{ isOpen: boolean }>()
const emit = defineEmits<{ (e: 'close'): void }>()

function close() {
  emit('close')
}
</script>

<style scoped>
.greeting-modal {
  border-radius: 16px;
  overflow: hidden;
}

.greeting-body {
  padding: 32px 24px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.greeting-image {
  width: 100%;
  max-width: 320px;
  max-height: 320px;
  object-fit: cover;
  border-radius: 12px;
}

.greeting-title {
  margin: 0;
  color: #2c3e50;
  font-size: 1.4rem;
  font-weight: 700;
}

.greeting-text {
  margin: 0;
  color: #4a5568;
  font-size: 1rem;
  line-height: 1.5;
  max-width: 560px;
}

.greeting-btn {
  margin-top: 8px;
  padding: 10px 32px;
  font-weight: 600;
}
</style>