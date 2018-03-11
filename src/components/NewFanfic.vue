<template>
    <div class="w-full max-w-md">

        <Form
        class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4"
        title="Nouvelle histoire"
        :operation="operation"
        :valid="valid">
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
                        <select class="block appearance-none w-full bg-white border border-grey-light hover:border-grey px-4 py-2 pr-8 rounded shadow" id="classement" name="classement" v-if="loading" v-model="classement" @change="onChange($event.target.value)">
                            <option value="">Sélectionner</option>
                            <option v-for="(option, index) in options[0].classement" :value="option[0]">{{ option[1] }}</option>
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
                    <multiselect v-model="genres" name="genres" id="genres" v-if="loading" :options="dataGenresFormatted" :multiple="true" :close-on-select="false" :option-height="104" :show-labels="true" placeholder="Sélectionner" class="shadow appearance-none border rounded w-full py-2 px-3 text-grey-darker"></multiselect>
                </div>
              </div>
              <div class="w-full md:w-1/3 px-3 mb-6 md:mb-0">
                  <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="status">
                    Status
                  </label>
                  <div class="relative">
                    <select class="block appearance-none w-full bg-white border border-grey-light hover:border-grey px-4 py-2 pr-8 rounded shadow" id="status" v-if="loading" v-model="status">
                        <option value="">Sélectionner</option>
                        <option v-for="(option, index) in options[0].status" :value="option[0]" v-bind:value="option[0]">{{ option[1] }}</option>
                    </select>
                    <div class="pointer-events-none absolute pin-y pin-r flex items-center px-2 text-grey-darker">
                      <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg>
                    </div>
                  </div>
              </div>
          </div>
            <Input name="author" v-model="author" type="hidden" />
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
export default {
    name: 'NewFanfic',
    data(){
        return{
            error: null,
            loading: false,
            options: [],
            dataGenresFormatted: [],
            title: '',
            description: '',
            synopsis: '',
            credits: '',
            author: '',
            genres: '',
            classement: '',
            status: '',
            category: '',
            subcategory: '',
        }
    },
    computed: {
        valid () {
            return !!this.title && !!this.description && !!this.synopsis && !!this.credits && !!this.author && !!this.genres && !!this.classement && !!this.status && !!this.category && !!this.subcategory
        },
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
                    author: this.$state.user.username,
                    genres: this.genres,
                    classement: this.classement,
                    status: this.status,
                    category: this.category,
                    subcategory: this.subcategory,
                }),
            })
            console.log(result)
            this.title = this.description = this.synopsis = this.credits = this.author = this.genres = this.classement = this.status = this.category = this.subcategory = ''
        },
        check (e) {
            if (e.target.checked) {
            }
        },
        onChange(value) {
            this.classement = value
        },
        async populate () {
            this.options = await this.$fetch('fanfics/options')
            this.loading = true
            if (this.options[0].genres.length) {
                this.options[0].genres.forEach(obj => {
                    this.dataGenresFormatted.push(obj[1])
                })
            }

        }
    },
    created () {
        this.populate()
    },
}
</script>

<style scoped>
.w-full {
    margin: 0 auto;
}
input[name="genres"]{
    margin-left: -10px;
}
</style>
