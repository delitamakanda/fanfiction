import { fetchAppConfig } from '../../../api/appConfigApi';
import { apiStatus } from '../../../api/constants/apiStatus';
import { withAsync } from '../../..//api/helpers/withAsync';

const { PENDING, ERROR, SUCCESS } = apiStatus;

const apiPendingFactory = () => {
    return {
        status: PENDING,
    }
}

const apiSuccessFactory = (data) => {
    return {
        status: SUCCESS,
        data
    }
}

const apiErrorFactory = (error, errorMessage = '') => {
    return {
        status: ERROR,
        error,
        errorMessage
    }
}

export default {
    async fetchAppConfig(context) {
        context.commit('SET_FETCH_APP_CONFIG_STATE', apiPendingFactory());

        const { response, error } = await withAsync(fetchAppConfig);
        console.log('response', { response, error });

        if (error) {
            context.commit('SET_FETCH_APP_CONFIG_ERROR', apiErrorFactory(error, (error as any).message));
            return;
        }

        context.commit('SET_FETCH_APP_CONFIG_STATE', apiSuccessFactory(response.data));
    }
}