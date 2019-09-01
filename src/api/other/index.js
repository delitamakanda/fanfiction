import VueFetch, { $fetch } from '../../plugins/fetch'

export function getNotificationsUser() {
    return $fetch('notifications')
    .then(res => res.results)
    .catch(err => {
        console.log(err);
        throw err;
    });
}

export function getPages(page) {
    return $fetch(`pages/${page}`)
    .then(res => res)
    .catch(err => {
        console.log(err);
        throw err;
    });
}

export function sendMail(user, subject, message) {
    return $fetch('contact-mail', {
        method: 'post',
        body: JSON.stringify({
            from_email: user,
            subject: subject,
            message: message
        })
    })
    .then(res => res)
    .catch(err => console.log(err));
}

export function preventAbuse(fanficId) {
    return $fetch('feedback', {
        method: 'post',
        body: JSON.stringify({
            id: fanficId
        })
    })
    .then(res => res)
    .catch(err => console.log(err));
}

export function followFanfic (fromUserId, followFanficId) {
    return $fetch('follow-stories', {
        method: 'post',
        body: JSON.stringify({
            from_user: fromUserId,
            to_fanfic: followFanficId
        })
    })
    .then(res => res)
    .catch(err => console.log(err))
}

export function disFollowFanfic (followFanficId) {
    return $fetch('follow-stories', {
        method: 'delete',
        body: JSON.stringify({
            id: followFanficId
        })
    })
    .then(res => res)
    .catch(err => console.log(err))
}

export function followAuthor (fromUserId, toUserId) {
    return $fetch('follow-user', {
        method: 'post',
        body: JSON.stringify({
            user_from: fromUserId,
            user_to: toUserId
        })
    })
    .then(res => res)
    .catch(err => console.log(err))
}

export function disFollowAuthor (fromUserId) {
    return $fetch('follow-user', {
        method: 'delete',
        body: JSON.stringify({
            id: fromUserId
        })
    })
    .then(res => res)
    .catch(err => console.log(err))
}

export function getFollowAuthor () {
    return $fetch('follow-user')
    .then(res => res)
    .catch(err => console.log(err))
}

export function getFollowFanfic () {
    return $fetch('follow-stories')
    .then(res => res)
    .catch(err => console.log(err))
}

export function favorite (fanficId, userId) {
    return $fetch('favorite', {
        method: 'post',
        body: JSON.stringify({
            id: fanficId,
            user: userId
        })
    })
    .then(res => res)
    .catch(err => console.log(err))
}

export function unfavorite (fanficId, userId) {
    return $fetch('unfavorite', {
        method: 'post',
        body: JSON.stringify({
            id: fanficId,
            user: userId
        })
    })
    .then(res => res)
    .catch(err => console.log(err))
}
