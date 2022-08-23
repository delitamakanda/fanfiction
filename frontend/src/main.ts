import 'flowbite';
import { createApp } from 'vue';
import Root from './App.vue';
export const app = createApp(Root);
import { registerBaseComponents } from './helpers/registerBaseComponents';
import VuelidatePlugin from '@vuelidate/core';
import { i18n } from './plugins/i18n';
import store from './store/store';

import router from './router';
import loadPlugins from './helpers/loadPlugins';
registerBaseComponents(app);
loadPlugins(['i18n']);

app.config.performance = true;

import './styles/global.scss';

app
    .use(i18n)
    .use(VuelidatePlugin)
    .use(router)
    .use(store)
    .mount('#app');
