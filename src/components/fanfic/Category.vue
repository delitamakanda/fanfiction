<template>
    <div>
        <div class="flex flex-wrap list-reset -mx-2">
            <div class="md:w-1/3 sm:w-1/2 w-full px-2 relative overflow mb-4" v-for="(category, i) in categories" :key="category.id" v-if="categories && categories.length > 0 && i <= limitationList"><a nohref class="cursor-pointer" @click="sortByCategories(category.id)">
                <div v-if="category.logic_value !== ''" :style="{backgroundImage: 'url(' + require('./../../assets/img/categories/'+ category.logic_value + '.jpg') + ')' }" :alt="category.name" :title="category.name" class="img-thumbnail border border-grey-light shadow"></div>
                <div v-else :style="{backgroundImage: 'url(' + require('./../../assets/img/categories/empty.jpg') + ')' }" class="img-thumbnail border border-grey-light shadow"></div>
                <span class="caption">{{ category.name }}</span>
            </a></div>
        </div>
        <div class="flex">
            <div @click="readMore(limitationList)" class="flex-1 mb-4 cursor-pointer bg-teal hover:bg-teal-dark text-center text-white font-bold py-2 px-4 rounded-full">{{ $t('message.watchLabel')}} {{ limitationList == 5 ? $t('message.showMore'): $t('message.showLess')}}</div>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        categories: {type: Array, required: true, default: {}}
    },
    data () {
        return {
            moreStr: this.$t('message.showMore'),
            limitationList: 5,
        }
    },
    computed: {
        categoryName: function () {
            return this.selected;
        }
    },
    methods: {
        sortByCategories (categoryId) {
            for (let i = 0; i < this.categories.length; i++) {
                if (this.categories[i].id == categoryId) {
                    this.$emit('selectedCategory', this.categories[i])
                }
            }
        },
        readMore (limitationList) {
            if (this.limitationList == this.categories.length) {
                this.limitationList = 5
            } else {
                this.limitationList = this.categories.length
            }
        }
    }
}
</script>

<style scoped>
.img-thumbnail {
    height: 250px;
    background-size: cover;
}

.caption {
    background: rgba(0, 0, 0, 0.5);
    color: #fff;
    display: table;
    position: absolute;
    float: left;
    text-transform: uppercase;
    bottom: 15%;
    padding: 5px;
}
</style>
