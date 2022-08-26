<template>

<nav class="bg-white border-gray-200 px-2 sm:px-4 py-2.5 rounded dark:bg-gray-900">
  <div class="container flex flex-wrap justify-between items-center mx-auto">
  <router-link to="/" class="flex items-center">
      <img src="./../../../assets/images/logo.png" class="mr-3 h-6 sm:h-9" :alt="title">
      <span class="self-center text-xl font-semibold whitespace-nowrap dark:text-white">{{title}}</span>
  </router-link>
  <div class="flex items-center md:order-2">
      <button type="button" @click="openNotificationModal" class="bg-white p-1 rounded-full text-gray-400 hover:text-gray-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-800 focus:ring-gray-300">
              <span class="sr-only">View notifications</span>
              <!-- Heroicon name: outline/bell -->
              <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
              </svg>
      </button>

      <router-link to="/dashboard" type="button" class="flex mr-3 text-sm bg-gray-800 rounded-full md:mr-0 focus:ring-4 focus:ring-gray-300 dark:focus:ring-gray-600" id="user-menu-button" aria-expanded="false">
        <span class="sr-only">Open user menu</span>
        <!-- <img class="w-8 h-8 rounded-full" src="./../../../assets/images/logo.png" alt="user photo"> -->
        <avatar ref="avatar" email="name@flowbite.com" />
      </router-link>
    </div>
  </div>
</nav>
</template>

<script lang="ts">
import { useRouter } from 'vue-router';
import Avatar from '../../common/Avatar.vue';
import { ref, onMounted, getCurrentInstance } from 'vue';

const options = {
  placement: 'right',
  backdrop: true,
  bodyScrolling: false,
  edge: false,
  edgeOffset: '',
  backdropClasses: 'bg-gray-900 bg-opacity-50 dark:bg-opacity-80 fixed inset-0 z-30',
  onHide: () => {
    console.log('drawer is hidden');
  },
  onShow: () => {
    console.log('drawer is shown');
  },
  onToggle: () => {
    console.log('drawer has been toggled');
  }
};


export default {
  components: {
    'avatar': Avatar
  },
  props: {
    title: {
      type: String,
      required: true
      }
    },
  setup(props, ctx) {
    const $router = useRouter();
    
    const openNotificationModal = () => {
      console.log('todo open modal');
    };

   
    const logout = () => {
      $router.push('signin');
    }

    return {
      $router,
      logout,
      openNotificationModal,
    };
  }
}
</script>