<template>
<div class="input-group mb-3 inputs">
  <p><input
      v-model="dishName"
      type="text"
      class="form-control"
      placeholder="Добавить по названию"
      @keyup.enter="addDish"
  /></p>
  <p class="btn_p">
    <button
        type="button" class="btn btn-info" @click="addDish" :disabled="isLoading">
      <span v-if="isLoading">⏳ Добавление...</span>
      <span v-else>Внести в меню</span>
    </button>
  </p>
  <p><input
    type="file"
    accept="image/*"
    @change="handleFileUpload"
    class="form-control"
  /></p>
<p class="btn_p">
  <button
    type="button"
    class="btn btn-warning"
    @click="uploadPhoto"
    :disabled="isLoading || !selectedFile"
  >
    <span v-if="isLoading">⏳ Загрузка...</span>
    <span v-else>📤 Загрузить фото</span>
  </button>
</p>
</div>
</template>
<script setup lang="ts">
import { ref } from 'vue'
import { dishesApi } from '@/api/dishes.ts'
import {router} from "@/router/router.ts";

const dishName = ref('')
const isLoading = ref(false)
const selectedFile = ref(null)

const addDish = async () => {
  if (!dishName.value.trim()) {
    console.warn('⚠️ Поле пустое')
    return
  }

  isLoading.value = true

  try {
    const newDish = await dishesApi.create(dishName.value.trim())
    console.log('✅ Блюдо добавлено:', newDish)
    dishName.value = ''
    router.push('/menu')

  } catch (error: any) {
    console.error('❌ Ошибка:', error)
    if (error.response?.status === 400) {
      alert(`⚠️ Блюдо "${dishName.value}" уже есть в меню!`)
    } else if (error.response?.status === 403) {
      alert(`❌ Блюдо "${dishName.value}" добавить нельзя`)
    } else {
      alert('❌ Ошибка добавления блюда')
    }
  } finally {
    isLoading.value = false
  }
}

const handleFileUpload = (event) => {
  const file = event.target.files[0]
  if (file) {
    selectedFile.value = file
    console.log('📸 Выбран файл:', file.name)
  }
}

const uploadPhoto = async () => {
    if (!selectedFile.value) return
    isLoading.value = true
    try {
        await dishesApi.createByPhoto(selectedFile.value)
        router.push('/menu')
    } catch (error) {
        console.error('Ошибка распознавания:', error)
    }finally {
      isLoading.value = false
    }
}

</script>

<style scoped>
.inputs{
    margin: 0 auto;
    display:flex;
    flex-direction:column;
}

.btn-info:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

@media (max-width: 600px) {
  .form-control {
    max-width: 300px;
  }
}

</style>