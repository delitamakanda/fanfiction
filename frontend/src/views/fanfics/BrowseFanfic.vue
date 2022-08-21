<template>
<div>
    <div class="space-x-4 mb-8 mx-auto flex justify-center items-center mt-4"> 
        <button @click.prevent="setLayout(LAYOUTS.standard)">Layout standard </button>
        <button @click.prevent="setLayout(LAYOUTS.auth)"> Layout auth</button>
    </div>
    <Layout class="mx-auto max-w-7xl">
        <template #header>
            <p>Header</p>
        </template>
        <template #content>
            <p>Content</p>
        </template>
        <template #aside>
            <p>Aside</p>
        </template>
        <template #footer>
            <p>Footer</p>
        </template>
    </Layout>
</div>
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
        const {setLayout, LAYOUTS } = useLayout();
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