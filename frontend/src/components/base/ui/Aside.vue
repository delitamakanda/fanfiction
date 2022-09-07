<template>
<aside class="lg:w-64" aria-label="Sidebar">
   <div class="overflow-y-auto py-4 px-3 bg-gray-50 rounded dark:bg-gray-800">
      <ul class="space-y-2">
         <template v-if="isLoggedIn">
            <li v-for="(link, idx) of asideLinksConnected" :key="idx">
               <router-link :to="link.route" class="flex items-center p-2 text-base font-normal text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700">
                  <img  class="w-6 h-6 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white" :src="require('../../../assets/images/icons/' +link.icon + '.svg').default" />
                  <span class="ml-3 hidden lg:inline-flex">{{ $t(`message.aside.${link.title}`)}}</span>
               </router-link>
            </li>
         </template>
         <template v-if="!isLoggedIn">
            <li v-for="(link, idx) of asideLinksNotConnected" :key="idx">
               <router-link :to="link.route" class="flex items-center p-2 text-base font-normal text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700">
                  <img  class="w-6 h-6 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white" :src="require('../../../assets/images/icons/' +link.icon + '.svg').default" />
                  <span class="ml-3 hidden lg:inline-flex">{{ $t(`message.aside.${link.title}`)}}</span>
               </router-link>
            </li>
         </template>
         <template v-for="(link, idx) of asideLinks" :key="idx">
            <li>
               <template v-if="link.navigation">
                  <router-link :to="link.route" class="flex items-center p-2 text-base font-normal text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700">
                     <img  class="w-6 h-6 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white" :src="require('../../../assets/images/icons/' +link.icon + '.svg').default" />
                     <span class="ml-3 hidden lg:inline-flex">{{ $t(`message.aside.${link.title}`)}}</span>
                  </router-link>
               </template>
               <template v-if="!link.navigation && link.name === 'Forum'">
                  <a :href="link.route" target="_blank" class="flex items-center p-2 text-base font-normal text-gray-900 rounded-lg transition duration-75 hover:bg-gray-100 dark:hover:bg-gray-700 dark:text-white group">
                     <img  class="w-6 h-6 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white" :src="require('../../../assets/images/icons/' +link.icon + '.svg').default" />
                     <span class="ml-3  hidden lg:inline-flex">{{ $t(`message.aside.${link.title}`)}}</span>
                  </a>
               </template>
            </li>
         </template>
      </ul>
   </div>
</aside>
</template>

<script lang="ts">
import { computed, ref } from 'vue';
import { useStore } from 'vuex';
import { menuAside, menuAsideConnected, menuAsideNotConnected } from '../../../constants/appConstants';

export default {
   setup() {
      const store = useStore();
      const inboxMessage = ref([]) as any;
      const isLoggedIn = computed(() => store.state['auth'].status.loggedIn);

      const asideLinks = ref([]) as any;
      const asideLinksConnected = ref([]) as any;
      const asideLinksNotConnected = ref([]) as any;
      asideLinks.value = menuAside;
      asideLinksConnected.value = menuAsideConnected;
      asideLinksNotConnected.value = menuAsideNotConnected;

      const getSrc = (icon: string) => {
         return `./../../../../../assets/images/icons/${icon}.svg`;
      };


      return {
         isLoggedIn,
         inboxMessage,
         store,
         asideLinks,
         asideLinksConnected,
         asideLinksNotConnected,
         getSrc,
      };
   }
}
</script>