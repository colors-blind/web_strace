<script setup lang="ts">
import SessionList from '../sessions/SessionList.vue'

defineProps<{ open: boolean }>()
const emit = defineEmits<{ selectSession: [id: string] }>()
</script>

<template>
  <aside class="app-sidebar" :class="{ open }">
    <SessionList @select="emit('selectSession', $event)" />
  </aside>
</template>

<style scoped>
.app-sidebar {
  width: var(--sidebar-width);
  background: var(--bg-secondary);
  border-right: 1px solid var(--border-primary);
  overflow: hidden;
  transition: width var(--transition), opacity var(--transition);
}
.app-sidebar:not(.open) {
  width: 0;
  opacity: 0;
  pointer-events: none;
}
</style>
