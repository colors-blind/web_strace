import { ref, computed, onMounted, onUnmounted, type Ref } from 'vue'

interface VirtualScrollOptions {
  itemHeight: number
  buffer: number
  containerRef: Ref<HTMLElement | null>
  itemCount: Ref<number>
}

export function useVirtualScroll({ itemHeight, buffer, containerRef, itemCount }: VirtualScrollOptions) {
  const scrollTop = ref(0)
  const containerHeight = ref(0)
  const pinToBottom = ref(true)

  const startIndex = computed(() => {
    const start = Math.floor(scrollTop.value / itemHeight) - buffer
    return Math.max(0, start)
  })

  const endIndex = computed(() => {
    const visibleCount = Math.ceil(containerHeight.value / itemHeight)
    const end = startIndex.value + visibleCount + buffer * 2
    return Math.min(end, itemCount.value)
  })

  const totalHeight = computed(() => itemCount.value * itemHeight)
  const offsetY = computed(() => startIndex.value * itemHeight)

  let rafPending = false

  function onScroll() {
    if (rafPending) return
    rafPending = true
    requestAnimationFrame(() => {
      rafPending = false
      if (!containerRef.value) return
      scrollTop.value = containerRef.value.scrollTop
      containerHeight.value = containerRef.value.clientHeight
      const atBottom = containerRef.value.scrollTop + containerRef.value.clientHeight >= containerRef.value.scrollHeight - itemHeight
      pinToBottom.value = atBottom
    })
  }

  function scrollToBottom() {
    if (containerRef.value) {
      containerRef.value.scrollTop = containerRef.value.scrollHeight
      pinToBottom.value = true
    }
  }

  function autoScroll() {
    if (pinToBottom.value) scrollToBottom()
  }

  onMounted(() => {
    if (containerRef.value) {
      containerHeight.value = containerRef.value.clientHeight
      containerRef.value.addEventListener('scroll', onScroll, { passive: true })
    }
  })

  onUnmounted(() => {
    if (containerRef.value) {
      containerRef.value.removeEventListener('scroll', onScroll)
    }
  })

  return { startIndex, endIndex, totalHeight, offsetY, pinToBottom, scrollToBottom, autoScroll }
}
