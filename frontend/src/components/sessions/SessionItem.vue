<script setup lang="ts">
import type { SessionInfo } from '../../types'

defineProps<{ session: SessionInfo; active: boolean }>()
const emit = defineEmits<{ select: [id: string] }>()
</script>

<template>
  <div class="session-item" :class="{ active }" @click="emit('select', session.id)">
    <div class="session-command mono truncate">{{ session.command }}</div>
    <div class="session-meta">
      <span class="session-status" :class="'s-' + session.status">{{ session.status }}</span>
      <span class="session-count">{{ session.total_syscalls }} calls</span>
    </div>
    <div class="session-time">{{ session.start_time?.split('T')[1]?.split('.')[0] || '' }}</div>
  </div>
</template>

<style scoped>
.session-item {
  padding: var(--space-sm) var(--space-md);
  border-bottom: 1px solid var(--border-subtle);
  cursor: pointer;
  transition: background var(--transition);
}
.session-item:hover {
  background: var(--bg-tertiary);
}
.session-item.active {
  background: rgba(88, 166, 255, 0.08);
  border-left: 2px solid var(--accent);
}

.session-command {
  font-size: var(--font-size-sm);
  color: var(--text-primary);
  margin-bottom: 2px;
}

.session-meta {
  display: flex;
  gap: var(--space-sm);
  font-size: var(--font-size-xs);
}

.session-status {
  text-transform: uppercase;
  letter-spacing: 0.3px;
}
.s-running { color: var(--success); }
.s-finished { color: var(--accent); }
.s-error { color: var(--danger); }

.session-count {
  color: var(--text-muted);
}

.session-time {
  font-size: var(--font-size-xs);
  color: var(--text-muted);
  margin-top: 2px;
}
</style>
