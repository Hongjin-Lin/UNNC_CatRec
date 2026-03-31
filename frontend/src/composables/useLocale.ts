import { ref, computed } from 'vue'
import zh from '@/locales/zh'
import en from '@/locales/en'

type Lang = 'zh' | 'en'
type TabKey = 'identify' | 'profiles' | 'map' | 'add' | 'account'

const STORAGE_KEY = 'app_lang'

// Map page path substrings to nav keys
const PATH_TO_KEY: Array<[string, TabKey]> = [
  ['identify', 'identify'],
  ['profiles', 'profiles'],
  ['map', 'map'],
  ['add', 'add'],
  ['account', 'account'],
]

function loadLang(): Lang {
  try {
    const saved = uni.getStorageSync(STORAGE_KEY)
    if (saved === 'zh' || saved === 'en') return saved
  } catch {}
  return 'zh'
}

const lang = ref<Lang>(loadLang())
const messages = { zh, en }

const TAB_KEYS: TabKey[] = ['identify', 'profiles', 'map', 'account']

function applyTabBar(l: Lang) {
  const tabs = messages[l].tab
  TAB_KEYS.forEach((key, index) => {
    const ret = uni.setTabBarItem({ index, text: tabs[key] }) as unknown
    if (ret && typeof (ret as Promise<unknown>).catch === 'function') {
      ;(ret as Promise<unknown>).catch(() => {})
    }
  })
}

function applyCurrentNavTitle(l: Lang) {
  try {
    const pages = getCurrentPages()
    if (!pages.length) return
    const currentPage = pages[pages.length - 1]
    const route: string = (currentPage as any).route || ''
    for (const [pathFragment, key] of PATH_TO_KEY) {
      if (route.includes(pathFragment)) {
        uni.setNavigationBarTitle({ title: messages[l].nav[key] })
        break
      }
    }
  } catch {}
}

export function useLocale() {
  const t = computed(() => messages[lang.value])

  function toggleLang() {
    lang.value = lang.value === 'zh' ? 'en' : 'zh'
    try {
      uni.setStorageSync(STORAGE_KEY, lang.value)
    } catch {}
    applyTabBar(lang.value)
    applyCurrentNavTitle(lang.value)
  }

  function setNavTitle(key: TabKey) {
    uni.setNavigationBarTitle({ title: messages[lang.value].nav[key] })
  }

  return { lang, t, toggleLang, setNavTitle }
}
