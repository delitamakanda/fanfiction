import axios from 'axios';

const axiosParams = {
    baseURL: process.env.NODE_ENV === 'development' ? 'http://localhost:8080' : '/',
};

const axiosInstance = axios.create(axiosParams);
export const didAbort = error => axios.isCancel(error);
export const getCancelSource = () => axios.CancelToken.source();

const api = (axios) => {
    const withAbort = fn => async (...args) => {
        const originalConfig = args[args.length - 1];
        let {abort, ...config} = originalConfig;

        if (typeof abort === 'function') {
            const { cancel, token} = getCancelSource();
            config.cancelToken = token;
            abort(cancel, token);
         }

         try {
            return await fn(...args.slice(0, args.length - 1), config);
         } catch (error: any) {
            didAbort(error) && (error.aborted = true);
            throw error;
         }
    }

    const withLogger = async promise => 
        promise.catch(error => {
            if (!process.env.VUE_APP_DEBUG_API) throw error;

            if (error.response) {
                console.log(error.response.data);
                console.log(error.response.status);
                console.log(error.response.headers);
            } else if (error.request) {
                console.log(error.request);
            } else {
                console.log('error', error.message);
            }
            console.log(error.config);
            throw error;
        });

    return {
        get: (url, config = {}) => withLogger(withAbort(axios.get)(url, config)),
        post: (url, body, config = {}) => withLogger(withAbort(axios.post)(url, body, config)),
        put: (url, body, config = {}) => withLogger(withAbort(axios.put)(url, body, config)),
        patch: (url, body, config = {}) => withLogger(withAbort(axios.patch)(url, body, config)),
        delete: (url, config = {}) => withLogger(withAbort(axios.delete)(url, config))
    };
};

export const abortable = fn => {
    const { cancel, token } = getCancelSource();
    return {
        abort: cancel,
        fn: (...args) => {
            if (typeof args[args.length - 1] !== 'object') {
                throw new Error('the last argument must be a config object');
            }
            args[args.length - 1] = {
                ...args[args.length - 1],
                cancelToken: token
            };

            return fn(...args);
        }
    }
}

export default api(axiosInstance);