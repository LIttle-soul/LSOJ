<template>
  <div ref="container" class="monaco-editor" :style="`height: ${height}px`"></div>
</template>

<script>
import * as monaco from 'monaco-editor'
export default {
    name: 'AcMonaco',
    props: {
        opts: {
            type: Object,
            default() {
                return {}
            }
        },
        height: {
            type: Number,
            default: 300
        }
    },
    data() {
        return {
            // 主要配置
            defaultOpts: {
                value: '', // 编辑器的值
                theme: 'vs-dark', // 编辑器主题：vs, hc-black, or vs-dark，更多选择详见官网
                selectOnLineNumbers: true,
                roundedSelection: true, // 右侧不显示编辑器预览框
                autoIndent: true, // 自动缩进
                automaticLayout: true, // 自动布局
                lineNumbers: "on", // 行号显示 on 、 off
                cursorStyle: "line", // 光标样式
                readOnly: false, // 只读模式
                glyphMargin: true, // 字形边缘
                fontSize: 16, // 字体大小
                mouseStyle: "text",
                contextmenu: false,
                fontLigatures: true,
            }

        }
    },
    watch: {
        opts: {
            handler(n) {
                this.init()
            },
            deep: true
        }
    },
    mounted() {
        this.init()
    },
    methods: {
        init() {
            // 初始化container的内容，销毁之前生成的编辑器
            this.$refs.container.innerHTML = ''
            
            this.editorOptions = Object.assign(this.defaultOpts, this.opts)
            // 生成编辑器对象
            this.monacoEditor = monaco.editor.create(this.$refs.container, this.editorOptions)
            // 编辑器内容发生改变时触发
            this.monacoEditor.onDidChangeModelContent(() => {
                this.$emit('change', this.monacoEditor.getValue())
            })
        },
        // 供父组件调用手动获取值
        getVal() {
            return this.monacoEditor.getValue()
        }
    }
}
</script>

<style scoped>
.breakpoints{
    background: red;
    background: radial-gradient(circle at 3px 3px, white, red);
    width: 10px !important;
    height: 10px !important;
    left: 0px !important;
    top: 3px;
    border-radius: 5px;
  }
</style>