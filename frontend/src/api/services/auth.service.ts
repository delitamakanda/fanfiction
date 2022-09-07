import { login, signup, logout, refreshToken } from '../../api/authApi';
import { withAsync } from '../../api/helpers/withAsync';


class AuthService {
    async connect(username: string, password: string) {
        const { response, error } = await withAsync(login, { username, password })
        if (response && response.data && response.data.access) {
            localStorage.setItem('token', (response as any).data.access);
            localStorage.setItem('refreshToken', (response as any).data.refresh);
        }
        return { response, error };
    }
    async logout() {
        const { response, error } = await withAsync(logout);
        if (response && response.data && response.data.status === 'ok') {
            localStorage.removeItem('token');
            localStorage.removeItem('refreshToken');
        }
        return {response, error};
    }
    async register(data) {
        const { response, error } = await withAsync(signup, data);
        return {response, error};
    }
    async refresh(token) {
        const { response, error } = await withAsync(refreshToken, token);
        return {response, error};
    }
}

export default new AuthService();
