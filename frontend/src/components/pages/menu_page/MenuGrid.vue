<template>
  <div class="product-grid">
    <h2 class="section-title text-center">Можно заказать</h2>
    
    <div class="container">
      <div class="row">
        <div
            v-for="dish in dishesFromDB"
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
import { ref, onMounted } from 'vue'
import { dishesApi, type Dish } from '@/api/dishes.ts'
import ProductCard from './ProductCard.vue'

const dishesFromDB = ref<Dish[]>([])

const loadDishesFromDB = async () => {
  try {
    const data:Dish[] = await dishesApi.getAll()
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
</style>
