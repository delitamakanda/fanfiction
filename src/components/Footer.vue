<template>
    <div>
        <div class="error bg-red-lightest border border-red-light text-red-dark px-4 py-3 rounded relative" v-if="hasRemoteErrors" role="alert">
            {{ errorFetch }}
        </div>

        <Loading v-if="remoteDataBusy" />

        <footer>
            <ul class="list-horizontal">
                <li>Copyright 2018 {{ title }}</li>
                <li v-for="page in pages" :key="page.id">
                    <button type="button" @click="openModal(page.type)">{{ page.title }}</button>
                </li>
            </ul>
        </footer>

        <modal
          v-show="isModalVisible"
              @close="closeModal"
            >

            <h3 slot="header">{{ legal.title }}</h3>
            <div slot="body">
                <vue-markdown :source='legal.content'>{{legal.content}}</vue-markdown>
            </div>
        </modal>

        <modal
          v-show="isRgpdModalVisible"
              @close="closeRgpdModal"
            >
            <h3 slot="header">{{ rgpd.title }}</h3>
            <div slot="body">
                <vue-markdown :source='rgpd.content'>{{rgpd.content}}</vue-markdown>
            </div>
        </modal>
    </div>
</template>

<script>
import modal from './Modal.vue'
import VueMarkdown from 'vue-markdown'
import RemoteData from '../mixins/RemoteData'

export default {
    props: {
      title: {
        type: String,
        required: true,
      }
    },
    components: {
     modal,
     VueMarkdown,
   },
   mixins: [
       RemoteData({
           legal () {
               return 'pages/legal'
           },
           rgpd () {
               return 'pages/rgpd'
           },
           pages () {
               return 'pages'
           }
       })
   ],
    data(){
        return{
          isModalVisible: false,
          isRgpdModalVisible: false,
          legal: [],
          rgpd: [],
          pages: [],
          errorFetch: 'Il y a un problème avec la requète.'
        }
    },
    methods: {
        openModal (pageType) {
            switch (pageType) {
                case "legal":
                    this.legalModal();
                    break;
                case "rgpd":
                    this.rgpdModal();
                    break;
                default:

            }
        },
        legalModal () {
            this.isModalVisible = true;
        },

        rgpdModal () {
            this.isRgpdModalVisible = true;
        },
        closeModal() {
            this.isModalVisible = false;
        },

        closeRgpdModal () {
            this.isRgpdModalVisible = false;
       }
    },
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
