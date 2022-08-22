import { camelCase } from 'lodash-es';

const requireModule = require.context(
    '.',
    true,
    /^(?!.*(Actions|Mutations|Getters|Types|helpers|index)).*\.ts$/
);

const modules = {};
requireModule.keys().forEach(fileName => {
    if (/\.unit\.ts$/.test(fileName)) return;

    modules[camelCase(fileName.split('/')[1].replace(/(\.\/|\.ts)/g, ''))] = {
        namespaced: true,
        ...requireModule(fileName).default,
    }
});

export default modules;
