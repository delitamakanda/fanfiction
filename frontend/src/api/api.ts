import axios from 'axios';
import TokenService from './services/token.service';
import AuthService from './services/auth.service';

const axiosParams = {
    baseURL: process.env.NODE_ENV === 'development' ? 'http://localhost:8080' : '/',
    headers: {
        'Content-Type': 'application/json',
    }
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

const actionScope = `loader`;

export const setupInterceptors = ({dispatch}) => {
    let requestPending = 0;

    const req = {
        pending: () => {
            requestPending++;
            dispatch(`${actionScope}/show`);
        },
        done: () => {
            requestPending--;
            if (requestPending <= 0) {
                dispatch(`${actionScope}/hide`);
            }
        }
    };

    axiosInstance.interceptors.request.use(
        config => {
            req.pending();
            /* const token = TokenService.getAccessToken();
            if (token) {
                (config as any).headers['Authorization'] = `AccessToken ${token}` ;
            } */
            return config;
        }, error => {
            req.done();
            return Promise.reject(error);
        }
    );

    axiosInstance.interceptors.response.use(
        (response) => {
            req.done();
            return Promise.resolve(response);
        },
        async error => {
            req.done();
            /* const originalConfig = error.config;
            if (originalConfig.url !== '/api/token' && error.response) {
                if (error.response.status === 401 && !originalConfig._retry) {
                    originalConfig._retry = true;
                }
                try {
                    const rs = await AuthService.refresh(TokenService.getRefreshToken());
                    if (rs) {
                        TokenService.updateAccessToken(rs.response.data.refresh);

                        return axiosInstance(originalConfig);
                    }
                    if (error) {
                        console.error(error);
                    }
                } catch (_error) {
                    return Promise.reject(error);
                }
            } */
            return Promise.reject(error);
        }
    );
}

export default api(axiosInstance);
