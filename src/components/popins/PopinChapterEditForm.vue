<template>
    <transition name="modal-fade">
        <div class="modal-container" v-model="dialog" v-show="dialog">
            <div class="modal"
                role="dialog"
                aria-labelledby="modalTitle"
                aria-describedby="modalDescription"
                >
                <header class="modal-header" id="modalTitle">
                </header>
                <section
                class="modal-body"
                id="modalDescription"
                >
                <Form
                    class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4"
                    :title="(obj_chapter.title === undefined) ? '' : obj_chapter.title"
                    :operation="operation"
                    :valid="valid">
                    <div class="mb-4">
                        <label class="block tracking-wide text-grey-500 text-xs font-bold mb-2" for="title">
                          {{ $t('message.textTitleChapter') }}
                        </label>
                        <Input
                            name="title"
                            v-model="chapterTitle"
                            :placeholder="$t('message.textTitleChapter')"
                            maxlength="255"
                            required />
                    </div>
                    <div class="mb-4">
                        <label class="block tracking-wide text-grey-500 text-xs font-bold mb-2" for="description">
                          {{ $t('message.descriptionLabel') }}
                        </label>
                        <Input
                            type="textarea"
                            name="description"
                            v-model="chapterDescription"
                            :placeholder="$t('message.descriptionLabel')"
                            maxlength="1000"
                            rows="4" />
                    </div>
                    <div class="mb-4">
                        <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="text">
                          {{ $t('message.contentLabel') }}
                        </label>
                        <trumbowyg v-model="chapterText"></trumbowyg>
                    </div>
                    <div class="mb-4">
                        <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="status">
                          {{ $t('message.textStatus' )}}
                        </label>
                        <div class="relative">
                          <select class="block appearance-none w-full bg-white border border-grey-light hover:border-grey px-4 py-2 pr-8 rounded shadow" id="status" v-model="chapterStatus">
                              <option value="">{{ $t('message.selectLabel') }}</option>
                              <option v-for="(status, i) in statusDialogOptions" :key="i" :value="status.key">{{ status.value }}</option>
                          </select>
                          <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700">
                              <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg>
                          </div>
                        </div>
                    </div>
                    <template slot="actions">
                        <button
                            type="submit"
                            class="bg-blue-500 hover:bg-blue-800 text-white font-bold py-2 px-4 rounded"
                            :disabled="!valid">
                            {{ $t('message.editChapterTitle') }}
                        </button>
                    </template>
                </Form>
                </section>
                <footer class="modal-footer">
                    <slot name="footer">
                        <button
                        type="button"
                        class="btn-green"
                        @click="close"
                        aria-label="Close modal"
                        >
                        {{ $t('message.fermerButtonLabel') }}
                    </button>
                </slot>
                </footer>
            </div>
        </div>
    </transition>
</template>

<script>
import { mapGetters, mapState, mapMutations } from 'vuex'

export default {
    data: () => ({
        dialog: false,
        resolve: null,
        reject: null,
        form: {},
    }),
    computed: {
        ...mapGetters('user', ['user']),
        ...mapState('fanfic', ['obj_chapter']),
        statusDialogOptions () {
            const choices = [{key: 'brouillon', value: this.$t('message.textDraft')}, {key: 'publié', value: this.$t('message.textPublish')}];

            return  choices;
        },
        valid () {
            return !!this.chapterTitle && !!this.chapterText && !!this.chapterStatus
        },
        chapterTitle: {
            get () {
                return this.obj_chapter.title
            },
            set (val) {
                this.setChapterTitle(val)
            }
        },
        chapterDescription: {
            get () {
                return this.obj_chapter.description
            },
            set (val) {
                this.setChapterDescription(val)
            }
        },
        chapterText: {
            get () {
                return this.obj_chapter.text
            },
            set (val) {
                this.setChapterText(val)
            }
        },
        chapterStatus: {
            get () {
                return this.obj_chapter.status
            },
            set (val) {
                this.setChapterStatus(val)
            }
        }
    },
    methods: {
        ...mapMutations('fanfic', ['setChapterTitle', 'setChapterDescription', 'setChapterText', 'setChapterStatus']),
        close() {
          this.resolve({ status: false })
          this.dialog = false
        },
        openModal () {
            this.dialog = true
            return new Promise((resolve, reject) => {
                this.resolve = resolve
                this.reject = reject
            })
        },
        operation () {
            this.form = {
                chapterId: this.obj_chapter.id,
                title: this.obj_chapter.title,
                description: this.obj_chapter.description,
                text: this.obj_chapter.text,
                fanfic: this.obj_chapter.fanfic,
                author: this.user.id,
                status: this.obj_chapter.status
            }
            this.validate()
        },
        validate () {
            this.dialog = false
            this.resolve({ status: true, r: this.form })
        }
    }
}
</script>

<style scoped>
.w-full {
    margin: 0 auto;
}
.modal-container {
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: rgba(0, 0, 0, 0.3);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 88;
}

.modal {
  background: #FFFFFF;
  box-shadow: 2px 2px 20px 1px;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  max-width: 750px;
  width: 100%;
}

.modal-header,
.modal-footer {
  padding: 15px;
  display: flex;
}

.modal-header {
  border-bottom: 1px solid #eeeeee;
  color: #4AAE9B;
  justify-content: space-between;
}

.modal-footer {
  border-top: 1px solid #eeeeee;
  justify-content: flex-end;
}

.modal-body {
  position: relative;
  padding: 20px 10px;
  max-height: 450px;
  overflow-x: hidden;
  overflow-y: auto;
}

.btn-close {
  border: none;
  font-size: 20px;
  padding: 20px;
  cursor: pointer;
  font-weight: bold;
  color: #4AAE9B;
  background: transparent;
}

.btn-green {
  color: #FFFFFF;
  background: #4AAE9B;
  border: 1px solid #4AAE9B;
  border-radius: 2px;
  padding: 5px 8px;
}

.modal-fade-enter,
.modal-fade-leave-active {
  opacity: 0;
}

.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity .5s ease
}
</style>
