import Vue from 'vue'
import VueI18n from 'vue-i18n'

Vue.use(VueI18n)

import fr from '@/langs/fr'
import en from '@/langs/en'

export const i18n = new VueI18n({
    locale: 'fr',
    messages: { fr, en }
});
