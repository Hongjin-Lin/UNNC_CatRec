<template>
  <view class="page">
    <view class="header">
      <view class="header-left" @tap="goBack">←</view>
      <view class="header-title">{{ cat?.Name || '个人资料' }}</view>
      <view class="spacer"></view>
    </view>

    <view class="content">
      <view v-if="loading" class="center">
        <text class="loading-text">加载中喵~</text>
      </view>

      <view v-else-if="!cat" class="center">
        <text class="no-data-text">找不到这只猫咪喵~</text>
      </view>

      <view v-else class="profile-container">
        <!-- Hero -->
        <view class="hero-section">
          <view class="avatar-wrapper">
            <image
              :src="imgUrl(cat.image_url || '')"
              class="avatar"
              mode="aspectFill"
            />
          </view>
          <view class="profile-info">
            <view class="name-star">
              <text class="cat-name">{{ cat.Name }}</text>
              <text class="star-icon">⭐</text>
            </view>
            <text class="cat-id">ID: {{ catId }}</text>
          </view>
        </view>

        <!-- 信息卡片 -->
        <view class="info-card">
          <view class="info-item">
            <text class="info-label">📍 位置</text>
            <text class="info-value">{{ cat.Location || '待发现' }}</text>
          </view>
          <view class="info-item">
            <text class="info-label">🎭 性格</text>
            <view class="traits-container">
              <view v-for="trait in traits(cat.Personality || '')" :key="trait" class="trait-tag">{{ trait }}</view>
              <view v-if="!cat.Personality" class="trait-tag">性格待记录</view>
            </view>
          </view>
          <view class="info-item">
            <text class="info-label">✒️ TNR 状态</text>
            <text class="info-value" :class="{ tnr: cat.TNR_Status }">
              {{ cat.TNR_Status ? '✓ 已进行绝育' : '○ 未进行绝育' }}
            </text>
          </view>
          <view class="info-item">
            <text class="info-label">📝 备注</text>
            <text class="info-value">{{ cat.Notes || '暂无备注' }}</text>
          </view>
        </view>

        <!-- Moments 预览 -->
        <view class="moments-section">
          <text class="section-title">喵友圈</text>
          <view class="moments-grid">
            <view
              v-for="(photoUrl, idx) in momentPhotos"
              :key="idx"
              class="moment-placeholder"
            >
              <image :src="imgUrl(photoUrl)" class="moment-image" mode="aspectFill" />
            </view>
          </view>
        </view>

        <!-- 行动按钮 -->
        <view class="action-buttons">
          <view class="btn btn-primary" @tap="navigateToMoments">查看喵友圈</view>
          <view class="btn btn-secondary" @tap="toggleFollow">
            {{ isFollowed ? '✓ 已关注' : '👁️ 关注' }}
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { getCatById, type CatDetail } from '@/api/index'

const catId = ref('')
const cat = ref<CatDetail | null>(null)
const isFollowed = ref(false)
const loading = ref(true)

const BASE = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

// Backend already filters to images only; take first 4
const momentPhotos = computed(() => (cat.value?.photos ?? []).slice(0, 4))

function traits(personality: string): string[] {
  if (!personality) return []
  return personality.split(',').filter(Boolean).map(t => t.trim()).slice(0, 3)
}

function imgUrl(url: string): string {
  if (!url) return ''
  if (url.startsWith('http')) return url
  return `${BASE}${url}`
}

function goBack() {
  uni.navigateBack()
}

function toggleFollow() {
  isFollowed.value = !isFollowed.value
}

function navigateToMoments() {
  const catName = cat.value?.Name || '猫咪'
  uni.navigateTo({
    url: `/pages/profiles/self-profile/cat-moment?catId=${catId.value}&catName=${encodeURIComponent(catName)}`,
    fail: (err) => console.error('导航失败:', err)
  })
}

onLoad(async (options: any) => {
  const id = options?.catId || options?.id || ''
  if (!id) {
    loading.value = false
    return
  }
  catId.value = id
  try {
    cat.value = await getCatById(id)
  } catch (e) {
    console.error('获取猫咪数据失败:', e)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.page { background-color: #FFF8DC; min-height: 100vh; }
.header {
  display: flex; align-items: center; padding: 12rpx 24rpx;
  background: #FFF8DC; border-bottom: 1rpx solid #F4A460;
  position: sticky; top: 0; z-index: 100;
}
.header-left { font-size: 32rpx; color: #B7C9C0; font-weight: 700; }
.header-title { font-size: 28rpx; font-weight: 700; color: #1C1917; flex: 1; text-align: center; }
.spacer { width: 40rpx; }
.content { padding: 20rpx 0; }
.center { display: flex; justify-content: center; align-items: center; min-height: 60vh; }
.loading-text { font-size: 28rpx; color: #D8BFD8; font-weight: 600; }
.no-data-text { font-size: 28rpx; color: #D8BFD8; font-weight: 600; }
.profile-container { padding: 0 16rpx 40rpx; }
.hero-section {
  display: flex; gap: 20rpx; background: white; padding: 20rpx;
  border-radius: 12rpx; border: 1rpx solid #F4A460; margin-bottom: 16rpx;
}
.avatar-wrapper { flex-shrink: 0; }
.avatar { width: 140rpx; height: 140rpx; border-radius: 12rpx; object-fit: cover; background: linear-gradient(135deg,#FFF8DC,#FEF3E2); }
.profile-info { flex: 1; display: flex; flex-direction: column; justify-content: center; gap: 8rpx; }
.name-star { display: flex; align-items: center; gap: 8rpx; }
.cat-name { font-size: 32rpx; font-weight: 700; color: #1C1917; }
.star-icon { font-size: 28rpx; color: #F0C350; }
.cat-id { font-size: 22rpx; color: #D8BFD8; }
.info-card { background: white; border-radius: 12rpx; border: 1rpx solid #F4A460; padding: 16rpx; margin-bottom: 16rpx; }
.info-item { padding: 12rpx 0; border-bottom: 1rpx solid #FFF8DC; display: flex; flex-direction: column; gap: 8rpx; }
.info-item:last-child { border-bottom: none; }
.info-label { font-size: 22rpx; font-weight: 600; color: #1C1917; }
.info-value { font-size: 22rpx; color: #7A8A80; line-height: 1.5; }
.info-value.tnr { color: #B7C9C0; font-weight: 600; }
.traits-container { display: flex; flex-wrap: wrap; gap: 8rpx; }
.trait-tag { background: #FFF8DC; color: #7A8A80; padding: 6rpx 12rpx; border-radius: 20rpx; font-size: 20rpx; border: 1rpx solid #B7C9C0; }
.moments-section { margin-bottom: 16rpx; }
.section-title { font-size: 26rpx; font-weight: 700; color: #1C1917; margin-bottom: 12rpx; display: block; }
.moments-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 8rpx; margin-bottom: 20rpx; }
.moment-placeholder { aspect-ratio: 1; border-radius: 8rpx; background: linear-gradient(135deg,#FFF8DC,#FEF3E2); display: flex; align-items: center; justify-content: center; border: 1rpx dashed #F4A460; overflow: hidden; }
.moment-image { width: 100%; height: 100%; object-fit: cover; }
.action-buttons { display: flex; flex-direction: column; gap: 12rpx; padding: 0 16rpx; }
.btn { padding: 16rpx; border-radius: 8rpx; text-align: center; font-weight: 600; font-size: 26rpx; border: none; }
.btn-primary { background: linear-gradient(135deg,#B7C9C0,#D8BFD8); color: white; }
.btn-secondary { background: white; color: #B7C9C0; border: 2rpx solid #B7C9C0; }
</style>
