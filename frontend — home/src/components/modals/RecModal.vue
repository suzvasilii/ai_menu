<template>
  <Teleport to="body">
    <div
      v-if="isOpen"
      class="modal fade show d-block"
      tabindex="-1"
      role="dialog"
      @click.self="close"
    >
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Предлагаю заказать еще это</h5>
            <button
              type="button"
              class="btn-close"
              aria-label="Закрыть"
              @click="close"
            ></button>
          </div>

          <div class="modal-body">
            <div
              v-for="rec in recommendations"
              :key="rec.name"
              class="recommendation-item d-flex align-items-center gap-3 mb-3"
            >
              <img
                :src="rec.image_url"
                :alt="rec.name"
                class="recommendation-image"
              />
              <div class="flex-grow-1">
                <h6 class="mb-0">{{ rec.name }}</h6>
              </div>
              <button
                class="btn btn-sm btn-success"
                @click="addRecommendation(rec.name)"
              >
                Добавить
              </button>
            </div>
          </div>

          <div class="modal-footer">
            <button class="btn btn-secondary" @click="close">Нет, спасибо</button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="isOpen" class="modal-backdrop fade show"></div>
  </Teleport>
</template>

<script setup lang="ts">
import type { Recommendation } from '@/api/orders'

const props = defineProps<{
  isOpen: boolean
  recommendations: Recommendation[]
}>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'add', name: string): void
}>()

function close() {
  emit('close')
}

function addRecommendation(name: string) {
  emit('add', name)
  emit('close')
}
</script>

<style scoped>
.recommendation-image {
  width: 64px;
  height: 64px;
  object-fit: cover;
  border-radius: 8px;
}
</style>