import { createStore } from 'vuex';
import appConfig from './modules/appConfig/appConfig';
import user from './modules/user/user';
import fanfic from './modules/fanfic/fanfic';
import loader from './modules/loader/loader';
import auth from './modules/auth/auth';
import snackbar from './modules/snackbar/snackbar';

const store = createStore({
    strict: process.env.NODE_ENV !== 'production',
    modules: {
        appConfig,
        user,
        fanfic,
        loader,
        auth,
        snackbar,
    },
});

export default store;
