<template>
<footer class="p-4 bg-white rounded-lg shadow md:flex md:items-center md:justify-between md:p-6 dark:bg-gray-800">
    <span class="text-sm text-gray-500 sm:text-center dark:text-gray-400">{{fullYear}} <a :href="link" class="hover:underline">{{title}}</a>. {{ $t("message.footer.baseLine") }}.
    </span>
    <ul class="flex flex-wrap items-center mt-3 text-sm text-gray-500 dark:text-gray-400 sm:mt-0">
        <li>
            <router-link to="/announcement"  class="mr-4 hover:underline md:mr-6 ">{{ $t("message.footer.announcementLabel") }}</router-link>
        </li>
        <li class="mr-4 hover:underline md:mr-6 ">
            <router-link to="/contact" class="hover:underline">{{ $t("message.footer.contactLabel") }}</router-link>
        </li>
        <li>
            {{ VERSION.tag }}
        </li>
    </ul>
</footer>
</template>

<script lang="ts">
import { ref } from 'vue';
import { VERSION } from '../../../constants/version';

export default {
    props: {
        title: {
            type: String,
            required: true
        },
        link: {
            type: String,
            required: true
        }
    },
    setup() {
        const fullYear = `© ${new Date().getFullYear()}`;
        
        return {
            fullYear,
            VERSION,
        }
    }
};
</script>