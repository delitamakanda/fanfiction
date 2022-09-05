const authHeader = () => {
    const token = localStorage.getItem('token');
    if (token) {
        return { Authorization: `AccessToken ${token}` };
    } else {
        return {};
    }
}

export default authHeader;
