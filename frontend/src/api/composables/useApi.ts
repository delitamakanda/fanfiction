import { ref, computed } from 'vue';
import { upperFirst } from 'lodash-es';
import { apiStatus } from '../constants/apiStatus';

const { IDLE, SUCCESS, ERROR, PENDING} = apiStatus;

const createNormalisedApiStatuses = (status, apiName) => {
    let normalisedApiStatuses = {};

    for (const [statusKey, statusValue] of Object.entries(apiStatus)) {
        let propertyName = '';

        if (apiName) {
            propertyName = `${apiName}Status${upperFirst(statusKey.toLowerCase())}`;
        } else {
            propertyName = `status${upperFirst(statusKey.toLowerCase())}`;
        }

        normalisedApiStatuses[propertyName] = computed(() => statusValue === status.value);
    }
    return normalisedApiStatuses;
}

export const useApi = (apiName, fn, config = {} as any) => {
    const { initialData, responseAdapter } = config;
    const data = ref(initialData);
    const status = ref(IDLE);
    const error = ref(null);

    const exec = async (...args: any[]) => {
        try {
            error.value = null;
            status.value = PENDING;
            const response = await fn(...args);
            data.value = typeof responseAdapter === 'function' ? responseAdapter(response) : response;
            status.value = SUCCESS;
        } catch (error: any) {
            error.value = error;
            status.value = ERROR;
            
        }
    }

    return {
        data,
        status,
        error,
        exec,
        ...createNormalisedApiStatuses(status, apiName)
    }
}