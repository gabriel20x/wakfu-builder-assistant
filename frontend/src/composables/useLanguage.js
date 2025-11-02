import { ref, computed } from 'vue'

// Available languages
export const LANGUAGES = {
  ES: 'es',
  EN: 'en',
  FR: 'fr'
}

// Language labels
export const LANGUAGE_LABELS = {
  [LANGUAGES.ES]: 'Español',
  [LANGUAGES.EN]: 'English',
  [LANGUAGES.FR]: 'Français'
}

// Current selected language (default Spanish)
const currentLanguage = ref(localStorage.getItem('language') || LANGUAGES.ES)

// Watch for changes and save to localStorage
export function useLanguage() {
  const setLanguage = (lang) => {
    if (Object.values(LANGUAGES).includes(lang)) {
      currentLanguage.value = lang
      localStorage.setItem('language', lang)
    }
  }

  const getItemName = (item) => {
    if (!item) return ''
    
    const lang = currentLanguage.value
    
    // Try to get name in selected language
    if (lang === LANGUAGES.ES && item.name_es) return item.name_es
    if (lang === LANGUAGES.EN && item.name_en) return item.name_en
    if (lang === LANGUAGES.FR && item.name_fr) return item.name_fr
    
    // Fallback chain: EN -> ES -> FR -> default name
    return item.name_en || item.name_es || item.name_fr || item.name || 'Unknown Item'
  }

  const languageOptions = computed(() => {
    return Object.entries(LANGUAGE_LABELS).map(([value, label]) => ({
      value,
      label
    }))
  })

  return {
    currentLanguage,
    setLanguage,
    getItemName,
    languageOptions,
    LANGUAGES
  }
}

