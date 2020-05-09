import VueFetch, { $fetch } from '../../plugins/fetch'

export function getProfile(username) {
    return $fetch(`users/${username}/profile`)
    .then(res => res)
    .catch(err => {
        console.log(err);
        throw err;
    });
}

export function editProfile(userUsername, dateOfBirth, profileBio) {
    return $fetch(`users/${userUsername}/profile`, {
        method: 'put',
        body: JSON.stringify({
            date_of_birth: dateOfBirth,
            bio: profileBio
        })
    })
    .then(res => res)
    .catch(err => console.log(err));
}

export function editPhoto(userUsername, profilePhoto) {
    return $fetch(`users/${userUsername}/profile`, {
        method: 'put',
        body: JSON.stringify({
            photo: profilePhoto
        })
    })
    .then(res => res)
    .catch(err => console.log(err));
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
    .then(res => res.json())
    .catch(err => {
        console.log(err);
        throw err;
    });
}

export function createSocialAccount(profileId, network, nichandle, userId) {
    return $fetch(`users/social-account`, {
        method: 'post',
        body: JSON.stringify({
            account: profileId,
            network: network,
            nichandle: nichandle,
            user: userId
        })
    })
    .then(res => res)
    .catch(err => {
        console.log(err);
        throw err;
    });
}

export function deleteSocialAccount(socialAccountId) {
    return $fetch(`users/social-account/${socialAccountId}/delete`, {
        method: 'delete',
        body: JSON.stringify({
            id: socialAccountId
        })
    })
    .then(res => res.json())
    .catch(err => console.log(err));
}

export function deletePhoto(profileId) {
    return $fetch(`remove-photo/${profileId}`, {
        method: 'put',
        body: JSON.stringify({
            id: profileId
        })
    })
    .then(res => res.json())
    .catch(err => console.log(err));
}

