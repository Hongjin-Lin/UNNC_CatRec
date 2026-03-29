import { ref, computed } from 'vue'
import zh from '@/locales/zh'
import en from '@/locales/en'

type Lang = 'zh' | 'en'

const STORAGE_KEY = 'app_lang'

function loadLang(): Lang {
  try {
    const saved = uni.getStorageSync(STORAGE_KEY)
    if (saved === 'zh' || saved === 'en') return saved
  } catch {}
  return 'zh'
}

const lang = ref<Lang>(loadLang())

const messages = { zh, en }

export function useLocale() {
  const t = computed(() => messages[lang.value])

  function toggleLang() {
    lang.value = lang.value === 'zh' ? 'en' : 'zh'
    try {
      uni.setStorageSync(STORAGE_KEY, lang.value)
    } catch {}
  }

  return { lang, t, toggleLang }
}
