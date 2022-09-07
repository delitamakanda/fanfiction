<template>
    <Layout class="mx-auto max-w-7xl">
        <template #header>
            <Header :title="appTitle" />
        </template>
        <template #content>
            <Loader :isVisible="loading"/>
            <div v-if="errors">{{ errors }}</div>
            <router-view></router-view>
            <!--{{ $t("message.hello", {name: "dma"}) }}
            <button @click="increase">Clicked {{ count }} times.</button> -->
        </template>
        <template #aside>
            <Aside />
        </template>
        <template #footer>
            <Footer :title="appTitle" :link="appBaseUrl" />
        </template>
    </Layout>    
</template>

<script lang="ts">
import { ref, computed } from 'vue';
import { useStore } from 'vuex'
import Layout from './layout/Layout.vue';
import Footer from './components/base/ui/Footer.vue';
import Aside from './components/base/ui/Aside.vue';
import Header from './components/base/ui/Header.vue';
import { APP_NAME, APP_BASE_URL } from './constants/appConstants';
import Loader from './components/base/Loader.vue';

export default {
    components: {
        Layout,
        Footer,
        Aside,
        Header,
        Loader,
    },
    setup() {
        const count = ref(0);
        const increase = () => {
            count.value++;
        }

        const appTitle = APP_NAME;
        const appBaseUrl = APP_BASE_URL;

        const store = useStore();
        const loading = computed(() => store.state['loader'].loading,);
        const errors = computed(() => store.state['auth'].error,);

        return {
            count,
            increase,
            appTitle,
            appBaseUrl,
            store,
            loading,
            errors,
        }
    }
}
</script>

<style lang="scss">
* {
    padding: 0;
    margin: 0;
}
</style>