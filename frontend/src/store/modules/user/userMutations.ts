import * as types from '../appConfig/types';

export default {
    fetchUserSuccess (state, user) {
        state.user = user;
    },
    fetchUserFailure(state) {
        state.user = null;
    }
}