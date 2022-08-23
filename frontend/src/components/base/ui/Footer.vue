<template>
<footer class="p-4 bg-white rounded-lg shadow md:flex md:items-center md:justify-between md:p-6 dark:bg-gray-800">
    <span class="text-sm text-gray-500 sm:text-center dark:text-gray-400">{{fullYear}} <a :href="link" class="hover:underline">{{title}}</a>. {{ $t("message.footer.baseLine") }}.
    </span>
    <ul class="flex flex-wrap items-center mt-3 text-sm text-gray-500 dark:text-gray-400 sm:mt-0">
        <li>
            <a href="#" class="mr-4 hover:underline md:mr-6 ">{{ $t("message.footer.aboutLabel") }}</a>
        </li>
        <li>
            <a href="#" class="mr-4 hover:underline md:mr-6">{{ $t("message.footer.privacyPolicyLabel") }}</a>
        </li>
        <li>
            <a href="#" class="mr-4 hover:underline md:mr-6">{{ $t("message.footer.licensingLabel") }}</a>
        </li>
        <li>
            <a href="#" class="hover:underline">{{ $t("message.footer.contactLabel") }}</a>
        </li>
    </ul>
</footer>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';

export default defineComponent({
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
        }
    }
});
</script>