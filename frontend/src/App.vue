<template>
  <Layout class="mx-auto max-w-7xl">
    <template #header>
      <Header :title="appTitle" />
    </template>
    <template #content>
      <Loader :isVisible="loading" />
      <div v-if="toaster.open">
        <Toaster :msg="toaster.message" :type="toaster.type" />
      </div>
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
import Toaster from './components/common/Toaster.vue';

export default {
  components: {
    Layout,
    Footer,
    Aside,
    Header,
    Loader,
    Toaster,
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
    const toaster = computed(() => store.state['snackbar'].snackbar,);

    if (store.state['auth'].status.loggedIn) {
      store.dispatch('user/fetchCurrentUser');
    }


    return {
      count,
      increase,
      appTitle,
      appBaseUrl,
      store,
      loading,
      toaster,
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