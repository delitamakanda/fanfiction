<template>
    <ul class="pagination">
        <li class="pagination-item">
            <button type="button" @click="onClickFirstPage" :disabled="isInFirstPage">Premier</button>
        </li>
        <li class="pagination-item">
            <button type="button" @click="onClickPreviousPage" :disabled="isInFirstPage">Précédent</button>
        </li>
        <li class="pagination-item" v-for="page in pages">
            <button type="button" @click="onClickPage(page.name)" :disabled="page.isDisabled" :class="{active: isPageActive(page.name) }">{{ page.name }}</button>
        </li>
        <li class="pagination-item">
            <button type="button" @click="onClickNextPage" :disabled="isInLastPage">Suivant</button>
        </li>
        <li class="pagination-item">
            <button type="button" @click="onClickLastPage" :disabled="isInLastPage">Dernier</button>
        </li>
    </ul>
</template>

<script>
export default {
    name: 'pagination',
    props: {
        maxVisibleButtons: {
            type: Number,
            required: false,
            default: 3
        },
        totalPages: {
            type: Number,
            required: true
        },
        total: {
            type: Number,
            required: true
        },
        perPage: {
            type: Number,
            required: true
        },
        currentPage: {
            type: Number,
            required: true
        }
    },
    data () {
        return {
            currentPage: 1
        }
    },
    computed: {
        startPage () {
            if (this.currentPage === 1) {
                return 1
            }

            if (this.currentPage === this.totalPages) {
                return this.totalPages - this.maxVisibleButtons + 1
            }

            return this.currentPage - 1
        },

        endPage () {
            return Math.min(this.startPage + this.maxVisibleButtons - 1, this.totalPages)
        },

        pages () {
            const range = []

            for (let i = this.startPage; i <= Math.min(this.startPage + this.maxVisibleButtons - 1, this.totalPages); i+=1) {
                range.push({
                    name: i,
                    isDisabled: i === this.currentPage
                })
            }

            return range
        },

        isInFirstPage() {
            return this.currentPage === 1
        },

        isInLastPage() {
            return this.currentPage === this.totalPages
        },
    },

    methods: {
        onClickFirstPage () {
            this.$emit('pagechanged', 1)
        },

        onClickPreviousPage () {
            this.$emit('pagechanged', this.currentPage - 1)
        },

        onClickPage(page) {
            this.$emit('pagechanged', page)
        },

        onClickNextPage() {
            this.$emit('pagechanged', this.currentPage + 1)
        },

        onClickLastPage() {
            this.$emit('pagechanged', this.totalPages)
        },

        isPageActive(page) {
            return this.currentPage === page
        },

        onPageChange(page) {
            console.log(page)
            this.currentPage = page
        }
    }

}
</script>

<style scoped>
.pagination {
  list-style-type: none;
}

.pagination-item {
  display: inline-block;
}

.active {
  background-color: #4aae98;
  color: #fff;
}
</style>
