<template>
    <div>
        <div class="error bg-red-200 border border-red-200 text-red-500 px-4 py-3 rounded relative" v-if="hasRemoteErrors" role="alert">
            {{ errorFetch }}
        </div>
        <Loading v-if="remoteDataBusy" />

        {{ obj_fanfic }}
        <Form
            class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4"
            :title="$t('message.writeStoryLabel')"
            :operation="edit"
            :valid="valid"
        >
            <div class="flex flex-wrap -mx-2 mb-6">
                <div class="w-full md:w-1/2 px-3 mb-6 md:mb-0">
                  <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="category">
                    {{ $t('message.textCategory') }}
                  </label>
                  <div class="inline-block relative w-64">
                      <select class="block appearance-none w-full bg-white border border-gray-400 hover:border-gray-500 px-4 py-2 pr-8 rounded shadow leading-tight focus:outline-none focus:shadow-outline" id="category" name="category" v-model="category">
                          <option value="">{{ $t('message.selectLabel') }}</option>
                          <option v-for="(option, index) of categories" v-bind:value="option.id">{{ option.name }}</option>
                      </select>
                      <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700">
                          <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg>
                      </div>
                    </div>
                </div>
                <div class="w-full md:w-1/2 px-3">
                  <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="subcategory">
                      {{ $t('message.textSubcategory') }}
                  </label>
                  <div class="inline-block relative w-64">
                      <select :disabled="category.length == 0" class="block appearance-none w-full bg-white border border-gray-400 hover:border-gray-500 px-4 py-2 pr-8 rounded shadow leading-tight focus:outline-none focus:shadow-outline" id="subcategory" name="subcategory" v-model="subcategory">
                          <option value="">{{ $t('message.selectLabel') }}</option>
                          <option v-for="(option, index) of subcategories" v-if="option.category === obj_fanfic.category" v-bind:value="option.id">{{ option.name }}</option>
                      </select>
                      <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700">
                          <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg>
                      </div>
                  </div>
                </div>
            </div>
            <div class="mb-4">
                <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="title">
                  {{ $t('message.textTitleStoy') }}
                </label>
                <Input
                    name="title"
                    v-model="title"
                    :placeholder="$t('message.textTitleStoy')"
                    maxlength="255"
                    required
                />
            </div>
        </Form>
    </div>
</template>

<script>
import RemoteData from '@/mixins/RemoteData'
import get_cookie from '@/cookie'
import '@/compiled-icons/trash'
import '@/compiled-icons/edit-pencil'
import '@/compiled-icons/add-outline'

import confirm from '@/mixins/confirm'

import { mapGetters, mapActions, mapState, mapMutations } from 'vuex'

export default {
    name:'EditFanfic',
    props: {
        id: {
            type: Number,
            required: true
        }
    },
    mixins: [
        RemoteData({}),
        confirm
    ],
    data () {
        return {
            errorFetch: this.$t('message.errorFetch'),
            error: null,
            newCategory: 0,
            newSubCategory: 0,
            newTitle: ''
        }
    },
    computed: {
        ...mapGetters('user', ['user']),
        ...mapState('fanfic', ['obj_fanfic', 'genres', 'classement', 'status']),
        ...mapState('chapter', ['chapters']),
        ...mapState('category', ['categories', 'subcategories']),
        valid() {
            return !!this.title;
        },
        category: {
            get() {
                return this.obj_fanfic.category
            },
            set(val) {
                this.newCategory = val
            }
        },
        title: {
            get() {
                return this.obj_fanfic.title
            },
            set (val) {
                this.newTitle = val
            }
        },
        subcategory: {
            get() {
                return this.obj_fanfic.subcategory
            },
            set(val) {
                this.newSubCategory = val
            }
        }
    },
    created() {
        this.editFanfic({ id: this.id })
        this.fetchCategories()
        this.fetchSubCategories()
        this.fetchGenres()
        this.fetchChapters({ id: this.id })
    },
    methods: {
        ...mapActions('fanfic', ['editFanfic', 'changeFanfic', 'removeFanfic', 'fetchGenres']),
        ...mapActions('category', ['fetchSubCategories', 'fetchCategories']),
        ...mapActions('chapter', ['fetchChapters', 'postChapter', 'removeChapter']),
        edit () {
            this.changeFanfic({
                id: this.id,
                title: this.newTitle,
                description: this.obj_fanfic.description,
                synopsis: this.obj_fanfic.synopsis,
                credits: this.obj_fanfic.credits,
                author: this.user.id,
                genres: this.obj_fanfic.genres,
                classement: this.obj_fanfic.classement,
                status: this.obj_fanfic.status,
                category: this.newCategory,
                subcategory: this.newSubCategory
            });
        },
        check(e) {
            if (e.target.checked) {
                console.log(e.target.value)
            }
        }
    },
    watch: {

    }
}
</script>

<style scoped>

</style>