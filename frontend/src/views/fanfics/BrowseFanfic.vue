<template>
<!-- <div class="space-x-4 mb-8 mx-auto flex justify-center items-center mt-4"> 
    <button @click.prevent="setLayout(LAYOUTS.standard)">Layout standard </button>
    <button @click.prevent="setLayout(LAYOUTS.auth)"> Layout auth</button>
</div> -->
<Layout class="mx-auto max-w-7xl">
    <template #header>
        <p>Header</p>
    </template>
    <template #content>
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
        <button @click.prevent="onAddTag(addTag)">Add tag</button> </div>
        </template>
    </TagProvider>

    <br/><br/>
    <p v-if="fetchHomeFanficsStatusIdle">Welcome</p>
    <BaseLazyLoad :show="fetchHomeFanficsStatusPending">
        <p>Loading data</p>
    </BaseLazyLoad>
    <Select :options="$options.selectedOptions" v-model="selected" label="label" caption="select at least 1 option">
        <template v-slot:option="{ option }" >
        <div class="option">
            <img class="img" :src="option.src" :alt="option.label" />
            <span> {{ option.label }}</span>
        </div>
        </template>
    </Select>
    <p v-if="fetchHomeFanficsStatusError">There was a problem.</p>
    <template v-if="fetchHomeFanficsStatusSuccess">
        <div v-for="fanfic of homeFanfics">
            {{ fanfic.title }}
        </div>
    </template>
    <base-button>click</base-button>
    <base-input></base-input>
    </template>
    <template #aside>
        <p>Aside</p>
    </template>
    <template #footer>
        <p>Footer</p>
    </template>
</Layout>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { fetchHomeFanfics } from '../../api/fanficApi'
import { apiStatus } from '../../api/constants/apiStatus';
import { withAsync } from '../../api/helpers/withAsync';
import { apiStatusComputedFactory } from '../../api/helpers/apiStatusComputedFactory';
import BaseLazyLoad from '../../components/base/BaseLazyLoad.vue';
import Select from '../../components/common/Select.vue';
import TagProvider from '../../components/common/TagProvider.vue';
import Tag from '../../components/common/Tag.vue';
import { getRandomUUID } from '../../helpers/utils';
import Layout from '../../layout/Layout.vue';
import { useLayout } from "../../layout/composables/useLayout";

const { IDLE, PENDING, SUCCESS, ERROR } = apiStatus;

export default defineComponent({
    components: { 
        BaseLazyLoad,
        Select,
        TagProvider,
        Tag,
        Layout,
    },
    setup() {
        const { setLayout, LAYOUTS } = useLayout();
        return {
            setLayout,
            LAYOUTS,
        }
    },
    computed: {
        ...apiStatusComputedFactory(['fetchHomeFanficsStatus', 'updateHomeFanficsStatus'])
    },
    data() {
        return {
            homeFanfics: null,
            fanfics: null,
            fetchHomeFanficsStatus: apiStatus.IDLE,
            apiStatus: null,
            fanficQuery: '',
            selected: '',
            value: ''
        }
    },
    watch: {
        fanficQuery: {
            immediate: true,
            handler: 'initSearchFanfics'
        }
    },
    methods: {
        async fetchHomeFanfics() {
            this.fetchHomeFanficsStatus = apiStatus.PENDING;
            const { response, error } = await withAsync(fetchHomeFanfics);
            if (error) {
                this.fetchHomeFanficsStatus = apiStatus.ERROR;
                return;
            }
            this.homeFanfics = response.data.most_liked_fanfics;
            this.fetchHomeFanficsStatus = apiStatus.SUCCESS;
        },
        onTagAdded({ tags, val }) {
            console.log("Tag added", { tags, val });
        },
        onTagDeleted({ tags, val }) {
            console.log("Tag deleted", { tags, val });
        },
        onAddTag(addTag) {
            // addTag is coming from the TagsProvider
            addTag({ id: getRandomUUID(), text: this.value }); 
            this.value = "";
        },
    },
    created() {
        apiStatus;
        this.fetchHomeFanfics();
        this.$options.selectedOptions = [
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
        ],

        this.$options.defaultTags = [
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
});
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