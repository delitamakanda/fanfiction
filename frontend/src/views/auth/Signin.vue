<template>
    <Layout class="mx-auto max-w-7xl">
        <template #header>
            <p>Header</p>
        </template>
        <template #content>
            <p>Content</p>
        </template>
        <template #aside>
            <p>Aside</p>
        </template>
        <template #footer>
            <p>Footer</p>
        </template>
    </Layout>
</template>

<script lang="ts">
import Layout from '../../layout/Layout.vue';

export default {
    components: {
        Layout
    }
    
}
</script>