<template>
  <view class="page">
    <!-- 成功状态 -->
    <view v-if="success" class="success-wrap">
      <text class="success-icon">✨</text>
      <text class="success-title">添加成功喵！</text>
      <text class="success-subtitle">这只小可爱已经加入名册了</text>
      <button class="btn-primary" @tap="reset">继续添加</button>
    </view>

    <view v-else>
      <view class="header">
        <text class="title">🐱 添加新猫咪</text>
        <text class="subtitle">让更多人认识这位校园小明星</text>
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
          <text class="label">
            <text class="required">*</text> 名字
          </text>
          <input
            class="input"
            v-model="form.name"
            placeholder="例如：橘猫小花"
            placeholder-class="placeholder"
          />
        </view>

        <view class="field">
          <text class="label">常见位置</text>
          <input
            class="input"
            v-model="form.location"
            placeholder="例如：图书馆门口"
            placeholder-class="placeholder"
          />
        </view>

        <view class="field">
          <text class="label">性格特点</text>
          <input
            class="input"
            v-model="form.personality"
            placeholder="例如：亲人、爱撒娇、贪吃"
            placeholder-class="placeholder"
          />
        </view>

        <view class="field-row">
          <text class="label">性别</text>
          <view class="radio-group">
            <view
              class="radio-item"
              @tap="form.gender = '公'"
              :class="{ active: form.gender === '公' }"
            >
              <text>公</text>
            </view>
            <view
              class="radio-item"
              @tap="form.gender = '母'"
              :class="{ active: form.gender === '母' }"
            >
              <text>母</text>
            </view>
            <view
              class="radio-item"
              @tap="form.gender = '未知'"
              :class="{ active: form.gender === '未知' }"
            >
              <text>未知</text>
            </view>
          </view>
        </view>

        <view class="field">
          <text class="label">TNR状态</text>
          <view class="checkbox-group">
            <view class="checkbox-item" @tap="form.tnr_status = !form.tnr_status">
              <text class="checkbox" :class="{ checked: form.tnr_status }">{{ form.tnr_status ? '✓' : '' }}</text>
              <text class="checkbox-label">已进行TNR</text>
            </view>
          </view>
        </view>

        <view class="field">
          <text class="label">备注</text>
          <textarea
            class="textarea"
            v-model="form.notes"
            placeholder="其他补充信息..."
            placeholder-class="placeholder"
          />
        </view>
      </view>

      <!-- 提交按钮 -->
      <button class="btn-primary" @tap="submit" :disabled="submitting">
        {{ submitting ? '提交中...' : '✨ 提交' }}
      </button>

      <!-- 错误提示 -->
      <text v-if="error" class="error-text">{{ error }}</text>
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

.img-picker {
  width: 100%;
  height: 360rpx;
  background: linear-gradient(135deg, #FEF3E2 0%, #FFF8DC 100%);
  border-radius: 16rpx;
  border: 2rpx dashed #B7C9C0;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 32rpx;
  overflow: hidden;
}

.preview-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.img-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12rpx;
}

.img-icon {
  font-size: 64rpx;
}

.img-hint {
  color: #D8BFD8;
  font-size: 26rpx;
  font-weight: 500;
}

.form {
  background: white;
  border-radius: 16rpx;
  padding: 32rpx 24rpx;
  margin-bottom: 32rpx;
  border: 1rpx solid #F4A460;
}

.field {
  margin-bottom: 28rpx;
}

.field:last-child {
  margin-bottom: 0;
}

.field-row {
  margin-bottom: 28rpx;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.label {
  font-size: 28rpx;
  color: #1C1917;
  margin-bottom: 12rpx;
  display: block;
  font-weight: 600;
}

.field-row .label {
  margin-bottom: 0;
}

.required {
  color: #ef4444;
  margin-right: 4rpx;
}

.input,
.textarea {
  border: 1rpx solid #B7C9C0;
  border-radius: 8rpx;
  padding: 16rpx 12rpx;
  font-size: 28rpx;
  background: #FFF8DC;
  width: 100%;
  box-sizing: border-box;
  color: #1C1917;
}

.input::placeholder,
.textarea::placeholder {
  color: #D8BFD8;
}

.textarea {
  height: 160rpx;
  vertical-align: top;
}

.radio-group {
  display: flex;
  flex-direction: row;
  gap: 12rpx;
  flex: 1;
}

.radio-item {
  padding: 10rpx 20rpx;
  border: 2rpx solid #B7C9C0;
  border-radius: 20rpx;
  font-size: 26rpx;
  color: #7A8A80;
  background: white;
  transition: all 0.2s;
}

.radio-item:active {
  background: #FFF8DC;
}

.radio-item.active {
  background: #F0C350;
  color: white;
  border-color: #F0C350;
}

.checkbox-group {
  display: flex;
  align-items: center;
  gap: 8rpx;
}

.checkbox-item {
  display: flex;
  align-items: center;
  gap: 8rpx;
  padding: 8rpx 0;
}

.checkbox {
  width: 32rpx;
  height: 32rpx;
  border: 2rpx solid #B7C9C0;
  border-radius: 4rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20rpx;
  color: white;
  font-weight: 600;
  transition: all 0.2s;
}

.checkbox.checked {
  background: #F0C350;
  border-color: #F0C350;
}

.checkbox-label {
  font-size: 26rpx;
  color: #1C1917;
}

.btn-primary {
  background: linear-gradient(135deg, #B7C9C0 0%, #D8BFD8 100%);
  color: white;
  border-radius: 16rpx;
  font-size: 32rpx;
  padding: 24rpx 0;
  width: 100%;
  border: none;
  font-weight: 600;
  transition: all 0.2s;
  margin-bottom: 24rpx;
}

.btn-primary:active {
  opacity: 0.9;
}

.btn-primary[disabled] {
  opacity: 0.6;
}

.error-text {
  display: block;
  color: #ef4444;
  font-size: 26rpx;
  text-align: center;
  font-weight: 600;
}

.success-wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 80vh;
  gap: 16rpx;
}

.success-icon {
  font-size: 100rpx;
  margin-bottom: 16rpx;
}

.success-title {
  font-size: 40rpx;
  font-weight: 700;
  color: #1C1917;
}

.success-subtitle {
  font-size: 26rpx;
  color: #D8BFD8;
  margin-bottom: 40rpx;
}
</style>
