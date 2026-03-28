<template>
  <view class="page">
    <!-- 成功状态 -->
    <view v-if="success" class="success-wrap">
      <text class="success-icon">✅</text>
      <text class="success-title">添加成功！</text>
      <button class="btn-primary" @tap="reset">继续添加</button>
    </view>

    <view v-else>
      <view class="header">
        <text class="title">添加新猫咪</text>
      </view>

      <!-- 图片上传 -->
      <view class="img-picker" @tap="chooseImage">
        <image v-if="filePath" :src="filePath" class="preview-img" mode="aspectFill" />
        <view v-else class="img-placeholder">
          <text class="img-icon">📷</text>
          <text class="img-hint">点击上传猫咪照片</text>
        </view>
      </view>

      <!-- 表单 -->
      <view class="form">
        <view class="field">
          <text class="label">名字 <text class="required">*</text></text>
          <input class="input" v-model="form.name" placeholder="例如：橘猫小花" />
        </view>
        <view class="field">
          <text class="label">常见位置</text>
          <input class="input" v-model="form.location" placeholder="例如：图书馆门口" />
        </view>
        <view class="field">
          <text class="label">性格特点</text>
          <input class="input" v-model="form.personality" placeholder="例如：亲人、爱撒娇" />
        </view>
        <view class="field-row">
          <text class="label">性别</text>
          <view class="radio-group">
            <view class="radio-item" @tap="form.gender = '公'" :class="{ active: form.gender === '公' }">
              <text>公</text>
            </view>
            <view class="radio-item" @tap="form.gender = '母'" :class="{ active: form.gender === '母' }">
              <text>母</text>
            </view>
            <view class="radio-item" @tap="form.gender = '未知'" :class="{ active: form.gender === '未知' }">
              <text>未知</text>
            </view>
          </view>
        </view>
        <view class="field">
          <text class="label">备注</text>
          <textarea class="textarea" v-model="form.remark" placeholder="其他补充信息..." />
        </view>
      </view>

      <button class="btn-primary" @tap="submit" :disabled="submitting">
        {{ submitting ? '提交中...' : '提交' }}
      </button>
    </view>
  </view>
</template>

<script>
import { addCat } from '@/api/index'

export default {
  data() {
    return {
      filePath: '',
      form: {
        name: '',
        location: '',
        personality: '',
        gender: '未知',
        remark: ''
      },
      submitting: false,
      success: false
    }
  },
  methods: {
    chooseImage() {
      uni.chooseImage({
        count: 1,
        success: (res) => {
          this.filePath = res.tempFilePaths[0]
        }
      })
    },
    async submit() {
      if (!this.form.name) {
        uni.showToast({ title: '请填写猫咪名字', icon: 'none' })
        return
      }
      if (!this.filePath) {
        uni.showToast({ title: '请上传猫咪照片', icon: 'none' })
        return
      }
      this.submitting = true
      try {
        await addCat({ 
          name: this.form.name,
          location: this.form.location,
          personality: this.form.personality,
          tnr_status: false,
          notes: this.form.remark || this.form.gender,
          filePath: this.filePath
        })
        this.success = true
      } catch (e) {
        uni.showToast({ title: '提交失败，请重试', icon: 'none' })
      } finally {
        this.submitting = false
      }
    },
    reset() {
      this.filePath = ''
      this.form = { name: '', location: '', personality: '', gender: '未知', remark: '' }
      this.success = false
    }
  }
}
</script>

<style scoped>
.page { padding: 24rpx; background: #f7f7f7; min-height: 100vh; }
.header { margin-bottom: 24rpx; }
.title { font-size: 40rpx; font-weight: bold; color: #333; }
.img-picker { width: 100%; height: 340rpx; background: #fff; border-radius: 16rpx; display: flex; align-items: center; justify-content: center; margin-bottom: 24rpx; overflow: hidden; }
.preview-img { width: 100%; height: 100%; }
.img-placeholder { display: flex; flex-direction: column; align-items: center; }
.img-icon { font-size: 64rpx; }
.img-hint { color: #aaa; font-size: 26rpx; margin-top: 12rpx; }
.form { background: #fff; border-radius: 16rpx; padding: 24rpx; margin-bottom: 32rpx; }
.field { margin-bottom: 24rpx; }
.field-row { margin-bottom: 24rpx; }
.label { font-size: 28rpx; color: #555; margin-bottom: 8rpx; display: block; }
.required { color: #e74c3c; }
.input { border: 1rpx solid #eee; border-radius: 8rpx; padding: 16rpx; font-size: 28rpx; background: #fafafa; width: 100%; box-sizing: border-box; }
.textarea { border: 1rpx solid #eee; border-radius: 8rpx; padding: 16rpx; font-size: 28rpx; background: #fafafa; width: 100%; box-sizing: border-box; height: 160rpx; }
.radio-group { display: flex; flex-direction: row; margin-top: 8rpx; }
.radio-item { padding: 10rpx 32rpx; border: 1rpx solid #ddd; border-radius: 32rpx; margin-right: 16rpx; font-size: 28rpx; color: #555; background: #fafafa; }
.radio-item.active { background: #ff9f43; color: #fff; border-color: #ff9f43; }
.btn-primary { background: #ff9f43; color: #fff; border-radius: 48rpx; font-size: 32rpx; padding: 24rpx 0; width: 100%; margin-top: 8rpx; }
.success-wrap { display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 80vh; }
.success-icon { font-size: 100rpx; }
.success-title { font-size: 40rpx; font-weight: bold; color: #27ae60; margin: 32rpx 0; }
</style>
