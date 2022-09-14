import { createI18n } from 'vue-i18n'
import fr from '../i18n/fr'
import en from '../i18n/en'

export const i18n = createI18n({
  legacy: false,
  locale: 'fr',
  fallbackLocale: 'en',
  messages: { fr, en}
})
