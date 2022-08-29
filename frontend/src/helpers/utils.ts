export const getRandomUUID = () => 
    Math.random().toString(36).toString().substring(2, 15) +
    Math.random().toString(36).toString().substring(2, 15);


export const options_FR = {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
};

export const options_US = {
    day: 'numeric',
    month: 'numeric',
    year: 'numeric',
};

export const formatDate = (date, options) => {
    return new Intl.DateTimeFormat('fr-FR', options).format(date);
};

export const readMore = (text, length, suffix) => {
    return text.substring(0, length) + suffix;
};


