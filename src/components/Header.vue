<template>
    <nav class="flex items-center justify-between flex-wrap bg-white p-6 shadow">
        <div class="flex items-center flex-no-shrink text-teal mr-6">
            <svg width="23.999999999999996" height="23.999999999999996" xmlns="http://www.w3.org/2000/svg">
             <g>
              <title>background</title>
              <rect fill="none" id="canvas_background" height="402" width="582" y="-1" x="-1"/>
             </g>
             <g>
              <title>Layer 1</title>
              <path id="svg_2" fill="#16a085" d="m3,8l0,2l0,1l0,3l0,1l0,5l0,1c0,1.105 0.8954,2 2,2l14,0c1.105,0 2,-0.895 2,-2l0,-1l0,-5l0,-4l0,-3l-18,0z"/>
              <path id="svg_3" fill="#ecf0f1" d="m3,6.999976l0,2l0,1l0,3l0,1l0,5l0,1c0,1.1 0.8954,2 2,2l14,0c1.105,0 2,-0.9 2,-2l0,-1l0,-5l0,-4l0,-3l-18,0z"/>
              <path id="svg_4" fill="#bdc3c7" d="m3,5.999976l0,2l0,1l0,3l0,1l0,5l0,1c0,1.1 0.8954,2 2,2l14,0c1.105,0 2,-0.9 2,-2l0,-1l0,-5l0,-4l0,-3l-18,0z"/>
              <path id="svg_5" fill="#ecf0f1" d="m3,4.999976l0,2l0,1l0,3l0,1l0,5l0,1c0,1.1 0.8954,2 2,2l14,0c1.105,0 2,-0.9 2,-2l0,-1l0,-5l0,-4l0,-3l-18,0z"/>
              <path id="svg_6" fill="#16a085" d="m5,1c-1.1046,0 -2,0.8954 -2,2l0,1l0,4l0,2l0,1l0,3l0,1l0,5l0,1c0,1.105 0.8954,2 2,2l2,0l0,-1l-1.5,0c-0.8284,0 -1.5,-0.672 -1.5,-1.5s0.6716,-1.5 1.5,-1.5l12.5,0l1,0c1.105,0 2,-0.895 2,-2l0,-1l0,-5l0,-4l0,-3l0,-1c0,-1.1046 -0.895,-2 -2,-2l-4,0l-10,0z"/>
              <path id="svg_7" fill="#1abc9c" d="m8,1l0,18l1,0l9,0l1,0c1.105,0 2,-0.895 2,-2l0,-1l0,-5l0,-4l0,-3l0,-1c0,-1.1046 -0.895,-2 -2,-2l-4,0l-6,0l-1,0z"/>
             </g>
            </svg>
            <span class="font-semibold text-xl tracking-tight">{{ title }}</span>
        </div>
        <div class="block lg:hidden">
            <button @click="toggle" class="flex items-center px-3 py-2 border rounded text-teal-lighter border-teal-light hover:text-teal hover:border-white">
              <svg class="fill-current h-3 w-3" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><title>Menu</title><path d="M0 3h20v2H0V3zm0 6h20v2H0V9zm0 6h20v2H0v-2z"/></svg>
            </button>
        </div>
        <div :class="open ? 'block': 'hidden'" class="w-full block flex-grow lg:flex lg:items-center lg:w-auto">
            <div class="text-sm lg:flex-grow">
                <router-link :to="{ name: 'List' }" class="block mt-4 lg:inline-block lg:mt-0 text-teal hover:text-teal-darker mr-4">Lire des histoires</router-link>
                <router-link :to="{ name: 'Category' }" class="block mt-4 lg:inline-block lg:mt-0 text-teal hover:text-teal-darker mr-4">Parcourir les catégories</router-link>
                <router-link :to="{ name: 'Login' }" class="block mt-4 lg:inline-block lg:mt-0 text-teal hover:text-teal-darker mr-4">Se connecter</router-link>
                <router-link :to="{ name: 'Blog' }" class="block mt-4 lg:inline-block lg:mt-0 text-teal hover:text-teal-darker">Blog</router-link>
            </div>
        </div>
    </nav>

</template>

<script>
export default {
    props: {
      title: {
        type: String,
        required: true
      }
    },
    data(){
        return{
            open: false,
        }
    },
    methods: {
      toggle (){
        this.open = !this.open
      }
    }
}
</script>

<style scoped>
nav {
    margin-bottom: 14px;
}
</style>
