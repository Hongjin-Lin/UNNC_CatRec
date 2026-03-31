<template>
  <view class="page">
    <view class="header">
      <view class="header-left">
        <text class="title">{{ t.profiles.title }}</text>
        <text class="subtitle">{{ t.profiles.subtitle }}</text>
      </view>
      <LangToggle />
    </view>

    <view class="mode-tabs">
      <view class="mode-tab" :class="{ active: activeMode === 'all' }" @tap="toggleAllMode">
        <text>{{ t.profiles.tabs.all }} {{ activeMode === 'all' && showFilterPanel ? '▴' : '▾' }}</text>
      </view>
      <view class="mode-tab" :class="{ active: activeMode === 'favorites' }" @tap="switchMode('favorites')">
        <text>{{ t.profiles.tabs.favorites }}</text>
      </view>
      <view class="mode-tab" :class="{ active: activeMode === 'search' }" @tap="switchMode('search')">
        <text>{{ t.profiles.tabs.search }}</text>
      </view>
    </view>

    <view v-if="activeMode === 'search'" class="search-row">
      <input
        class="search-input"
        v-model="searchQuery"
        :placeholder="t.profiles.searchPlaceholder"
        placeholder-class="search-placeholder"
      />
    </view>

    <view v-if="activeMode === 'all' && showFilterPanel" class="filter-panel">
      <view class="filter-section">
        <text class="section-title">{{ t.profiles.sort.title }}</text>
        <view class="chips">
          <view class="chip" :class="{ active: sortMode === 'default' }" @tap="sortMode = 'default'">
            {{ t.profiles.sort.default }}
          </view>
          <view class="chip" :class="{ active: sortMode === 'hot' }" @tap="sortMode = 'hot'">
            {{ t.profiles.sort.hot }}
          </view>
          <view class="chip" :class="{ active: sortMode === 'category' }" @tap="sortMode = 'category'">
            {{ t.profiles.sort.category }}
          </view>
        </view>
      </view>

      <view class="filter-section">
        <text class="section-title">{{ t.profiles.filters.gender }}</text>
        <view class="chips">
          <view class="chip" :class="{ active: genderFilter === 'all' }" @tap="genderFilter = 'all'">{{ t.profiles.filters.all }}</view>
          <view class="chip" :class="{ active: genderFilter === '公' }" @tap="genderFilter = '公'">{{ t.profiles.filters.male }}</view>
          <view class="chip" :class="{ active: genderFilter === '母' }" @tap="genderFilter = '母'">{{ t.profiles.filters.female }}</view>
          <view class="chip" :class="{ active: genderFilter === '不详' }" @tap="genderFilter = '不详'">{{ t.profiles.filters.unknownGender }}</view>
        </view>
      </view>

      <view class="filter-section">
        <text class="section-title">{{ t.profiles.filters.neutered }}</text>
        <view class="chips">
          <view class="chip" :class="{ active: neuteredFilter === 'all' }" @tap="neuteredFilter = 'all'">{{ t.profiles.filters.all }}</view>
          <view class="chip" :class="{ active: neuteredFilter === 'yes' }" @tap="neuteredFilter = 'yes'">{{ t.profiles.filters.neuteredYes }}</view>
          <view class="chip" :class="{ active: neuteredFilter === 'no' }" @tap="neuteredFilter = 'no'">{{ t.profiles.filters.neuteredNo }}</view>
        </view>
      </view>

      <view class="filter-section">
        <text class="section-title">{{ t.profiles.filters.status }}</text>
        <view class="chips">
          <view class="chip" :class="{ active: statusFilter === 'all' }" @tap="statusFilter = 'all'">{{ t.profiles.filters.all }}</view>
          <view
            v-for="status in statusOptions"
            :key="status"
            class="chip"
            :class="{ active: statusFilter === status }"
            @tap="statusFilter = status"
          >
            {{ status }}
          </view>
        </view>
      </view>

      <view class="filter-actions">
        <view class="action-btn" @tap="resetFilters">{{ t.profiles.filters.reset }}</view>
        <view class="action-btn" @tap="showFilterPanel = false">{{ t.profiles.filters.confirm }}</view>
      </view>
    </view>

    <view v-if="loading" class="center">
      <text class="loading-text">{{ t.profiles.loading }}</text>
    </view>
    <view v-else-if="error" class="center">
      <text class="error-text">{{ error }}</text>
    </view>
    <view v-else-if="displayCats.length === 0" class="center">
      <text class="empty-text">{{ emptyMessage }}</text>
    </view>
    <view v-else class="grid">
      <view
        v-for="cat in displayCats"
        :key="cat.id"
        class="card-link"
        @tap="navigateToCat(cat)"
      >
        <view class="card">
          <view class="card-img-wrap">
            <image
              v-if="cat.image_url"
              :src="imgUrl(cat.image_url)"
              class="card-img"
              mode="aspectFill"
            />
            <view v-else class="card-img-placeholder">🐱</view>
            <view v-if="cat.TNR_Status" class="tnr-label">TNR</view>
            <view class="fav-toggle" @tap.stop="toggleFavorite(cat)">
              {{ isFavorite(cat.id) ? '⭐' : '☆' }}
            </view>
          </view>
          <view class="card-body">
            <view class="card-name-row">
              <text class="card-name">{{ cat.Name }}</text>
              <text class="card-gender">{{ cat.Gender || t.profiles.filters.unknownGender }}</text>
            </view>
            <view class="card-location">
              <text>📍 {{ cat.Location || t.profiles.unknown }}</text>
            </view>
            <view class="tags">
              <text
                v-for="trait in traits(cat.Personality)"
                :key="trait"
                class="tag"
              >{{ trait }}</text>
            </view>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { onShow, onShareAppMessage, onShareTimeline } from '@dcloudio/uni-app'
import { getCats, type CatProfile } from '@/api/index'
import { useLocale } from '@/composables/useLocale'
import LangToggle from '@/components/LangToggle.vue'
import { setCatCache } from '@/composables/catCache'
import { getFavoriteCatIds, toggleFavoriteCat } from '@/composables/catFavorites'

const { lang, t: tRef, setNavTitle } = useLocale()
const t = computed(() => tRef.value)

function refreshNavTitle() {
  setNavTitle('profiles')
}

onShareAppMessage(() => {
  return {
    title: t.value.profiles.title,
    path: '/pages/profiles/index'
  }
})

onShareTimeline(() => {
  return {
    title: t.value.profiles.title,
    query: ''
  }
})

onShow(() => {
  refreshNavTitle()
  favoriteIds.value = getFavoriteCatIds()
})

watch(lang, refreshNavTitle)

const BASE = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'
const DEFAULT_NAMES = ['橙子', '森森', '馒头', '黄苹果', '小话痨', '小话唠']
const DEFAULT_RANK = new Map(DEFAULT_NAMES.map((name, index) => [name, index + 1]))

const cats = ref<CatProfile[]>([])
const loading = ref(true)
const error = ref<string | null>(null)
const searchQuery = ref('')
const favoriteIds = ref<string[]>([])

const activeMode = ref<'all' | 'favorites' | 'search'>('all')
const showFilterPanel = ref(false)
const sortMode = ref<'default' | 'hot' | 'category'>('default')
const genderFilter = ref<'all' | '公' | '母' | '不详'>('all')
const neuteredFilter = ref<'all' | 'yes' | 'no'>('all')
const statusFilter = ref<string>('all')

const statusOptions = computed(() => {
  const set = new Set<string>()
  cats.value.forEach(cat => {
    if (cat.Current_status) set.add(cat.Current_status)
  })
  return Array.from(set)
})

const emptyMessage = computed(() => {
  if (activeMode.value === 'favorites') return t.value.profiles.emptyFavorites
  if (activeMode.value === 'search' && searchQuery.value.trim()) return t.value.profiles.notFound(searchQuery.value.trim())
  if (activeMode.value === 'search') return t.value.profiles.searchHint
  return t.value.profiles.empty
})

const displayCats = computed(() => {
  let list = [...cats.value]

  if (activeMode.value === 'favorites') {
    const favSet = new Set(favoriteIds.value)
    list = list.filter(cat => favSet.has(cat.id))
  }

  if (activeMode.value === 'search') {
    const query = searchQuery.value.trim().toLowerCase()
    if (query) {
      list = list.filter(cat => cat.Name && cat.Name.toLowerCase().includes(query))
    }
  }

  if (genderFilter.value !== 'all') {
    if (genderFilter.value === '不详') {
      list = list.filter(cat => {
        const gender = (cat.Gender || '').trim()
        return !gender || gender === '不详' || gender === '未知' || gender.toLowerCase() === 'unknown'
      })
    } else {
      list = list.filter(cat => (cat.Gender || '不详') === genderFilter.value)
    }
  }

  if (neuteredFilter.value !== 'all') {
    const target = neuteredFilter.value === 'yes'
    list = list.filter(cat => !!cat.TNR_Status === target)
  }

  if (statusFilter.value !== 'all') {
    list = list.filter(cat => (cat.Current_status || '') === statusFilter.value)
  }

  if (sortMode.value === 'hot') {
    list.sort((a, b) => {
      const scoreA = (a.click_count || 0) * 0.4 + (a.likes_count || 0) * 0.4 + (a.comments_count || 0) * 0.2
      const scoreB = (b.click_count || 0) * 0.4 + (b.likes_count || 0) * 0.4 + (b.comments_count || 0) * 0.2
      return scoreB - scoreA
    })
    return list
  }

  if (sortMode.value === 'category') {
    list.sort((a, b) => {
      const ca = (a.Breed || a.Species || '').toLowerCase()
      const cb = (b.Breed || b.Species || '').toLowerCase()
      if (ca !== cb) return ca.localeCompare(cb)
      return resolveDefaultRank(a) - resolveDefaultRank(b)
    })
    return list
  }

  list.sort((a, b) => resolveDefaultRank(a) - resolveDefaultRank(b))
  return list
})

function resolveDefaultRank(cat: CatProfile): number {
  if (typeof cat.default_rank === 'number' && Number.isFinite(cat.default_rank)) {
    return cat.default_rank
  }
  const fromName = DEFAULT_RANK.get(cat.Name)
  if (fromName) return fromName
  return 9999 + Number(cat.id || 0)
}

function switchMode(mode: 'all' | 'favorites' | 'search') {
  activeMode.value = mode
  if (mode !== 'all') {
    showFilterPanel.value = false
  }
}

function toggleAllMode() {
  if (activeMode.value !== 'all') {
    activeMode.value = 'all'
    showFilterPanel.value = true
    return
  }
  showFilterPanel.value = !showFilterPanel.value
}

function resetFilters() {
  sortMode.value = 'default'
  genderFilter.value = 'all'
  neuteredFilter.value = 'all'
  statusFilter.value = 'all'
}

function isFavorite(catId: string): boolean {
  return favoriteIds.value.includes(catId)
}

function toggleFavorite(cat: CatProfile) {
  const nowFavorite = toggleFavoriteCat(cat.id)
  favoriteIds.value = getFavoriteCatIds()
  uni.showToast({ title: nowFavorite ? t.value.profiles.favoriteAdded : t.value.profiles.favoriteRemoved, icon: 'none' })
}

function traits(personality: string): string[] {
  return personality ? personality.split(',').filter(Boolean).slice(0, 3) : []
}

function imgUrl(url: string): string {
  if (!url) return ''
  if (url.startsWith('http')) return url
  return `${BASE}${url}`
}

function navigateToCat(cat: CatProfile) {
  setCatCache(cat)
  const navUrl = `/pages/profiles/self-profile?catId=${cat.id}&catName=${encodeURIComponent(cat.Name)}`
  uni.navigateTo({
    url: navUrl,
    fail: (err) => {
      console.error('Navigation failed:', err)
    }
  })
}

onMounted(async () => {
  try {
    cats.value = await getCats({ sort: 'default' })
    favoriteIds.value = getFavoriteCatIds()
  } catch (e: unknown) {
    error.value = e instanceof Error ? e.message : t.value.profiles.loadFailed
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.page {
  padding: 32rpx 24rpx 120rpx;
  background: #FFF8DC;
  min-height: 100vh;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24rpx;
}
.header-left { flex: 1; }
.title { display: block; font-size: 48rpx; font-weight: 700; color: #1C1917; letter-spacing: 1rpx; }
.subtitle { display: block; font-size: 26rpx; color: #7A8A80; margin-top: 8rpx; font-weight: 500; }

.mode-tabs {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 12rpx;
  margin-bottom: 16rpx;
}
.mode-tab {
  background: rgba(255, 255, 255, 0.7);
  border: 1rpx solid #FED7AA;
  border-radius: 22rpx;
  text-align: center;
  padding: 12rpx 8rpx;
  font-size: 26rpx;
  color: #7A8A80;
  font-weight: 600;
}
.mode-tab.active {
  color: #B45309;
  border-color: #F59E0B;
  background: #FFF3D4;
}

.search-row { margin-bottom: 14rpx; }
.search-input {
  width: 100%;
  background: white;
  border: 2rpx solid #FED7AA;
  border-radius: 28rpx;
  height: 72rpx;
  line-height: 72rpx;
  padding: 0 22rpx;
  font-size: 26rpx;
  color: #1C1917;
}
.search-placeholder { color: #D8BFD8; }

.filter-panel {
  background: rgba(255, 255, 255, 0.9);
  border: 1rpx solid #FED7AA;
  border-radius: 18rpx;
  padding: 18rpx;
  margin-bottom: 18rpx;
}
.filter-section { margin-bottom: 16rpx; }
.section-title {
  display: block;
  font-size: 24rpx;
  font-weight: 700;
  color: #7A8A80;
  margin-bottom: 10rpx;
}
.chips { display: flex; flex-wrap: wrap; gap: 10rpx; }
.chip {
  padding: 8rpx 16rpx;
  border-radius: 18rpx;
  background: #F8FAFC;
  color: #334155;
  font-size: 22rpx;
  border: 1rpx solid #E2E8F0;
}
.chip.active {
  background: #FFF3D4;
  color: #B45309;
  border-color: #F59E0B;
}
.filter-actions {
  display: flex;
  justify-content: space-between;
  gap: 12rpx;
  margin-top: 8rpx;
}
.action-btn {
  flex: 1;
  text-align: center;
  background: #1F2937;
  color: #fff;
  border-radius: 14rpx;
  padding: 12rpx 0;
  font-size: 24rpx;
}

.center { display: flex; justify-content: center; align-items: center; min-height: 60vh; flex-direction: column; }
.loading-text { font-size: 28rpx; color: #7A8A80; font-weight: 600; }
.error-text { font-size: 28rpx; color: #ef4444; font-weight: 600; }
.empty-text { font-size: 28rpx; color: #7A8A80; font-weight: 600; text-align: center; }
.grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20rpx; }
.card-link { text-decoration: none; }
.card { background: white; border-radius: 16rpx; border: 1rpx solid #F4A460; overflow: hidden; transition: all 0.2s ease; }
.card:active { transform: translateY(-3rpx); box-shadow: 0 8rpx 20rpx rgba(240,195,80,0.16); }
.card-img-wrap { width: 100%; aspect-ratio: 1; background: linear-gradient(135deg,#FFF8DC 0%,#FEF3E2 100%); position: relative; overflow: hidden; }
.card-img { width: 100%; height: 100%; object-fit: cover; }
.card-img-placeholder { width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; font-size: 64rpx; }
.tnr-label { position: absolute; top: 12rpx; left: 12rpx; background: #B7C9C0; color: white; padding: 6rpx 12rpx; border-radius: 8rpx; font-size: 20rpx; font-weight: 600; }
.fav-toggle { position: absolute; right: 12rpx; top: 12rpx; font-size: 30rpx; }
.card-body { padding: 16rpx; }
.card-name-row { display: flex; align-items: center; justify-content: space-between; margin-bottom: 8rpx; }
.card-name { font-size: 28rpx; font-weight: 700; color: #1C1917; }
.card-gender { font-size: 22rpx; color: #64748B; }
.card-location { font-size: 22rpx; color: #7A8A80; margin-bottom: 10rpx; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.tags { display: flex; flex-wrap: wrap; gap: 8rpx; }
.tag { background: #F4A460; color: white; padding: 4rpx 12rpx; border-radius: 12rpx; font-size: 20rpx; font-weight: 500; }
</style>
