import getters from './snackbarGetters';
import actions from './snackbarActions';
import mutations from './snackbarMutations';

const state = {
    snackbar: {
        open: false,
        message: '',
        type: 'info'
    },
};

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
};
