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
        </fieldset> </form>
        <div>
        <h1 class="font-bold text-2xl mb-2">Fanfics</h1>
        <div v-for="fanfic of fanfics" :key="fanfic.id" class="py-1"> <p>{{ fanfic.title }}</p>
        </div> </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { searchFanfics } from '../../api/fanficApi'
import { withAsync } from '../../api/helpers/withAsync';

export default defineComponent({
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
            this.$options.abort?.();
            const { response, error } = await withAsync(searchFanfics, q, {
                abort: abort => (this.$options.abort = abort)
            });
            if (error as any) {
            // Log the error
            console.log('error', error);
                if ((error as any).aborted) {
                    console.warn("Aborted!");
                }
                return; 
            }
            this.fanfics = response.data.results;
        }
    }
})
</script>

<style lang="scss">
</style>
