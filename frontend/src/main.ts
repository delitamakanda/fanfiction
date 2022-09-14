import 'flowbite';
import { createApp } from 'vue';
import Root from './App.vue';
export const app = createApp(Root);
import { registerBaseComponents } from './helpers/registerBaseComponents';
import { i18n } from './plugins/i18n';
import store from './store/store';
import { setupInterceptors } from './api/api';

import router from './router';
import loadPlugins from './helpers/loadPlugins';
import mixins from './mixins';
registerBaseComponents(app);
loadPlugins(['i18n']);
setupInterceptors(store);

app.config.performance = true;

import './styles/global.scss';

app
    .use(i18n)
    .use(router)
    .use(store)
    .mixin(mixins)
    .mount('#app');
