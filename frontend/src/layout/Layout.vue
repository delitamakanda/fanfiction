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

export default {
    setup() {
        const { layout, LAYOUTS } = useLayout();

        const layoutComponents = {
            [LAYOUTS.standard]: StandardLayout,
            [LAYOUTS.auth]: AuthLayout,
        };

        const currentLayoutComponent = computed(
            () => layoutComponents[layout.value],
        );

        return {
            currentLayoutComponent,
        }
    }
};
</script>
