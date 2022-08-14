import { APP_NAME, APP_VERSION } from '../constants/appConstants';

export const fetchAppConfig = () => {
    return new Promise(resolve => {
        setTimeout(() => {
            resolve({
                data: {
                    app_name: APP_NAME,
                    version: APP_VERSION,
                },
            });
        }, 2000);
    })
};
