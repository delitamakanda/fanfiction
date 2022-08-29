<template>
<footer class="p-4 bg-white rounded-lg shadow md:flex md:items-center md:justify-between md:p-6 dark:bg-gray-800">
    <span class="text-sm text-gray-500 sm:text-center dark:text-gray-400">{{fullYear}} <a :href="link" class="hover:underline">{{title}}</a>. {{ $t("message.footer.baseLine") }}.
    </span>
    <ul class="flex flex-wrap items-center mt-3 text-sm text-gray-500 dark:text-gray-400 sm:mt-0">
        <li>
            <router-link to="/announcement"  class="mr-4 hover:underline md:mr-6 ">{{ $t("message.footer.announcementLabel") }}</router-link>
        </li>
        <template v-if="pages && pages.length">
            <li v-for="page of pages" :key="page.id">
                <router-link :to="`/static-page/${page.type}`" class="mr-4 hover:underline md:mr-6">{{ $t(`message.footer.${page.type}Label`) }}</router-link>
            </li>
        </template>
        <li>
            <router-link to="/contact" class="hover:underline">{{ $t("message.footer.contactLabel") }}</router-link>
        </li>
    </ul>
</footer>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { withAsync } from '../../../api/helpers/withAsync';
import { fetchPages } from '../../../api/infoApi';

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
        
        const pages = ref<any[]>([]);

        const getPages = async () => {
            const { response, error } = await withAsync(fetchPages);
            if (error) {
                return;
            }
            pages.value = response.data;
        }
        onMounted(() => {
            getPages();
        });
        return {
            fullYear,
            getPages,
            pages,
        }
    }
});
</script>