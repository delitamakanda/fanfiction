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
                <Form
                    class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4"
                    title=""
                    :operation="operation"
                    :valid="valid">
                    <div class="mb-4">
                        <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="name">
                            {{ $t('message.UsernameOrPseudoLabel') }}
                        </label>
                        <Input
                        name="name"
                        v-model="name"
                        :placeholder="$t('message.UsernameOrPseudoLabel')"
                        maxlength="255"
                        required />
                    </div>
                    <div class="mb-4">
                        <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="email">
                            {{ $t('message.formContactEmailLabel') }}
                        </label>
                        <Input
                        name="email"
                        v-model="email"
                        :placeholder="$t('message.emailPlaceholderLabel')"
                        maxlength="255" />
                    </div>
                    <div class="mb-4">
                        <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="body">
                            {{ $t('message.formContactMessageLabel') }}
                        </label>
                        <Input
                        type="textarea"
                        name="body"
                        v-model="body"
                        :placeholder="$t('message.formContactMessageLabel')"
                        rows="6"
                        required />
                    </div>
                    <template slot="actions">
                        <div class="flex items-center justify-between">
                            <button
                            class="bg-blue-500 hover:bg-blue-800 text-white font-bold py-2 px-4 rounded"
                            type="submit"
                            :disabled="!valid">
                            {{ $t('message.donnezVotreAvisLabel') }}
                        </button>
                    </div>
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
import { mapActions, mapState, mapGetters } from 'vuex'
import PersistantData from '@/mixins/PersistantData'

export default {
    data: () => ({
        dialog: false,
        resolve: null,
        reject: null,
        fanfic: {},
        comments: [],
        name: '',
        email: '',
        body: '',
        form: {}
    }),
    mixins: [
        PersistantData('NewComment', [
            'name',
            'email',
            'body',
        ]),
    ],
    computed: {
        ...mapGetters('user', ['user']),
        valid () {
            return !!this.name && !!this.body
        },
    },
    methods: {
      close() {
        this.resolve({ status: false })
        this.dialog = false
        this.name = this.email = this.body = ''
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
      operation () {
          this.form = {
              name: this.name,
              email: this.email,
              body: this.body
          }
          if (!('fanfic' in this.fanfic)) {
              this.form['fanfic'] = this.fanfic.id
          } else {
              this.form['chapter'] = this.fanfic.id
              this.form['fanfic'] = this.fanfic.fanfic
          }
          this.validate()
      },
      validate () {
          this.dialog = false
          this.resolve({ status: true, r: this.form })
          this.name = this.email = this.body = '';
      }
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
