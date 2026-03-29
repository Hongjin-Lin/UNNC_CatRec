<template>
  <view class="page">
    <!-- 顶部 -->
    <view class="header">
      <view class="back-btn" @tap="goBack">←</view>
      <text class="header-title">{{ catName }}的喵友圈</text>
      <view class="spacer"></view>
    </view>

    <!-- 加载状态 -->
    <view v-if="loading" class="loading-container">
      <text class="loading-text">加载中喵~</text>
    </view>

    <!-- 主内容区 -->
    <view v-else class="feed">
      <!-- 空状态 -->
      <view v-if="moments.length === 0" class="empty-state">
        <text class="empty-emoji">🐾</text>
        <text class="empty-title">还没有喵片呢</text>
        <text class="empty-subtitle">快来为{{ catName }}拍照吧~</text>
      </view>

      <!-- 图片网格 + 动态 -->
      <view v-else>
        <!-- 时间线动态 -->
        <view v-for="moment in moments" :key="moment.id" class="moment-item">
          <!-- 头部信息 -->
          <view class="moment-header">
            <text class="user-avatar emoji">{{ getRandomAvatar() }}</text>
            <view class="user-info">
              <text class="username">{{ moment.username }}</text>
              <text class="timestamp">{{ moment.created_at }}</text>
            </view>
          </view>

          <!-- 内容文本 -->
          <view class="moment-body">
            <text class="moment-text">{{ moment.content }}</text>
          </view>

          <!-- 多图展示 (微信朋友圈式排版) -->
          <view v-if="moment.image_urls && moment.image_urls.length > 0" class="moment-images">
            <view 
              :class="`image-grid-${Math.min(moment.image_urls.length, 6)}`"
              class="image-grid"
            >
              <view
                v-for="(photoUrl, imgIdx) in moment.image_urls"
                :key="imgIdx"
                class="image-item"
                @tap="toggleImageLike(moment, imgIdx)"
              >
                <image 
                  :src="imgUrl(photoUrl)" 
                  class="moment-image"
                  mode="aspectFill"
                />
                <view v-if="moment.image_likes && moment.image_likes[imgIdx]" class="image-like-badge">
                  ❤️
                </view>
              </view>
            </view>
          </view>

          <!-- 交互栏 -->
          <view class="moment-actions">
            <view class="action" :class="{ active: moment.liked }" @tap="toggleLike(moment)">
              <text class="action-icon">{{ moment.liked ? '❤️' : '🤍' }}</text>
              <text class="action-text">{{ moment.likes }}</text>
            </view>
            <view class="action">
              <text class="action-icon">💬</text>
              <text class="action-text">{{ moment.comments }}</text>
            </view>
            <view class="action">
              <text class="action-icon">🔖</text>
              <text class="action-text">{{ moment.saves }}</text>
            </view>
          </view>

          <!-- 评论预览 -->
          <view v-if="moment.recent_comments && moment.recent_comments.length > 0" class="comments-preview">
            <view class="comments-label">💬 评论</view>
            <view v-for="comment in moment.recent_comments.slice(0, 3)" :key="comment.id" class="comment">
              <text class="comment-username">{{ comment.username }}:</text>
              <text class="comment-text">{{ comment.content }}</text>
            </view>
          </view>
        </view>

        <!-- 底部提示 -->
        <view class="footer-tip">
          <text>🎉 别忘了为喜欢的喵片点赞呀！</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed, watch, onBeforeUnmount } from 'vue'
import { onLoad } from '@dcloudio/uni-app'

interface Moment {
  id: string
  username: string
  created_at: string
  content: string
  image_urls?: string[]  // 支持多张图片
  image_url?: string     // 向后兼容单图
  image_likes?: boolean[]  // 每张图片的点赞状态
  likes: number
  comments: number
  saves: number
  liked: boolean
  recent_comments?: Array<{
    id: string
    username: string
    content: string
  }>
}

const catId = ref<string>('')
const catName = ref<string>('这只猫咪')
const moments = ref<Moment[]>([])
const loading = ref(true)

// 预定义的评论模板 - 更多样化
const commentTemplates = [
  { username: '校园猫奴', content: '太治愈了！' },
  { username: '爱晒猫', content: '求坐标~' },
  { username: '我是铲屎官', content: '这就是猫咪的特权！' },
  { username: '文艺少女', content: '这眼神真的绝了' },
  { username: '猫片收集者', content: '能分享高清版吗' },
  { username: '摄影爱好者', content: '构图绝了！' },
  { username: '校园漫游者', content: '今天又发现了新地点' },
  { username: '猫咪粉丝团', content: '萌到爆炸！！！' },
  { username: '小菜鸡', content: '好可爱啊啊啊' },
  { username: '日常记录者', content: '这就是校园的日常吗' },
  { username: '点赞小能手', content: '走过路过不点赞❤️' },
  { username: '话痨小王', content: '给你点个赞！' },
]

const emoticons = ['😻', '😸', '😹', '😺', '🐱', '😼', '😽', '😻']

const BASE = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

// 计算图片动态列表 - 移除（不再需要分开的图片网格）
// 现在所有图片都在moment中


function getRandomAvatar(): string {
  return emoticons[Math.floor(Math.random() * emoticons.length)]
}

function getRandomComments(count: number = 2) {
  const shuffled = [...commentTemplates].sort(() => Math.random() - 0.5)
  return shuffled.slice(0, Math.max(1, count)).map((c, i) => ({
    id: `c-${i}`,
    ...c,
  }))
}

function imgUrl(url: string): string {
  if (!url) return ''
  // 移除强制 encodeURI，避免双重转义导致 %25E9 等 404 错误
  // 如果已经是完整URL，直接返回
  if (url.startsWith('http')) return url
  // 如果是相对路径，补上BASE前缀
  return `${BASE}${url}`
}

function toggleLike(moment: Moment) {
  moment.liked = !moment.liked
  moment.likes += moment.liked ? 1 : -1
}

function toggleImageLike(moment: Moment, imgIdx: number) {
  if (!moment.image_likes) {
    moment.image_likes = []
  }
  moment.image_likes[imgIdx] = !moment.image_likes[imgIdx]
  // 更新总点赞数
  moment.likes += moment.image_likes[imgIdx] ? 1 : -1
}

function goBack() {
  uni.navigateBack()
}

// 从 URL 查询参数中提取参数（简化版）
function extractParamsFromUrl(): { catId: string; catName: string } {
  try {
    // uni-app H5模式下，URL格式为: /#/pages/profiles/self-profile/cat-moment?catId=1&catName=xxx
    const hash = window.location.hash
    console.log('cat-moment hash:', hash)
    
    const questionIndex = hash.indexOf('?')
    console.log('cat-moment ? position:', questionIndex)
    
    if (questionIndex === -1) {
      console.log('cat-moment: 没有参数')
      return { catId: '', catName: '这只猫咪' }
    }
    
    const queryString = hash.substring(questionIndex + 1)
    console.log('cat-moment queryString:', queryString)
    
    const urlParams = new URLSearchParams(queryString)
    
    const catId = urlParams.get('catId') || ''
    const catName = decodeURIComponent(urlParams.get('catName') || '这只猫咪')
    
    console.log('cat-moment 提取结果:', { catId, catName })
    return { catId, catName }
  } catch (error) {
    console.error('cat-moment 提取URL参数失败:', error)
    return { catId: '', catName: '这只猫咪' }
  }
}

// 检查图片是否存在（通过Promise）
function checkImageExists(url: string): Promise<boolean> {
  return new Promise((resolve) => {
      uni.getImageInfo({
        src: url,
        success: () => resolve(true),
        fail: () => resolve(false)
      })
  })
}

async function fetchCatPhotos() {
  try {
    console.log('开始获取猫咪图片:', catName.value)
    
    // 本地库中的图片是按 {catName}/{catName}_1.jpeg, {catName}_2.jpeg 等命名的
    // 我们尝试加载这些图片，直到某个数字失败
    const photoUrls: string[] = []
    
    // 尝试加载最多20张图片，但连续失败3个就停止
    let consecutiveFailures = 0
    for (let i = 1; i <= 20 && consecutiveFailures < 3; i++) {
      const photoUrl = `/static/cats/${catName.value}/${catName.value}_${i}.jpeg`
      const fullUrl = imgUrl(photoUrl)
      
      console.log(`尝试加载第${i}张图片:`, fullUrl)
      const exists = await checkImageExists(fullUrl)
      
      if (exists) {
        photoUrls.push(photoUrl)
        consecutiveFailures = 0 // 重置计数器
        console.log(`✓ 第${i}张图片存在`)
      } else {
        consecutiveFailures++
        console.log(`✗ 第${i}张图片不存在，连续失败${consecutiveFailures}次`)
      }
    }

    console.log('图片加载完成，共找到', photoUrls.length, '张')

    if (photoUrls.length === 0) {
      console.log('没有找到任何图片，显示空状态')
      moments.value = []
      loading.value = false
      return
    }

    // 生成动态：每3-5张图片为一条动态
    const usernames = [
      '校园摄影师',
      '猫咪爱好者', 
      '喵友圈小卖部',
      '校园漫游者',
      catName.value + '家族',
      '日常记录官',
      '温暖的人'
    ]
    
    const groupSize = Math.floor(Math.random() * 4) + 2  // 2-5张
    moments.value = []
    
    for (let groupIdx = 0; groupIdx < Math.ceil(photoUrls.length / groupSize); groupIdx++) {
      // 每组取一些图片
      const startIdx = groupIdx * groupSize
      const endIdx = Math.min(startIdx + groupSize, photoUrls.length)
      const groupPhotos = photoUrls.slice(startIdx, endIdx)
      
      if (groupPhotos.length === 0) continue

      const likeCount = Math.floor(Math.random() * 150) + 30
      const commentCount = Math.floor(Math.random() * 50) + 10
      const username = usernames[Math.floor(Math.random() * usernames.length)]

      moments.value.push({
        id: `moment-${groupIdx}`,
        username: username,
        created_at: formatDateAgo(groupIdx),
        content: getRandomPhotoCaption(catName.value),
        image_urls: groupPhotos, // 多张图片
        image_likes: new Array(groupPhotos.length).fill(false),
        likes: likeCount,
        comments: commentCount,
        saves: Math.floor(likeCount * 0.5),
        liked: false,
        recent_comments: getRandomComments(Math.floor(Math.random() * 2) + 2),
      })
    }

    console.log('成功生成', moments.value.length, '条动态')
    loading.value = false
  } catch (error) {
    console.error('获取猫咪图片失败:', error)
    moments.value = []
    loading.value = false
  }
}

// 格式化时间（几天前、几小时前等）
function formatDateAgo(index: number): string {
  const daysAgo = Math.floor(Math.random() * 30) + index * 2
  const hoursAgo = Math.floor(Math.random() * 24)
  
  if (daysAgo > 0) {
    return `${daysAgo}天前`
  } else if (hoursAgo > 0) {
    return `${hoursAgo}小时前`
  } else {
    return '刚刚'
  }
}

function getRandomPhotoCaption(catName: string): string {
  const captions = [
    // 日常观察类
    `${catName}今天又在"巡视"校园啦，认真的样子超可爱！`,
    `在阳光下捕捉到${catName}最萌的一刻💕`,
    `${catName}：我就静静地躺着，你们别吵我😴`,
    `有谁见过${catName}这么专注的样子？`,
    `${catName}的眼神，满是校园的故事呢~`,
    
    // 互动类
    `抓拍${catName}的日常，完美！`,
    `美妙的${catName}时刻🐾`,
    `${catName}今天的表情包真的绝了！`,
    `校园三号卡位，${catName}实力演员！`,
    `不经意间发现${catName}偷懒的时刻`,
    
    // 季节类
    `秋日午后，${catName}在阳光下打盹`,
    `冬日暖阳，看${catName}慵懒地伸懒腰`,
    `春日骄阳，${catName}开启"散步"模式`,
    `夏日炎炎，${catName}躲在阴凉处乘凉`,
    
    // 互动关系类
    `${catName}跟我玩"躲猫猫"呢😹`,
    `这就是${catName}吃饭的样子，萌度爆表！`,
    `${catName}：你们人类好有趣呀`,
    `同框不同框，但${catName}永远是主角`,
    `${catName}：这个位置光线刚刚好`,
    
    // 情感类
    `治愈！一张照片就足以拯救糟糕的一天`,
    `${catName}用行动诠释什么叫"慵懒贵妃"`,
    `看着${catName}，所有烦恼都烟消云散`,
    `${catName}教会我：慢下来，感受当下`,
    `${catName}的存在，就是校园最大的幸运`,
  ]
  return captions[Math.floor(Math.random() * captions.length)]
}

onLoad((options: any) => {
    console.log('cat-moment 页面加载')

    const id = options?.catId || ''
    const name = options?.catName ? decodeURIComponent(options.catName) : '这只猫咪'
    
    console.log('提取到的参数:', { id, name })

    catId.value = id
    catName.value = name
  
  // 如果有catId，尝试获取数据
  if (catId.value) {
    fetchCatPhotos()
  } else {
    // 没有catId也允许页面显示
    loading.value = false
  }
})

// 监听catId变化，重新获取照片
watch(catId, async (newCatId) => {
  console.log('cat-moment: catId changed to:', newCatId)
  if (newCatId) {
    loading.value = true
    moments.value = []  // 清空旧数据
    await fetchCatPhotos()
  }
})
</script>

<style scoped>
.page {
  background-color: #FFF8DC;
  min-height: 100vh;
  padding-bottom: 40rpx;
}

/* Header */
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12rpx 24rpx;
  background: #FFF8DC;
  border-bottom: 1rpx solid #F4A460;
  position: sticky;
  top: 0;
  z-index: 100;
}

.back-btn {
  font-size: 32rpx;
  color: #B7C9C0;
  font-weight: 600;
  padding: 8rpx;
  cursor: pointer;
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

.loading-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
}

.loading-text {
  font-size: 28rpx;
  color: #D8BFD8;
  font-weight: 600;
}

.feed {
  padding: 0;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
  gap: 16rpx;
}

.empty-emoji {
  font-size: 80rpx;
  margin-bottom: 16rpx;
}

.empty-title {
  font-size: 32rpx;
  font-weight: 600;
  color: #1C1917;
}

.empty-subtitle {
  font-size: 24rpx;
  color: #D8BFD8;
}

/* 图片网格 */
.photos-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rpx;
  padding: 0;
}

.photo-card {
  position: relative;
  aspect-ratio: 1;
  overflow: hidden;
  background: linear-gradient(135deg, #FFF8DC, #FEF3E2);
}

.photo-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.photo-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0);
  display: flex;
  align-items: flex-end;
  justify-content: flex-end;
  padding: 8rpx;
  transition: all 0.2s ease;
}

.photo-card:active .photo-overlay {
  background: rgba(0, 0, 0, 0.3);
}

.like-count {
  font-size: 20rpx;
  color: white;
  font-weight: 700;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.5);
}

.like-count.active {
  color: #F0C350;
}

/* 分隔线 */
.section-divider {
  height: 20rpx;
  background: linear-gradient(90deg, transparent, #D8BFD8, transparent);
  margin: 24rpx 0;
}

/* Moment Item */
.moment-item {
  background: white;
  margin: 12rpx 16rpx;
  border-radius: 12rpx;
  border: 1rpx solid #F4A460;
  overflow: hidden;
  padding: 20rpx 24rpx;
}

.moment-header {
  display: flex;
  align-items: center;
  gap: 12rpx;
  margin-bottom: 16rpx;
}

.user-avatar {
  font-size: 40rpx;
  width: 48rpx;
  height: 48rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}

.user-avatar.emoji {
  background: #FEF3E2;
  border-radius: 24rpx;
}

.user-info {
  display: flex;
  flex-direction: column;
  gap: 4rpx;
}

.username {
  font-size: 26rpx;
  font-weight: 600;
  color: #1C1917;
}

.timestamp {
  font-size: 20rpx;
  color: #D8BFD8;
}

/* Moment Body */
.moment-body {
  margin-bottom: 12rpx;
}

.moment-text {
  font-size: 26rpx;
  color: #1C1917;
  line-height: 1.6;
  word-break: break-word;
}

/* Actions */
.moment-actions {
  display: flex;
  gap: 24rpx;
  padding: 12rpx 0;
  border-top: 1rpx solid #FFF8DC;
  border-bottom: 1rpx solid #FFF8DC;
  margin-bottom: 12rpx;
}

.action {
  display: flex;
  align-items: center;
  gap: 6rpx;
  padding: 6rpx 8rpx;
  border-radius: 6rpx;
  transition: all 0.2s ease;
  cursor: pointer;
}

.action:active {
  background: #FFF8DC;
}

.action-icon {
  font-size: 20rpx;
}

.action-text {
  font-size: 20rpx;
  color: #7A8A80;
  font-weight: 500;
}

.action.active {
  color: #F0C350;
}

.action.active .action-text {
  color: #F0C350;
  font-weight: 700;
}

/* Comments */
.comments-preview {
  background: #FFF8DC;
  padding: 12rpx 16rpx;
  border-radius: 6rpx;
  max-height: 100rpx;
  overflow: hidden;
}

.comments-label {
  font-size: 20rpx;
  color: #7A8A80;
  font-weight: 600;
  margin-bottom: 8rpx;
}

.comment {
  display: flex;
  gap: 8rpx;
  margin-bottom: 8rpx;
  font-size: 22rpx;
}

.comment:last-child {
  margin-bottom: 0;
}

.comment-username {
  color: #7A8A80;
  font-weight: 600;
  min-width: 80rpx;
}

.comment-text {
  color: #1C1917;
  flex: 1;
}

/* 多图展示 - 微信朋友圈式布局 */
.moment-images {
  margin: 12rpx 0;
}

.image-grid {
  display: grid;
  gap: 8rpx;
  width: 100%;
}

/* 1张图：全宽 */
.image-grid-1 {
  grid-template-columns: 1fr;
}

.image-grid-1 .image-item {
  aspect-ratio: 16 / 9;
}

/* 2张图：两列 */
.image-grid-2 {
  grid-template-columns: 1fr 1fr;
}

.image-grid-2 .image-item {
  aspect-ratio: 1;
}

/* 3张图：三列 */
.image-grid-3 {
  grid-template-columns: 1fr 1fr 1fr;
}

.image-grid-3 .image-item {
  aspect-ratio: 1;
}

/* 4张图：2x2 */
.image-grid-4 {
  grid-template-columns: 1fr 1fr;
}

.image-grid-4 .image-item {
  aspect-ratio: 1;
}

/* 5张图：3列布局 */
.image-grid-5 {
  grid-template-columns: 1fr 1fr 1fr;
}

.image-grid-5 .image-item {
  aspect-ratio: 1;
}

/* 6张图：3x2布局 */
.image-grid-6 {
  grid-template-columns: 1fr 1fr 1fr;
}

.image-grid-6 .image-item {
  aspect-ratio: 1;
}

.image-item {
  position: relative;
  border-radius: 8rpx;
  overflow: hidden;
  background: #FEF3E2;
  cursor: pointer;
  transition: all 0.2s ease;
}

.image-item:active {
  transform: scale(0.95);
}

.moment-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-like-badge {
  position: absolute;
  bottom: 8rpx;
  right: 8rpx;
  font-size: 32rpx;
  text-shadow: 0 1rpx 3rpx rgba(0, 0, 0, 0.3);
}

/* Footer */
.footer-tip {
  text-align: center;
  padding: 48rpx 24rpx;
  font-size: 24rpx;
  color: #D8BFD8;
}
</style>