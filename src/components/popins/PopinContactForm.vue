<template>
<transition name="modal-fade">
        <div class="modal-container" v-model="dialog" v-show="dialog">
            <div class="modal"
            role="dialog"
            aria-labelledby="modalTitle"
            aria-describedby="modalDescription"
            >
            <header class="modal-header" id="modalTitle">
                <h3>{{ $t('message.formContactTitle') }}</h3>
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
            <div class="mb-4" v-if="!isOnline">
                <label class="block text-grey-darker text-sm font-bold mb-2" for="from_email">
                    {{ $t('message.formContactEmailLabel') }}
                </label>
                <Input
                name="from_email"
                type="email"
                v-model="from_email"
                :placeholder="$t('message.formContactEmailLabel')"
                required />
            </div>
            <div class="mb-6">
                <label class="block text-grey-darker text-sm font-bold mb-2" for="subject">
                    {{ $t('message.formContactSubjectLabel') }}
                </label>
                <Input
                name="subject"
                type="text"
                v-model="subject"
                :placeholder="$t('message.formContactSubjectLabel')" />
            </div>
            <div class="mb-6">
                <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="message">
                    {{ $t('message.formContactMessageLabel') }}
                </label>
                <Input
                type="textarea"
                name="message"
                v-model="message"
                :placeholder="$t('message.formContactMessageLabel')"
                maxlength="1000"
                rows="4" />
            </div>
            <template slot="actions">
                <div class="flex items-center justify-between">
                    <button
                    class="bg-blue hover:bg-blue-dark text-white font-bold py-2 px-4 rounded"
                    type="submit"
                    :disabled="!valid">
                    {{ $t('message.formContactValidateLabel') }}
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
    import { mapGetters } from 'vuex'

    export default {
        data: () => ({
            dialog: false,
            resolve: null,
            reject: null,
            from_email: '',
            subject: '',
            message: '',
            form: {},
            isOnline: false
        }),
        computed: {
            ...mapGetters('user', ['user']),
            valid () {
                return !!this.subject && !!this.message
            }
        },
        methods: {
            close() {
                this.resolve({ status: false })
                this.dialog = false
                this.subject = this.message = ''
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
                    subject: this.subject,
                    message: this.message
                }
                this.form['from_email'] = (this.user && this.user.id != null ? this.user.email : this.from_email)

                this.validate()
            },
            validate () {
                this.dialog = false
                this.resolve({ status: true,  r: this.form })
                this.subject = this.message = ''
            }
        },
        watch: {
            user(val, old) {
                const obj = val
                if (Object.keys(obj).length === 0 && obj.constructor === Object) {
                    this.isOnline = false;
                } else {
                    this.isOnline = true;
                }
            }
        }
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
