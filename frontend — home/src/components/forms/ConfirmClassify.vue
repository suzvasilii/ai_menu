<template>
  <div class="card shadow-sm">
    <div class="card-body">
      Блюдо: <EditableInput v-model="props.dishVar.dish_name" />
      Категория: <EditableSelect v-model="props.dishVar.category" :options="CATEGORIES_RU" />

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
import { ref } from 'vue'
import type { ClassifiedResponse } from '@/api/ai'
import EditableInput from './inputs/EditableInput.vue'
import EditableSelect from "@/components/forms/selects/EditableSelect.vue"
import { CATEGORIES_RU } from "@/сonstants/categories.ts"

const props = defineProps<{ dishVar: ClassifiedResponse }>()
const emit = defineEmits<{
  (e: 'confirm', payload: ClassifiedResponse): void
  (e: 'cancel'): void
}>()

const originalCategory = ref(props.dishVar.category)

function confirm() {
  emit('confirm', {
    dish_name: props.dishVar.dish_name,
    category: props.dishVar.category,
    category_changed: props.dishVar.category !== originalCategory.value,
  } as any)
}
</script>