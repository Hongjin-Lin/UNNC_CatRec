<template>
  <view class="container">
    <view class="empty-state">
      <text class="placeholder">{{ t.account.pages.myCatsEmpty }}</text>
      <button class="add-btn" @click="goToAddCat">{{ t.account.pages.myCatsAdd }}</button>
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
  uni.setNavigationBarTitle({ title: t.value.account.pages.myCatsTitle })
}

onShow(refreshNavTitle)
watch(lang, refreshNavTitle)

const goToAddCat = () => {
  uni.navigateTo({
    url: '/pages/add/index'
  })
}
</script>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: var(--bg-color, #FFF8DC);
}
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.placeholder {
  font-size: 32rpx;
  color: #666;
  margin-bottom: 40rpx;
}
.add-btn {
  background-color: #F0C350;
  color: #fff;
  border-radius: 40rpx;
  padding: 0 60rpx;
  font-size: 32rpx;
  line-height: 80rpx;
}
</style>