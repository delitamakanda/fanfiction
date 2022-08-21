import { createWebHashHistory, createRouter } from 'vue-router';
import fanficRoutes from '../views/fanfics/fanficRoutes';
import accountRoutes from '../views/account/accountRoutes';
import authRoutes from '../views/auth/authRoutes';


const routes = [
    ...authRoutes,
    ...fanficRoutes,
    ...accountRoutes,
]


const router = createRouter({
    history: createWebHashHistory(),
    routes,
});

export default router;
