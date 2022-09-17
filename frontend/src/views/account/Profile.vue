<template>
<main v-if="profile" class="profile-page">
  <section class="relative py-16 bg-blueGray-200">
    <div class="container mx-auto px-4">
      <div class="relative flex flex-col min-w-0 break-words bg-white w-full mb-6">
        <div class="px-6">
          <div class="flex flex-wrap justify-center">
            <div class="w-full lg:w-3/12 px-4 lg:order-2 flex justify-center">
              <div class="relative">
                <img :alt="profile.username" v-if="profile.photo" :src="profile.photo" class="shadow-xl roundedCircle align-middle border-none">
                <Avatar v-else :email="profile.email" ref="avatar" class="shadow-xl roundedCircle align-middle border-none " />
              </div>
            </div>
            <div class="w-full lg:w-4/12 px-4 lg:order-3 lg:text-right lg:self-center">
              <div class="py-6 px-3 mt-32 sm:mt-0">
                <button class="bg-pink-500 active:bg-pink-600 uppercase text-white font-bold hover:shadow-md shadow text-xs px-4 py-2 rounded outline-none focus:outline-none sm:mr-2 mb-1 ease-linear transition-all duration-150" type="button">
                  {{ $t('message.profilePage.followButtonLabel') }}
                </button>
                <button class="bg-pink-500 active:bg-pink-600 uppercase text-white font-bold hover:shadow-md shadow text-xs px-4 py-2 rounded outline-none focus:outline-none sm:mr-2 mb-1 ease-linear transition-all duration-150" type="button">
                  {{ $t('message.profilePage.unfollowButtonLabel') }}
                </button>
              </div>
            </div>
            <div class="w-full lg:w-4/12 px-4 lg:order-1">
              <div class="flex justify-center py-4 lg:pt-4 pt-8">
                <div class="mr-4 p-3 text-center">
                  <span class="text-xl font-bold block uppercase tracking-wide text-blueGray-600">22</span><span class="text-sm text-blueGray-400">
                    {{ $t('message.profilePage.fanficsLabel') }}
                </span>
                </div>
                <div class="mr-4 p-3 text-center">
                  <span class="text-xl font-bold block uppercase tracking-wide text-blueGray-600">10</span><span class="text-sm text-blueGray-400">
                    {{ $t('message.profilePage.favAuthorsLabel') }}
                  </span>
                </div>
                <div class="lg:mr-4 p-3 text-center">
                  <span class="text-xl font-bold block uppercase tracking-wide text-blueGray-600">89</span><span class="text-sm text-blueGray-400">
                    {{ $t('message.profilePage.favFanficsLabel') }}
                </span>
                </div>
              </div>
            </div>
          </div>
          <div class="text-center mt-12">
            <h3 class="text-4xl font-semibold leading-normal mb-2 text-blueGray-700 mb-2">
              {{ profile.username }}
            </h3>
            <div v-if="profile.location" class="text-sm leading-normal mt-0 mb-2 text-blueGray-400 font-bold uppercase">
              <i class="fas fa-map-marker-alt mr-2 text-lg text-blueGray-400"></i>
              {{ profile.location }}
            </div>
          </div>
          <div v-if="profile.bio" class="mt-10 py-10 border-t border-blueGray-200 text-center">
            <div class="flex flex-wrap justify-center">
              <div class="w-full lg:w-9/12 px-4">
                <p class="mb-4 text-lg leading-relaxed text-blueGray-700">
                  {{ profile.bio }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</main>
</template>

<script lang="ts">
import Breadcrumb from '../../components/base/Breadcrumb.vue';
import Avatar from '../../components/common/Avatar.vue';
import { useRoute } from 'vue-router';
import { getCurrentProfile } from '../../api/accountApi';
import { ref, onMounted } from 'vue';
import { useStore } from 'vuex';
import { withAsync } from '../../api/helpers/withAsync';

export default {
    components: {
        Breadcrumb,
        Avatar,
    },

    setup() {
        const route = useRoute();
        const store = useStore();
        const profile = ref<any>();

        onMounted( async() => {
            const { response, error } = await withAsync(getCurrentProfile, route.params.username);
            if (response) {
                profile.value = response.data;
            }
        });

        return {
            route,
            store,
            profile,
        };
    }
}
</script>

<style lang="scss" scoped>
.roundedCircle {
    width: 150px;
    height: 150px;
    border-radius: 50%;
}
</style>