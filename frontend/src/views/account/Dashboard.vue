<template>
<div>
    dashboard
    <BaseButton @click="disconnect()">Logout</BaseButton>
</div>
</template>

<script lang="ts">
import { useRouter } from 'vue-router';
import { onMounted } from 'vue';
import { useStore } from 'vuex';
import BaseButton from '../../components/base/BaseButton.vue';


export default {
    components: {
        BaseButton,
    },
    setup() {
        const store = useStore();
        const $router = useRouter();

        const disconnect = () => {
            store.dispatch('auth/logout');
            $router.push({ name: 'Signin' });
        };

        onMounted(() => {
            store.dispatch('user/fetchCurrentUser');
            
        });
        
        return {
            store,
            $router,
            disconnect,
        }
    }
}
</script>