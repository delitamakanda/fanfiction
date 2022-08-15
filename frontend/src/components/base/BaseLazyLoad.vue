<template>
    <div v-show="showLoader">
        <slot></slot>
    </div>
</template>

<script lang="ts">
import { ref, watch } from 'vue';

export default {
    name: 'BaseLazyLoad',
    props: {
        show: {
            type: Boolean,
            default: false
        },
        delay: {
            type: Number,
            default: 500
        }
    },
    setup(props) {
        const showLoader = ref(false);

        let timeout;

        watch(
            () => props.show, 
            (show) => {
            if(show) {
                timeout = setTimeout(() => {
                    showLoader.value = true;
                }, props.delay);
            } else {
                clearTimeout(timeout);
                showLoader.value && (showLoader.value = false);
            }
        });

        return {
            showLoader
        }
    }
}
</script>