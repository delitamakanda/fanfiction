<template>
    <div>
        <Loading v-if="remoteDataBusy" />

        <div class="error bg-red-lightest border border-red-light text-red-dark px-4 py-3 rounded relative"
            v-if="hasRemoteErrors" role="alert">
            {{ errorFetch }}
        </div>

        <form class="w-full">
            <div class="flex items-center py-2">
                <input
                    class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline mr-3"
                    type="text" :placeholder="$t('message.searchLabelFanfiction')" v-model="search_term"
                    aria-label="Search">
                <button
                    class="flex-shrink-0 bg-teal-500 hover:bg-teal-700 border-teal-500 hover:border-teal-700 text-sm border-4 text-white py-1 px-2 rounded"
                    @click.prevent="getSearchFanfics">{{ $t('message.searchLabel') }}</button>
            </div>
        </form>

        <category :categories="categories" @selectedCategory="categorySelected" />

        <div class="text-xl mb-4 font-bold" v-if="selected != '' || search_term != ''">
            {{ categoryName }}
        </div>

        <div class="flex flex-wrap -mx-2" v-if="fanfics">
            <fanfic v-for="item in fanfics" class="mb-4 w-full px-1 md:w-1/2" :fanfic="item" :displayDescription="true"
                :key="item.id" />
        </div>

        <button v-if="isPrevIsShown" @click="loadPrev()">Prev</button>
        <button v-if="fanfics.length > 1" @click="loadNext()">Next</button>
    </div>
</template>

<script>
    import RemoteData from '@/mixins/RemoteData'
    import Category from '@/components/fanfic/Category'
    import Fanfic from '@/components/fanfic/Fanfic'

    import { mapActions, mapState } from 'vuex'

    export default {
        created() {
            this.fetchCategories();
            const isNegative = Math.sign(this.currentOffset)
            if (this.fanfics.length && isNegative === 0) {
                this.isPrevIsShown = false
            }
            this.fetchFanficsPublished({ status: 'publié', offset: this.currentOffset })
        },
        mixins: [
            RemoteData(),
        ],
        data() {
            return {
                errorFetch: this.$t('message.errorFetch'),
                search_term: '',
                selected: '',
                currentOffset: 0,
                isPrevIsShown: false,
            }
        },
        computed: {
            ...mapState('fanfic', ['fanfics']),
            ...mapState('category', ['categories']),
            categoryName() {
                return this.selected;
            }
        },
        methods: {
            ...mapActions('category', ['fetchCategories']),
            ...mapActions('fanfic', ['clearFanficsPublished', 'fetchFanficsPublished', 'fetchFanficsPublishedCategory', 'fetchFanficsPublishedSearch']),
            getSearchFanfics() {
                this.fetchFanficsPublishedSearch({ status: 'publié', search_term: `${this.search_term}` })
                this.selected = ''
            },
            categorySelected(val) {
                this.selected = val.name
                this.fetchFanficsPublishedCategory({ status: 'publié', categoryId: val.id })
            },
            loadNext() {
                this.currentOffset = this.currentOffset + 4;
                const isNegative = Math.sign(this.currentOffset)
                if (isNegative !== -1 || isNegative !== 0) {
                    this.isPrevIsShown = true
                }
                this.fetchFanficsPublished({ status: 'publié', offset: this.currentOffset })
            },
            loadPrev() {
                this.currentOffset = this.currentOffset - 4;
                const isNegative = Math.sign(this.currentOffset)
                if (isNegative === -1 || isNegative === 0) {
                    this.isPrevIsShown = false
                }
                this.fetchFanficsPublished({ status: 'publié', offset: this.currentOffset })
            },
        },
        components: { Fanfic, Category }
    }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>