import { h } from 'vue';
import { useLayoutFactory } from '../composables/useLayoutFactory';

export const layoutFactory = ({
    LayoutComponent,
    layoutComponents,
    LAYOUTS,
    defaultLayout,
}) => {
    const { useLayout } = useLayoutFactory({
        layoutComponents,
        LAYOUTS,
        defaultLayout,
    });

    const Component = (props, { attrs, slots }) => {
        const options = { useLayout, ...props, ...attrs };
        return h(LayoutComponent, options, slots);
    };

    return {
        LayoutComponent: Component,
        useLayout,
    };
}