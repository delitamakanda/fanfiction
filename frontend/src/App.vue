<template>
    <div>
        <p v-if="fetchHomeFanficsStatusIdle">Welcome</p>
        <BaseLazyLoad :show="fetchHomeFanficsStatusPending">
            <p>Loading data</p>
        </BaseLazyLoad>
        <Select :options="$options.selectedOptions" v-model="value" label="label" caption="select at least 1 option">
            <template v-slot:option="{ option }" >
            <div class="option">
                <img class="img" :src="option.src" :alt="option.label" />
                <span> {{ option.label }}</span>
            </div>
            </template>
        </Select>
        <p v-if="fetchHomeFanficsStatusError">There was a problem.</p>
        {{ $t("message.hello", {name: "dma"}) }}
        <button @click="increase">Clicked {{ count }} times.</button>
        <template v-if="fetchHomeFanficsStatusSuccess">
            <div v-for="fanfic of homeFanfics">
                {{ fanfic.title }}
            </div>
        </template>

        <form class="mb-8">
        <fieldset class="flex flex-col">
        <label class="mb-4 font-semibold" for="meal">Search fanfics</label> <input
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
        <base-button>click</base-button>
        <base-input></base-input>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { fetchHomeFanfics, searchFanfics } from './api/fanficApi'
import { apiStatus } from './api/constants/apiStatus';
import { withAsync } from './api/helpers/withAsync';
import { apiStatusComputedFactory } from './api/helpers/apiStatusComputedFactory';
import BaseLazyLoad from './components/base/BaseLazyLoad.vue';
import Select from './components/common/Select.vue';

const { IDLE, PENDING, SUCCESS, ERROR } = apiStatus;

export default defineComponent({
    components: { 
        BaseLazyLoad,
        Select,
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
            value: 'Option One'
        }
    },
    watch: {
        fanficQuery: {
            immediate: true,
            handler: 'initSearchFanfics'
        }
    },
    setup() {
        const count = ref(0);
        const increase = () => {
            count.value++;
        }

        return {
            count, increase
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
        ]
    }
})
</script>

<style lang="scss">
* {
    padding: 0;
    margin: 0;
}
div {
    background-color: red;
}

.option {
    display: flex;
}

.img {
    display: block;
    max-width: 75px;
    max-height: 50px;
    margin-right: 10px;
}
</style>