import { createStore } from 'vuex';
import appConfig from './modules/appConfig/appConfig';
import user from './modules/user/user';
import fanfic from './modules/fanfic/fanfic';
import loader from './modules/loader/loader';

const store = createStore({
    strict: process.env.NODE_ENV !== 'production',
    modules: {
        appConfig,
        user,
        fanfic,
        loader,
    },
});

export default store;
