<script setup lang="ts">
defineProps<{ sidebarOpen: boolean }>()
const emit = defineEmits<{ toggleSidebar: [] }>()
</script>

<template>
  <header class="app-header">
    <div class="header-left">
      <button class="sidebar-toggle" @click="emit('toggleSidebar')">☰</button>
      <h1 class="app-title">
        <span class="title-icon">⚡</span>
        strace-web
      </h1>
    </div>
    <div class="header-right">
      <span class="subtitle">Real-time Syscall Visualization</span>
    </div>
  </header>
</template>

<style scoped>
.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: var(--header-height);
  padding: 0 var(--space-lg);
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border-primary);
  grid-column: 1 / -1;
}

.header-left {
  display: flex;
  align-items: center;
  gap: var(--space-md);
}

.sidebar-toggle {
  color: var(--text-secondary);
  font-size: 16px;
  padding: var(--space-xs) var(--space-sm);
  border-radius: var(--radius-sm);
}
.sidebar-toggle:hover {
  background: var(--bg-tertiary);
  color: var(--text-primary);
}

.app-title {
  margin: 0;
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  gap: var(--space-xs);
}

.title-icon {
  font-size: 16px;
}

.subtitle {
  font-size: var(--font-size-xs);
  color: var(--text-muted);
}
</style>
