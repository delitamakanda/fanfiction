<template>
<div>
    {{$route.params.legal}}
</div>
</template>

<script lang="ts">
import { useRoute } from "vue-router";

export default {
    setup() {
        const $route = useRoute();

        return {
            $route,
        };
    },
}
</script>