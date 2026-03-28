<template>
  <view class="page">
    <view class="header">
      <text class="title">校园地图</text>
      <text class="subtitle">猫咪出没热点</text>
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
        <text class="hotspot-cats">{{ h.cats.join('、') }}</text>
      </view>
    </view>
    <view v-if="error" class="center">
      <text class="error-text">{{ error }}</text>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getMapData, type Hotspot } from '@/api/index'

const center = { lat: 31.8315, lng: 121.6832 }
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
          bgColor: '#FEF3E2',
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
.page { background: #FFF8F0; min-height: 100vh; }
.header { padding: 40rpx 32rpx 24rpx; }
.title { display: block; font-size: 48rpx; font-weight: 700; color: #1C1917; }
.subtitle { display: block; font-size: 26rpx; color: #78716C; margin-top: 8rpx; }
.map { width: 100%; height: 520rpx; }
.hotspot-list { padding: 24rpx 32rpx 120rpx; }
.hotspot-item {
  background: #fff; border-radius: 20rpx; border: 2rpx solid #FED7AA;
  padding: 24rpx; margin-bottom: 16rpx;
  display: flex; flex-direction: column; gap: 8rpx;
}
.hotspot-tag { font-size: 28rpx; font-weight: 600; color: #F97316; }
.hotspot-cats { font-size: 26rpx; color: #78716C; }
.center { display: flex; justify-content: center; padding: 40rpx; }
.error-text { color: #ef4444; font-size: 26rpx; }
</style>
