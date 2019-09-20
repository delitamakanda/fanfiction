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
                    placeholder="Titre de l'histoire"
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
                <div class="w-full md:w-1/3 px-3 mb-6 md:mb-0">
                    <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="classement">
                      {{ $t('message.textRating') }}
                    </label>
                    <div class="inline-block relative w-64">
                        <select class="block appearance-none w-full bg-white border border-gray-400 hover:border-gray-500 px-4 py-2 pr-8 rounded shadow leading-tight focus:outline-none focus:shadow-outline" id="classement" name="classement" v-model="classement">
                            <option value="">{{ $t('message.selectLabel') }}</option>
                            <option v-for="(classement, i) in classementOptions" :key="i" :value="classement.key">{{ classement.value }}</option>
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
                            <li v-for="value in genres">
                              <input type="checkbox" :value="value[0]" :id="value[0]" v-model="choices" @click="check($event)"> {{ value[1] }}
                            </li>
                       </ul>
                    </div>
                </div>
                <div class="w-full md:w-1/3 px-3 mb-6 md:mb-0">
                    <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="status">
                      {{ $t('message.textStatus') }}
                    </label>
                    <div class="inline-block relative w-64">
                        <select class="block appearance-none w-full bg-white border border-gray-400 hover:border-gray-500 px-4 py-2 pr-8 rounded shadow leading-tight focus:outline-none focus:shadow-outline" id="status" name="status" v-model="status">
                            <option value="">{{ $t('message.selectLabel') }}</option>
                            <option v-for=" (status, i) in statusOptions" :key="i" :value="status.key">{{ status.value }}</option>
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
                    class="bg-blue-500 hover:bg-blue-800 text-white font-bold py-2 px-4 rounded"
                    :disabled="!valid">
                    {{ $t('message.editStoryLabel') }}
                </button>
                <button
                    type="button"
                    @click="deleteStory"
                    class="bg-blue-500 hover:bg-blue-800 text-white font-bold py-2 px-4 rounded"
                    >
                    {{ $t('message.removeStoryLabel') }}
                </button>
            </template>
        </Form>
        <table class="w-full text-left m-4" style="border-collapse:collapse">
        <thead>
            <tr>
                <th class="py-4 px-6 bg-grey-200 font-sans font-medium uppercase text-sm text-grey border-b border-grey-200">
                    {{ $t('message.chapterLabel') }}
                    <button type="button" :title="$t('message.addChapterLabel')" class="mt-4 lg:inline-block lg:mt-0 text-teal hover:text-teal-darker" @click="writeChapter"><svgicon icon="add-outline" width="22" height="18" color="#000"></svgicon> </button>
                </th>
                <th class="py-4 px-6 bg-grey-200 font-sans font-medium uppercase text-sm text-grey border-b border-grey-200"></th>
                <th class="py-4 px-6 bg-grey-200 font-sans font-medium uppercase text-sm text-grey border-b border-grey-200"></th>
                <th class="py-4 px-6 bg-grey-200 font-sans font-medium uppercase text-sm text-grey border-b border-grey-200"></th>
            </tr>
        </thead>
        <tbody>
            <tr class="hover:bg-blue-200" v-for="(chapter, i) in chapters" :key="chapter.id">
                <td class="py-4 px-6 border-b border-grey-200">{{ i + 1 }} - {{ chapter.title }}</td>
                <td class="py-4 px-6 border-b border-grey-200">{{ chapter.published | date }}</td>
                <td class="py-4 px-6 border-b border-grey-200">{{ chapter.status }}</td>
                <td class="py-4 px-6 border-b border-grey-200 text-center">
                    <button type="button" :title="$t('message.editChapterTitle')" class="mt-4 lg:inline-block lg:mt-0 text-teal hover:text-teal-darker" @click="editChapter(chapter.id)"><svgicon icon="edit-pencil" width="22" height="18" color="#000"></svgicon> </button>

                    <button type="button" :title="$tc('message.removeChapterTitle', chapter.title, chapter.id, {a: chapter.title, n: chapter.id})" @click="deleteChapter(chapter.title, chapter.id)"><svgicon icon="trash" width="22" height="18" color="#000"></svgicon></button>
                </td>
            </tr>
        </tbody>
        </table>
        <modal ref="chapterForm"></modal>
        <popin ref="chapterEditForm"></popin>
    </div>
</template>

<script>
import RemoteData from '@/mixins/RemoteData'
import get_cookie from '@/cookie'
import '@/compiled-icons/trash'
import '@/compiled-icons/edit-pencil'
import '@/compiled-icons/add-outline'

import modal from '@/components/popins/PopinChapterForm.vue'
import popin from '@/components/popins/PopinChapterEditForm.vue'
import confirm from '@/mixins/confirm'

import { mapGetters, mapActions, mapState, mapMutations } from 'vuex'

export default {
    mixins: [
        RemoteData({
            comments () {
                return `comments/fanfic/${this.id}/list`
            },
            anwserByComments () {
                return `comments/${this.id}/fanfic`;
            }
        }),
        confirm
    ],
    components: { modal, popin },
    computed: {
        ...mapGetters('user', ['user']),
        ...mapState('fanfic', ['obj_fanfic', 'obj_chapter', 'chapters', 'genres', 'subcategories', 'categories']),
        status: {
            get() {
                return this.obj_fanfic.status;
            },
            set(val) {
                this.editStatus(val)
            }
        },
        category: {
            get() {
                return this.obj_fanfic.category;
            },
            set (val) {
                this.editCategory(val)
            }
        },
        synopsis: {
            get() {
                return this.obj_fanfic.synopsis;
            },
            set(val) {
                this.editSynopsis(val)
            }
        },
        subcategory: {
            get() {
                return this.obj_fanfic.subcategory;
            },
            set(val) {
                this.editSubCategory(val)
            }
        },
        title: {
            get() {
                return this.obj_fanfic.title;
            },
            set(val) {
                this.editTitle(val)
            }
        },
        classement: {
            get() {
                return this.obj_fanfic.classement;
            },
            set(val) {
                this.editClassement(val)
            }
        },
        totalComments() {
            return this.comments.length
        },
        totalAnwsersComment(){
            return this.anwserByComments.length
        },
        totalEffectiveComment() {
            return (this.totalAnwsersComment - this.totalComments)
        },
        valid() {
            return !!this.title;
        },
        choices: {
            get() {
                return this.obj_fanfic.genres;
            },
            set(val) {
                this.editGenres(val)
            }
        },
        description: {
            get () {
                return this.obj_fanfic.description;
            },
            set(val) {
                this.editDescription(val)
            }
        },
        credits: {
            get() {
                return this.obj_fanfic.credits;
            },
            set(val) {
                this.editCredits(val)
            }
        }
    },
    data () {
        return {
            comments: [],
            comment: {},
            anwserByComments: [],
            errorFetch: this.$t('message.errorFetch'),
            error: null,
            classementOptions: [{key: 'g', value: 'G'},{key: '13', value: '13+'},{key: 'r', value: 'R'},{key: '18', value: '18+'}],
            statusOptions: [{key: 'brouillon', value: this.$t('message.textDraft')}, {key: 'publié', value: this.$t('message.textPublish')}],
        }
    },
    props: {
        id: {
            type: Number,
            required: true,
        }
    },
    created () {
        this.editFanfic({ id: this.id })
        this.fetchChapters({ id: this.id, status: '' })
        this.fetchCategories ()
        this.fetchSubCategories ()
        this.fetchGenres ()
    },
    mounted () {
        this.$root.$chapterForm = this.$refs.chapterForm.openModal
        this.$root.$chapterEditForm = this.$refs.chapterEditForm.openModal
    },
    methods: {
        ...mapActions('fanfic', ['fetchCategories', 'fetchSubCategories', 'fetchGenres', 'postFanfic', 'fetchFanficsPublishedByAuthor', 'editFanfic', 'fetchChapters', 'fetchChapter', 'changeFanfic', 'removeFanfic', 'postChapter', 'putChapter', 'clearChapter', 'removeChapter']),
        ...mapMutations('fanfic', ['editGenres', 'editCategory', 'editStatus', 'editTitle', 'editCredits', 'editSubCategory', 'editClassement', 'editDescription', 'editSynopsis']),
        deleteChapter (chapterTitle, chapterId) {
            const message = this.$tc('message.removeChapterTitle', chapterTitle, chapterId, {a: chapterTitle, n: chapterId})

            this.confirm(message, () => {
                this.removeChapter({ id: chapterId })
            });
        },
        deleteStory () {
            const message = this.$tc('message.removeStoryDisclaimerText', this.obj_fanfic.title, this.id, { a: this.obj_fanfic.title, n: this.id })

            this.confirm(message, () => {
                this.removeFanfic({ id: this.id })
                this.$router.replace(this.$route.params.wantedRoute || { name: 'NewFanfic'})
            })
        },
        edit () {
            this.changeFanfic({
                id: this.id,
                title: this.obj_fanfic.title,
                description: this.obj_fanfic.description,
                synopsis: this.obj_fanfic.synopsis,
                credits: this.obj_fanfic.credits,
                author: this.user.id,
                genres: this.obj_fanfic.genres,
                classement: this.obj_fanfic.classement,
                status: this.obj_fanfic.status,
                category: this.obj_fanfic.category,
                subcategory: this.obj_fanfic.subcategory
            });
        },
        writeChapter () {
            this.$root
              .$chapterForm(this.obj_fanfic)
              .then(res => {
                  if (res.status) {
                     const data = res.r
                     this.postChapter(data)
                  }
              })
              .catch(err => console.log(err))
        },
        editChapter ( chapterId ) {
            this.fetchChapter({ id: chapterId })

            this.$root
                .$chapterEditForm(this.obj_chapter)
                .then(res => {
                    if (res.status) {
                        const data = res.r
                        this.putChapter(data)
                    }
                })
        },
        check(e) {
          if (e.target.checked) {
            console.log(e.target.value)
          }
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
