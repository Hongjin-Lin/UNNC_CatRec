<template>
  <view class="page">
    <!-- 顶部粘性头部 -->
    <view class="header">
      <view class="header-left" @tap="goBack">←</view>
      <view class="header-title">个人资料</view>
      <view class="spacer"></view>
    </view>

    <!-- 内容区 -->
    <view class="content">
      <!-- 有catId时显示内容 -->
      <view v-if="catId" class="profile-container">
        <!-- Hero 部分 -->
        <view class="hero-section">
          <view class="avatar-wrapper">
            <image 
              :src="imgUrl(cat?.image_url || '/static/default-cat.png')" 
              class="avatar"
              mode="aspectFill"
            />
          </view>
          <view class="profile-info">
            <view class="name-star">
              <text class="cat-name">{{ cat?.Name || '小可爱' }}</text>
              <text class="star-icon">⭐</text>
            </view>
            <text class="cat-id">ID: {{ catId }}</text>
          </view>
        </view>

        <!-- 信息卡片 -->
        <view class="info-card">
          <!-- 位置 -->
          <view class="info-item">
            <text class="info-label">📍 位置</text>
            <text class="info-value">{{ cat?.Location || '待发现' }}</text>
          </view>

          <!-- 性格 -->
          <view class="info-item">
            <text class="info-label">🎭 性格</text>
            <view class="traits-container">
              <view v-for="trait in traits(cat?.Personality || '')" :key="trait" class="trait-tag">
                {{ trait }}
              </view>
              <view v-if="!cat?.Personality" class="trait-tag placeholder">性格待记录</view>
            </view>
          </view>

          <!-- TNR 状态 -->
          <view class="info-item">
            <text class="info-label">✒️ TNR 状态</text>
            <text class="info-value" :class="{ tnr: cat?.TNR_Status }">
              {{ cat?.TNR_Status ? '✓ 已进行绝育' : '○ 未进行绝育' }}
            </text>
          </view>

          <!-- 备注 -->
          <view class="info-item">
            <text class="info-label">📝 备注</text>
            <text class="info-value">{{ cat?.Notes || '暂无备注' }}</text>
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
              <image 
                :src="imgUrl(photoUrl)" 
                class="moment-image"
                mode="aspectFill"
              />
            </view>
          </view>
        </view>

        <!-- 行动按钮 -->
        <view class="action-buttons">
          <view class="btn btn-primary" @tap="navigateToMoments">
            查看喵友圈
          </view>
          <view class="btn btn-secondary" @tap="toggleFollow">
            {{ isFollowed ? '✓ 已关注' : '👁️ 关注' }}
          </view>
        </view>
      </view>

      <!-- 无catId显示 -->
      <view v-else class="no-data">
        <text class="no-data-text">未指定猫咪ID</text>
        <!-- 调试信息 -->
        <view class="debug-info">
          <text class="debug-label">调试信息：</text>
          <text class="debug-item">当前URL: {{ currentUrl }}</text>
          <text class="debug-item">提取的catId: {{ debugCatId }}</text>
          <text class="debug-item">提取的catName: {{ debugCatName }}</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { getCats, type CatProfile } from '@/api/index'

interface Cat {
  id: string
  Name: string
  Location: string
  Personality: string
  TNR_Status: boolean
  Notes?: string
  image_url?: string
}

const catId = ref<string>('')
const cat = ref<Cat | null>(null)
const isFollowed = ref(false)
const loading = ref(true)
const momentPhotos = ref<string[]>([])  // 改为ref，动态加载

// 调试信息
const currentUrl = ref<string>('')
const debugCatId = ref<string>('')
const debugCatName = ref<string>('')

const BASE = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

function traits(personality: string): string[] {
  if (!personality) return []
  return personality
    .split(',')
    .filter(Boolean)
    .map(t => t.trim())
    .slice(0, 3)
}

function imgUrl(url: string): string {
  if (!url) return ''
    try { url = encodeURI(decodeURI(url)) } catch(e) {}
}

function goBack() {
  uni.navigateBack()
}

function toggleFollow() {
  isFollowed.value = !isFollowed.value
}

// 检查图片是否存在
function checkImageExists(url: string): Promise<boolean> {
  return new Promise((resolve) => {
      // 兼容微信小程序，不能使用 new Image() DOM API
      uni.getImageInfo({
        src: url,
        success: () => resolve(true),
        fail: () => resolve(false)
      })
  })
}

// 动态加载猫咪预览图片（最多4张）
async function loadMomentPhotos(catName: string) {
  if (!catName) {
    momentPhotos.value = []
    return
  }

  const validPhotos: string[] = []
  
  // 尝试加载最多10张，但只取前4张有效的
  for (let i = 1; i <= 10 && validPhotos.length < 4; i++) {
    const photoUrl = `/static/cats/${catName}/${catName}_${i}.jpeg`
    const fullUrl = imgUrl(photoUrl)
    
    const exists = await checkImageExists(fullUrl)
    if (exists) {
      validPhotos.push(photoUrl)
      console.log(`✓ 预览图[${i}] 加载成功: ${catName}_${i}.jpeg`)
    } else {
      console.log(`✗ 预览图[${i}] 不存在: ${catName}_${i}.jpeg`)
    }
  }
  
  momentPhotos.value = validPhotos
  console.log(`猫咪${catName}的预览图片加载完成，共${validPhotos.length}张`)
}

function navigateToMoments() {
  const catName = cat.value?.Name || '猫咪'
  const navUrl = `/pages/profiles/self-profile/cat-moment?catId=${catId.value}&catName=${encodeURIComponent(catName)}`
  console.log('导航到moment:', navUrl)
  uni.navigateTo({
    url: navUrl,
    fail: (err) => {
      console.error('导航失败:', err)
    }
  })
}

// 从后端获取猫咪数据
  async function fetchCatData() {
    try {
      const data = await getCats()
      const found = data.find((c: Cat) => String(c.id) === String(catId.value))
      if (found) {
        cat.value = found
        // 加载该猫咪的预览图片
        await loadMomentPhotos(found.Name)
      } else {
        momentPhotos.value = []
      }
      // 即使找不到也允许显示占位内容
    } catch (error) {
      console.error('获取猫咪数据失败:', error)
      momentPhotos.value = []
      // 获取失败也允许页面显示
    }
  }

  onLoad((options: any) => {
      console.log('--- onLoad 触发 ---')
      console.log('完整的 options:', JSON.stringify(options))
      
      // 兼容可能被映射到组件 props 或者其他格式的参数
      let id = options?.catId || options?.id || ''
      let name = options?.catName || options?.name || ''
      
      if (name) {
        name = decodeURIComponent(name)
      }

      console.log('最终解析结果 -> id:', id, 'name:', name)
    debugCatId.value = id
    debugCatName.value = name

    if (!id) {
      console.log('没有catId，显示占位UI')
      momentPhotos.value = []
      loading.value = false
      return
    }

    catId.value = id

  fetchCatData().finally(() => {
    loading.value = false
  })
})

// 监听catId变化，重新获取数据
watch(catId, async (newCatId) => {
  console.log('catId changed to:', newCatId)
  if (newCatId) {
    cat.value = null  // 清空旧数据，防止显示错误的猫咪
    momentPhotos.value = []  // 清空旧的预览图片
    await fetchCatData()
  }
})
</script>

<style scoped>
.page {
  background-color: #FFF8DC;
  min-height: 100vh;
}

.header {
  display: flex;
  align-items: center;
  padding: 12rpx 24rpx;
  background: #FFF8DC;
  border-bottom: 1rpx solid #F4A460;
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-left {
  font-size: 32rpx;
  color: #B7C9C0;
  font-weight: 700;
}

.header-title {
  font-size: 28rpx;
  font-weight: 700;
  color: #1C1917;
  flex: 1;
  text-align: center;
}

.spacer {
  width: 40rpx;
}

.content {
  padding: 20rpx 0;
}

.no-data {
  padding: 60rpx 24rpx;
  text-align: center;
}

.no-data-text {
  font-size: 28rpx;
  color: #D8BFD8;
  margin-bottom: 24rpx;
}

.debug-info {
  margin-top: 32rpx;
  background: #f5f5f5;
  padding: 16rpx;
  border-radius: 8rpx;
  text-align: left;
}

.debug-label {
  font-size: 20rpx;
  color: #666;
  display: block;
  margin-bottom: 8rpx;
  font-weight: 600;
}

.debug-item {
  font-size: 16rpx;
  color: #999;
  display: block;
  margin: 6rpx 0;
  word-break: break-all;
  font-family: monospace;
}

.profile-container {
  padding: 0 16rpx 40rpx;
}

.hero-section {
  display: flex;
  gap: 20rpx;
  background: white;
  padding: 20rpx;
  border-radius: 12rpx;
  border: 1rpx solid #F4A460;
  margin-bottom: 16rpx;
}

.avatar-wrapper {
  flex-shrink: 0;
}

.avatar {
  width: 140rpx;
  height: 140rpx;
  border-radius: 12rpx;
  object-fit: cover;
  background: linear-gradient(135deg, #FFF8DC, #FEF3E2);
}

.profile-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 8rpx;
}

.name-star {
  display: flex;
  align-items: center;
  gap: 8rpx;
}

.cat-name {
  font-size: 32rpx;
  font-weight: 700;
  color: #1C1917;
}

.star-icon {
  font-size: 28rpx;
  color: #F0C350;
}

.cat-id {
  font-size: 22rpx;
  color: #D8BFD8;
}

.info-card {
  background: white;
  border-radius: 12rpx;
  border: 1rpx solid #F4A460;
  padding: 16rpx;
  margin-bottom: 16rpx;
}

.info-item {
  padding: 12rpx 0;
  border-bottom: 1rpx solid #FFF8DC;
  display: flex;
  flex-direction: column;
  gap: 8rpx;
}

.info-item:last-child {
  border-bottom: none;
}

.info-label {
  font-size: 22rpx;
  font-weight: 600;
  color: #1C1917;
}

.info-value {
  font-size: 22rpx;
  color: #7A8A80;
  line-height: 1.5;
}

.info-value.tnr {
  color: #B7C9C0;
  font-weight: 600;
}

.traits-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8rpx;
}

.trait-tag {
  background: #FFF8DC;
  color: #7A8A80;
  padding: 6rpx 12rpx;
  border-radius: 20rpx;
  font-size: 20rpx;
  border: 1rpx solid #B7C9C0;
}

.moments-section {
  margin-bottom: 16rpx;
}

.section-title {
  font-size: 26rpx;
  font-weight: 700;
  color: #1C1917;
  margin-bottom: 12rpx;
  margin-left: 0;
}

.moments-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8rpx;
  margin-bottom: 20rpx;
}

.moment-placeholder {
  aspect-ratio: 1;
  border-radius: 8rpx;
  background: linear-gradient(135deg, #FFF8DC, #FEF3E2);
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1rpx dashed #F4A460;
  overflow: hidden;
}

.moment-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.placeholder-image {
  font-size: 40rpx;
}

.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 12rpx;
  padding: 0 16rpx;
}

.btn {
  padding: 16rpx;
  border-radius: 8rpx;
  text-align: center;
  font-weight: 600;
  font-size: 26rpx;
  border: none;
}

.btn-primary {
  background: linear-gradient(135deg, #B7C9C0, #D8BFD8);
  color: white;
}

.btn-secondary {
  background: white;
  color: #B7C9C0;
  border: 2rpx solid #B7C9C0;
}
</style>