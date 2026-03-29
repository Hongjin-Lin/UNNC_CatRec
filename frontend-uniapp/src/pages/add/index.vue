<template>
  <view class="page">
    <!-- 成功状态 -->
    <view v-if="success" class="success-wrap">
      <text class="success-icon">✨</text>
      <text class="success-title">{{ t.add.successTitle }}</text>
      <text class="success-subtitle">{{ t.add.successSub }}</text>
      <button class="btn-primary" @tap="reset">{{ t.add.continueAdd }}</button>
    </view>

    <view v-else>
      <view class="header">
        <view class="header-left">
          <text class="title">{{ t.add.title }}</text>
          <text class="subtitle">{{ t.add.subtitle }}</text>
        </view>
        <LangToggle />
      </view>

      <!-- 图片上传 -->
      <view class="img-picker" @tap="chooseImage">
        <image v-if="filePath" :src="filePath" class="preview-img" mode="aspectFill" />
        <view v-else class="img-placeholder">
          <text class="img-icon">📷</text>
          <text class="img-hint">{{ t.add.uploadHint }}</text>
        </view>
      </view>

      <!-- 表单 -->
      <view class="form">
        <view class="field">
          <text class="label"><text class="required">*</text> {{ t.add.name }}</text>
          <input class="input" v-model="form.name" :placeholder="t.add.namePlaceholder" placeholder-class="placeholder" />
        </view>
        <view class="field">
          <text class="label">{{ t.add.location }}</text>
          <input class="input" v-model="form.location" :placeholder="t.add.locationPlaceholder" placeholder-class="placeholder" />
        </view>
        <view class="field">
          <text class="label">{{ t.add.personality }}</text>
          <input class="input" v-model="form.personality" :placeholder="t.add.personalityPlaceholder" placeholder-class="placeholder" />
        </view>
        <view class="field-row">
          <text class="label">{{ t.add.gender }}</text>
          <view class="radio-group">
            <view class="radio-item" @tap="form.gender = t.add.genderMale" :class="{ active: form.gender === t.add.genderMale }">
              <text>{{ t.add.genderMale }}</text>
            </view>
            <view class="radio-item" @tap="form.gender = t.add.genderFemale" :class="{ active: form.gender === t.add.genderFemale }">
              <text>{{ t.add.genderFemale }}</text>
            </view>
            <view class="radio-item" @tap="form.gender = t.add.genderUnknown" :class="{ active: form.gender === t.add.genderUnknown }">
              <text>{{ t.add.genderUnknown }}</text>
            </view>
          </view>
        </view>
        <view class="field">
          <text class="label">{{ t.add.tnr }}</text>
          <view class="checkbox-group">
            <view class="checkbox-item" @tap="form.tnr_status = !form.tnr_status">
              <text class="checkbox" :class="{ checked: form.tnr_status }">{{ form.tnr_status ? '✓' : '' }}</text>
              <text class="checkbox-label">{{ t.add.tnrDone }}</text>
            </view>
          </view>
        </view>
        <view class="field">
          <text class="label">{{ t.add.notes }}</text>
          <textarea class="textarea" v-model="form.notes" :placeholder="t.add.notesPlaceholder" placeholder-class="placeholder" />
        </view>
        <view class="field">
          <text class="label"><text class="required">*</text> {{ t.add.adminPassword }}</text>
          <input class="input" password v-model="adminPassword" :placeholder="t.add.adminPasswordPlaceholder" placeholder-class="placeholder" />
        </view>
      </view>

      <!-- 提交按钮 -->
      <button class="btn-primary" @tap="submit" :disabled="submitting">
        {{ submitting ? t.add.submitting : t.add.submit }}
      </button>

      <!-- 错误提示 -->
      <text v-if="errorMsg" class="error-text">{{ errorMsg }}</text>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { addCat } from '@/api/index'
import { useLocale } from '@/composables/useLocale'
import LangToggle from '@/components/LangToggle.vue'

const { t: tRef } = useLocale()
const t = computed(() => tRef.value)

const adminPassword = ref('')
const filePath = ref('')
const form = ref({
  name: '',
  location: '',
  personality: '',
  gender: '',
  notes: '',
  tnr_status: false,
})
const submitting = ref(false)
const success = ref(false)
const errorMsg = ref('')

function chooseImage() {
  uni.chooseImage({
    count: 1,
    success: (res) => {
      filePath.value = res.tempFilePaths[0]
    }
  })
}

async function submit() {
  if (adminPassword.value !== 'UNNC2026') {
    uni.showToast({ title: t.value.add.errPassword, icon: 'error' })
    return
  }
  if (!form.value.name) {
    uni.showToast({ title: t.value.add.errName, icon: 'none' })
    return
  }
  if (!filePath.value) {
    uni.showToast({ title: t.value.add.errPhoto, icon: 'none' })
    return
  }
  submitting.value = true
  errorMsg.value = ''
  try {
    await addCat({
      name: form.value.name,
      location: form.value.location,
      personality: form.value.personality,
      tnr_status: form.value.tnr_status,
      notes: form.value.notes || form.value.gender,
      filePath: filePath.value
    })
    success.value = true
  } catch {
    uni.showToast({ title: t.value.add.errSubmit, icon: 'none' })
  } finally {
    submitting.value = false
  }
}

function reset() {
  filePath.value = ''
  form.value = { name: '', location: '', personality: '', gender: '', notes: '', tnr_status: false }
  success.value = false
  errorMsg.value = ''
  adminPassword.value = ''
}
</script>

<style scoped>
.page { padding: 40rpx 24rpx 120rpx; background: #FFF8DC; min-height: 100vh; }
.header { display: flex; align-items: flex-start; justify-content: space-between; margin-bottom: 40rpx; }
.header-left { flex: 1; }
.title { display: block; font-size: 48rpx; font-weight: 700; color: #1C1917; letter-spacing: 1rpx; }
.subtitle { display: block; font-size: 26rpx; color: #D8BFD8; margin-top: 8rpx; font-weight: 500; }
.img-picker { width: 100%; height: 360rpx; background: linear-gradient(135deg,#FEF3E2 0%,#FFF8DC 100%); border-radius: 16rpx; border: 2rpx dashed #B7C9C0; display: flex; align-items: center; justify-content: center; margin-bottom: 32rpx; overflow: hidden; }
.preview-img { width: 100%; height: 100%; object-fit: cover; display: block; }
.img-placeholder { display: flex; flex-direction: column; align-items: center; gap: 12rpx; }
.img-icon { font-size: 64rpx; }
.img-hint { color: #D8BFD8; font-size: 26rpx; font-weight: 500; }
.form { background: white; border-radius: 16rpx; padding: 32rpx 24rpx; margin-bottom: 32rpx; border: 1rpx solid #F4A460; }
.field { margin-bottom: 28rpx; }
.field:last-child { margin-bottom: 0; }
.field-row { margin-bottom: 28rpx; display: flex; align-items: center; justify-content: space-between; }
.label { font-size: 28rpx; color: #1C1917; margin-bottom: 12rpx; display: block; font-weight: 600; }
.field-row .label { margin-bottom: 0; }
.required { color: #ef4444; margin-right: 4rpx; }
.input, .textarea { border: 1rpx solid #B7C9C0; border-radius: 8rpx; padding: 16rpx 12rpx; font-size: 28rpx; background: #FFF8DC; width: 100%; box-sizing: border-box; color: #1C1917; }
.textarea { height: 160rpx; vertical-align: top; }
.radio-group { display: flex; flex-direction: row; gap: 12rpx; flex: 1; justify-content: flex-end; }
.radio-item { padding: 10rpx 20rpx; border: 2rpx solid #B7C9C0; border-radius: 20rpx; font-size: 26rpx; color: #7A8A80; background: white; }
.radio-item.active { background: #F0C350; color: white; border-color: #F0C350; }
.checkbox-group { display: flex; align-items: center; gap: 8rpx; }
.checkbox-item { display: flex; align-items: center; gap: 8rpx; padding: 8rpx 0; }
.checkbox { width: 32rpx; height: 32rpx; border: 2rpx solid #B7C9C0; border-radius: 4rpx; display: flex; align-items: center; justify-content: center; font-size: 20rpx; color: white; font-weight: 600; }
.checkbox.checked { background: #F0C350; border-color: #F0C350; }
.checkbox-label { font-size: 26rpx; color: #1C1917; }
.btn-primary { background: linear-gradient(135deg,#B7C9C0 0%,#D8BFD8 100%); color: white; border-radius: 16rpx; font-size: 32rpx; padding: 24rpx 0; width: 100%; border: none; font-weight: 600; margin-bottom: 24rpx; }
.btn-primary[disabled] { opacity: 0.6; }
.error-text { display: block; color: #ef4444; font-size: 26rpx; text-align: center; font-weight: 600; }
.success-wrap { display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 80vh; gap: 16rpx; }
.success-icon { font-size: 100rpx; margin-bottom: 16rpx; }
.success-title { font-size: 40rpx; font-weight: 700; color: #1C1917; }
.success-subtitle { font-size: 26rpx; color: #D8BFD8; margin-bottom: 40rpx; }
</style>
