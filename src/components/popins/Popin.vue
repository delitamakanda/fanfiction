<template>
  <transition name="modal-fade">
    <div class="modal-container" v-model="dialog" v-show="dialog">
      <div class="modal"
        role="dialog"
        aria-labelledby="modalTitle"
        aria-describedby="modalDescription"
      >
        <header class="modal-header" id="modalTitle">
            <h3>{{ pages.title }}</h3>
        </header>
        <section
          class="modal-body"
          id="modalDescription"
        >
          <vue-markdown :source='pages.content'>{{ pages.content }}</vue-markdown>
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
import VueMarkdown from 'vue-markdown'
import { mapState, mapActions } from 'vuex'

 export default {
    data: () => ({
        dialog: false,
        resolve: null,
        reject: null
    }),
    computed: {
        ...mapState('other', ['pages']),
    },
    methods: {
      ...mapActions('other', ['clearPages']),
      close() {
        this.resolve({ status: false })
        this.dialog = false
        this.clearPages()
      },
      openModal () {
        this.dialog = true
        return new Promise((resolve, reject) => {
            this.resolve = resolve
            this.reject = reject
        })
      },
    },
    components: { VueMarkdown }
  };
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
