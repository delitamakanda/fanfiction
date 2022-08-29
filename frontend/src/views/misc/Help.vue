<template>
<div>
    <h2 class="mb-4 text-3xl font-extrabold tracking-tight leading-none text-gray-900 md:text-4xl dark:text-white">{{ $t('message.aside.helpLabel')}}</h2>


<form class="flex items-center">   
    <label for="simple-search" class="sr-only">Search</label>
    <div class="relative w-full">
        <div class="flex absolute inset-y-0 left-0 items-center pl-3 pointer-events-none">
            <svg aria-hidden="true" class="w-5 h-5 text-gray-500 dark:text-gray-400" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd"></path></svg>
        </div>
        <input type="text" id="simple-search" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Search" required="" autocomplete="off" v-model="lexiqueQuery">
    </div>

</form>

<div>
    <template v-for="dico of dictionnary">
        <article class="mt-8 format lg:format-lg">
            <h1>{{ dico.group }}</h1>
            <template v-for="child of dico.children">
                <h2>{{ child.title }}</h2>
                <p class="mb-3 font-light text-gray-500 dark:text-gray-400">{{ child.definition }}</p>
            </template>
        </article>
    </template>
</div>


</div>
</template>

<script lang="ts">
import { searchLexique } from '../../api/miscApi';
import { withAsync } from '../../api/helpers/withAsync';

export default {
    data() {
        return {
            lexiqueQuery: '',
            dictionnary: null
        }
    },
    watch: {
        lexiqueQuery: {
            immediate: true,
            handler: 'initSearchLexique'
        }
    },
    methods: {
        async initSearchLexique(q) {
            (<any>this).$options.abort?.();
            const { response, error } = await withAsync(searchLexique, q, {
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
            let rawData = response.data;

            let data = rawData.reduce((r, e) => {
            // get first letter of name of current element
            let group = e.title[0];
            // if there is no property in accumulator with this letter create it
            if(!r[group]) r[group] = {group, children: [e]}
            // if there is push current element to children array for that letter
            else r[group].children.push(e);
            // return accumulator
            return r;
            }, {});
            let children = [];    // since data at this point is an object, to get array of values
            // we use Object.values method
            let result = (<any>Object).values(data);
            (<any>this).dictionnary = result;
            }
        }
}
</script>