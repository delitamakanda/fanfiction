import { upperFirst } from 'lodash-es';
import { apiStatus } from './apiStatus';

export const apiStatusComputedFactory = (reactivePropertyKeys = [""]) => {
    let computed  = {};

    const properties = Array.isArray(reactivePropertyKeys) ? reactivePropertyKeys : [reactivePropertyKeys];

    for(const reactivePropertyKey of properties) {

        for (const [statusKey, statusValue] of Object.entries(apiStatus)) {
            const normalisedStatus = upperFirst(statusKey.toLowerCase());
    
            computed[`${reactivePropertyKey}${normalisedStatus}`] = function () {
                return this[reactivePropertyKey] === statusValue;
            };
        }
    }


    return computed;
}