<template>
  <view class="container safe-area-bottom">
    <view class="header glass-card">
      <view class="user-info">
        <image class="avatar" src="/static/logo.png" mode="aspectFill" />
        <view class="info-text">
          <text class="username">{{ username }}</text>
          <text class="subtitle">{{ t.account.subtitle }}</text>
        </view>
        <LangToggle class="lang-toggle" />
      </view>
      
      <view class="stats-row">
        <view class="stat-item">
          <text class="stat-num">12</text>
          <text class="stat-label">{{ t.account.stats.likes }}</text>
        </view>
        <view class="stat-item">
          <text class="stat-num">5</text>
          <text class="stat-label">{{ t.account.stats.comments }}</text>
        </view>
        <view class="stat-item">
          <text class="stat-num">8</text>
          <text class="stat-label">{{ t.account.stats.savedCats }}</text>
        </view>
      </view>
    </view>
    
    <view class="menu-list glass-card">
      <view class="menu-item" hover-class="menu-item-hover" @click="navigateTo('/pages/account/my-cats')">
        <view class="menu-left">
          <text class="menu-icon">🐱</text>
          <text class="menu-text">{{ t.account.menu.myCats }}</text>
        </view>
        <text class="menu-arrow">></text>
      </view>
      <view class="menu-item" hover-class="menu-item-hover" @click="navigateTo('/pages/account/my-moments')">
        <view class="menu-left">
          <text class="menu-icon">🐾</text>
          <text class="menu-text">{{ t.account.menu.myMoments }}</text>
        </view>
        <text class="menu-arrow">></text>
      </view>
      <view class="divider"></view>
      <view class="menu-item" hover-class="menu-item-hover" @click="navigateTo('/pages/account/bookmarks')">
        <view class="menu-left">
          <text class="menu-icon">⭐</text>
          <text class="menu-text">{{ t.account.menu.bookmarks }}</text>
        </view>
        <text class="menu-arrow">></text>
      </view>
      <view class="menu-item" hover-class="menu-item-hover" @click="navigateTo('/pages/account/settings')">
        <view class="menu-left">
          <text class="menu-icon">⚙️</text>
          <text class="menu-text">{{ t.account.menu.settings }}</text>
        </view>
        <text class="menu-arrow">></text>
      </view>
    </view>

    <view class="footer-tips">
      <text class="tips-text">{{ t.account.feedbackPrefix }}</text>
      <!-- #ifdef H5 || WEB -->
      <a class="tips-link" :href="feedbackUrl" target="_blank">{{ t.account.feedbackLink }}</a>
      <!-- #endif -->
      <!-- #ifndef H5 || WEB -->
      <text class="tips-link" @click="openFeedback">{{ t.account.feedbackLink }}</text>
      <!-- #endif -->
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useLocale } from '@/composables/useLocale'
import LangToggle from '@/components/LangToggle.vue'

const { t } = useLocale()
const username = ref('加载中...') // 默认随机名
const feedbackUrl = 'https://my.feishu.cn/share/base/form/shrcnNRGvcBn9bHTTFko0JxygYf'

onMounted(() => {
  // 模拟从本地缓存读取固定的用户名，如果没有则生成并保存
  let savedName = uni.getStorageSync('cat_username')
  if (!savedName) {
    const adjectives = ['爱喵的', '贪吃的', '慵懒的', '神秘的', '调皮的', '高冷的']
    const nouns = ['同学', '两脚兽', '铲屎官', '过客', '黑猫', '橘猫']
    const randomAdj = adjectives[Math.floor(Math.random() * adjectives.length)]
    const randomNoun = nouns[Math.floor(Math.random() * nouns.length)]
    savedName = `${randomAdj}${randomNoun}`
    uni.setStorageSync('cat_username', savedName)
  }
  username.value = savedName
})

const navigateTo = (url: string) => {
  uni.navigateTo({ url })
}

const openFeedback = () => {
  // #ifndef H5 || WEB
  uni.setClipboardData({
    data: feedbackUrl,
    success: () => {
      uni.showToast({ title: '链接已复制，请在浏览器中打开', icon: 'none' })
    }
  })
  // #endif
}
</script>

<style scoped lang="scss">
.container {
  min-height: 100vh;
  padding: 30rpx;
  background-color: var(--bg-color);
  display: flex;
  flex-direction: column;
}

.header {
  margin-bottom: 30rpx;
  padding: 40rpx;
  border-radius: 30rpx;
  
  .user-info {
    display: flex;
    align-items: center;
    position: relative;
    margin-bottom: 40rpx;

    .avatar {
      width: 120rpx;
      height: 120rpx;
      border-radius: 60rpx;
      background-color: #eee;
      margin-right: 30rpx;
    }
    
    .info-text {
      flex: 1;
      display: flex;
      flex-direction: column;

      .username {
        font-size: 40rpx;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 10rpx;
      }
      
      .subtitle {
        font-size: 24rpx;
        color: var(--text-secondary);
      }
    }

    .lang-toggle {
      position: absolute;
      top: 0;
      right: 0;
    }
  }

  .stats-row {
    display: flex;
    justify-content: space-around;
    padding-top: 30rpx;
    border-top: 1rpx solid rgba(0,0,0,0.05);

    .stat-item {
      display: flex;
      flex-direction: column;
      align-items: center;

      .stat-num {
        font-size: 36rpx;
        font-weight: bold;
        color: var(--text-primary);
        margin-bottom: 8rpx;
      }

      .stat-label {
        font-size: 24rpx;
        color: var(--text-secondary);
      }
    }
  }
}

.menu-list {
  border-radius: 30rpx;
  padding: 10rpx 0;
  margin-bottom: 40rpx;

  .menu-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 30rpx 40rpx;
    transition: background-color 0.2s;

    .menu-left {
      display: flex;
      align-items: center;

      .menu-icon {
        font-size: 36rpx;
        margin-right: 20rpx;
      }

      .menu-text {
        font-size: 30rpx;
        color: var(--text-primary);
      }
    }

    .menu-arrow {
      font-size: 30rpx;
      color: #999;
    }
  }

  .menu-item-hover {
    background-color: rgba(0,0,0,0.02);
  }

  .divider {
    height: 1rpx;
    background-color: rgba(0,0,0,0.05);
    margin: 0 40rpx;
  }
}

.footer-tips {
  margin-top: auto;
  text-align: center;
  padding: 40rpx 0;
  display: flex;
  justify-content: center;

  .tips-text {
    font-size: 24rpx;
    color: var(--text-secondary);
    margin-right: 8rpx;
  }

  .tips-link {
    font-size: 24rpx;
    color: #4a90e2;
    text-decoration: underline;
    display: inline-block;
  }
}
</style>