<template>
  <view class="page">
    <view class="header">
      <text class="title">猫咪名册</text>
      <text class="subtitle">校园里的每一只小可爱</text>
    </view>

    <view v-if="loading" class="center">
      <text class="loading-text">加载中…</text>
    </view>
    <view v-else-if="error" class="center">
      <text class="error-text">{{ error }}</text>
    </view>
    <view v-else-if="cats.length === 0" class="center">
      <text class="empty-text">还没有猫咪档案，快去添加吧~</text>
    </view>
    <view v-else class="grid">
      <view v-for="cat in cats" :key="cat.id" class="card">
        <view class="card-img-wrap">
          <image
            v-if="cat.image_url"
            :src="imgUrl(cat.image_url)"
            class="card-img"
            mode="aspectFill"
          />
          <view v-else class="card-img-placeholder">🐱</view>
        </view>
        <view class="card-body">
          <view class="card-name-row">
            <text class="card-name">{{ cat.Name }}</text>
            <text v-if="cat.TNR_Status" class="tnr-icon">✅</text>
          </view>
          <view class="card-location">
            <text>📍 {{ cat.Location || '未知' }}</text>
          </view>
          <view class="tags">
            <text
              v-for="t in traits(cat.Personality)"
              :key="t"
              class="tag"
            >{{ t }}</text>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getCats, type CatProfile } from '@/api/index'

const BASE = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

const cats = ref<CatProfile[]>([])
const loading = ref(true)
const error = ref<string | null>(null)

function traits(personality: string): string[] {
  return personality ? personality.split(',').filter(Boolean).slice(0, 3) : []
}

function imgUrl(url: string): string {
  if (url.startsWith('http')) return url
  return `${BASE}${url}`
}

onMounted(async () => {
  try {
    cats.value = await getCats()
  } catch (e: unknown) {
    error.value = e instanceof Error ? e.message : '加载失败'
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.page { padding: 40rpx 32rpx 120rpx; background: #FFF8F0; min-height: 100vh; }
.header { margin-bottom: 40rpx; }
.title { display: block; font-size: 48rpx; font-weight: 700; color: #1C1917; }
.subtitle { display: block; font-size: 26rpx; color: #78716C; margin-top: 8rpx; }
.center { display: flex; justify-content: center; padding: 80rpx 0; }
.loading-text, .error-text, .empty-text { font-size: 28rpx; color: #78716C; }
.error-text { color: #ef4444; }
.grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24rpx; }
.card { background: #fff; border-radius: 24rpx; border: 2rpx solid #FED7AA; overflow: hidden; }
.card-img-wrap { width: 100%; aspect-ratio: 1; background: #FEF3E2; }
.card-img { width: 100%; height: 100%; }
.card-img-placeholder { width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; font-size: 64rpx; }
.card-body { padding: 16rpx; }
.card-name-row { display: flex; align-items: center; justify-content: space-between; margin-bottom: 8rpx; }
.card-name { font-size: 28rpx; font-weight: 600; color: #1C1917; }
.tnr-icon { font-size: 24rpx; }
.card-location { font-size: 22rpx; color: #78716C; margin-bottom: 12rpx; }
.tags { display: flex; flex-wrap: wrap; gap: 8rpx; }
.tag { background: #FDE8C8; color: #F97316; padding: 4rpx 16rpx; border-radius: 50rpx; font-size: 20rpx; font-weight: 500; }
</style>
