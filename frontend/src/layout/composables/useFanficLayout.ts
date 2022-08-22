import { layoutFactory } from '../helpers/layoutFactory';
import FanficLayoutComponent from '../FanficLayout.vue';
import GridLayout from '../components/GridLayout.vue';
import ListLayout from '../components/ListLayout.vue';

const LAYOUTS = {
    grid: Symbol('grid'),
    list: Symbol('list'),
};

const layoutComponents = {
    [LAYOUTS.grid]: GridLayout,
    [LAYOUTS.list]: ListLayout,
}

const { 
    LayoutComponent: FanficLayout,
    useLayout: useFanficLayout
} = layoutFactory({
    LayoutComponent: FanficLayoutComponent,
    layoutComponents,
    LAYOUTS,
    defaultLayout: LAYOUTS.grid
});

export { FanficLayout, useFanficLayout, LAYOUTS };
