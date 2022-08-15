<template>
    <div>
        <p v-if="fetchHomeFanficsStatusIdle">Welcome</p>
        <p v-if="fetchHomeFanficsStatusPending">
            Loading data
        </p>
        <p v-if="fetchHomeFanficsStatusError">There was a problem.</p>
        {{ $t("message.hello", {name: "dma"}) }}
        <button @click="increase">Clicked {{ count }} times.</button>
        <template v-if="fetchHomeFanficsStatusSuccess">
            <div v-for="fanfic of homeFanfics">
                {{ fanfic.title }}
            </div>
        </template>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { fetchHomeFanfics, fetchFanfics } from './api/fanficApi'
import { apiStatus } from './api/helpers/apiStatus';
import { withAsync } from './api/helpers/withAsync';
import { apiStatusComputedFactory } from './api/helpers/apiStatusComputedFactory';
// import BaseLazyLoad from './components/base/BaseLazyLoad.vue';

const { IDLE, PENDING, SUCCESS, ERROR } = apiStatus;

export default defineComponent({
    components: { 
        // BaseLazyLoad
    },
    computed: {
        ...apiStatusComputedFactory(['fetchHomeFanficsStatus', 'updateHomeFanficsStatus'])
    },
    data() {
        return {
            homeFanfics: null,
            fanfics: null,
            fetchHomeFanficsStatus: apiStatus.IDLE,
            apiStatus: null
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
        async fetchFanfics() {
            const response = await fetchFanfics();
            this.fanfics = response.data
        }
    },
    created() {
        apiStatus;
        this.fetchHomeFanfics();
        this.fetchFanfics();
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
</style>