<template>
  <view class="page">
    <view class="header">
      <view class="header-left">
        <text class="title">{{ t.map.title }}</text>
        <text class="subtitle">{{ t.map.subtitle }}</text>
      </view>
      <LangToggle />
    </view>
    <map
      class="map"
      :latitude="center.lat"
      :longitude="center.lng"
      :scale="16"
      :markers="markers"
    />
    <!-- 热点列表 -->
    <view class="hotspot-list">
      <view v-for="h in hotspots" :key="h.tag" class="hotspot-item">
        <view class="hotspot-tag">{{ h.tag }}</view>
        <text class="hotspot-cats">🐱 {{ h.cats.join('、') }}</text>
        <text v-if="h.lat && h.lng" class="hotspot-coords">
          📍 {{ h.lat.toFixed(4) }}, {{ h.lng.toFixed(4) }}
        </text>
      </view>
    </view>
    <view v-if="error" class="center">
      <text class="error-text">{{ error }}</text>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { getMapData, type Hotspot } from '@/api/index'
import { useLocale } from '@/composables/useLocale'
import LangToggle from '@/components/LangToggle.vue'

const { t: tRef } = useLocale()
const t = computed(() => tRef.value)

const center = { lat: 29.80002, lng: 121.56351 }
const hotspots = ref<Hotspot[]>([])
const error = ref<string | null>(null)

interface Marker {
  id: number
  latitude: number
  longitude: number
  title: string
  label: { content: string; color: string; fontSize: number; bgColor: string; padding: number; borderRadius: number }
  width: number
  height: number
}

const markers = ref<Marker[]>([])

onMounted(async () => {
  try {
    const data = await getMapData()
    hotspots.value = data
    markers.value = data
      .filter((h) => h.lat !== null && h.lng !== null)
      .map((h, i) => ({
        id: i,
        latitude: h.lat as number,
        longitude: h.lng as number,
        title: h.tag,
        label: {
          content: `${h.tag} (${h.cats.length}只)`,
          color: '#1C1917',
          fontSize: 12,
          bgColor: '#B7C9C0',
          padding: 5,
          borderRadius: 4,
        },
        width: 30,
        height: 30,
      }))
  } catch (e: unknown) {
    error.value = e instanceof Error ? e.message : '加载失败'
  }
})
</script>

<style scoped>
.page { background: #FFF8DC; min-height: 100vh; }
.header { padding: 40rpx 24rpx 24rpx; display: flex; align-items: flex-start; justify-content: space-between; }
.header-left { flex: 1; }
.title { display: block; font-size: 48rpx; font-weight: 700; color: #1C1917; letter-spacing: 1rpx; }
.subtitle { display: block; font-size: 26rpx; color: #D8BFD8; margin-top: 8rpx; font-weight: 500; }
.map { width: 100%; height: 480rpx; }
.hotspot-list { padding: 24rpx 24rpx 120rpx; }
.hotspot-item {
  background: white; border-radius: 16rpx; border: 1rpx solid #F4A460;
  padding: 20rpx 24rpx; margin-bottom: 16rpx;
  display: flex; flex-direction: column; gap: 8rpx; transition: all 0.2s;
}
.hotspot-item:active { background: #FFF8DC; border-color: #B7C9C0; }
.hotspot-tag { font-size: 28rpx; font-weight: 600; color: #1C1917; }
.hotspot-cats { font-size: 26rpx; color: #7A8A80; line-height: 1.5; }
.hotspot-coords { font-size: 22rpx; color: #D8BFD8; }
.center { display: flex; justify-content: center; align-items: center; padding: 40rpx; min-height: 40vh; }
.error-text { color: #ef4444; font-size: 26rpx; font-weight: 600; }
</style>
