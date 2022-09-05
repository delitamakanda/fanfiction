class TokenService {
    getRefreshToken() {
        return localStorage.getItem('refreshToken');
    }

    getAccessToken() {
        return localStorage.getItem('token');
    }

    updateAccessToken(token: string) {
        let accessToken = localStorage.getItem('token');
        accessToken = token;
        localStorage.setItem('token', accessToken);
    }
}

export default new TokenService();
