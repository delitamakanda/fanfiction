import { apiStatus } from '../../../api/constants/apiStatus';

const { PENDING, SUCCESS, ERROR } = apiStatus;

export default {
    SET_FETCH_APP_CONFIG_STATE(state, payload) {
        switch (payload.status) {
            case PENDING:
                state.appConfigError && (state.appConfigError = null);
                state.appConfigErrorMessage && (state.appConfigErrorMessage = '');
                break;
            case SUCCESS:
                state.appConfig = payload.data;
                break;
                case ERROR:
                state.appConfigError = payload.error;
                state.appConfigErrorMessage = payload.errorMessage || '';
                break;
        }
        state.appConfigStatus = payload.status;
    }
}