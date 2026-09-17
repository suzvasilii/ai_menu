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

  <!-- ================== МОДАЛКА ================== -->
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
              :original-query="lastQuery"
              @confirm="onConfirmDish"
              @cancel="closeModal"
            />

            <!-- Компонент 2: без картинок -->
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

    <!-- Затемнение фона -->
    <div v-if="isModalOpen" class="modal-backdrop fade show"></div>
  </Teleport>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { aiApi } from '@/api/ai.ts'
import ConfirmDish from './ConfirmDish.vue'
import ConfirmClassify from './ConfirmClassify.vue'

const dishName = ref('')
const isLoading = ref(false)
const selectedFile = ref<File | null>(null)
const lastQuery = ref('')

// --- состояние модалки ---
const isModalOpen = ref(false)
const result = ref<any>(null)
const resultType = ref<'dish' | 'classify' | null>(null)

// --- добавление блюда по названию ---
const addDish = async () => {
  if (!dishName.value.trim()) {
    console.warn('⚠️ Поле пустое')
    return
  }
  lastQuery.value = dishName.value.trim()
  isLoading.value = true
  try {
    const response = await aiApi.getDishPhoto(dishName.value.trim())
    openModal(response)

    dishName.value = ''
  } catch (e) {
    console.error(e)
  } finally {
    isLoading.value = false
  }
}

// --- загрузка фото ---
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

// --- открытие модалки и определение типа ---
function openModal(response: any) {
  result.value = response

  // Определи тип ответа под свой бэк.
  // Пример: если есть непустой массив images — это 'dish', иначе 'classify'
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
}

// --- обработчики подтверждения ---
function onConfirmDish(payload: any) {
  console.log('✅ Подтверждено (dish):', payload)
  // тут отправка на сервер / router.push / что нужно
  closeModal()
}

function onConfirmClassify(payload: any) {
  console.log('✅ Подтверждено (classify):', payload)
  // тут отправка на сервер / router.push / что нужно
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