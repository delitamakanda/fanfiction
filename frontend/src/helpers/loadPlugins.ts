const loadPlugins = (filenames) => {
    const requirePlugin = require.context('../plugins', false, /\.ts$/);

    let fileMap = {};
    console.log(requirePlugin.keys());

    for (const filename of requirePlugin.keys()) {
        fileMap[filename.replace('./', '')] = true;
    }

    for (const filename of filenames) {
        const filenameWithExtension = `${filename}.ts`;
        if (Object.prototype.hasOwnProperty.call(fileMap, filenameWithExtension)) {
            requirePlugin(`./${filenameWithExtension}`);
        } else {
            throw new Error(
                `No plugin for ${filename}.
                Did you apply the plugin correctly?
                `
            );
            
        }
    }
}

export default loadPlugins;
