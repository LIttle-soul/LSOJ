<template>
    <div class="code-editor" ref="container"></div>
</template>

<script>
import * as monaco from "monaco-editor";
import {mapState} from "vuex";
export default {
    mounted() {
        this.editor_init();
    },
    computed: {
        ...mapState('code', {
            editor_config: state => state.editor_config
        })
    },
    props: {
        language: {
            type: String,
            default: 'cpp'
        }
    },
    watch: {
        language() {
            this.changeLanguage(this.language);
        },
    },
    methods: {
        editor_init() {
            this.$refs.container.innerHTML = "";
            this.monacoEditor = monaco.editor.create(this.$refs.container, this.editor_config);
        },
        changeLanguage(val) {
            // console.log(val);
            var mod = monaco.editor.createModel('', val);
            this.monacoEditor.setModel(mod);
        },
        getVal() {
            var text = this.monacoEditor.getValue();
            return text;
        }
    }
}
</script>

<style scoped>
.code-editor {
    width: 100%;
    height: 100%;
}
</style>
