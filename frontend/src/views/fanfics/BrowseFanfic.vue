<template>
    <div>

        <Splide :options="{
            rewind: true,
            gap: '1rem',
            perPage: 3,
            autoplay: false,
        }" aria-label="" :has-track="false" class="splideDynamic">
            <div style="position: relative; height: 250px;">
                <SplideTrack>
                    <SplideSlide v-for="category of categories" :key="category.id"
                        class="img-thumbnail border shadow-lg rounded-lg"
                        :style="{ backgroundImage: 'url(' + require('./../../assets/images/categories/' + category.logic_value + '.jpg').default + ')' }">
                        <p>{{ category.name }}</p>
                    </SplideSlide>
                </SplideTrack>

                <div class="splide__arrows">
                    <button class="splide__arrow splide__arrow--prev">Prev</button>
                    <button class="splide__arrow splide__arrow--next">Next</button>
                </div>
            </div>
        </Splide>

        <p v-if="fetchHomeFanficsStatusIdle">Welcome</p>
        <BaseLazyLoad :show="fetchHomeFanficsStatusPending">
            <p>Loading data</p>
        </BaseLazyLoad>
        <p v-if="fetchHomeFanficsStatusError">There was a problem.</p>
        <template v-if="fetchHomeFanficsStatusSuccess">
            <h2
                class="mb-4 text-3xl font-extrabold tracking-tight leading-none text-gray-900 md:text-4xl dark:text-white">
                {{ $t('message.browseFanfics.mostRecentLabel') }}
            </h2>
            <BaseCard v-for="fanfic of newestFanfics" :fanfic="fanfic" />
            <h2
                class="mb-4 text-3xl font-extrabold tracking-tight leading-none text-gray-900 md:text-4xl dark:text-white">
                {{ $t('message.browseFanfics.mostPopularLabel') }}
            </h2>
            <BaseCard v-for="fanfic of mostLikedFanfics" :fanfic="fanfic" />
            <h2
                class="mb-4 text-3xl font-extrabold tracking-tight leading-none text-gray-900 md:text-4xl dark:text-white">
                {{ $t('message.browseFanfics.mostRecommendedLabel') }}
            </h2>
            <BaseCard v-for="fanfic of recommendedFanfics" :fanfic="fanfic" />
        </template>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { fetchHomeFanfics } from '../../api/fanficApi'
import { apiStatus } from '../../api/constants/apiStatus';
import { withAsync } from '../../api/helpers/withAsync';
import { apiStatusComputedFactory } from '../../api/helpers/apiStatusComputedFactory';
import BaseLazyLoad from '../../components/base/BaseLazyLoad.vue';
import Layout from '../../layout/Layout.vue';
import { useLayout } from "../../layout/composables/useLayout";
import { Splide, SplideSlide, SplideTrack } from '@splidejs/vue-splide';

import '@splidejs/vue-splide/css';

const { IDLE, PENDING, SUCCESS, ERROR } = apiStatus;

export default defineComponent({
    components: {
        BaseLazyLoad,
        Layout,
        Splide,
        SplideSlide,
        SplideTrack,
    },
    setup() {
        const { setLayout, LAYOUTS } = useLayout();
        return {
            setLayout,
            LAYOUTS,
        }
    },
    computed: {
        ...apiStatusComputedFactory(['fetchHomeFanficsStatus', 'updateHomeFanficsStatus']),
    },
    data() {
        return {
            homeFanfics: null,
            categories: null,
            recommendedFanfics: null,
            mostLikedFanfics: null,
            newestFanfics: null,
            fanfics: null,
            fetchHomeFanficsStatus: apiStatus.IDLE,
            apiStatus: null,
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
            this.mostLikedFanfics = response.data.most_liked_fanfics;
            this.newestFanfics = response.data.newest_fanfics;
            this.recommendedFanfics = response.data.recommended_fanfics;
            this.categories = response.data.all_categories;
            this.fetchHomeFanficsStatus = apiStatus.SUCCESS;
        },
    },
    created() {
        apiStatus;
        this.fetchHomeFanfics();
    }
});
</script>

<style scoped>
.splideDynamic {
    padding: 0;
}

.splideDynamic ul>li {
    background-size: cover;
}
</style>