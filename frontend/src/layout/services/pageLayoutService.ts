import { reactive } from "vue";

export const LAYOUTS = {
    standard: Symbol("standard"),
    auth: Symbol("auth"),
};

const initialState = {
    layout: LAYOUTS.standard,
};

const state = reactive(initialState);

export const layoutComputed = {
    layout: {
        get() {
            return state.layout
        },
        set(layoutType) {
            state.layout = layoutType;
        }
    }
};

export const setLayout = layoutType => {
    state.layout = layoutType;
};
