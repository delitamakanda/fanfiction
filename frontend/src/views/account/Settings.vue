<template>
<div>
    <Breadcrumb />
    <h2 class="mb-4 text-3xl font-extrabold tracking-tight leading-none text-gray-900 md:text-4xl dark:text-white">{{ $t('message.settings.title') }}</h2>
   <p class="my-4 text-lg text-gray-500">{{ $t('message.settings.baseline') }}</p>

<div class="w-full text-sm font-medium text-gray-900 bg-white rounded-lg border border-gray-200 dark:bg-gray-700 dark:border-gray-600 dark:text-white">
    <div v-for="(menu, idx) in menuSettings" :key="idx" @click="navigate(menu)" aria-current="true" class="block py-2 px-4 w-full border-b border-gray-200 cursor-pointer hover:bg-gray-100 hover:text-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-700 focus:text-blue-700 dark:border-gray-600 dark:hover:bg-gray-600 dark:hover:text-white dark:focus:ring-gray-500 dark:focus:text-white">
        {{ $t('message.settings.' + menu.title) }}
    </div>
    <div class="block py-2 px-4 w-full border-b border-gray-200 cursor-pointer hover:bg-gray-100 hover:text-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-700 focus:text-blue-700 dark:border-gray-600 dark:hover:bg-gray-600 dark:hover:text-white dark:focus:ring-gray-500 dark:focus:text-white">
        
        <label for="default-toggle" class="inline-flex relative items-center cursor-pointer">
        <input type="checkbox" value="" id="default-toggle" class="sr-only peer">
        <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600"></div>
        <span class="ml-3 text-sm font-medium text-gray-900 dark:text-gray-300">{{ $t('message.settings.darkModeLabel')}}</span>
        </label>

    </div>
    
    <div class="block py-2 px-4 w-full rounded-b-lg cursor-pointer hover:bg-gray-100 hover:text-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-700 focus:text-blue-700 dark:border-gray-600 dark:hover:bg-gray-600 dark:hover:text-white dark:focus:ring-gray-500 dark:focus:text-white">
        <Select :options="$options.selectedOptions" v-model="selected" label="label" caption="">
            <template v-slot:option="{ option }" >
            <div class="option">
                <img class="img" :src="option.src" :alt="option.label" />
                <span> {{ option.label }}</span>
            </div>
            </template>
        </Select>
    </div>
    
</div>

</div>
</template>

<script lang="ts">
import Breadcrumb from '../../components/base/Breadcrumb.vue';
import { menuSettings } from '../../constants/appConstants';
import Select from '../../components/common/Select.vue';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';

export default {
    components: {
        Breadcrumb,
        Select,
    },
    data() {
        return {
            selected: 'Français'
        }
    },
    setup() {
        const router = useRouter();
        const store = useStore();
        const navigate = (menu: any) => {
            if (menu.navigation) {
                router.push(menu.route);
            } else if (menu.name === 'AccountDelete') {
                console.log('AccountDelete');
            } else if (menu.name === 'ClearCache') {
                console.log('ClearCache');
            }
        }

        return {
            router,
            menuSettings,
            navigate,
            store,
        }
    },
    created() {
        (<any>this).$options.selectedOptions = [
            {
                src: "https://cdn.countryflags.com/thumbs/france/flag-3d-250.png",
                label: (<any>this).$t("message.settings.switchLanguageLabel.fr"),

            },
            {
                src: "https://cdn.countryflags.com/thumbs/united-kingdom/flag-3d-250.png",
                label: (<any>this).$t("message.settings.switchLanguageLabel.en"),

            },
        ];
    }
}
</script>

<style lang="scss" scoped>
.option {
    display: flex;
}
</style>