import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";

// Element-plus 插件布局
import ElementPlus from "element-plus";
import 'element-plus/dist/index.css'
import "dayjs/locale/zh-cn";
import locale from "element-plus/lib/locale/lang/zh-cn";

// axios请求
import http from "./utils/http";
require("../mock");

// day.js时间日期格式化插件
import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
dayjs.extend(relativeTime);

// ECharts图标组件
import * as ECharts from "echarts";

// v-md-editor
import VMdEditor from "@kangc/v-md-editor/lib/codemirror-editor";
import "@kangc/v-md-editor/lib/style/codemirror-editor.css";

// VuePressTheme
import VuePressTheme from "@kangc/v-md-editor/lib/theme/vuepress.js";
import "@kangc/v-md-editor/lib/theme/style/vuepress.css";

// prism.js
import Prism from "prismjs";

// KaTex
import createKaTexPlugin from "@kangc/v-md-editor/lib/plugins/katex/cdn";

// Mermaid
import createMermaidPlugin from "@kangc/v-md-editor/lib/plugins/mermaid/cdn";
import "@kangc/v-md-editor/lib/plugins/mermaid/mermaid.css";

// TodoList
import createTodoListPlugin from "@kangc/v-md-editor/lib/plugins/todo-list/index";
import "@kangc/v-md-editor/lib/plugins/todo-list/todo-list.css";

// LineNumber
import createLineNumberPlugin from "@kangc/v-md-editor/lib/plugins/line-number/index";

// CopyCode
import createCopyCodePlugin from "@kangc/v-md-editor/lib/plugins/copy-code/index";
import "@kangc/v-md-editor/lib/plugins/copy-code/copy-code.css";

// Align
import createAlignPlugin from "@kangc/v-md-editor/lib/plugins/align";

// CodeMirror
import Codemirror from "codemirror";
// mode
import "codemirror/mode/markdown/markdown";
import "codemirror/mode/javascript/javascript";
import "codemirror/mode/css/css";
import "codemirror/mode/htmlmixed/htmlmixed";
import "codemirror/mode/vue/vue";
// edit
import "codemirror/addon/edit/closebrackets";
import "codemirror/addon/edit/closetag";
import "codemirror/addon/edit/matchbrackets";
// placeholder
import "codemirror/addon/display/placeholder";
// active-line
import "codemirror/addon/selection/active-line";
// scrollbar
import "codemirror/addon/scroll/simplescrollbars";
import "codemirror/addon/scroll/simplescrollbars.css";
// style
import "codemirror/lib/codemirror.css";

VMdEditor.Codemirror = Codemirror;
VMdEditor.use(VuePressTheme, { Prism });
// VueMarkdownEditor.use(createTipPlugin());
VMdEditor.use(createKaTexPlugin());
VMdEditor.use(createMermaidPlugin());
VMdEditor.use(createTodoListPlugin());
VMdEditor.use(createLineNumberPlugin());
VMdEditor.use(createCopyCodePlugin());
VMdEditor.use(createAlignPlugin());

VMdEditor.xss.extend({
  whiteList: {
    source: ["iframe"],
  },
});

import $ from 'jquery'

const app = createApp(App);
app.config.globalProperties.$dayJS = dayjs;
app.config.globalProperties.$http = http;
app.config.globalProperties.$ECharts = ECharts;
app.config.globalProperties.$ = $
app.use(ElementPlus, { locale });
app.use(VMdEditor);
app.use(store);
app.use(router);
app.mount("#app");
