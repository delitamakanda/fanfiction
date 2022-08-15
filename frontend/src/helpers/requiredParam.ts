export const requiredParam = (param = '') => {
    const msg = `Param ${param} is required`;
    console.error(msg);
    throw new Error(msg);
}