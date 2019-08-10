<template>
<footer>
    <ul class="list-horizontal">
        <li>{{ fullYear }} {{ title }}</li>
        <li><button type="button" @click="openMentionsLegal">{{ $t('message.mentionsLegalesLabel') }}</button></li>
        <li><button type="button" @click="openRgpd">{{ $t('message.politiqueDeConfidentialite') }}</button></li>
    </ul>
    <popin ref="popin"></popin>
</footer>
</template>

<script>
    import popin from '@/components/popins/Popin'
    import RemoteData from '@/mixins/RemoteData'
    import { mapActions } from 'vuex'

    export default {
        props: {
            title: {
                type: String,
                required: true,
            }
        },
        mounted () {
          this.$root.$popin = this.$refs.popin.openModal
        },
        components: { popin },
        computed: {
            fullYear () {
                return `Copyright © ${new Date().getFullYear()}`;
            }
        },
        data(){
            return{
                errorFetch: this.$t('message.errorFetch')
            }
        },
        methods: {
            ...mapActions('other', ['fetchPages']),
            openMentionsLegal () {
              this.fetchPages('legal')
              this.$root
                .$popin()
            },
            openRgpd () {
              this.fetchPages('rgpd');
              this.$root
                .$popin()
            }
        }
    }
</script>

<style scoped>

    footer {
        text-align: center;
        padding-top: 1rem;
        padding-bottom: 1rem;
    }

    ul.list-horizontal li {
        display: inline;
        padding: 0 0.5rem;
    }

    ul.list-horizontal {
        list-style-type: none;
    }
</style>
