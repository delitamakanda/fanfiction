export const withAsync = async (fn, ...args) => {
    try {
        const response = await fn(...args);
        return {
            response,
            error: null,
        }
    } catch (error) {
        return {
            response: null,
            error
        }
    }
};
