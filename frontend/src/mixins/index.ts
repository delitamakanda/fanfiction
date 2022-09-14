const mixins = {
    confirm (message, callback) {
        if (window.confirm(message)) {
            callback();
        }
    }
};

export default mixins;
