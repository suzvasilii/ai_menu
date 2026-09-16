<template>
  <div class="card shadow-sm">
    <div class="card-body">
      <EditableInput v-model="props.dishVar.dish_name" />
      <EditableInput v-model="props.dishVar.category" />

      <button
        type="button"
        class="btn btn-primary mt-3"
        @click="sendData"
      >
        Все верно
      </button>

      <h5 class="card-title mb-3 mt-3">Результаты работы могут быть неточными.</h5>
      <h5 class="card-title mb-3">Если есть необходимость, отредактируйте</h5>

      <button
        type="button"
        class="btn btn-secondary mt-3 ms-2"
        @click="$emit('cancel')"
      >
        Отмена
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { ClassifiedResponse } from '@/api/ai'
import EditableInput from './inputs/EditableInput.vue'

const props = defineProps<{ dishVar: ClassifiedResponse }>()
const emit = defineEmits<{
  (e: 'confirm', payload: any): void
  (e: 'cancel'): void
}>()

function sendData() {
  emit('confirm', {
    dish_name: props.dishVar.dish_name,
    category: props.dishVar.category
  })
}
</script>