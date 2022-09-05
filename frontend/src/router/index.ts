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
    scrollBehavior(to, from, savedPosition) {
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                resolve({ 
                    left: 0, 
                    top: 0,
                    behavior: 'smooth'
                })
            }, 200)
        })
    },
});

router.beforeEach((to, from, next) => {
    if (to.matched.some(record => record.meta.requiresAuth)) {
        if (!localStorage.getItem('token')) {
            next({
                path: '/signin',
                query: { redirect: to.fullPath }
            })
        } else {
            next()
        }
    } else {
        next()
    }
});

export default router;
