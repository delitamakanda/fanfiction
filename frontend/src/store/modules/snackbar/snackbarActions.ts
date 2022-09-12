import * as snackbarTypes from './snackbarTypes';

export default {
    showSnackbar ({commit}, { message, type }) {
        commit(snackbarTypes.showSnackbar, { message, type });
    },
    hideSnackbar({commit}) {
        commit(snackbarTypes.hideSnackbar);
    }
};
