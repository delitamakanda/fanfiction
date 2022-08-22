import { ref, computed } from "vue";

export const useLayoutFactory = ({
    layoutComponents,
    LAYOUTS,
    defaultLayout,
}) => {
    const layout = ref(defaultLayout);

    const currentLayoutComponent = computed(
        () => layoutComponents[layout.value],
    );

    const setLayout = layoutType => {
        layout.value = layoutType;
    };

    const useLayout = () => {
        return {
            currentLayoutComponent,
            layout,
            setLayout,
            LAYOUTS,
        };
    };

    return {
        useLayout,
    };
};
