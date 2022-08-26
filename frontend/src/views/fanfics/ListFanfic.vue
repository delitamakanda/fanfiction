<template>
<div>
    <form class="flex items-center">   
        <label for="simple-search" class="sr-only">Search</label>
        <div class="relative w-full">
            <div class="flex absolute inset-y-0 left-0 items-center pl-3 pointer-events-none">
                <svg aria-hidden="true" class="w-5 h-5 text-gray-500 dark:text-gray-400" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd"></path></svg>
            </div>
            <input type="text" id="simple-search" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Search" required="" autocomplete="off" v-model="fanficQuery">
        </div>

    </form>
    <div>
        <h1 class="font-bold text-2xl mb-2">Fanfics</h1>
        <div class="space-x-4 mb-8 mx-auto flex justify-center items-center mt-4"> 
            <button @click.prevent="setLayout(LAYOUTS.grid)">Layout grid</button>
            <button @click.prevent="setLayout(LAYOUTS.list)">Layout list</button>
        </div>
        <FanficLayout class="mx-auto max-w-7-xl">
            <component :is="fanficCardComponent" v-for="fanfic of fanfics" :key="fanfic.id" :fanfic="fanfic" /> 
        </FanficLayout>
    </div>
</div>
</template>

<script lang="ts">
import { computed } from 'vue';
import { searchFanfics } from '../../api/fanficApi'
import { withAsync } from '../../api/helpers/withAsync';
import { useFanficLayout, FanficLayout} from '../../layout/composables/useFanficLayout';
import FanficGridCard from './components/FanficGridCard.vue';
import FanficListCard from './components/FanficListCard.vue';
import Layout from '../../layout/Layout.vue';

export default {
    components: {
        FanficLayout,
        Layout,
    },
    setup() {
        const { layout, setLayout, LAYOUTS } = useFanficLayout();

        const fanficLayoutComponents = {
            [LAYOUTS.grid]: FanficGridCard,
            [LAYOUTS.list]: FanficListCard,
        };

        const fanficCardComponent = computed(
            () => fanficLayoutComponents[layout.value]
        );

        return {
            fanficCardComponent,
            LAYOUTS,
            setLayout,
        }
    },
    data() {
        return {
            fanfics: null,
            apiStatus: null,
            fanficQuery: ''
        }
    },
    watch: {
        fanficQuery: {
            immediate: true,
            handler: 'initSearchFanfics'
        }
    },
    methods: {
        async initSearchFanfics(q) {
            (<any>this).$options.abort?.();
            const { response, error } = await withAsync(searchFanfics, q, {
                abort: abort => ((<any>this).$options.abort = abort)
            });
            if (error as any) {
            // Log the error
            console.log('error', error);
                if ((error as any).aborted) {
                    console.warn("Aborted!");
                }
                return; 
            }
            (<any>this).fanfics = response.data.results;
        }
    }
}
</script>

<style lang="scss">
</style>
