<template>
  <div class="card shadow-sm">
    <div class="card-body">
      Блюдо: {{ props.dishVar.dish_name }}
      Категория: <EditableSelect v-model="props.dishVar.category" :options="CATEGORIES_RU" />

      <div class="row g-3 mt-2">
        <div
          v-for="(img, index) in props.dishVar.images"
          :key="index"
          class="col-12 col-sm-6 col-md-4"
        >
          <div class="ratio ratio-4x3 rounded overflow-hidden">
            <img
              :src="img.data_url"
              :alt="props.dishVar.category"
              class="img-fluid object-fit-cover"
              loading="lazy"
            />
          </div>
          <button
            type="button"
            class="btn btn-primary btn-sm mt-2 w-100"
            @click="chooseImage(img.data_url)"
          >
            Выбрать это фото
          </button>
        </div>
      </div>

      <h5 class="card-title mb-3 mt-3">Результаты работы могут быть неточными.</h5>
      <h5 class="card-title mb-3">Если есть необходимость, отредактируйте</h5>

      <div class="d-flex gap-2 mt-3">
        <button class="btn btn-warning" @click="$emit('retry')">Не подошло, ещё вариант</button>
        <button class="btn btn-secondary" @click="$emit('cancel')">Отмена</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import type { DishesResponse } from '@/api/ai'
import EditableSelect from "@/components/forms/selects/EditableSelect.vue"
import { CATEGORIES_RU } from "@/сonstants/categories.ts"

const props = defineProps<{ dishVar: DishesResponse }>()
const emit = defineEmits<{
  (e: 'confirm', payload: DishesResponse): void
  (e: 'cancel'): void
  (e: 'retry'): void
}>()

const originalCategory = ref(props.dishVar.category)

const chooseImage = (url: string) => {
  props.dishVar.selected_image = url
  emit('confirm', {
    ...props.dishVar,
    category_changed: props.dishVar.category !== originalCategory.value,
  } as any)
}
</script>

<style scoped>
.object-fit-cover {
  object-fit: cover;
}
</style>