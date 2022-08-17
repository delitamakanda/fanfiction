export const getRandomUUID = () => 
    Math.random().toString(36).toString().substring(2, 15) +
    Math.random().toString(36).toString().substring(2, 15);

