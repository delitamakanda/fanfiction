<template>
    <transition name="modal-fade">
        <div class="modal-container" v-model="dialog" v-show="dialog">
            <div class="modal"
                role="dialog"
                aria-labelledby="modalTitle"
                aria-describedby="modalDescription"
                >
                <header class="modal-header" id="modalTitle">
                    <h3>{{ $t('message.commentairesLabel') }} &laquo; {{ fanfic.title }} &raquo;</h3>
                </header>
                <section
                class="modal-body"
                id="modalDescription"
                >
                    <div v-for="(comment, i) in comments" :key="comment.id">
                        <div class="md:flex shadow my-4 bg:white rounded-lg p-6" v-if="comment.in_reply_to === null">
                            <div class="text-center md:text-left">
                                <h2 class="text-lg">{{ $t('message.authorLabel') }} : {{ comment.name }}</h2>
                                <div class="text-purple-500">{{ comment.body }}</div>
                                <div class="text-gray-500">{{ $t('message.publishedAtLabel')}} {{ comment.created | date }}</div>
                            </div>
                        </div>
                        <!-- réponse de l'auteur -->
                        <div v-for="(obj, a) in uniqComments">
                            <div class="my-4 shadow bg:white rounded-lg p-4" v-if="obj.in_reply_to != null && comment.id === obj.in_reply_to.id">
                                <div class="text-center md:text-left">
                                    <h2 class="text-lg">{{ $t('message.authorLabel') }} : {{ obj.name }}</h2>
                                    <div class="text-purple-500">{{ obj.body }}</div>
                                    <div class="text-gray-500">{{ $t('message.publishedAtLabel')}} {{ obj.created | date }}</div>
                                </div>

                            <div class="my-4 border bg:white rounded-lg p-4">
                                <div class="text-center md:text-left">
                                    <p>{{ $t('message.inReplyToLabel') }} :</p>
                                    <h2 class="text-lg">{{ $t('message.authorLabel') }} : {{ obj.in_reply_to.name }}</h2>
                                    <div class="text-purple-500">{{ obj.in_reply_to.body }}</div>
                                    <div class="text-gray-500">{{ $t('message.publishedAtLabel')}} {{ obj.in_reply_to.created | date }}</div>
                                </div>
                            </div>
                            </div>
                        </div>
                    </div>
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
import { mapActions, mapGetters } from 'vuex'
import * as _ from 'lodash'

export default {
    data: () => ({
        dialog: false,
        resolve: null,
        reject: null,
        fanfic: {},
        comments: []
    }),
    computed: {
        ...mapGetters('comment', ['allComments']),
        uniqComments () {
            let arr = _.concat([], this.allComments, this.comments)
            return _.uniqBy(arr, 'id')
        }
    },
    methods: {
      close() {
        this.resolve({ status: false })
        this.dialog = false
      },
      openModal (val, val2) {
        this.dialog = true
        this.fanfic = val
        this.comments = val2
        return new Promise((resolve, reject) => {
            this.resolve = resolve
            this.reject = reject
        })
      },
    }
}
</script>

<style scoped>
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
  max-width: 450px;
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
  max-height: 330px;
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
