import * as loaderTypes from './loaderTypes';

export default {
    show(state) {
        state.loading = true;
    },
    hide(state) {
        state.loading = false;
    },
};
