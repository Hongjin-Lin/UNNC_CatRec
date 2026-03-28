<template>
  <view class="page">
    <view class="header">
      <text class="title">🔍 猫咪识别</text>
      <text class="subtitle">上传照片，AI 帮你认出是哪只小家伙~</text>
    </view>

    <!-- 上传区 -->
    <view v-if="!preview" class="upload-box" @tap="chooseImage">
      <text class="upload-icon">📷</text>
      <text class="upload-hint">点击选择猫咪照片</text>
      <text class="upload-tip">支持拍照或从相册选择</text>
    </view>

    <!-- 预览 -->
    <view v-else class="preview-wrap">
      <image :src="preview" class="preview-img" mode="aspectFill" />
      <view class="reset-btn" @tap="reset">↺</view>
    </view>

    <!-- 识别按钮 -->
    <button v-if="preview && !result" class="btn-primary" :disabled="loading" @tap="identify">
      {{ loading ? '识别中…' : '✨ 开始识别' }}
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
        <text class="tip-text">这只猫可能很特别呢！想帮它建档吗？</text>
        <navigator url="/pages/add/index" class="btn-link">去添加这只猫</navigator>
      </view>
      <!-- 匹配成功 -->
      <view v-else class="match">
        <view class="match-header">
          <text class="match-emoji">😺</text>
          <view class="match-info">
            <text class="match-name">{{ result.match!.name }}</text>
            <text class="match-confidence">置信度 {{ (result.match!.confidence * 100).toFixed(1) }}%</text>
          </view>
        </view>
        <view v-if="result.match!.tnr_status" class="tnr-status">
          <text class="tnr-icon">✅</text>
          <text class="tnr-text">已进行TNR</text>
        </view>
        <view class="match-location">
          <text class="loc-icon">📍</text>
          <text>{{ result.match!.location || '未知' }}</text>
        </view>
        <view v-if="result.match!.personality?.length" class="tags">
          <text v-for="t in result.match!.personality" :key="t" class="tag">{{ t }}</text>
        </view>
        <text v-if="result.match!.notes" class="match-notes">{{ result.match!.notes }}</text>
        <navigator 
          :url="`/pages/profiles/self-profile?id=${result.match!.name}`"
          class="btn-detail"
        >
          查看详情 →
        </navigator>
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
.page {
  padding: 40rpx 24rpx 120rpx;
  background: #FFF8DC;
  min-height: 100vh;
}

.header {
  margin-bottom: 40rpx;
}

.title {
  display: block;
  font-size: 48rpx;
  font-weight: 700;
  color: #1C1917;
  letter-spacing: 1rpx;
}

.subtitle {
  display: block;
  font-size: 26rpx;
  color: #D8BFD8;
  margin-top: 8rpx;
  font-weight: 500;
}

.upload-box {
  border: 3rpx dashed #B7C9C0;
  border-radius: 20rpx;
  background: linear-gradient(135deg, #FEF3E2 0%, #FFF8DC 100%);
  padding: 80rpx 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12rpx;
  margin-bottom: 40rpx;
}

.upload-icon {
  font-size: 80rpx;
}

.upload-hint {
  font-size: 28rpx;
  color: #1C1917;
  font-weight: 600;
}

.upload-tip {
  font-size: 22rpx;
  color: #D8BFD8;
}

.preview-wrap {
  position: relative;
  width: 100%;
  aspect-ratio: 1;
  border-radius: 20rpx;
  overflow: hidden;
  margin-bottom: 40rpx;
}

.preview-img {
  width: 100%;
  height: 100%;
  display: block;
}

.reset-btn {
  position: absolute;
  top: 20rpx;
  right: 20rpx;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 50%;
  width: 64rpx;
  height: 64rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 36rpx;
  color: #1C1917;
  font-weight: 600;
}

.btn-primary {
  width: 100%;
  background: linear-gradient(135deg, #B7C9C0 0%, #D8BFD8 100%);
  color: white;
  border-radius: 20rpx;
  font-size: 32rpx;
  font-weight: 600;
  padding: 24rpx 0;
  border: none;
  margin-bottom: 40rpx;
}

.btn-primary:active {
  opacity: 0.9;
}

.btn-primary[disabled] {
  opacity: 0.6;
}

.error-text {
  display: block;
  margin-bottom: 40rpx;
  color: #ef4444;
  font-size: 26rpx;
  text-align: center;
  font-weight: 600;
}

.result-card {
  background: white;
  border-radius: 20rpx;
  border: 1rpx solid #F4A460;
  padding: 40rpx;
  margin-bottom: 32rpx;
}

.no-match {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12rpx;
  text-align: center;
}

.no-match-emoji {
  font-size: 80rpx;
}

.no-match-title {
  font-size: 36rpx;
  font-weight: 600;
  color: #1C1917;
}

.no-match-sub {
  font-size: 24rpx;
  color: #D8BFD8;
}

.tip-text {
  font-size: 26rpx;
  color: #7A8A80;
  margin-top: 8rpx;
}

.btn-link {
  display: inline-block;
  margin-top: 16rpx;
  background: #B7C9C0;
  color: white;
  padding: 12rpx 32rpx;
  border-radius: 20rpx;
  font-size: 28rpx;
  font-weight: 600;
}

.btn-link:active {
  opacity: 0.9;
}

.match-header {
  display: flex;
  align-items: center;
  gap: 16rpx;
  margin-bottom: 20rpx;
}

.match-emoji {
  font-size: 56rpx;
}

.match-info {
  display: flex;
  flex-direction: column;
  gap: 4rpx;
}

.match-name {
  display: block;
  font-size: 40rpx;
  font-weight: 700;
  color: #1C1917;
}

.match-confidence {
  display: block;
  font-size: 24rpx;
  color: #D8BFD8;
}

.tnr-status {
  display: flex;
  align-items: center;
  gap: 8rpx;
  background: #B7C9C0;
  color: white;
  padding: 12rpx 20rpx;
  border-radius: 20rpx;
  margin-bottom: 16rpx;
  width: fit-content;
}

.tnr-icon {
  font-size: 24rpx;
}

.tnr-text {
  font-size: 24rpx;
  font-weight: 600;
}

.match-location {
  display: flex;
  align-items: center;
  gap: 8rpx;
  font-size: 28rpx;
  color: #7A8A80;
  margin-bottom: 20rpx;
}

.loc-icon {
  font-size: 28rpx;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 12rpx;
  margin-bottom: 20rpx;
}

.tag {
  background: #F4A460;
  color: white;
  padding: 8rpx 16rpx;
  border-radius: 8rpx;
  font-size: 24rpx;
  font-weight: 500;
}

.match-notes {
  display: block;
  font-size: 26rpx;
  color: #7A8A80;
  border-top: 1rpx solid #FFF8DC;
  padding-top: 20rpx;
  margin-bottom: 20rpx;
  line-height: 1.6;
}

.btn-detail {
  display: block;
  text-align: center;
  background: #F0C350;
  color: white;
  padding: 12rpx 24rpx;
  border-radius: 8rpx;
  font-size: 26rpx;
  font-weight: 600;
}

.btn-detail:active {
  opacity: 0.9;
}
</style>
