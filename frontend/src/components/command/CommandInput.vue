<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits<{
  start: [command: string]
  stop: []
}>()

defineProps<{
  status: 'idle' | 'running' | 'finished' | 'error'
}>()

const command = ref('')

function onStart() {
  if (command.value.trim()) emit('start', command.value.trim())
}

function onKeydown(e: KeyboardEvent) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    onStart()
  }
}
</script>

<template>
  <div class="command-bar">
    <div class="input-wrapper">
      <span class="prompt-symbol">$</span>
      <input
        v-model="command"
        class="command-input mono"
        placeholder="Enter command, e.g.: ls -la /tmp   or   strace -e trace=network curl example.com"
        :disabled="status === 'running'"
        @keydown="onKeydown"
      />
    </div>
    <button
      v-if="status !== 'running'"
      class="btn btn-start"
      :disabled="!command.trim()"
      @click="onStart"
    >
      <span class="btn-icon">▶</span> Start
    </button>
    <button v-else class="btn btn-stop" @click="$emit('stop')">
      <span class="btn-icon">■</span> Stop
    </button>
    <div class="status-badge" :class="'status-' + status">
      <span class="status-dot"></span>
      {{ status }}
    </div>
  </div>
</template>

<style scoped>
.command-bar {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  padding: var(--space-sm) var(--space-lg);
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border-primary);
  height: var(--command-bar-height);
}

.input-wrapper {
  flex: 1;
  display: flex;
  align-items: center;
  background: var(--bg-input);
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-md);
  padding: 0 var(--space-md);
  transition: border-color var(--transition);
}
.input-wrapper:focus-within {
  border-color: var(--accent);
}

.prompt-symbol {
  color: var(--success);
  font-family: var(--font-mono);
  font-size: var(--font-size-lg);
  margin-right: var(--space-sm);
}

.command-input {
  flex: 1;
  border: none;
  background: transparent;
  color: var(--text-primary);
  font-size: var(--font-size-lg);
  padding: var(--space-sm) 0;
  outline: none;
}
.command-input::placeholder {
  color: var(--text-muted);
}
.command-input:disabled {
  opacity: 0.5;
}

.btn {
  display: flex;
  align-items: center;
  gap: var(--space-xs);
  padding: var(--space-sm) var(--space-lg);
  border-radius: var(--radius-md);
  font-size: var(--font-size-sm);
  font-weight: 600;
  transition: all var(--transition);
}
.btn-start {
  background: var(--success);
  color: #fff;
}
.btn-start:hover:not(:disabled) {
  background: #2ea043;
}
.btn-start:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
.btn-stop {
  background: var(--danger);
  color: #fff;
}
.btn-stop:hover {
  background: #da3633;
}
.btn-icon {
  font-size: 10px;
}

.status-badge {
  display: flex;
  align-items: center;
  gap: var(--space-xs);
  font-size: var(--font-size-xs);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  padding: var(--space-xs) var(--space-sm);
  border-radius: var(--radius-sm);
}
.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
}
.status-idle { color: var(--text-muted); }
.status-idle .status-dot { background: var(--text-muted); }
.status-running { color: var(--success); }
.status-running .status-dot { background: var(--success); animation: pulse 1.5s infinite; }
.status-finished { color: var(--accent); }
.status-finished .status-dot { background: var(--accent); }
.status-error { color: var(--danger); }
.status-error .status-dot { background: var(--danger); }

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.3; }
}
</style>
