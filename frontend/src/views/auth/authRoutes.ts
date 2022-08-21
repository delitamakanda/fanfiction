import Signin from './Signin.vue';
import Signup from './Signup.vue';


const authRoutes = [
    {
        path: '/signin',
        name: 'Signin',
        component: Signin,
        meta: {
            layout: 'auth'
        }
    },
    {
        path: '/signup',
        name: 'Signup',
        component: Signup,
        meta: {
            layout: 'auth'
        }
    },
];

export default authRoutes;
