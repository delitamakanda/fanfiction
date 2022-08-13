import fanficRoutes from '../views/fanfics/fanficRoutes';
import Signin from '../views/Signin.vue';
import Signup from '../views/Signup.vue';

{
    routes: [
        {
            path: '/signin',
            name: 'Signin',
            component: Signin
        },
        {
            path: '/signup',
            name: 'Signup',
            component: Signup
        },
        ...fanficRoutes
    ]
}