<template>
  <h6 class="main_title">Приветствуем в нашем ресторане, меня зовут Арсений и я буду вашим официантом! Вы можете сделать заказ из готовых блюд или же добавить свое блюдо. Или можете просто посмотреть на мои фотки </h6>
  <div class="slider-wrapper">
    <Carousel :items-to-show="1" :wrap-around="true" :autoplay="3000">
      <Slide v-for="slide in slides" :key="slide.id">
        <div class="slide-image">
          <img :src="slide.image" :alt="slide.alt" />
        </div>
      </Slide>

      <template #addons>
        <Pagination />
        <Navigation />
      </template>
    </Carousel>
  </div>
</template>

<script setup>
import { Carousel, Slide, Pagination, Navigation } from 'vue3-carousel'
import 'vue3-carousel/dist/carousel.css'

const slides = [
  {
    id: 1,
    image: '/images/ars2.jpg',
    alt: 'ars1'
  },
  {
    id: 2,
    image: '/images/ars4.jpg',
    alt: 'ars2',
  },
  {
    id: 3,
    image: '/images/ars5.jpg',
    alt: 'ars3'
  },
  {
    id: 4,
    image: '/images/ars3.jpg',
    alt: 'ars4'
  },
  {
    id: 5,
    image: '/images/ars6.jpg',
    alt: 'ars5',
  },
  {
    id: 6,
    image: '/images/ars1.jpg',
    alt: 'ars6'
  }
]
</script>

<style scoped>

h6{
  display: block;
  max-width: 1000px;
  margin: 0 auto;
}

.slider-wrapper {
  max-width: 1000px;
  margin: 20px auto;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 8px 24px rgba(0,0,0,0.15);
}

.slide-image {
  position: relative;
  width: 100%;
  height: 800px;
}

.slide-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;   /* верни обратно */
}

:deep(.carousel__prev),
:deep(.carousel__next) {
  background: rgba(0,0,0,0.4);
  border-radius: 50%;
  width: 40px;
  height: 40px;
  color: white;
}

:deep(.carousel__prev:hover),
:deep(.carousel__next:hover) {
  background: rgba(0,0,0,0.7);
}

:deep(.carousel__pagination-button) {
  background: #ccc;
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

:deep(.carousel__pagination-button--active) {
  background: #42b883;
}
</style>