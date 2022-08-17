<template>
    <component :is="component" class="tag" v-bind="$attrs">
        <slot /> 
    </component>
</template>

<script lang="ts">
export default {
    inheritAttrs: false, 
    props: {
        component: { 
            type: String, 
            default: 'div',
        },
    },
}
</script>

<style lang="scss"> 
.tag {
    padding: 3px 2px;
    font-weight: bold;
    color: white;
    background-color: purple;
    border-radius: 8px;
} 
</style>