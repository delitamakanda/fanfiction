import VueFetch, { $fetch } from '../plugins/fetch'

export function getNotificationsUser() {
    return $fetch('notifications')
    .then(res => res.results)
    .catch(err => {
        console.log(err);
        throw err;
    });
}
