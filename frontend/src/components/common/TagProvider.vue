<script lang="ts">
export default {
    emits: ['on-tag-added', 'on-tag-removed'],
    props: {
        options: {
            type: Array,
            default: () => []
        },
        trackBy: {
            type: String
        }
    },
    data() {
        return {
            tags: [...(<any>this).options]
        }
    },
    render() {
        const { tags, addTag, removeTag } = this as any 

        return (<any>this).$slots.default({
            tags,
            addTag,
            removeTag,
        })
    },
    watch: {
        options: {
            handler(val) {
                if (Array.isArray(val)) (<any>this).tags = [...val];
            },
            immediate: true
        }
    },
    methods: {
        addTag(val) {
            (<any>this).tags.push(val);
            (<any>this).$emit('on-tag-added', { tags: (<any>this).tags, val });
        },
        removeTag(val) {
            if ((<any>this).trackBy) {
                (<any>this).tags = (<any>this).tags.filter(tag => tag[(<any>this).trackBy] !== val);
            } else {
                (<any>this).tags.splice(val, 1);
            }
            (<any>this).$emit('on-tag-removed', { tags: (<any>this).tags, val });
        },
        getTags() {
            return (<any>this).tags;
        }
    }
}
</script>