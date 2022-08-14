<template>
    <div>
        {{ $t("message.hello", {name: "dma"}) }}
        <button @click="increase">Clicked {{ count }} times.</button>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';

export default defineComponent({
    setup() {
        const count = ref(0);
        const increase = () => {
            count.value++;
        }

        return {
            count, increase
        }
    }
})
</script>

<style lang="scss">
* {
    padding: 0;
    margin: 0;
}
div {
    background-color: red;
}
</style>