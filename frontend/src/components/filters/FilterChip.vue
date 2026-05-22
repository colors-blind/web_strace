<script setup lang="ts">
defineProps<{
  label: string
  active: boolean
  color?: string
}>()

const emit = defineEmits<{ click: [] }>()
</script>

<template>
  <button
    class="filter-chip"
    :class="{ active }"
    :style="active && color ? { borderColor: color, color } : {}"
    @click="emit('click')"
  >
    {{ label }}
  </button>
</template>

<style scoped>
.filter-chip {
  display: inline-flex;
  align-items: center;
  padding: 2px 8px;
  border: 1px solid var(--border-primary);
  border-radius: 12px;
  font-size: var(--font-size-xs);
  color: var(--text-secondary);
  background: transparent;
  transition: all var(--transition);
  white-space: nowrap;
}
.filter-chip:hover {
  border-color: var(--text-secondary);
  color: var(--text-primary);
}
.filter-chip.active {
  background: rgba(88, 166, 255, 0.08);
  border-color: var(--accent);
  color: var(--accent);
}
</style>
