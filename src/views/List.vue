<template>
    <div>
        <Loading v-if="remoteDataBusy" />

        <div class="error bg-red-lightest border border-red-light text-red-dark px-4 py-3 rounded relative" v-if="hasRemoteErrors" role="alert">
            {{ errorFetch }}
        </div>

        <form class="align-center w-full">
            <div class="flex items-center py-2">
                <input class="appearance-none bg-transparent border rounded w-full text-grey-darker mr-3 py-1 px-2 leading-tight" type="text" :placeholder="$t('message.searchLabelFanfiction')" v-model="search_term" aria-label="Search">
                <button class="bg-teal hover:bg-teal-dark text-white font-bold py-2 px-4 rounded" @click.prevent="getSearchFanfics">{{ $t('message.searchLabel') }}</button>
            </div>
        </form>

        <category :categories="categories" @selectedCategory="categorySelected" />

        <div class="text-xl mb-4 font-bold" v-if="selected !== '' || search_term !== ''">
            {{ categoryName }}
        </div>

        <div class="flex flex-wrap -mx-2">
            <fanfic
                v-for="(fanfic,i) in fanfics"
                class="mb-4 w-full px-1 md:w-1/2"
                :fanfic="fanfic"
                :key="i"
            />
        </div>
    </div>
</template>

<script>
    import RemoteData from '../mixins/RemoteData'
    import Category from '@/components/fanfic/Category'
    import Fanfic from '@/components/fanfic/Fanfic'

    import { mapActions, mapState } from 'vuex'

    export default {
        created () {
            this.fetchCategories();
            this.fetchFanficsPublished({ status: 'publié' })
        },
        mixins: [
        RemoteData(),
        ],
        data () {
            return {
                errorFetch: this.$t('message.errorFetch'),
                search_term: '',
                selected: ''
            }
        },
        computed: {
            ...mapState('fanfic', ['fanfics', 'categories']),
            categoryName () {
                return this.selected;
            }
        },
        methods: {
            ...mapActions('fanfic', ['fetchCategories', 'clearFanficsPublished', 'fetchFanficsPublished', 'fetchFanficsPublishedCategory', 'fetchFanficsPublishedSearch']),
            getSearchFanfics () {
                this.fetchFanficsPublishedSearch({ status: 'publié', search_term: `${this.search_term}`})
                this.selected = ''
            },
            categorySelected (val) {
                this.selected = val.name
                this.fetchFanficsPublishedCategory({ status: 'publié', categoryId: val.id })
            }
        },
        components: { Fanfic, Category }
    }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
