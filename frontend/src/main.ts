import { createApp } from 'vue';
import Root from './App.vue';
export const app = createApp(Root);
import { vueSelect } from './plugins/vue-select';

import loadPlugins from './helpers/loadPlugins';
loadPlugins(['vue-select'])
app
    .use(vueSelect)
    .mount('#app');

