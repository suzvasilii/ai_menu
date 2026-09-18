<template>
  <div class="product-grid">
    <h2 class="section-title text-center">Можно заказать</h2>

    <div class="container">
      <div class="filter-row mb-4">
        <label for="category-select" class="filter-label">Категория:</label>
        <select
          id="category-select"
          v-model="selectedCategory"
          class="form-select filter-select"
        >
          <option value="all">Все</option>
          <option
            v-for="category in categories"
            :key="category"
            :value="category"
          >
            {{ category }}
          </option>
        </select>
      </div>

      <div class="row">
        <div
          v-for="dish in filteredDishes"
          :key="'db-' + dish.id"
          class="col-12 col-sm-6 col-md-4 col-lg-3 mb-4 d-flex align-items-stretch"
        >
          <ProductCard :product="dish" @deleted="handleDelete" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { dishesApi, type Dish } from '@/api/dishes.ts'
import ProductCard from './ProductCard.vue'

const dishesFromDB = ref<Dish[]>([])
const selectedCategory = ref<string>('all')

const categories = computed(() => {
  const set = new Set(dishesFromDB.value.map(d => d.category))
  return Array.from(set).sort()
})

const filteredDishes = computed(() => {
  if (selectedCategory.value === 'all') return dishesFromDB.value
  return dishesFromDB.value.filter(d => d.category === selectedCategory.value)
})

const loadDishesFromDB = async () => {
  try {
    const data: Dish[] = await dishesApi.getAll()
    dishesFromDB.value = data
  } catch (error) {
    console.error('Ошибка загрузки блюд из БД:', error)
  }
}

const handleDelete = (deletedId: number) => {
  console.log('Получили сигнал! Удаляем блюдо:', deletedId)
  dishesFromDB.value = dishesFromDB.value.filter(dish => dish.id !== deletedId)
}

onMounted(() => {
  loadDishesFromDB()
})
</script>

<style scoped>
.product-grid {
  padding: 40px 0;
}

.section-title {
  font-size: 2rem;
  margin-bottom: 40px;
  color: #2c3e50;
}

.filter-row {
  display: flex;
  align-items: center;
  gap: 12px;
  max-width: 400px;
}

.filter-label {
  margin: 0;
  font-weight: 500;
  color: #2c3e50;
  white-space: nowrap;
}

.filter-select {
  max-width: 260px;
}
</style>