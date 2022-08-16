import { createApp } from 'vue';
import Root from './App.vue';
export const app = createApp(Root);
import { registerBaseComponents } from './helpers/registerBaseComponents';
import { i18n } from './plugins/i18n';

import loadPlugins from './helpers/loadPlugins';
registerBaseComponents(app);
loadPlugins(['i18n'])
app
    .use(i18n)
    .mount('#app');

