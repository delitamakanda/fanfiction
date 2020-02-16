<template>
  <div>
    <nav class="flex flex-col sm:flex-row">
      <router-link :to="{name: 'MonProfil', params: {}}" tag="button" :class="$route.name === 'MonProfil' ? 'border-b-2 font-medium border-blue-500': ''" class="text-gray-600 py-4 px-6 block hover:text-blue-500 focus:outline-none">Mon profil</router-link>
      <router-link :to="{name: 'Social', params: {}}" tag="button" :class="$route.name === 'Social' ? 'border-b-2 font-medium border-blue-500' : ''" class="text-gray-600 py-4 px-6 block hover:text-blue-500 focus:outline-none">Social</router-link>
      <router-link :to="{name: 'MyReviews', params: {}}" tag="button" :class="$route.name === 'MyReviews' ? 'border-b-2 font-medium border-blue-500': ''" class="text-gray-600 py-4 px-6 block hover:text-blue-500 focus:outline-none">Mes commentaires</router-link>
    </nav>
    <router-view />
  </div>
</template>

<script>
</script>

<style scoped>
</style>
