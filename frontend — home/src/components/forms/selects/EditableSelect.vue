<template>
  <div class="d-flex align-items-center gap-2">
    <h5 v-if="!isEditing" class="mb-0">
      {{ modelValue }}
    </h5>

    <template v-else>
      <select
        ref="selectRef"
        v-model="draft"
        class="form-select form-select-sm"
        @keyup.enter="save"
        @keyup.esc="cancel"
      >
        <option v-for="opt in options" :key="opt" :value="opt">
          {{ opt }}
        </option>
      </select>
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

<script setup lang="ts">
import { ref, nextTick } from 'vue'

const props = defineProps<{
  modelValue: string
  options: readonly string[]
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
}>()

const isEditing = ref(false)
const draft = ref('')
const selectRef = ref<HTMLSelectElement | null>(null)

function startEdit() {
  draft.value = props.modelValue
  isEditing.value = true
  nextTick(() => selectRef.value?.focus())
}

function save() {
  if (draft.value && draft.value !== props.modelValue) {
    emit('update:modelValue', draft.value)
  }
  isEditing.value = false
}

function cancel() {
  isEditing.value = false
}
</script>