<template>
  <!-- component -->
  <div class="rounded-xl border p-5 shadow-md w-full bg-white mt-5">
    <div class="flex w-full items-center justify-between border-b pb-3">
      <router-link :to="`/profile/${fanfic.author}`">
        <div class="flex items-center space-x-3">
          <Avatar ref="avatar" :email="fanfic.author_email" class="h-8 w-8 rounded-full bg-slate-400" />
          <div class="text-lg font-bold text-slate-700">{{ fanfic.author }}</div>
        </div>
      </router-link>
      <div class="flex items-center space-x-8">
        <button class="rounded-2xl border bg-neutral-100 px-3 py-1 text-xs font-semibold">{{ fanfic.category }}</button>
        <div class="text-xs text-neutral-500">{{ format(fanfic.publish) }}</div>
      </div>
    </div>

    <router-link :to="`/basic-fanfic-details/${fanfic.slug}`">
      <div class="mt-4 mb-6">
        <div class="mb-3 text-xl font-bold">{{ fanfic.title }}</div>
        <div class="text-sm text-neutral-600">{{ truncate(fanfic.synopsis, 130, '...') }}</div>
      </div>
      <div>
        <div class="flex items-center justify-between text-slate-500">
          <div class="flex space-x-4 md:space-x-8">
            <div class="flex cursor-pointer items-center transition hover:text-slate-600">
              <svg class="mr-1.5 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z">
                </path>
              </svg>
              <span>{{ fanfic.views }}</span>
            </div>
            <div class="flex cursor-pointer items-center transition hover:text-slate-600">
              <svg xmlns="http://www.w3.org/2000/svg" class="mr-1.5 h-5 w-5" fill="none" viewBox="0 0 24 24"
                stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round"
                  d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095c-.5 0-.905.405-.905.905 0 .714-.211 1.412-.608 2.006L7 11v9m7-10h-2M7 20H5a2 2 0 01-2-2v-6a2 2 0 012-2h2.5" />
              </svg>
              <span>{{ fanfic.total_likes }}</span>
            </div>
          </div>
        </div>
      </div>
    </router-link>

  </div>
</template>

<script lang="ts">
import Avatar from '../../common/Avatar.vue';
import { formatDate, options_FR, readMore } from '../../../helpers/utils';

export default {
  components: {
    Avatar
  },
  props: {
    fanfic: {
      type: Object,
      required: true,
    },
  },
  setup() {
    const format = (date: string) => {
      return formatDate(new Date(date), options_FR);
    };

    const truncate = (text, limit, suffix) => {
      return readMore(text, limit, suffix);
    };

    return {
      format,
      truncate,
    };
  },
};
</script>

<style scoped></style>