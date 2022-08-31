<template>
<div>
    <h2 class="mb-4 text-3xl font-extrabold tracking-tight leading-none text-gray-900 md:text-4xl dark:text-white">{{ $t('message.aside.documentationLabel')}}</h2>

    <div id="accordion-flush" data-accordion="collapse" data-active-classes="bg-white dark:bg-gray-900 text-gray-900 dark:text-white" data-inactive-classes="text-gray-500 dark:text-gray-400">
        <template  v-for="(faq, idx) of faqs">
            <h2 :id="'accordion-flush-heading-'+ idx">
                <button type="button" @click="toggleItem(faq, idx)" class="flex items-center justify-between w-full py-5 font-medium text-left text-gray-500 border-b border-gray-200 dark:border-gray-700 dark:text-gray-400" :data-accordion-target="'#accordion-flush-body-'+idx" aria-expanded="true" :aria-controls="'accordion-flush-body-'+idx">
                <span>{{ faq.question }}</span>
                <svg data-accordion-icon class="w-6 h-6 shrink-0" :class="{'rotate-180': !faq.is_active}" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
                </button>
            </h2>
            <div :id="'accordion-flush-body-'+idx" :class="{'hidden': !faq.is_active }" :aria-labelledby="'accordion-flush-heading-'+idx">
                <div class="py-5 font-light border-b border-gray-200 dark:border-gray-700">
                    <p class="mb-2 text-gray-500 dark:text-gray-400"><markdown :source="faq.reponse" :html="true" :linkify="true" /></p>
                </div>
            </div>
        </template>
    </div>
</div>
</template>

<script lang="ts">
import { withAsync } from '../../api/helpers/withAsync';
import { fetchFaq } from '../../api/miscApi';
import { ref, onMounted } from 'vue';
import Markdown from 'vue3-markdown-it';

export default {
    components: {
        'markdown': Markdown
    },
    setup() {
        const faqs = ref<any>();

        const fetchFaqs = async () => {
            const { response, error } = await withAsync(fetchFaq);
            if (error) {
                return;
            }
            faqs.value = response.data.map(f => ({
                ...f,
                is_active: false,
            }));
        }

        const toggleItem = (item, idx) => {
            item.is_active = !item.is_active;
        }

        onMounted(() => {
            fetchFaqs();
        });

        return {
            faqs,
            fetchFaqs,
            toggleItem,
        }
    }
}
</script>