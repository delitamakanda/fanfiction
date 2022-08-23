<template>

<nav class="bg-white border-gray-200 px-2 sm:px-4 py-2.5 rounded dark:bg-gray-900">
  <div class="container flex flex-wrap justify-between items-center mx-auto">
  <a href="https://flowbite.com/" class="flex items-center">
      <img src="https://flowbite.com/docs/images/logo.svg" class="mr-3 h-6 sm:h-9" alt="Flowbite Logo">
      <span class="self-center text-xl font-semibold whitespace-nowrap dark:text-white">{{title}}</span>
  </a>
  <div class="flex items-center md:order-2">
        <button type="button" class="bg-white p-1 rounded-full text-gray-400 hover:text-gray-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-800 focus:ring-gray-300">
                <span class="sr-only">View notifications</span>
                <!-- Heroicon name: outline/bell -->
                <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                </svg>
        </button>
      <button type="button" class="flex mr-3 text-sm bg-gray-800 rounded-full md:mr-0 focus:ring-4 focus:ring-gray-300 dark:focus:ring-gray-600" id="user-menu-button" aria-expanded="false" data-dropdown-toggle="user-dropdown" data-dropdown-placement="bottom">
        <span class="sr-only">Open user menu</span>
        <img class="w-8 h-8 rounded-full" src="/docs/images/people/profile-picture-3.jpg" alt="user photo">
      </button>
      <!-- Dropdown menu -->
      <div class="z-50 my-4 text-base list-none hidden bg-white rounded divide-y divide-gray-100 shadow dark:bg-gray-700 dark:divide-gray-600 block" id="user-dropdown" data-popper-reference-hidden="" data-popper-escaped="" data-popper-placement="bottom" style="position: absolute; inset: 0px auto auto 0px; margin: 0px; transform: translate(646px, 82px);">
        <div class="py-3 px-4">
          <span class="block text-sm text-gray-900 dark:text-white">Bonnie Green</span>
          <span class="block text-sm font-medium text-gray-500 truncate dark:text-gray-400">name@flowbite.com</span>
        </div>
        <ul class="py-1" aria-labelledby="user-menu-button">
          <li>
            <a href="#" class="block py-2 px-4 text-sm text-gray-700 hover:bg-gray-100 dark:hover:bg-gray-600 dark:text-gray-200 dark:hover:text-white">Dashboard</a>
          </li>
          <li>
            <a href="#" class="block py-2 px-4 text-sm text-gray-700 hover:bg-gray-100 dark:hover:bg-gray-600 dark:text-gray-200 dark:hover:text-white">Settings</a>
          </li>
          <li>
            <a href="#" class="block py-2 px-4 text-sm text-gray-700 hover:bg-gray-100 dark:hover:bg-gray-600 dark:text-gray-200 dark:hover:text-white">Sign out</a>
          </li>
        </ul>
      </div>
  </div>
  </div>
</nav>
</template>

<script lang="ts">
export default {
    props: {
        title: {
            type: String,
            required: true
        }
    }
}
</script>