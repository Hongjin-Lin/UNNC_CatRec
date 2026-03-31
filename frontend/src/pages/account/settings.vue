<template>
  <view class="container">
    <view class="setting-item" @tap="clearCache">
      <text>{{ t.account.pages.clearCache }}</text>
    </view>
    <view class="setting-item">
      <text>{{ t.account.pages.aboutUs }}</text>
    </view>
  </view>
</template>

<script setup lang="ts">
import { computed, watch } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { useLocale } from '@/composables/useLocale'

const { lang, t: tRef } = useLocale()
const t = computed(() => tRef.value)

function refreshNavTitle() {
  uni.setNavigationBarTitle({ title: t.value.account.pages.settingsTitle })
}

onShow(refreshNavTitle)
watch(lang, refreshNavTitle)

const clearCache = () => {
  try {
    uni.clearStorageSync()
    uni.showToast({ title: t.value.account.pages.cacheCleared, icon: 'none' })
  } catch {
    uni.showToast({ title: t.value.account.pages.cacheCleared, icon: 'none' })
  }
}
</script>

<style scoped>
.container {
  min-height: 100vh;
  background-color: var(--bg-color, #FFF8DC);
  padding: 20rpx;
}
.setting-item {
  background-color: #fff;
  padding: 30rpx;
  border-radius: 16rpx;
  margin-bottom: 20rpx;
  font-size: 30rpx;
  color: #333;
}
</style>