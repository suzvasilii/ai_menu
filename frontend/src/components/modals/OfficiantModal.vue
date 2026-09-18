<template>
  <Teleport to="body">
    <div
      v-if="isOpen"
      class="modal fade show d-block"
      tabindex="-1"
      role="dialog"
      @click.self="close"
    >
      <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Спросить у официанта</h5>
            <button
              type="button"
              class="btn-close"
              aria-label="Закрыть"
              @click="close"
            ></button>
          </div>

          <div class="modal-body chat-body" ref="chatBodyRef">
            <div v-if="messages.length === 0" class="text-muted text-center">
              Задайте вопрос — например, «что посоветуешь из супов?»
            </div>

            <div
              v-for="(msg, i) in messages"
              :key="i"
              class="chat-row"
              :class="msg.role === 'user' ? 'justify-end' : 'justify-start'"
            >
              <div class="chat-bubble" :class="msg.role">
                {{ msg.content }}
              </div>
            </div>

            <div v-if="isLoading" class="chat-row justify-start">
              <div class="chat-bubble assistant">Печатает...</div>
            </div>
          </div>

          <div class="modal-footer chat-footer">
            <input
              v-model="input"
              type="text"
              class="form-control"
              placeholder="Напишите вопрос..."
              @keyup.enter="send"
              :disabled="isLoading"
            />
            <button
              class="btn btn-primary"
              @click="send"
              :disabled="isLoading || !input.trim()"
            >
              Отправить
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="isOpen" class="modal-backdrop fade show"></div>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, nextTick } from 'vue'
import { aiApi, type OfficiantMessage } from '@/api/ai'

defineProps<{ isOpen: boolean }>()
const emit = defineEmits<{ (e: 'close'): void }>()

const messages = ref<OfficiantMessage[]>([])
const input = ref('')
const isLoading = ref(false)
const chatBodyRef = ref<HTMLElement | null>(null)

async function send() {
  const text = input.value.trim()
  if (!text || isLoading.value) return

  messages.value.push({ role: 'user', content: text })
  input.value = ''
  isLoading.value = true
  await scrollToBottom()

  try {
    const response = await aiApi.askOfficiant(messages.value)
    messages.value.push({ role: 'assistant', content: response.answer })
  } catch (e) {
    console.error(e)
    messages.value.push({ role: 'assistant', content: 'Ошибка связи с официантом' })
  } finally {
    isLoading.value = false
    await scrollToBottom()
  }
}

async function scrollToBottom() {
  await nextTick()
  chatBodyRef.value?.scrollTo({
    top: chatBodyRef.value.scrollHeight,
    behavior: 'smooth',
  })
}

function close() {
  messages.value = []
  input.value = ''
  isLoading.value = false
  emit('close')
}
</script>

<style scoped>
.chat-body {
  max-height: 60vh;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.chat-row {
  display: flex;
}

.justify-end {
  justify-content: flex-end;
}

.justify-start {
  justify-content: flex-start;
}

.chat-bubble {
  max-width: 75%;
  padding: 8px 12px;
  border-radius: 12px;
  white-space: pre-wrap;
  word-break: break-word;
}

.chat-bubble.user {
  background: #42b883;
  color: #fff;
  border-bottom-right-radius: 4px;
}

.chat-bubble.assistant {
  background: #f1f3f5;
  color: #2c3e50;
  border-bottom-left-radius: 4px;
}

.chat-footer {
  display: flex;
  gap: 8px;
}
</style>