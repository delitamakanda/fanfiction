<template>

<nav class="bg-white border-gray-200 px-2 sm:px-4 py-2.5 rounded dark:bg-gray-900">
  <div class="container flex flex-wrap justify-between items-center mx-auto">
  <router-link to="/" class="flex items-center">
      <img src="./../../../assets/images/logo.png" class="mr-3 h-6 sm:h-9" :alt="title">
      <span class="self-center text-xl font-semibold whitespace-nowrap dark:text-white">{{title}}</span>
  </router-link>
  <div class="flex items-center md:order-2">
      <button type="button" @click.prevent="openNotificationModal" class="bg-white p-1 rounded-full text-gray-400 hover:text-gray-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-800 focus:ring-gray-300">
              <span class="sr-only">View notifications</span>
              <!-- Heroicon name: outline/bell -->
              <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
              </svg>
      </button>
      <panel-modal :open="isPanelOpen">
        <lazy-panel-content v-if="loadPanelContent" @close-panel="closeNotificationModal" @retry="onRetry"></lazy-panel-content>
      </panel-modal>

      <button to="/dashboard" type="button" class="flex mr-3 text-sm bg-gray-800 rounded-full md:mr-0 focus:ring-4 focus:ring-gray-300 dark:focus:ring-gray-600" id="user-menu-button" aria-expanded="false">
        <span class="sr-only">Open user menu</span>
        <!-- <img class="w-8 h-8 rounded-full" src="./../../../assets/images/logo.png" alt="user photo"> -->
        <avatar ref="avatar" email="name@flowbite.com" />
      </button>
    </div>
  </div>
</nav>
</template>

<script lang="ts">
import { useRouter } from 'vue-router';
import Avatar from '../../common/Avatar.vue';
import { ref, onMounted, getCurrentInstance, defineAsyncComponent } from 'vue';
import PanelModal from '../../base/PanelModal.vue';
import LoadingComponent from '../../base/LoadingComponent.vue';
import ErrorComponent from '../../base/ErrorComponent.vue';

const LazyPanelContentLoader = () => 
  new Promise<any>((resolve, reject) => {
    setTimeout(() => {
      resolve(import('../../base/PanelModalContent.vue'));
    }, 3000);
});

const lazyPanelContent = defineAsyncComponent({
  loader: LazyPanelContentLoader,
  loadingComponent: LoadingComponent,
  errorComponent: ErrorComponent,
  delay: 200,
  timeout: 15000,
  onError: (error, retry, fail, attemps) => {
    if (error.message.match(/fetch/) && attemps <= 3) {
      retry();
    } else {
      fail();
    }
  },
});


export default {
  components: {
    'avatar': Avatar,
    'panel-modal': PanelModal,
    'lazy-panel-content': lazyPanelContent,
  },
  props: {
    title: {
      type: String,
      required: true
      }
    },
  setup() {
    const $router = useRouter();
    const isPanelOpen = ref(false);
    const loadPanelContent = ref(false);
    
    const openNotificationModal = () => {
      isPanelOpen.value = true;
      loadPanelContent.value = true;
    };

    const closeNotificationModal = () => {
      isPanelOpen.value = false;
    };

    const onRetry = async () => {
      loadPanelContent.value = false;
      await (<any>this).$nextTick();
      loadPanelContent.value = true;
    };

   
    const logout = () => {
      $router.push('signin');
    }

    return {
      $router,
      logout,
      openNotificationModal,
      closeNotificationModal,
      isPanelOpen,
      loadPanelContent,
      onRetry,
    };
  }
}
</script>