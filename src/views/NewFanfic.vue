<template>
    <div class="w-full max-w-md">
        <Form
            class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4"
            title="Nouvelle histoire"
            :operation="operation"
            :valid="valid">
            <div class="flex flex-wrap -mx-3 mb-6">
                <div class="w-full md:w-1/2 px-3 mb-6 md:mb-0">
                  <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="category">
                    {{ $t('message.textCategory') }}
                  </label>
                  <div class="relative">
                      <select class="block appearance-none w-full bg-white border border-grey-light hover:border-grey px-4 py-2 pr-8 rounded shadow" id="category" name="category" v-model="category">
                          <option value="">Sélectionner</option>
                          <option v-for="(option, index) of dataCategories" v-bind:value="option.id">{{ option.name }}</option>
                      </select>
                      <div class="pointer-events-none absolute pin-y pin-r flex items-center px-2 text-grey-darker">
                          <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg>
                      </div>
                  </div>
                </div>
                <div>
                </div>
                <div class="w-full md:w-1/2 px-3">
                  <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="subcategory">
                      {{ $t('message.textSubcategory') }}
                  </label>
                  <div class="relative">
                      <select :disabled="category.length == 0" class="block appearance-none w-full bg-white border border-grey-light hover:border-grey px-4 py-2 pr-8 rounded shadow" id="subcategory" name="subcategory" v-model="subcategory">
                          <option value="">Sélectionner</option>
                          <option v-for="(option, index) of dataSubCategories" v-if="option.category === category" v-bind:value="option.id">{{ option.name }}</option>
                      </select>
                      <div class="pointer-events-none absolute pin-y pin-r flex items-center px-2 text-grey-darker">
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
                        placeholder="Titre de l'histoire"
                        maxlength="255"
                        required />
                </div>
                <div class="mb-4">
                    <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="synopsis">
                      Synopsis
                    </label>
                    <Input
                        type="textarea"
                        name="synopsis"
                        v-model="synopsis"
                        placeholder="Synopsis"
                        maxlength="1000"
                        rows="4" />
                </div>
                <div class="mb-4">
                    <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="credits">
                      Crédits
                    </label>
                    <Input
                        type="textarea"
                        name="credits"
                        v-model="credits"
                        placeholder="Crédits"
                        maxlength="350" />
                </div>
                <div class="mb-6">
                    <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="description">
                      Description de l'histoire
                    </label>
                    <Input
                        type="textarea"
                        name="description"
                        v-model="description"
                        placeholder="Description"
                        maxlength="1000"
                        rows="4" />
                </div>
                <div class="flex flex-wrap -mx-3 mb-2">
                    <div class="w-full md:w-1/3 px-3 mb-6 md:mb-0">
                        <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="classement">
                          {{ $t('message.textRating') }}
                        </label>
                        <div class="relative">
                            <select class="block appearance-none w-full bg-white border border-grey-light hover:border-grey px-4 py-2 pr-8 rounded shadow" id="classement" name="classement" v-model="classement">
                                <option value="">Sélectionner</option>
                                <option value="g">G</option>
                                <option value="13">13+</option>
                                <option value="r">R</option>
                                <option value="18">18+</option>
                            </select>
                            <div class="pointer-events-none absolute pin-y pin-r flex items-center px-2 text-grey-darker">
                                <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg>
                            </div>
                        </div>
                    </div>
                    <div class="w-full md:w-1/3 px-3 mb-6 md:mb-0">
                        <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="genres">
                          Genres
                        </label>
                        <div class="relative">
                            <label v-if="loadingGenres" v-for="(genre, index) in dataGenres">
                                <input type="checkbox" v-bind:value="genre[0]" v-model="genres">
                                {{ genre[1] }}<br/>
                            </label>
                        </div>
                    </div>
                    <div class="w-full md:w-1/3 px-3 mb-6 md:mb-0">
                        <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="status">
                          {{ $t('message.textStatus') }}
                        </label>
                        <div class="relative">
                            <select class="block appearance-none w-full bg-white border border-grey-light hover:border-grey px-4 py-2 pr-8 rounded shadow" id="status" name="status" v-model="status">
                                <option value="">Sélectionner</option>
                                <option value="brouillon">Brouillon</option>
                                <option value="publié">Publié</option>
                            </select>
                            <div class="pointer-events-none absolute pin-y pin-r flex items-center px-2 text-grey-darker">
                                <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg>
                            </div>
                        </div>
                    </div>
                </div>
                <template slot="actions">
                    <router-link
                        tag="button"
                        :to="{name: 'ListUserFanfic'}"
                        class="secondary inline-block align-baseline font-bold text-sm text-blue hover:text-blue-darker">
                        Retour à la liste des fanfictions
                    </router-link>
                    <button
                        type="submit"
                        class="bg-blue hover:bg-blue-dark text-white font-bold py-2 px-4 rounded"
                        :disabled="!valid">
                        Créer une histoire
                    </button>
                </template>
            </Form>
    </div>
</template>

<script>
import PersistantData from '../mixins/PersistantData'
import { mapGetters } from 'vuex'

export default {
    mixins: [
        PersistantData('DraftFanfic', [
            'title',
            'description',
            'synopsis',
            'credits',
            'author',
            'classement',
            'status',
            'category',
            'subcategory',
        ]),
    ],
    data (){
        return{
            errorFetch: 'Il y a un problème avec la requète.',
            fanfic: [],
            error: null,
            dataCategories: [],
            dataSubCategories: [],
            dataGenres: {},
            title: '',
            description: '',
            synopsis: '',
            credits: '',
            author: '',
            genres: [],
            classement: '',
            status: '',
            category: '',
            subcategory: '',
            loadingGenres: false,
            startPlaceholder: "Start",
            endPlaceholder: "End"
        }
    },
    computed: {
        ...mapGetters('user', ['user']),
        valid () {
            return !!this.title && !!this.category && !!this.subcategory && !!this.status && !!this.genres && !!this.classement
        }
    },
    created () {
        this.getCategories ()
        this.getSubcategories ()
        this.getGenres ()
    },
    methods: {
        async operation () {
            const result = await this.$fetch('fanfics', {
                method: 'POST',
                body: JSON.stringify({
                    title: this.title,
                    description: this.description,
                    synopsis: this.synopsis,
                    credits: this.credits,
                    author: this.user.id,
                    genres: this.genres,
                    classement: this.classement,
                    status: this.status,
                    category: this.category,
                    subcategory: this.subcategory,
                }),
            })
            this.title = this.description = this.synopsis = this.credits = this.author = this.genres = this.classement = this.status = this.category = this.subcategory = ''
            this.$router.replace(this.$route.params.wantedRoute || { name: 'ListUserFanfic'})
        },
        async getGenres() {
            this.dataGenres = await this.$fetch('fanfics/genres')
            this.loadingGenres = true
            this.dataGenres = this.dataGenres[0]['genres']
        },
        async getCategories() {
            this.dataCategories = await this.$fetch('category')
        },
        async getSubcategories() {
            this.dataSubCategories = await this.$fetch('subcategory')
        },
    }
}
</script>

<style scoped>
.w-full {
    margin: 0 auto;
}
</style>
