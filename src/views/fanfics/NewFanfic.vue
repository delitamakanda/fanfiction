<template>
    <div class="flex md:flex-row flex-wrap">
        <Form
            class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4"
            :title="$t('message.writeStoryLabel')"
            :operation="operation"
            :valid="valid">
            <div class="flex flex-wrap -mx-2 mb-6">
                <div class="w-full md:w-1/2 px-3 mb-6 md:mb-0">
                <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="category">
                    {{ $t('message.textCategory') }}
                </label>
                <div class="inline-block relative w-64">
                    <select class="block appearance-none w-full bg-white border border-gray-400 hover:border-gray-500 px-4 py-2 pr-8 rounded shadow leading-tight focus:outline-none focus:shadow-outline" id="category" name="category" v-model="category">
                        <option value="">{{ $t('message.selectLabel') }}</option>
                        <option :key="option.id" v-for="(option) of categories" v-bind:value="option.id">{{ option.name }}</option>
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
                        <option :key="option.id" v-for="(option) of subcategories" v-if="option.category === category" v-bind:value="option.id">{{ option.name }}</option>
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
                    required />
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
            <div class="mb-6">
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
                <div class="w-full md:w-1/2 px-2 mb-6 md:mb-0">
                    <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="classement">
                    {{ $t('message.textRating') }}
                    </label>
                    <div class="inline-block relative w-64">
                        <select class="block appearance-none w-full bg-white border border-gray-400 hover:border-gray-500 px-4 py-2 pr-8 rounded shadow leading-tight focus:outline-none focus:shadow-outline" id="classement" name="classement" v-model="rating">
                            <option value="">{{ $t('message.selectLabel') }}</option>
                            <option v-for="(item, i) in classement" :key="i" :value="item[0]">{{ item[1] }}</option>
                        </select>
                        <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700">
                            <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg>
                        </div>
                    </div>
                </div>
                <div class="w-full md:w-1/2 px-2 mb-6 md:mb-0">
                    <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="status">
                    {{ $t('message.textStatus') }}
                    </label>
                    <div class="inline-block relative w-64">
                        <select class="block appearance-none w-full bg-white border border-gray-400 hover:border-gray-500 px-4 py-2 pr-8 rounded shadow leading-tight focus:outline-none focus:shadow-outline" id="status" name="status" v-model="statut">
                            <option value="">{{ $t('message.selectLabel') }}</option>
                            <option v-for=" (item, i) in status" :key="i" :value="item[0]">{{ item[1] }}</option>
                        </select>
                        <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700">
                            <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg>
                        </div>
                    </div>
                </div>
            </div>
            <div class="flex flex-wrap -mx-2 mb-2">
                <div class="w-full md:w-1/3 px-3 mb-6 md:mb-0">
                    <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2">
                    {{ $t('message.textGenres') }}
                    </label>
                    <div class="relative">
                        <ul>
                            <li v-for="(item, index) in genres" :key="index">
                                <input type="checkbox" :id="'checkbox-'+item[0]" :name="'checkbox-'+item[0]"  :value="item[0]"  @click="check($event)" v-model="checkedGenres"> 
                                <label :for="index">{{ item[1] }}</label>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
            <template slot="actions">
                <button
                    type="submit"
                    class="bg-blue-500  w-full hover:bg-blue-800 text-white font-bold py-2 px-4 rounded"
                    :disabled="!valid">
                    {{ $t('message.createStoryLabel') }}
                </button>
            </template>
        </Form>
    </div>
</template>

<script>
import PersistantData from '@/mixins/PersistantData'
import { mapGetters, mapActions, mapState, mapMutations } from 'vuex'

import '@/compiled-icons/trash'
import '@/compiled-icons/edit-pencil'

export default {
    mixins: [
        PersistantData('DraftFanfic', [
            'title',
            'description',
            'synopsis',
            'credits',
            'author',
            'rating',
            'statut',
            'checkedGenres',
            'category',
            'subcategory',
        ]),
    ],
    data (){
        return{
            errorFetch: this.$t('message.errorFetch'),
            error: null,
            title: '',
            description: '',
            synopsis: '',
            credits: '',
            author: '',
            rating: '',
            statut: '',
            category: '',
            subcategory: '',
            checked: []
        }
    },
    computed: {
        ...mapGetters('user', ['user']),
        ...mapState('fanfic', ['fanfics', 'genres', 'classement', 'status']),
        ...mapState('category', ['categories', 'subcategories']),
        valid () {
            return !!this.title && !!this.category && !!this.subcategory && !!this.statut && !!this.checkedGenres && !!this.rating
        },
        checkedGenres: {
            get() {
                return this.checked
            },
            set(val) {
                this.checked = val
            }
        }
    },
    created () {
        this.fetchFanficsPublishedByAuthor({ status: '', author: this.user.username })
        this.fetchCategories ()
        this.fetchSubCategories ()
        this.fetchGenres ()
        this.fetchStatus()
        this.fetchClassement()
    },
    methods: {
        ...mapActions('fanfic', ['fetchGenres', 'fetchStatus', 'fetchClassement', 'postFanfic', 'fetchFanficsPublishedByAuthor']),
        ...mapActions('category', ['fetchCategories', 'fetchSubCategories']),
        async operation () {
            this.postFanfic({ 
                title: this.title,
                description: this.description,
                synopsis: this.synopsis,
                credits: this.credits,
                author: this.user.id,
                genres: this.checkedGenres,
                classement: this.rating,
                status: this.statut,
                category: this.category,
                subcategory: this.subcategory,
            })
            this.clearForm()
        },
        clearForm() {
            this.title = this.description = this.synopsis = this.credits = this.author = this.checkedGenres = this.rating = this.statut = this.category = this.subcategory = ''
        },
        check(e) {
          if (e.target.checked) {
            console.log(e.target.value)
          } 
        }
    }
}
</script>

<style scoped>
</style>
