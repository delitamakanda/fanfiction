<template>
    <div>
        <div class="error bg-red-200 border border-red-200 text-red-500 px-4 py-3 rounded relative" v-if="hasRemoteErrors" role="alert">
            {{ errorFetch }}
        </div>
        <Loading v-if="remoteDataBusy" />

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
                      <select :disabled="categories && !categories.length" class="block appearance-none w-full bg-white border border-gray-400 hover:border-gray-500 px-4 py-2 pr-8 rounded shadow leading-tight focus:outline-none focus:shadow-outline" id="subcategory" name="subcategory" v-model="subcategory">
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
            <div class="mb-4">
                <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="synopsis">
                  {{ $t('message.synopsisLabel') }}
                </label>
                <Input
                    type="textarea"
                    name="synopsis"
                    v-model="synopsis"
                    :placeholder="$t('message.synopsisLabel')"
                    maxlength="1000"
                    rows="4" />
            </div>
            <div class="mb-4">
                <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="credits">
                  {{ $t('message.creditsLabel') }}
                </label>
                <Input
                    type="textarea"
                    name="credits"
                    v-model="credits"
                    :placeholder="$t('message.creditsLabel')"
                    maxlength="350" />
            </div>
            <div class="mb-4">
                <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="description">
                  {{ $t('message.descriptionLabel') }}
                </label>
                <Input
                    type="textarea"
                    name="description"
                    v-model="description"
                    :placeholder="$t('message.descriptionLabel')"
                    maxlength="1000"
                    rows="4" />
            </div>
            <div class="flex flex-wrap -mx-3 mb-2">
                <div class="w-full md:w-1/3 px-3 mb-6 md:mb-0">
                    <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="classement">
                      {{ $t('message.textRating') }}
                    </label>
                    <div class="inline-block relative w-64">
                        <select class="block appearance-none w-full bg-white border border-gray-400 hover:border-gray-500 px-4 py-2 pr-8 rounded shadow leading-tight focus:outline-none focus:shadow-outline" id="classement" name="classement" v-model="rating">
                            <option value="">{{ $t('message.selectLabel') }}</option>
                            <option v-for="item in classement" :key="item[0]" :value="item[0]">{{ item[1] }}</option>
                        </select>
                        <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700">
                            <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg>
                        </div>
                    </div>
                </div>
                <div class="w-full md:w-1/3 px-3 mb-6 md:mb-0">
                    <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2">
                      {{ $t('message.textGenres') }}
                    </label>
                    <div class="relative">
                        <ul>
                            <li v-for="(item, index) in genres" :key="index">
                              <input type="checkbox" :value="item[0]" :id="'checkbox-'+item[0]" v-model="checkedGenres" :name="'checkbox-'+item[0]" @click="check($event)">
                              <label :for="index">{{ item[1] }}</label>
                            </li>
                       </ul>
                    </div>
                </div>
                <div class="w-full md:w-1/3 px-3 mb-6 md:mb-0">
                    <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="status">
                      {{ $t('message.textStatus') }}
                    </label>
                    <div class="inline-block relative w-64">
                        <select class="block appearance-none w-full bg-white border border-gray-400 hover:border-gray-500 px-4 py-2 pr-8 rounded shadow leading-tight focus:outline-none focus:shadow-outline" id="status" name="status" v-model="statut">
                            <option value="">{{ $t('message.selectLabel') }}</option>
                            <option v-for="item in status" :key="item[0]" :value="item[0]">{{ item[1] }}</option>
                        </select>
                        <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700">
                            <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg>
                        </div>
                    </div>
                </div>
            </div>
            <template slot="actions">
                <button
                    type="submit"
                    class="bg-blue-500 w-full hover:bg-blue-800 text-white font-bold py-2 px-4 rounded"
                    :disabled="!valid">
                    {{ $t('message.editStoryLabel') }}
                </button>
            </template>
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
            newTitle: '',
            newDescription: '',
            newSynopsis: '',
            newCredits: '',
            newGenres: [],
            newClassement: '',
            newStatus: ''
        }
    },
    computed: {
        ...mapGetters('user', ['user']),
        ...mapState('fanfic', ['obj_fanfic', 'genres', 'classement', 'status']),
        ...mapState('chapter', ['chapters']),
        ...mapState('category', ['categories', 'subcategories']),
        valid() {
            return true;
        },
        statut: {
            get() {
                return this.obj_fanfic.status
            },
            set(val) {
                this.newStatus = val
            }
        },
        rating: {
            get() {
                return this.obj_fanfic.classement
            },
            set(val) {
                this.newClassement = val
            }
        },
        checkedGenres: {
            get() {
                return this.obj_fanfic.genres
            },
            set(val) {
                this.newGenres = val
            }
        },
        credits: {
            get() {
                return this.obj_fanfic.credits
            },
            set(val) {
                this.newCredits = val
            }
        },
        synopsis: {
            get() {
                return this.obj_fanfic.synopsis
            },
            set(val) {
                this.newSynopsis = val
            }
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
        },
        description: {
            get() {
                return this.obj_fanfic.description
            },
            set(val) {
                this.newDescription = val
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
                title: this.newTitle ? this.newTitle : this.title,
                description: this.newDescription ? this.newDescription : this.description,
                synopsis: this.newSynopsis ? this.newSynopsis : this.synopsis,
                credits: this.newCredits ? this.newCredits : this.credits,
                author: this.user.id,
                genres: this.newGenres ? this.newGenres : this.checkedGenres,
                classement: this.newClassement ? this.newClassement : this.rating,
                status: this.newStatus ? this.newStatus : this.statut,
                category: this.newCategory ? this.newCategory : this.category,
                subcategory: this.newSubCategory ? this.newSubCategory : this.subcategory
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