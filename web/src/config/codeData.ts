export default {
  result_data: [
    { text: "等待中..", value: 0 },
    { text: "等待重判", value: 1 },
    { text: "编译中", value: 2 },
    { text: "运行并评判", value: 3 },
    { text: "答案正确", value: 4 },
    { text: "格式错误", value: 5 },
    { text: "答案错误", value: 6 },
    { text: "时间超限", value: 7 },
    { text: "内存超限", value: 8 },
    { text: "输出超限", value: 9 },
    { text: "运行错误", value: 10 },
    { text: "编译错误", value: 11 },
    { text: "编译器错误", value: 12 },
  ],
  language_data: [
    { text: "C", value: 0, code: "c" },
    { text: "C++", value: 1, code: "cpp" },
    { text: "Java", value: 2, code: "java" },
    { text: "Python2", value: 3, code: "python" },
    { text: "Python3", value: 4, code: "python" },
    { text: "Bash", value: 5, code: "bash" },
    { text: "Pascal", value: 6, code: "pascal" },
    // { text: "Switch", value: 7, code: "swift" },
    // { text: "C#", value: 8, code: "csharp" },
    // { text: "Go", value: 9, code: "go" },
    // { text: "Ruby", value: 10, code: "ruby" },
  ],
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
    vb: "vb",
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
