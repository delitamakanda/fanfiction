<template>
<div>
    <TagProvider
        trackBy="id"
        @on-tag-added="onTagAdded"
        @on-tag-removed="onTagDeleted"
        :options="$options.defaultTags"
        >
        <template #default="{ tags, addTag, removeTag }">
        <div>
        <!-- Vertical stack --> <div vertical class="mb-4">
                <!-- Label -->
        <label class="mb-2" for="tag-input">Tags</label> <!-- Horizontal stack -->
        <div
                    v-if="tags.length"
                    class="flex space-x-3 tagsContainer">
                    <!-- Loop through tags -->
        <Tag v-for="tag of tags" :key="tag.id" class="mb-2"> <div class="tagContent">
                        <!-- Tag text -->
        <span class="tagText"> {{ tag.text }}
        </span>
        <!-- Delete tag icon --> <button
                        class="tagDeleteIcon"
                        @click.prevent="removeTag(tag.id)"
                        >
        x </button>
        </div> </Tag>
        </div>
        <!-- Add new tag input --> <input
                    v-model="value"
                    type="text"
                    id="tag-input"
                    placeholder="Add a tag..."
        /> </div>
                <!-- Submit tag -->
        <BaseButton @click.prevent="onAddTag(addTag)">Add tag</BaseButton> </div>
        </template>
    </TagProvider>

    <Select :options="$options.selectedOptions" v-model="selected" label="label" caption="select at least 1 option">
        <template v-slot:option="{ option }" >
        <div class="option">
            <img class="img" :src="option.src" :alt="option.label" />
            <span> {{ option.label }}</span>
        </div>
        </template>
    </Select>

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

        <BaseButton v-if="more_exist" @click="loadMore">Load more</BaseButton>
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
import { getRandomUUID } from '../../helpers/utils';
import Select from '../../components/common/Select.vue';
import TagProvider from '../../components/common/TagProvider.vue';
import Tag from '../../components/common/Tag.vue';

export default {
    components: {
    FanficLayout,
    Layout,
    Select,
    TagProvider,
    Tag,
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
            fanficQuery: '',
            selected: '',
            value: '',
            next_url: '',
            pageNumber: null,
            more_exist: false,
            count: null,
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
            let hasMore = false;
            (<any>this).count = response?.data?.count;
            if (response?.data?.next) {
                hasMore = true;
                (<any>this).next_url = response?.data?.next;
                const url = new URL(response?.data?.next);
                const params = url.searchParams;
                (<any>this).pageNumber = params.get('page');
                (<any>this).more_exist = hasMore;
            }
            (<any>this).fanfics = response.data.results;
            (<any>this).more_exist = hasMore;
        },
        async loadMore() {
            // load more button
            let hasMore = false;
            const { response, error } = await withAsync(searchFanfics, (<any>this).fanficQuery, {}, (<any>this).pageNumber);
            if (error as any) {
                // Log the error
                console.log('error', error);
                return; 
            }
            (<any>this).count = response.data.count;
            if (response.data.next) {
                hasMore = true;
                (<any>this).next_url = response.data.next;
                const url = new URL(response.data.next);
                const params = url.searchParams;
                (<any>this).pageNumber = params.get('page');
                (<any>this).more_exist = hasMore;
                (<any>this).fanfics = (<any>this).fanfics.concat(response.data.results);
            }
            (<any>this).more_exist = hasMore;

        },
        onTagAdded({ tags, val }) {
            console.log("Tag added", { tags, val });
        },
        onTagDeleted({ tags, val }) {
            console.log("Tag deleted", { tags, val });
        },
        onAddTag(addTag) {
            // addTag is coming from the TagsProvider
            addTag({ id: getRandomUUID(), text: (<any>this).value }); 
            (<any>this).value = "";
        },
    },
    created() {
        (<any>this).$options.selectedOptions = [
            {
                src: "https://picsum.photos/id/100/75/50",
                label: "Option One",

            },
            {
                src: "https://picsum.photos/id/10/75/50",
                label: "Option Two",

            },
            {
                src: "https://picsum.photos/id/20/75/50",
                label: "Option Three",

            },
        ];

        (<any>this).$options.defaultTags = [
            {
                id: getRandomUUID(),
                text: "Apple",
            },
            {
                id: getRandomUUID(),
                text: "Orange",
            }, 
            {
                id: getRandomUUID(),
                text: "Banana",
            },
        ];
    }
}
</script>

<style lang="scss">
.option {
    display: flex;
}

.img {
    display: block;
    max-width: 75px;
    max-height: 50px;
    margin-right: 10px;
}

.tagsContainer {
    display: flex;
    flex-wrap: wrap;
}

.tagContent {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.tagText{
    font-weight: semibold;
}

.tagDeleteIcon {
    margin-left: 2px;
    cursor: pointer;
}
</style>
