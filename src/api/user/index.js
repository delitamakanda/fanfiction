import VueFetch, { $fetch } from '../../plugins/fetch'

export function getProfile(username) {
    return $fetch(`users/${username}/profile`)
    .then(res => res)
    .catch(err => {
        console.log(err);
        throw err;
    });
}

export function editUserEmail(userId, userEmail) {
    return $fetch(`users/${userId}`, {
        method: 'put',
        body: JSON.stringify({
            email: userEmail
        })
    })
    .then(res => res)
    .catch(err => {
        console.log(err);
        throw err;
    });
}

export function changePassword(oldPassword, newPassword) {
    return $fetch(`change-password`, {
        method: 'put',
        body: JSON.stringify({
            old_password: oldPassword,
            new_password: newPassword
        })
    })
    .then(res => res)
    .catch(err => {
        console.log(err);
        throw err;
    });
}
