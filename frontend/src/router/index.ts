import { createRouter, createWebHashHistory } from 'vue-router';
import fanficRoutes from '../views/fanfics/fanficRoutes';
import accountRoutes from '../views/account/accountRoutes';
import authRoutes from '../views/auth/authRoutes';
import miscRoutes from '../views/misc/miscRoutes';
import infoRoutes from '../views/info/infoRoutes';


const routes = [
    ...authRoutes,
    ...fanficRoutes,
    ...accountRoutes,
    ...miscRoutes,
    ...infoRoutes,
]


const router = createRouter({
    history: createWebHashHistory(),
    routes,
});

export default router;
