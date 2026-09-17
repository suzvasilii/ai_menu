<template>
  <div class="input-group mb-3 inputs">
    <p>
      <input
        v-model="dishName"
        type="text"
        class="form-control"
        placeholder="Добавить по названию"
        @keyup.enter="addDish"
      />
    </p>

    <p class="btn_p">
      <button
        type="button"
        class="btn btn-info"
        @click="addDish"
        :disabled="isLoading"
      >
        <span v-if="isLoading">⏳ Добавление...</span>
        <span v-else>Внести в меню</span>
      </button>
    </p>

    <p>
      <input
        type="file"
        accept="image/*"
        @change="handleFileUpload"
        class="form-control"
      />
    </p>

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

  <Teleport to="body">
    <div
      v-if="isModalOpen"
      class="modal fade show d-block"
      tabindex="-1"
      role="dialog"
      @click.self="closeModal"
    >
      <div class="modal-dialog modal-lg modal-dialog-centered modal-dialog-scrollable">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Подтвердите данные</h5>
            <button
              type="button"
              class="btn-close"
              aria-label="Закрыть"
              @click="closeModal"
            ></button>
          </div>

          <div class="modal-body">
            <ConfirmDish
              v-if="resultType === 'dish'"
              :dish-var="result"
              @confirm="onConfirmDish"
              @cancel="closeModal"
              @retry="retry"
            />

            <ConfirmClassify
              v-else-if="resultType === 'classify'"
              :dish-var="result"
              @confirm="onConfirmClassify"
              @cancel="closeModal"
            />

            <div v-else class="text-muted">Нет данных для отображения</div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="isModalOpen" class="modal-backdrop fade show"></div>
  </Teleport>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { aiApi, type DishesResponse } from '@/api/ai'
import ConfirmDish from './ConfirmDish.vue'
import ConfirmClassify from './ConfirmClassify.vue'

const dishName = ref('')
const isLoading = ref(false)
const selectedFile = ref<File | null>(null)

const isModalOpen = ref(false)
const result = ref<any>(null)
const resultType = ref<'dish' | 'classify' | null>(null)

const originalQuery = ref('')
const attempts = ref<string[]>([])

const addDish = async () => {
  if (!dishName.value.trim()) {
    console.warn('⚠️ Поле пустое')
    return
  }
  originalQuery.value = dishName.value.trim()
  attempts.value = []
  isLoading.value = true
  try {
    const response = await aiApi.getDishPhoto(originalQuery.value)
    openModal(response)
    dishName.value = ''
  } catch (e) {
    console.error(e)
  } finally {
    isLoading.value = false
  }
}

const retry = async () => {
  isLoading.value = true
  try {
    const current = result.value as DishesResponse | null
    if (current?.english_dish_name) {
      attempts.value.push(current.english_dish_name)
    }

    const response = await aiApi.retryGetDishPhoto({
      dish_name: originalQuery.value,
      attempts: attempts.value,
    })
    openModal(response)
  } catch (e) {
    console.error(e)
  } finally {
    isLoading.value = false
  }
}

const handleFileUpload = (event: Event) => {
  const target = event.target as HTMLInputElement
  selectedFile.value = target.files?.[0] ?? null
}

const uploadPhoto = async () => {
  if (!selectedFile.value) return

  isLoading.value = true
  try {
    const response = await aiApi.classifyByPhoto(selectedFile.value)
    openModal(response)
    selectedFile.value = null
  } catch (e) {
    console.error(e)
  } finally {
    isLoading.value = false
  }
}

function openModal(response: any) {
  result.value = response

  if (Array.isArray(response?.images) && response.images.length > 0) {
    resultType.value = 'dish'
  } else {
    resultType.value = 'classify'
  }

  isModalOpen.value = true
}

function closeModal() {
  isModalOpen.value = false
  result.value = null
  resultType.value = null
  attempts.value = []
  originalQuery.value = ''
}

function onConfirmDish(payload: any) {
  console.log('✅ Подтверждено (dish):', payload)
  closeModal()
}

function onConfirmClassify(payload: any) {
  console.log('✅ Подтверждено (classify):', payload)
  closeModal()
}
</script>

<style scoped>
.inputs {
  flex-wrap: wrap;
  gap: 0.5rem;
}
.btn_p {
  margin: 0;
}
</style>