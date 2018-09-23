<template>
    <div class="w-full max-w-md">
        <template v-if="!id">
            <Form
            class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4"
            title="Nouvelle histoire"
            :operation="create"
            :valid="valid">
            <div class="flex flex-wrap -mx-3 mb-6">
                <div class="w-full md:w-1/2 px-3 mb-6 md:mb-0">
                  <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="category">
                    Catégorie
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
                <div class="w-full md:w-1/2 px-3">
                  <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="subcategory">
                      Sous - Catégories
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
                      Titre de l'histoire
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
                          Classement
                        </label>
                        <div class="relative">
                            <select class="block appearance-none w-full bg-white border border-grey-light hover:border-grey px-4 py-2 pr-8 rounded shadow" id="classement" name="classement" v-model="classement" v-if="loadingClassement">
                                <option value="">Sélectionner</option>
                                <option v-for="(option, index) in dataClassement[0]['classement']" v-bind:value="option[0]">{{ option[1] }}</option>
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
                          Status
                        </label>
                        <div class="relative">
                            <select class="block appearance-none w-full bg-white border border-grey-light hover:border-grey px-4 py-2 pr-8 rounded shadow" id="status" name="status" v-model="status" v-if="loadingStatus">
                                <option value="">Sélectionner</option>
                                <option v-for="(option, index) in dataStatus[0]['status']"  v-bind:value="option[0]">{{ option[1] }}</option>
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
        </template>
        <template v-else>
            <Loading v-if="remoteDataBusy" />
            <div class="error bg-red-lightest border border-red-light text-red-dark px-4 py-3 rounded relative" v-if="hasRemoteErrors" role="alert">
                {{ errorFetch }}
            </div>
            <form
            @submit.prevent="edit"
            enctype="multipart/form-data"
            class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
                <h2>Editer l' histoire</h2>
            <div class="flex flex-wrap -mx-3 mb-6">
                <div class="w-full md:w-1/2 px-3 mb-6 md:mb-0">
                  <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="category">
                    Catégorie
                  </label>
                  <div class="relative">
                      <select class="block appearance-none w-full bg-white border border-grey-light hover:border-grey px-4 py-2 pr-8 rounded shadow" id="category" name="category" v-model="fanfic.category">
                          <option value="">Sélectionner</option>
                          <option v-for="(option, index) of dataCategories" v-bind:value="option.id">{{ option.name }}</option>
                      </select>
                      <div class="pointer-events-none absolute pin-y pin-r flex items-center px-2 text-grey-darker">
                          <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg>
                      </div>
                  </div>
                </div>
                <div class="w-full md:w-1/2 px-3">
                  <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="subcategory">
                      Sous - Catégories
                  </label>
                  <div class="relative">
                      <select class="block appearance-none w-full bg-white border border-grey-light hover:border-grey px-4 py-2 pr-8 rounded shadow" id="subcategory" name="subcategory" v-model="fanfic.subcategory">
                          <option value="">Sélectionner</option>
                          <option v-for="(option, index) of dataSubCategories" v-bind:value="option.id">{{ option.name }}</option>
                      </select>
                      <div class="pointer-events-none absolute pin-y pin-r flex items-center px-2 text-grey-darker">
                          <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg>
                      </div>
                  </div>
                </div>
              </div>
                <div class="mb-4">
                    <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="title">
                      Titre de l'histoire
                    </label>
                    <Input
                        name="title"
                        v-model="fanfic.title"
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
                        v-model="fanfic.synopsis"
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
                        v-model="fanfic.credits"
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
                        v-model="fanfic.description"
                        placeholder="Description"
                        maxlength="1000"
                        rows="4" />
                </div>
                <div class="flex flex-wrap -mx-3 mb-2">
                    <div class="w-full md:w-1/3 px-3 mb-6 md:mb-0">
                        <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="classement">
                          Classement
                        </label>
                        <div class="relative">
                            <select class="block appearance-none w-full bg-white border border-grey-light hover:border-grey px-4 py-2 pr-8 rounded shadow" id="classement" name="classement" v-model="fanfic.classement" v-if="loadingClassement">
                                <option value="">Sélectionner</option>
                                <option v-for="(option, index) in dataClassement[0].classement" :value="option[0]" :key="index" :selected="index == 1">{{ option[1] }}</option>
                            </select>
                            <div class="pointer-events-none absolute pin-y pin-r flex items-center px-2 text-grey-darker">
                                <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg>
                            </div>
                        </div>
                  </div>
                  <div class="w-full md:w-1/3 px-3 mb-6 md:mb-0">
                    <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2">
                      Genres
                    </label>
                    <div class="relative">
                        <label :for="select[0]" v-for="select in dataGenresFormatted">
                            <input :value="select[0]" v-model="fanfic.genres" :id="select[0]" type="checkbox">
                            {{ select[1] }}<br>
                        </label>
                    </div>
                  </div>
                  <div class="w-full md:w-1/3 px-3 mb-6 md:mb-0">
                      <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="status">
                        Status
                      </label>
                      <div class="relative">
                        <select class="block appearance-none w-full bg-white border border-grey-light hover:border-grey px-4 py-2 pr-8 rounded shadow" id="status" v-model="fanfic.status" v-if="loadingStatus">
                            <option value="">Sélectionner</option>
                            <option v-for="(option, index) in dataStatus[0].status" :value="option[0]" :key="index" :selected="index == 1">{{ option[1] }}</option>
                        </select>
                        <div class="pointer-events-none absolute pin-y pin-r flex items-center px-2 text-grey-darker">
                          <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg>
                        </div>
                      </div>
                  </div>
              </div>
                <router-link
                    tag="button"
                    :to="{name: 'ListUserFanfic'}"
                    class="secondary inline-block align-baseline font-bold text-sm text-blue hover:text-blue-darker">
                    Retour à la l'histoire
                </router-link>
                <button
                    type="submit"
                    class="bg-blue hover:bg-blue-dark text-white font-bold py-2 px-4 rounded">
                    Editer l' histoire
                </button>
            </form>
        </template>
    </div>
</template>

<script>
import PersistantData from '../mixins/PersistantData'
import RemoteData from '../mixins/RemoteData'

export default {
    name: 'NewFanfic',
    mixins: [
        PersistantData('NewFanfic', [
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
        RemoteData({
            fanfic () {
                return this.id ? `fanfics/${this.$route.params.id}` : ``
            }
        }),
    ],
    data(){
        return{
            errorFetch: 'Il y a un problème avec la requète.',
            fanfic: [],
            error: null,
            dataClassement: [],
            dataStatus: [],
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
            loadingClassement: false,
            loadingGenres: false,
            loadingStatus: false,
            dataGenresFormatted: {}
        }
    },
    props: {
        id: {
            type: Number,
            required: false,
        },
    },
    computed: {
        valid () {
            return !!this.title && !!this.category && !!this.subcategory && !!this.status && !!this.genres && !!this.classement
        }
    },
    async created () {
        this.dataGenresFormatted = await this.$fetch('fanfics/genres')
        this.loadingGenres = true
        this.dataGenresFormatted = this.dataGenresFormatted[0]['genres']

        this.dataClassement = await this.$fetch('fanfics/classement')
        this.loadingClassement = true

        this.dataStatus = await this.$fetch('fanfics/status')
        this.loadingStatus = true

        this.dataCategories = await this.$fetch('category')
        this.dataSubCategories = await this.$fetch('subcategory')
    },
    mounted () {
        this.getClassement ()
        this.getCategories ()
        this.getSubcategories ()
        this.getStatus ()
        this.getGenres ()
    },
    methods: {
        async create () {
            const result = await this.$fetch('fanfics', {
                method: 'POST',
                body: JSON.stringify({
                    title: this.title,
                    description: this.description,
                    synopsis: this.synopsis,
                    credits: this.credits,
                    author: this.$state.user.id,
                    genres: this.genres,
                    classement: this.classement,
                    status: this.status,
                    category: this.category,
                    subcategory: this.subcategory,
                }),
            })
            this.title = this.description = this.synopsis = this.credits = this.author = this.genres = this.classement = this.status = this.category = this.subcategory = ''
        },
        async edit () {
            const result = await this.$fetch(`fanfics/${this.$route.params.id}`, {
                method: 'PUT',
                body: JSON.stringify({
                    title: this.fanfic.title,
                    description: this.fanfic.description,
                    synopsis: this.fanfic.synopsis,
                    credits: this.fanfic.credits,
                    author: this.fanfic.author,
                    genres: this.fanfic.genres,
                    classement: this.fanfic.classement,
                    status: this.fanfic.status,
                    category: this.fanfic.category,
                    subcategory: this.fanfic.subcategory,
                }),
            })
            this.$router.push({name: 'Fanfic', params: { id: this.fanfic.id }})
        },
        async getGenres() {
            this.dataGenres = await this.$fetch('fanfics/genres')
            this.loadingGenres = true
            this.dataGenres = this.dataGenres[0]['genres']
        },
        async getClassement() {
            this.dataClassement = await this.$fetch('fanfics/classement')
            this.loadingClassement = true
        },
        async getStatus() {
            this.dataStatus = await this.$fetch('fanfics/status')
            this.loadingStatus = true
        },
        async getCategories() {
            this.dataCategories = await this.$fetch('category')
        },
        async getSubcategories() {
            this.dataSubCategories = await this.$fetch('subcategory')
        },
    },
}
</script>

<style scoped>
.w-full {
    margin: 0 auto;
}
</style>
