<template>
  <view class="container">
    <text class="placeholder">{{ t.account.pages.myMomentsPlaceholder }}</text>
  </view>
</template>

<script setup lang="ts">
import { computed, watch } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { useLocale } from '@/composables/useLocale'

const { lang, t: tRef } = useLocale()
const t = computed(() => tRef.value)

function refreshNavTitle() {
  uni.setNavigationBarTitle({ title: t.value.account.pages.myMomentsTitle })
}

onShow(refreshNavTitle)
watch(lang, refreshNavTitle)
</script>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: var(--bg-color, #FFF8DC);
}
.placeholder {
  font-size: 32rpx;
  color: #666;
}
</style>