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
    <view v-if="result" class="result-card">
      <!-- 未匹配 -->
      <view v-if="result.no_match" class="no-match">
        <text class="no-match-emoji">🤔</text>
        <text class="no-match-title">没找到匹配的猫咪</text>
        <text class="no-match-sub">
          置信度 {{ result.confidence !== undefined ? (result.confidence * 100).toFixed(1) : '--' }}%
        </text>
        <navigator url="/pages/add/index" class="btn-link">去添加这只猫</navigator>
      </view>
      <!-- 匹配成功 -->
      <view v-else class="match">
        <view class="match-header">
          <text class="match-emoji">😺</text>
          <view>
            <text class="match-name">{{ result.match!.name }}</text>
            <text class="match-confidence">置信度 {{ (result.match!.confidence * 100).toFixed(1) }}%</text>
          </view>
          <text v-if="result.match!.tnr_status" class="tnr-badge">✅ TNR</text>
        </view>
        <view class="match-location">
          <text>📍 {{ result.match!.location || '未知' }}</text>
        </view>
        <view v-if="result.match!.personality?.length" class="tags">
          <text v-for="t in result.match!.personality" :key="t" class="tag">{{ t }}</text>
        </view>
        <text v-if="result.match!.notes" class="match-notes">{{ result.match!.notes }}</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { identifyCat, type IdentifyResult } from '@/api/index'

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

async function identify() {
  if (!filePath.value) return
  loading.value = true
  error.value = null
  try {
    result.value = await identifyCat(filePath.value)
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
  border-radius: 24rpx; font-size: 32rpx; font-weight: 600; padding: 24rpx 0;
  border: none;
}
.btn-primary[disabled] { opacity: 0.6; }
.error-text { display: block; margin-top: 24rpx; color: #ef4444; font-size: 26rpx; text-align: center; }
.result-card {
  margin-top: 40rpx; background: #fff; border-radius: 32rpx;
  border: 2rpx solid #FED7AA; padding: 40rpx;
}
.no-match { display: flex; flex-direction: column; align-items: center; gap: 12rpx; }
.no-match-emoji { font-size: 80rpx; }
.no-match-title { font-size: 36rpx; font-weight: 600; color: #1C1917; }
.no-match-sub { font-size: 24rpx; color: #78716C; }
.btn-link {
  margin-top: 16rpx; background: #F97316; color: #fff;
  padding: 16rpx 48rpx; border-radius: 50rpx; font-size: 28rpx;
}
.match-header { display: flex; align-items: center; gap: 16rpx; margin-bottom: 20rpx; }
.match-emoji { font-size: 56rpx; }
.match-name { display: block; font-size: 40rpx; font-weight: 700; color: #1C1917; }
.match-confidence { display: block; font-size: 24rpx; color: #78716C; }
.tnr-badge { margin-left: auto; font-size: 24rpx; color: #22c55e; }
.match-location { font-size: 28rpx; color: #78716C; margin-bottom: 20rpx; }
.tags { display: flex; flex-wrap: wrap; gap: 12rpx; margin-bottom: 20rpx; }
.tag {
  background: #FDE8C8; color: #F97316;
  padding: 8rpx 20rpx; border-radius: 50rpx; font-size: 24rpx; font-weight: 500;
}
.match-notes { font-size: 26rpx; color: #78716C; border-top: 2rpx solid #FEF3E2; padding-top: 20rpx; }
</style>
