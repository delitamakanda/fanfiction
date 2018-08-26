import Vue from 'vue'
import Router from 'vue-router'
import state from '../state'
import List from '@/components/List'
import Detail from '@/components/Detail'
import Login from '@/components/Login'
import Posts from '@/components/Posts'
import PostDetail from '@/components/PostDetail'
import Dashboard from '@/components/Dashboard'
import ListUserFanfic from '@/components/ListUserFanfic'
import UpdateFanfic from '@/components/UpdateFanfic'
import UpdateChapter from '@/components/UpdateChapter'
import NewFanfic from '@/components/NewFanfic'
import NewChapter from '@/components/NewChapter'
import Fanfic from '@/components/Fanfic'
import ChangePassword from '@/components/ChangePassword'
import ShowUserFanfic from '@/components/ShowUserFanfic'
import Loading from '@/components/Loading'
import Form from '@/components/Form'
import Input from '@/components/Input'

import VueFetch from '../plugins/fetch'
import VeeValidate from 'vee-validate'
import VueSVGIcon from 'vue-svgicon'
import VueTrumbowyg from 'vue-trumbowyg';

Vue.component('Loading', Loading)
Vue.component('Form', Form)
Vue.component('Input', Input)

Vue.use(Router)
Vue.use(VueFetch, {
    baseUrl: 'api/'
})
Vue.use(VeeValidate)
Vue.use(VueSVGIcon)
Vue.use(VueTrumbowyg)

import 'trumbowyg/dist/ui/trumbowyg.css'

const router = new Router({
    routes: [
        { path: '/', name: 'List', component: List, meta: {
            title: 'Toutes les fanfictions',
            metaTags: [
                {
                    name: 'description',
                    content: 'Fanfictions basées sur des Animés, mangas, films, romans, faits historiques, etc.'
                },
                {
                    property: 'og:description',
                    content: 'Fanfictions basées sur des Animés, mangas, films, romans, faits historiques, etc.'
                }
            ]
        } },
        { path: '/fanfic/detail/:slug', name: 'Detail', component: Detail, props: true},
        { path: '/login', name: 'Login', component: Login, meta: { guest: true, title: 'Créer un compte ou se connecter à l\'espace membre' } },
        { path: '/news', name: 'Posts', component: Posts, meta: {
            title: 'News du site Fanfiction',
            metaTags: [
                {
                    name: 'description',
                    content: 'Toutes les nouveautés et annonces du site.'
                },
                {
                    property: 'og:description',
                    content: 'Toutes les nouveautés et annonces du site.'
                }
            ]
        } },
        { path: '/news/:slug', name: 'PostDetail', component: PostDetail, props: true },
        { path: '/dashboard', name: 'Dashboard', component: Dashboard, meta: { private: true, title: 'Tableau de bord' },
            children: [
                { path: '/fanfics', name: 'ListUserFanfic', component: ListUserFanfic, title: 'Vos fanfictions' },
                { path: '/create', name: 'NewFanfic', component: NewFanfic, title: 'Ecrire une fanfiction' },
                { path: '/update/:id/edit', name: 'UpdateFanfic', component: UpdateFanfic, props: true, title: 'Editer une fanfiction' },
                { path: '/new/:id/chapter', name: 'NewChapter', component: NewChapter, props: true, title: 'Ecrire un chapitre' },
                { path: '/update/:id/chapter/:chapter_id/edit', name: 'UpdateChapter', component: UpdateChapter, props: true, title: 'Editer un chapitre' },
                { path: '/fanfic/:id', name: 'Fanfic', component: Fanfic, props: true, title: 'Voir la fanfiction' },
                { path: '/change-password', name: 'ChangePassword', component: ChangePassword, title: 'Changer le mot de passe' },
            ]
        },
        { path: '*', component: List },
        { path: '/fanfics/:username/show', name: 'ShowUserFanfic', component: ShowUserFanfic, props: true, title: 'Voir les fanfictions d\'un utilisateur' },
    ],
    mode: 'hash',
    scrollBehavior (to, from, savedPosition) {
        if (savedPosition) {
            return savedPosition
        }
        if (to.hash) {
            return { selector: to.hash }
        }
        return { x: 0, y: 0 }
    },
})

router.beforeEach((to, from, next) => {

    if (to.meta.private) {
        // TODO:  redirect to login
    }

    if (to.matched.some(r => r.meta.private) && !state.user && state.user.id == null) {
        next({
            name: 'Login',
            params: {
                wantedRoute: to.fullPath,
            },
        })
        return
    }

    if ( to.matched.some(r => r.meta.guest) && state.user && state.user.id != null) {
        next({name: 'Dashboard'})
        return
    }

    const nearestWithTitle = to.matched.slice().reverse().find(r => r.meta && r.meta.title);
    const nearestWithMeta = to.matched.slice().reverse().find(r => r.meta && r.meta.metaTags);
    const previousNearestWithMeta = from.matched.slice().reverse().find(r => r.meta && r.meta.metaTags);

    if(nearestWithTitle) document.title = nearestWithTitle.meta.title;

    Array.from(document.querySelectorAll('[data-vue-router-controlled]')).map(el => el.parentNode.removeChild(el));

    if(!nearestWithMeta) return next();

    nearestWithMeta.meta.metaTags.map(tagDef => {
        const tag = document.createElement('meta');
        Object.keys(tagDef).forEach(key => {
          tag.setAttribute(key, tagDef[key]);
        });

        tag.setAttribute('data-vue-router-controlled', '');

        return tag;
      })
      .forEach(tag => document.head.appendChild(tag));

    next()
})

export default router
