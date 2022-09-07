<template>
<div>
    <h2 v-if="currentUser" class="text-4xl font-extrabold dark:text-white">{{ $t("message.hello", {name: currentUser.username}) }}</h2>
    <Breadcrumb />
    <div class="w-full dark:bg-gray-800">
        <div class="grid grid-cols-3 gap-4 p-4 lg:grid-cols-4">
            <template v-for="(menu, idx) in menus" :key="idx">
                <div class="p-4 rounded-lg cursor-pointer bg-gray-50 hover:bg-gray-100 dark:hover:bg-gray-600 dark:bg-gray-700" @click="navigate(menu)">
                    <div class="flex justify-center items-center p-2 mx-auto mb-2 max-w-[48px] bg-gray-200 dark:bg-gray-500 rounded-full w-18 h-18">
                        <img  class="w-6 h-6 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white" :src="require('../../assets/images/icons/' +menu.icon + '.svg').default" />
                    </div>
                    <div class="font-medium text-center text-gray-500 dark:text-gray-400">{{ $t(`message.dashboard.${menu.title}`) }}</div>
                </div>
            </template>
        </div>
    </div>
</div>
</template>

<script lang="ts">
import { useRouter } from 'vue-router';
import { onMounted, computed, ref } from 'vue';
import { useStore } from 'vuex';
import { menuDashboard } from '../../constants/appConstants';

export default {
    setup() {
        const store = useStore();
        const $router = useRouter();

        const disconnect = () => {
            store.dispatch('auth/logout');
            $router.push({ name: 'Signin' });
        };

        const currentUser = computed(() => store.getters['user/user']);

        const menus = ref([]) as any;
        menus.value  = menuDashboard;



        onMounted(() => {
            store.dispatch('user/fetchCurrentUser'); 
        });

        const navigate = (objMenu: any) => {
            if (!objMenu.navigation && objMenu.route === 'disconnect') {
                disconnect();
            } else {
                $router.push(objMenu.route);
            }
        };
        
        return {
            store,
            $router,
            disconnect,
            currentUser,
            menus,
            navigate,
        }
    }
}
</script>