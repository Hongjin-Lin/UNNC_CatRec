<template>
  <view class="page">
    <view class="header">
      <text class="title">猫咪识别</text>
      <text class="subtitle">上传一张照片，AI 帮你认出是哪只猫~</text>
    </view>

    <!-- 上传区 -->
    <view v-if="!preview" class="upload-box" @tap="chooseImage">
      <text class="upload-icon">📷</text>
      <text class="upload-hint">点击选择猫咪照片</text>
    </view>

    <!-- 预览 -->
    <view v-else class="preview-wrap">
      <image :src="preview" class="preview-img" mode="aspectFill" />
      <view class="reset-btn" @tap="reset">↺</view>
    </view>

    <!-- 识别按钮 -->
    <button v-if="preview && !result" class="btn-primary" :disabled="loading" @tap="identify">
      {{ loading ? '识别中…' : '🔍 开始识别' }}
    </button>

    <!-- 错误 -->
    <text v-if="error" class="error-text">{{ error }}</text>

    <!-- 结果 -->
    <view v-if="result">
      <!-- 未匹配 -->
      <view v-if="result.no_match" class="no-match-card">
        <text class="no-match-emoji">🤔</text>
        <text class="no-match-title">没找到匹配的猫咪</text>
        <text class="no-match-sub">要不要把这只新猫加入名册？</text>
        <navigator url="/pages/add/index" class="btn-link">去添加</navigator>
      </view>

      <!-- 匹配结果列表 -->
      <view v-else>
        <text class="result-label">可能是以下猫咪：</text>
        <view v-for="(cat, index) in result.matches" :key="index" class="result-card" @tap="navigateToCat(cat)">
          <view class="match-header">
            <text class="match-rank">#{{ index + 1 }}</text>
            <text class="match-emoji">😺</text>
            <view class="match-info">
              <text class="match-name">{{ cat.name }}</text>
              <text class="match-confidence">置信度 {{ (cat.confidence * 100).toFixed(1) }}%</text>
            </view>
            <text v-if="cat.tnr_status" class="tnr-badge">✅ TNR</text>
          </view>
          <view v-if="cat.location" class="match-location">
            <text>📍 {{ cat.location }}</text>
          </view>
          <view v-if="cat.personality?.length" class="tags">
            <text v-for="t in cat.personality" :key="t" class="tag">{{ t }}</text>
          </view>
          <text v-if="cat.notes" class="match-notes">{{ cat.notes }}</text>
        </view>

        <!-- 都不是 -->
        <view class="not-found-row">
          <text class="not-found-text">以上都不是？</text>
          <navigator url="/pages/add/index" class="btn-link-small">去添加这只猫</navigator>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { identifyCat } from '@/api/index'

interface CatMatch {
  id?: string
  name: string
  confidence: number
  location?: string
  personality?: string[]
  tnr_status?: boolean
  notes?: string
}

interface IdentifyResult {
  no_match: boolean
  matches: CatMatch[]
}

const preview = ref<string | null>(null)
const filePath = ref<string | null>(null)
const result = ref<IdentifyResult | null>(null)
const loading = ref(false)
const error = ref<string | null>(null)

function chooseImage() {
  uni.chooseImage({
    count: 1,
    sizeType: ['compressed'],
    sourceType: ['album', 'camera'],
    success: (res) => {
      filePath.value = res.tempFilePaths[0]
      preview.value = res.tempFilePaths[0]
      result.value = null
      error.value = null
    },
  })
}

function reset() {
  preview.value = null
  filePath.value = null
  result.value = null
  error.value = null
}

function navigateToCat(cat: CatMatch) {
  if (!cat.id) {
    console.error('Error: cat ID is missing, cannot navigate to profile.')
    return
  }
  const navUrl = `/pages/profiles/self-profile?catId=${cat.id}&catName=${encodeURIComponent(cat.name)}`
  uni.navigateTo({
    url: navUrl,
    fail: (err) => {
      console.error('导航失败:', err)
    }
  })
}

async function identify() {
  if (!filePath.value) return
  loading.value = true
  error.value = null
  try {
    result.value = await identifyCat(filePath.value) as IdentifyResult
  } catch (e: unknown) {
    error.value = e instanceof Error ? e.message : '识别失败，请重试'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.page { padding: 40rpx 32rpx 120rpx; background: #FFF8F0; min-height: 100vh; }
.header { margin-bottom: 40rpx; }
.title { display: block; font-size: 48rpx; font-weight: 700; color: #1C1917; }
.subtitle { display: block; font-size: 26rpx; color: #78716C; margin-top: 8rpx; }
.upload-box {
  border: 4rpx dashed #FED7AA; border-radius: 32rpx;
  background: #FEF3E2; padding: 80rpx 0;
  display: flex; flex-direction: column; align-items: center; gap: 16rpx;
}
.upload-icon { font-size: 80rpx; }
.upload-hint { font-size: 28rpx; color: #78716C; }
.preview-wrap { position: relative; width: 100%; aspect-ratio: 1; border-radius: 32rpx; overflow: hidden; }
.preview-img { width: 100%; height: 100%; }
.reset-btn {
  position: absolute; top: 20rpx; right: 20rpx;
  background: rgba(255,255,255,0.85); border-radius: 50%;
  width: 64rpx; height: 64rpx; display: flex; align-items: center; justify-content: center;
  font-size: 36rpx; color: #1C1917;
}
.btn-primary {
  margin-top: 32rpx; width: 100%; background: #F97316; color: #fff;
  border-radius: 24rpx; font-size: 32rpx; font-weight: 600; padding: 24rpx 0; border: none;
}
.btn-primary[disabled] { opacity: 0.6; }
.error-text { display: block; margin-top: 24rpx; color: #ef4444; font-size: 26rpx; text-align: center; }
.no-match-card {
  margin-top: 40rpx; background: #fff; border-radius: 32rpx;
  border: 2rpx solid #FED7AA; padding: 48rpx 40rpx;
  display: flex; flex-direction: column; align-items: center; gap: 16rpx;
}
.no-match-emoji { font-size: 80rpx; }
.no-match-title { font-size: 36rpx; font-weight: 600; color: #1C1917; }
.no-match-sub { font-size: 26rpx; color: #78716C; }
.result-label { display: block; margin-top: 40rpx; margin-bottom: 20rpx; font-size: 28rpx; font-weight: 600; color: #78716C; }
.result-card {
  background: #fff; border-radius: 28rpx; border: 2rpx solid #FED7AA;
  padding: 32rpx; margin-bottom: 20rpx;
  transition: all 0.2s ease;
}
.result-card:active {
  transform: scale(0.98);
  background: #FEF3E2;
}
.match-header { display: flex; align-items: center; gap: 16rpx; margin-bottom: 16rpx; }
.match-rank { font-size: 28rpx; font-weight: 700; color: #F97316; min-width: 40rpx; }
.match-emoji { font-size: 48rpx; }
.match-info { flex: 1; }
.match-name { display: block; font-size: 36rpx; font-weight: 700; color: #1C1917; }
.match-confidence { display: block; font-size: 24rpx; color: #78716C; }
.tnr-badge { font-size: 22rpx; color: #22c55e; }
.match-location { font-size: 26rpx; color: #78716C; margin-bottom: 16rpx; }
.tags { display: flex; flex-wrap: wrap; gap: 12rpx; margin-bottom: 16rpx; }
.tag { background: #FDE8C8; color: #F97316; padding: 8rpx 20rpx; border-radius: 50rpx; font-size: 24rpx; font-weight: 500; }
.match-notes { font-size: 26rpx; color: #78716C; border-top: 2rpx solid #FEF3E2; padding-top: 16rpx; }
.not-found-row {
  margin-top: 8rpx; padding: 32rpx; background: #fff; border-radius: 28rpx;
  border: 2rpx dashed #FED7AA;
  display: flex; align-items: center; justify-content: space-between;
}
.not-found-text { font-size: 28rpx; color: #78716C; }
.btn-link {
  background: #F97316; color: #fff;
  padding: 16rpx 48rpx; border-radius: 50rpx; font-size: 28rpx; display: block; text-align: center;
}
.btn-link-small {
  background: #F97316; color: #fff;
  padding: 12rpx 32rpx; border-radius: 50rpx; font-size: 26rpx;
}
</style>
