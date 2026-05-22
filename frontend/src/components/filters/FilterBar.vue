<script setup lang="ts">
import { ref } from 'vue'
import { useFiltersStore } from '../../stores/filters'
import { allCategories, allSeverities, categoryLabels, severityLabels } from '../../utils/constants'
import { categoryColors, severityColors } from '../../utils/colors'
import FilterChip from './FilterChip.vue'

const { state, toggleCategory, toggleSeverity, setSyscallFilter, setPidFilter, clearAll, hasActiveFilters } = useFiltersStore()

const syscallInput = ref('')
const pidInput = ref('')

function onSyscallInput() {
  setSyscallFilter(syscallInput.value)
}

function onPidInput() {
  const n = parseInt(pidInput.value)
  setPidFilter(isNaN(n) ? null : n)
}

function onClear() {
  syscallInput.value = ''
  pidInput.value = ''
  clearAll()
}
</script>

<template>
  <div class="filter-bar">
    <div class="filter-group">
      <span class="filter-label">Category:</span>
      <FilterChip
        v-for="cat in allCategories"
        :key="cat"
        :label="categoryLabels[cat]"
        :active="state.categories.has(cat)"
        :color="categoryColors[cat]"
        @click="toggleCategory(cat)"
      />
    </div>
    <div class="filter-group">
      <span class="filter-label">Severity:</span>
      <FilterChip
        v-for="sev in allSeverities"
        :key="sev"
        :label="severityLabels[sev].split(' ')[0]"
        :active="state.severities.has(sev)"
        :color="severityColors[sev]"
        @click="toggleSeverity(sev)"
      />
    </div>
    <div class="filter-group">
      <input
        v-model="syscallInput"
        class="filter-input mono"
        placeholder="syscall..."
        @input="onSyscallInput"
      />
      <input
        v-model="pidInput"
        class="filter-input mono"
        placeholder="pid..."
        style="width: 60px"
        @input="onPidInput"
      />
    </div>
    <button v-if="hasActiveFilters" class="clear-btn" @click="onClear">Clear</button>
  </div>
</template>

<style scoped>
.filter-bar {
  display: flex;
  align-items: center;
  gap: var(--space-lg);
  padding: var(--space-sm) var(--space-lg);
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border-primary);
  flex-wrap: wrap;
  min-height: 36px;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: var(--space-xs);
}

.filter-label {
  font-size: var(--font-size-xs);
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-right: var(--space-xs);
}

.filter-input {
  background: var(--bg-input);
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-sm);
  padding: 2px 8px;
  font-size: var(--font-size-xs);
  color: var(--text-primary);
  width: 90px;
  outline: none;
}
.filter-input:focus {
  border-color: var(--accent);
}
.filter-input::placeholder {
  color: var(--text-muted);
}

.clear-btn {
  font-size: var(--font-size-xs);
  color: var(--danger);
  padding: 2px 8px;
  border-radius: var(--radius-sm);
}
.clear-btn:hover {
  background: rgba(248, 81, 73, 0.1);
}
</style>
