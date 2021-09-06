<template>
  <div class="code-editor">
    <div class="nav">
      <el-select
      v-model="editor_config.language"
      size="mini"
      @change="changeLanguage"
    >
      <el-option
        v-for="item in sets.language"
        :key="item"
        :label="item"
        :value="item"
      >
      </el-option>
    </el-select>
      <el-button type="primary" size="mini" @click="getVal"
      >提交</el-button>
    </div>
    <div class="code">
      <div class="editor-style" ref="container"></div>
    </div>
    <div class="info">
      <div class="info-text">

      </div>
    </div>
  </div>
</template>
<script>
import * as monaco from "monaco-editor";
export default {
  mounted() {
    this.editor_init();
  },
  data() {
    return {
      sets: {
        language: {
          c: "c",
          cpp: "cpp",
          csharp: "csharp",
          go: "go",
          java: "java",
          javascript: "javascript",
          pascal: "pascal",
          perl: "perl",
          php: "php",
          python: "python",
          r: "r",
          ruby: "ruby",
          rust: "rust",
          swift: "swift",
          vb: "vb"
        },
      },
      editor_config: {
        value: "",
        language: "cpp",
        theme: "vs-dark",
        cursorStyle: "line",
        contextmenu: true,
        automaticLayout: true,
        autoIndent: false,
        lineNumbers: true,
        mouseStyle: "text",
        quickSuggestions: false,
        renderLineHighlight: "none",
        wordWrap: "off",
        stopRenderingLineAfter: -1,
        scrollbar: {
          horizontal: "auto",
          vertical: "hidden",
          verticalScrollbarSize: 0,
        },
        minimap: {
          enabled: false,
        },
        lineDecorationsWidth: 0,
        lineNumbersMinChars: 3,
      },
    };
  },
  methods: {
    editor_init() {
      this.$refs.container.innerHTML = "";
      this.monacoEditor = monaco.editor.create(this.$refs.container, this.editor_config);
    },
    changeLanguage(val) {
      var mod = monaco.editor.createModel('', val);
      this.monacoEditor.setModel(mod);  
    },
    // 手动获取值
    getVal() {
      var text = this.monacoEditor.getValue();
      console.log(text);
    }
  },
};
</script>

<style scoped>
.code-editor {
  width: 100%;
  height: 100%;
  position: relative;
}
.nav {
  width: 100%;
  height: 40px;
  position: absolute;
  top: 0;
  background: rgba(1,18,25,0.8);
}
.el-select {
  width: 120px;
  margin-top: 5px;
  margin-left: 10px;
}
.el-button {
  float: right;
  margin: 5px 10px;
}
.code {
  width: 100%;
  position: absolute;
  top: 40px;
  bottom: 200px;
}
.editor-style {
  width: 100%;
  height: 100%;
}
.info {
  width: 100%;
  height: 200px;
  position: absolute;
  bottom: 0;
  background: rgba(1,1,12,0.8);
}
.info-text {
  width: 98%;
  height: 95%;
  margin: 1%;
  background: rgba(124,124,124,0.6);
}
</style>