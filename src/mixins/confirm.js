module.exports = {
    methods: {
        confirm (message, callback) {
            if (window.confirm(message)) {
                callback();
            }
        }
    }
};
