<!-- app/components/ProductCard.vue -->
<template>
  <div class="product-card">
    <div class="product-image">
      <img :src="product.image_url" :alt="product.name" />
    </div>

    <div class="product-body">
      <h3 class="product-name">{{ product.name }}</h3>
      <button type="button" class="btn btn-info" @click="addToCart">Выбрать это</button>
      <button type="button" class="btn btn-danger" @click="deleteFromMenu">Удалить это</button>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Product {
  id: number
  name: string
  image_url: string
}
import { useCartStore } from '@/stores/cart.ts'
import { dishesApi } from "@/api/dishes.ts"

const props = defineProps<{
  product: Product
}>()

const emit = defineEmits<{
    (e: 'deleted', id: number): void
}>()

const cartStore = useCartStore()

const addToCart = () =>{
    cartStore.addToCart({
    id: props.product.id,
    name: props.product.name,
    image: props.product.image_url
    })
}

const deleteFromMenu = () =>{
  try{
    dishesApi.delete(props.product.id)
    emit('deleted', props.product.id)
  }
  catch (error:any) {
    alert("Не удалось удалить блюдо из меню")
  }
}
</script>

<style scoped>
.product-card {
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  transition: transform 0.3s ease;
  height: 100%;
}

.product-card:hover {
  transform: translateY(-5px);
}

.product-image {
  width: 100%;
  height: 200px;
  overflow: hidden;
  background: #f5f7fa;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.product-body {
  padding: 16px;
}

.product-name {
  font-size: 1.1rem;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 8px 0;
}
</style>
