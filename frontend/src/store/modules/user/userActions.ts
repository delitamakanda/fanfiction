import { getCurrentUser } from '../../../api/accountApi';
import { withAsync } from '../../../api/helpers/withAsync';


export default {
    async fetchCurrentUser({ commit }) {
        const { response, error } = await withAsync(getCurrentUser);
        if (response && response.data) {
            commit('fetchUserSuccess', response.data);
        }
        if (error) {
            commit('fetchUserFailure');
        }
    },
    clearUser({ commit }) {
        commit('fetchUserFailure');
    }
}