import VueFetch, { $fetch } from '../../plugins/fetch'

export function getProfile(username) {
    return $fetch(`users/${username}/profile`)
    .then(res => res)
    .catch(err => {
        console.log(err);
        throw err;
    });
}
