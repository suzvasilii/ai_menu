<template>
  <div class="card shadow-sm">
    <div class="card-body">
      <EditableInput v-model="props.dishVar.dish_name" />
      <EditableInput v-model="props.dishVar.category" />

      <h5 class="card-title mb-3 mt-3">Результаты работы могут быть неточными.</h5>
      <h5 class="card-title mb-3">Если есть необходимость, отредактируйте</h5>

      <div class="d-flex gap-2 mt-3">
        <button class="btn btn-success" @click="confirm">Все верно</button>
        <button class="btn btn-secondary" @click="$emit('cancel')">Отмена</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { ClassifiedResponse } from '@/api/ai'
import EditableInput from './inputs/EditableInput.vue'

const props = defineProps<{ dishVar: ClassifiedResponse }>()
const emit = defineEmits<{
  (e: 'confirm', payload: ClassifiedResponse): void
  (e: 'cancel'): void
}>()

function confirm() {
  emit('confirm', {
    dish_name: props.dishVar.dish_name,
    category: props.dishVar.category,
  })
}
</script>