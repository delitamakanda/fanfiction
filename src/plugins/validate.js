import Vue from 'vue';
import VeeValidate from 'vee-validate';
import VueI18n from 'vue-i18n';
import validationMessagesFR from 'vee-validate/dist/locale/fr';
import validationMessagesEN from 'vee-validate/dist/locale/en';

Vue.use(VueI18n);

const i18n = new VueI18n();
i18n.locale = "fr";

const config = {
  aria: true,
  classNames: {},
  classes: false,
  delay: 0,
  dictionary: {
      fr: validationMessagesFR,
      en: validationMessagesEN
  },
  errorBagName: 'err', // change if property conflicts
  events: 'input|blur',
  fieldsBagName: 'field',
  i18n: i18n, // the vue-i18n plugin instance
  i18nRootKey: 'validations', // the nested key under which the validation messages will be located
  inject: true,
  locale: 'en',
  validity: false,
  useConstraintAttrs: true
};

export const validate = new VeeValidate(config, Vue);
