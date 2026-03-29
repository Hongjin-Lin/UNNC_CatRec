<template>
  <view class="lang-toggle" @tap="toggleLang">
    <text class="lang-text">{{ lang === 'zh' ? 'A' : '文' }}</text>
    <text class="lang-sep">/</text>
    <text class="lang-text" :class="{ active: true }">{{ lang === 'zh' ? '文' : 'A' }}</text>
  </view>
</template>

<script setup lang="ts">
import { useLocale } from '@/composables/useLocale'
const { lang, toggleLang } = useLocale()
</script>

<style scoped>
.lang-toggle {
  display: flex;
  align-items: center;
  gap: 2rpx;
  background: rgba(255, 255, 255, 0.7);
  border: 2rpx solid #FED7AA;
  border-radius: 32rpx;
  padding: 8rpx 20rpx;
  cursor: pointer;
}
.lang-text {
  font-size: 26rpx;
  color: #B7C9C0;
  font-weight: 600;
  line-height: 1;
}
.lang-text.active {
  color: #F97316;
}
.lang-sep {
  font-size: 22rpx;
  color: #D8BFD8;
  line-height: 1;
}
</style>
