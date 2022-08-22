<template>
<component :is="currentLayoutComponent">
    <template
        v-for="slotName in Object.keys($slots)"
        :key="slotName"
        v-slot:[slotName]="slotProps"
    >
        <slot :name="slotName" v-bind="slotProps"></slot>
    </template>
</component>
</template>

<script lang="ts">
import StandardLayout from './components/StandardLayout.vue';
import AuthLayout from './components/AuthLayout.vue';
import { useLayout  } from './composables/useLayout';
import { computed  } from 'vue';

const layoutComponents = {
    standard: StandardLayout,
    auth: AuthLayout,
};

export default {
    computed: {
        currentLayoutComponent() {
            const layout = (<any>this).$router.currentRoute.value?.meta?.layout || 'standard';
            return layoutComponents[layout];
        }
    },
};
</script>
