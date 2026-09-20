<template>
  <div class="d-flex align-items-center gap-2">
    <h5 v-if="!isEditing" class="mb-0">
      {{ modelValue }}
    </h5>

    <template v-else>
      <input
        ref="inputRef"
        v-model="draft"
        type="text"
        class="form-control form-control-sm"
        @keyup.enter="save"
        @keyup.esc="cancel"
      />
      <button class="btn btn-sm btn-success" @click="save">ОК</button>
      <button class="btn btn-sm btn-secondary" @click="cancel">Отмена</button>
    </template>

    <button
      v-if="!isEditing"
      class="btn btn-sm btn-outline-primary"
      @click="startEdit"
    >
      ✏️
    </button>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'

const props = defineProps({
  modelValue: { type: String, default: '' }
})

const emit = defineEmits(['update:modelValue'])

const isEditing = ref(false)
const draft = ref('')
const inputRef = ref(null)

function startEdit() {
  draft.value = props.modelValue
  isEditing.value = true
  nextTick(() => inputRef.value?.focus())
}

function save() {
  const trimmed = draft.value.trim()
  if (trimmed && trimmed !== props.modelValue) {
    emit('update:modelValue', trimmed)
  }
  isEditing.value = false
}

function cancel() {
  isEditing.value = false
}
</script>