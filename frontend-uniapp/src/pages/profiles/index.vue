<template>
  <view class="page">
    <view class="header">
      <view class="header-left">
        <text class="title">{{ t.profiles.title }}</text>
        <text class="subtitle">{{ t.profiles.subtitle }}</text>
      </view>
      <view class="header-right">
        <LangToggle />
        <input
          class="search-input"
          v-model="searchQuery"
          :placeholder="t.profiles.searchPlaceholder"
          placeholder-class="search-placeholder"
        />
      </view>
    </view>

    <view v-if="loading" class="center">
      <text class="loading-text">{{ t.profiles.loading }}</text>
    </view>
    <view v-else-if="error" class="center">
      <text class="error-text">{{ error }}</text>
    </view>
    <view v-else-if="cats.length === 0" class="center">
      <text class="empty-text">{{ t.profiles.empty }}</text>
    </view>
    <view v-else-if="filteredCats.length === 0" class="center">
      <text class="empty-text">{{ t.profiles.notFound(searchQuery) }}</text>
    </view>
    <view v-else class="grid">
      <view
        v-for="cat in filteredCats"
        :key="cat.id"
        class="card-link"
        @tap="navigateToCat(cat)"
      >
        <view class="card">
          <view class="card-img-wrap">
            <image
              v-if="cat.image_url"
              :src="imgUrl(cat.image_url)"
              class="card-img"
              mode="aspectFill"
            />
            <view v-else class="card-img-placeholder">🐱</view>
            <view v-if="cat.TNR_Status" class="tnr-label">TNR</view>
          </view>
          <view class="card-body">
            <view class="card-name-row">
              <text class="card-name">{{ cat.Name }}</text>
            </view>
            <view class="card-location">
              <text>📍 {{ cat.Location || t.profiles.unknown }}</text>
            </view>
            <view class="tags">
              <text
                v-for="trait in traits(cat.Personality)"
                :key="trait"
                class="tag"
              >{{ trait }}</text>
            </view>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { getCats, type CatProfile } from '@/api/index'
import { useLocale } from '@/composables/useLocale'
import LangToggle from '@/components/LangToggle.vue'

const { t: tRef } = useLocale()
const t = computed(() => tRef.value)

const BASE = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

const cats = ref<CatProfile[]>([])
const loading = ref(true)
const error = ref<string | null>(null)
const searchQuery = ref('')

const filteredCats = computed(() => {
  if (!searchQuery.value.trim()) return cats.value
  const query = searchQuery.value.trim().toLowerCase()
  return cats.value.filter(cat =>
    cat.Name && cat.Name.toLowerCase().includes(query)
  )
})

function traits(personality: string): string[] {
  return personality ? personality.split(',').filter(Boolean).slice(0, 3) : []
}

function imgUrl(url: string): string {
  if (!url) return ''
  if (url.startsWith('http')) return url
  return `${BASE}${url}`
}

function navigateToCat(cat: CatProfile) {
  const navUrl = `/pages/profiles/self-profile?catId=${cat.id}&catName=${encodeURIComponent(cat.Name)}`
  uni.navigateTo({
    url: navUrl,
    fail: (err) => {
      console.error('导航失败:', err)
    }
  })
}

import { onMounted } from 'vue'
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
.page {
  padding: 40rpx 24rpx 120rpx;
  background: #FFF8DC;
  min-height: 100vh;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 40rpx;
}
.header-left { flex: 1; }
.header-right {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 12rpx;
  width: 240rpx;
}
.search-input {
  background: white;
  border: 2rpx solid #FED7AA;
  border-radius: 30rpx;
  padding: 10rpx 24rpx;
  font-size: 26rpx;
  color: #1C1917;
  text-align: right;
  width: 100%;
}
.search-input:focus { border-color: #F97316; }
.search-placeholder { color: #D8BFD8; }
.title { display: block; font-size: 48rpx; font-weight: 700; color: #1C1917; letter-spacing: 1rpx; }
.subtitle { display: block; font-size: 26rpx; color: #D8BFD8; margin-top: 8rpx; font-weight: 500; }
.center { display: flex; justify-content: center; align-items: center; min-height: 60vh; flex-direction: column; }
.loading-text { font-size: 28rpx; color: #D8BFD8; font-weight: 600; }
.error-text { font-size: 28rpx; color: #ef4444; font-weight: 600; }
.empty-text { font-size: 28rpx; color: #D8BFD8; font-weight: 600; }
.grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20rpx; }
.card-link { text-decoration: none; }
.card { background: white; border-radius: 16rpx; border: 1rpx solid #F4A460; overflow: hidden; transition: all 0.3s ease; }
.card:active { transform: translateY(-4rpx); box-shadow: 0 8rpx 20rpx rgba(240,195,80,0.15); }
.card-img-wrap { width: 100%; aspect-ratio: 1; background: linear-gradient(135deg,#FFF8DC 0%,#FEF3E2 100%); position: relative; overflow: hidden; }
.card-img { width: 100%; height: 100%; object-fit: cover; }
.card-img-placeholder { width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; font-size: 64rpx; }
.tnr-label { position: absolute; top: 12rpx; right: 12rpx; background: #B7C9C0; color: white; padding: 6rpx 12rpx; border-radius: 8rpx; font-size: 20rpx; font-weight: 600; }
.card-body { padding: 16rpx; }
.card-name-row { display: flex; align-items: center; justify-content: space-between; margin-bottom: 8rpx; }
.card-name { font-size: 28rpx; font-weight: 600; color: #1C1917; }
.card-location { font-size: 22rpx; color: #7A8A80; margin-bottom: 12rpx; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.tags { display: flex; flex-wrap: wrap; gap: 8rpx; }
.tag { background: #F4A460; color: white; padding: 4rpx 12rpx; border-radius: 12rpx; font-size: 20rpx; font-weight: 500; }
</style>
