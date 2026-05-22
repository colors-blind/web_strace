<script setup lang="ts">
import { onMounted } from 'vue'
import { useSessionStore } from '../../stores/session'
import SessionItem from './SessionItem.vue'

const { sessionList, currentSessionId, loadSessions } = useSessionStore()
const emit = defineEmits<{ select: [id: string] }>()

onMounted(loadSessions)
</script>

<template>
  <div class="session-list">
    <div class="list-header">
      <h4 class="list-title">Sessions</h4>
      <button class="refresh-btn" @click="loadSessions">↻</button>
    </div>
    <div class="list-body">
      <div v-if="sessionList.length === 0" class="empty-state">No sessions yet</div>
      <SessionItem
        v-for="s in sessionList"
        :key="s.id"
        :session="s"
        :active="s.id === currentSessionId"
        @select="emit('select', $event)"
      />
    </div>
  </div>
</template>

<style scoped>
.session-list {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.list-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-sm) var(--space-md);
  border-bottom: 1px solid var(--border-primary);
}

.list-title {
  margin: 0;
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  font-weight: 500;
}

.refresh-btn {
  color: var(--text-secondary);
  font-size: 14px;
  padding: 2px 6px;
  border-radius: var(--radius-sm);
}
.refresh-btn:hover {
  background: var(--bg-tertiary);
  color: var(--text-primary);
}

.list-body {
  flex: 1;
  overflow-y: auto;
}

.empty-state {
  padding: var(--space-xl);
  text-align: center;
  color: var(--text-muted);
  font-size: var(--font-size-sm);
}
</style>
