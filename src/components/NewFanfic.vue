<template>
    <div>
        <h1>{{ subtitle }}</h1>

    </div>
</template>

<script>
export default {
    name: 'NewFanfic',
    data(){
        return{
            subtitle: 'Ecrire une nouvelle fanfiction',
            error: null,
        }
    },
    async created () {
        
    },
}
</script>

<style scoped>
</style>
