<template>
  <transition name="modal-fade">
    <div class="modalContainer" v-show="dialog">
      <div class="modal"
        role="dialog"
        aria-labelledby="modalTitle"
        aria-describedby="modalDescription"
      >
        <header class="modalHeader" id="modalTitle">
          <slot name="header">

            <button
              type="button"
              class="btnClose"
              @click="close"
            >
              x
            </button>
          </slot>
        </header>
        <section
          class="modalBody"
          id="modalDescription"
        >
          <slot name="body">

          </slot>
         </section>
         <footer class="modalFooter">
            <slot name="footer">

              <button
                type="button"
                class="btnOutlineGreen"
                @click="confirm"
                aria-label="Close modal"
              >
                Confirmer
            </button>
              <button
                type="button"
                class="btnGreen"
                @click="close"
                aria-label="Close modal"
              >
                Fermer
            </button>
          </slot>
        </footer>
      </div>
    </div>
  </transition>
</template>

<script>
  export default {
    name: 'modal',
    data: () => ({
      dialog: false,
      resolve: null,
      reject: null,
    }),

    methods: {
      open() {
        this.dialog = true;
        return new Promise((resolve, reject) => {
          this.resolve = resolve;
          this.reject = reject;
        });
      },
      close() {
        this.dialog = false;
        this.resolve({ status: false });
      },
      confirm() {
        this.dialog = false;
        this.resolve({ status: true });
      }
    },
  };
</script>

<style lang="scss" scoped>
  .modalContainer {
    position: fixed;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    z-index: 88;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #0000004d;
  }

  .modal {
    display: flex;
    flex-direction: column;
    width: 100%;
    max-width: 450px;
    overflow-y: auto;
    background: #FFF;
    box-shadow: 2px 2px 20px 1px;
  }

  .modalHeader,
  .modalFooter {
    display: flex;
    padding: 15px;
  }

  .modalHeader {
    justify-content: space-between;
    color: #4AAE9B;
    border-bottom: 1px solid #eee;
  }

  .modalFooter {
    justify-content: flex-end;
    border-top: 1px solid #eee;
  }

  .modalBody {
    position: relative;
    max-height: 330px;
    padding: 20px 10px;
    overflow-x: hidden;
    overflow-y: auto;
  }

  .btnClose {
    padding: 20px;
    font-size: 20px;
    font-weight: bold;
    color: #4AAE9B;
    cursor: pointer;
    background: transparent;
    border: none;
  }

  .btnGreen {
    padding: 5px 8px;
    color: #FFF;
    background: #4AAE9B;
    border: 1px solid #4AAE9B;
    border-radius: 2px;
  }
  .btnOutlineGreen {
    padding: 5px 8px;
    margin-right: 10px;
    color: #4AAE9B;
    background: #FFF;
    border: 1px solid #4AAE9B;
    border-radius: 2px;
  }
</style>
