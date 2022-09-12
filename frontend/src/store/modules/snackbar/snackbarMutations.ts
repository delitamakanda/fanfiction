import * as snackbarTypes from './snackbarTypes';

export default {
    showSnackbar(state, {message, type}) {
        state.snackbar.open = true;
        state.snackbar.message = message;
        state.snackbar.type = type;
    },
    hideSnackbar(state) {
        state.snackbar.open = false;
    }
};
