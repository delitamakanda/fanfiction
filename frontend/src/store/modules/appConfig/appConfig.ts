import getters from './appConfigGetters';
import actions from './appConfigActions';
import mutations from './appConfigMutations';
import { apiStatus } from '../../../api/constants/apiStatus';
const { IDLE } = apiStatus;

const state = {
    appConfig: {},
    appConfigStatus: IDLE,
    appConfigError: null,
    appConfigErrorMessage: '',
}

export default {
    state,
    actions,
    getters,
    mutations,
};
