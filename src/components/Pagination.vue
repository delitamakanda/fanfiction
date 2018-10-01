<template>
    <ul class="list-reset flex">
        <li class="mr-3">
            <button class="inline-block border border-white rounded hover:border-grey-lighter text-teal hover:bg-grey-lighter py-1 px-3" type="button" @click="onClickFirstPage" :disabled="isInFirstPage">Premier</button>
        </li>
        <li class="mr-3">
            <button class="inline-block border border-white rounded hover:border-grey-lighter text-teal hover:bg-grey-lighter py-1 px-3" type="button" @click="onClickPreviousPage" :disabled="isInFirstPage">Précédent</button>
        </li>
        <li class="mr-3"
            v-for="page in pages"
            :key="page.name">
            <button
            class="inline-block border border-white rounded hover:border-grey-lighter text-teal hover:bg-grey-lighter py-1 px-3"
            type="button"
            @click="onClickPage(page.name)"
            :disabled="page.isDisabled"
            :class="{ 'inline-block border border-teal rounded py-1 px-3 text-white': isPageActive(page.name) }"
            >
                {{ page.name }}
            </button>
        </li>
        <li class="mr-3">
            <button class="inline-block border border-white rounded hover:border-grey-lighter text-teal hover:bg-grey-lighter py-1 px-3" type="button" @click="onClickNextPage" :disabled="isInLastPage">Suivant</button>
        </li>
        <li class="mr-3">
            <button class="inline-block border border-white rounded hover:border-grey-lighter text-teal hover:bg-grey-lighter py-1 px-3" type="button" @click="onClickLastPage" :disabled="isInLastPage">Dernier</button>
        </li>
    </ul>
</template>

<script>
export default {
    name: 'Pagination',
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
        currentPage: {
            type: Number,
            required: true
        }
    },
    computed: {
        startPage () {
            if (this.currentPage === 1) {
                return 1
            }

            if (this.currentPage === this.totalPages) {
                return this.totalPages - this.maxVisibleButtons
            }

            return this.currentPage - 1
        },
        isInFirstPage () {
            return this.currentPage === 1
        },
        isInLastPage () {
            return this.currentPage === this.totalPages
        },
        pages () {
            const range = []

            for (let i = this.startPage; i <= Math.min(this.startPage + this.maxVisibleButtons - 1, this.totalPages); i+= 1) {
                range.push({
                    name: i,
                    isDisabled: i === this.currentPage
                });
            }
            return range
        }
    },
    methods: {
        onClickFirstPage () {
            this.$emit('pagechanged', 1)
        },
        onClickPreviousPage () {
            this.$emit('pagechanged', this.currentPage - 1)
        },
        onClickPage (page) {
            this.$emit('pagechanged', page)
        },
        onClickNextPage () {
            this.$emit('pagechanged', this.currentPage + 1)
        },
        onClickLastPage () {
            this.$emit('pagechanged', this.totalPages)
        },
        isPageActive (page) {
            return this.currentPage === page
        }
    }
};
</script>

<style scoped>
</style>
