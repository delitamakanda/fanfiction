const fs = require('fs');
const path = require('path');
const chalk = require('chalk');

const error = (...args) => {
    console.error(chalk.red(...args));
};

const success = (...args) => {
    console.log(chalk.green(...args));
};

const args = process.argv.slice(2);

const modulesPath = 'src/store/modules';

if (!args.length) {
    error('you must provide a name for the module');
    return;
}

const fullModulePath = path.join(__dirname, '../', modulesPath);
if (!fs.existsSync(fullModulePath)) {
    fs.mkdirSync(fullModulePath);
}

const moduleName = args[0];
const modulePath = path.join(__dirname, '../', modulesPath, moduleName);

if (fs.existsSync(modulePath)) {
    error(`${moduleName} directory already exists`);
    process.exit(1);
}

const stateContent = `import getters from './${moduleName}Getters';
import actions from './${moduleName}Actions';
import mutations from './${moduleName}Mutations';

const state = {};

export default {
    state,
    getters,
    actions,
    mutations
};
`;

const exportFileContent = `import * as ${moduleName}Types from './${moduleName}Types';

export default {

};
`;


const statePath = `${path.join(modulePath, `${moduleName}.ts`)}`;
const gettersPath = `${path.join(modulePath, `${moduleName}Getters.ts`)}`;
const actionsPath = `${path.join(modulePath, `${moduleName}Actions.ts`)}`;
const mutationsPath = `${path.join(modulePath, `${moduleName}Mutations.ts`)}`;
const typesPath = `${path.join(modulePath, `${moduleName}Types.ts`)}`;

fs.mkdirSync(modulePath);
fs.appendFileSync(statePath, stateContent);
fs.appendFileSync(gettersPath, exportFileContent);
fs.appendFileSync(actionsPath, exportFileContent);
fs.appendFileSync(mutationsPath, exportFileContent);
fs.appendFileSync(typesPath, '');

success('Module', moduleName, 'generated');
