<template>
<div>
    <form class="mb-8">
        <fieldset class="flex flex-col">
        <label class="mb-4 font-semibold" for="meal">Search fanfics</label>
        <input
                class="px-4 py-2 border border-gray-300 rounded-lg"
                type="text"
                autocomplete="off"
                v-model="fanficQuery"
        id="fanfic" />
        </fieldset> 
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

export default {
    components: {
        FanficLayout,
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
