<template>
  <div class="pdf-container">
    <canvas id="pdf-canvas"></canvas>
    <div class="bottom-button">
      <el-button @click="prePage">上一页</el-button>
      <p>第{{ data.cur_page }}/{{ data.pdfPages }}页</p>
      <el-button @click="nextPage">下一页</el-button>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref, nextTick } from "vue";
import * as PdfJs from "pdfjs-dist";
import * as PDFViewer from "pdfjs-dist/web/pdf_viewer";
import * as webSrc from "pdfjs-dist/build/pdf.worker.entry";
import { Agent } from "https";
PdfJs.GlobalWorkerOptions.workerSrc = webSrc;

let prop = defineProps({
  src: {
    default: "/api/course/Video/",
  },
});

let data = ref({
  cur_page: 1,
  pdfPages: 0, // pdf文件的页数
  pdfScale: 1.0, // 缩放比例
});

let prePage = () => {
  if (data.value.cur_page > 1) {
    data.value.cur_page -= 1;
    renderPage(data.value.cur_page, pdfDOC);
  }
};
let nextPage = () => {
  if (data.value.cur_page < data.value.pdfPages) {
    data.value.cur_page += 1;
    renderPage(data.value.cur_page, pdfDOC);
  }
};

let pdfDOC = <any>null;

let loadFile = (url: string): void => {
  const loadingTask = PdfJs.getDocument({
    url: url,
    // data: atob(
    //   "JVBERi0xLjcKCjEgMCBvYmogICUgZW50cnkgcG9pbnQKPDwKICAvVHlwZSAvQ2F0YWxvZwog" +
    //     "IC9QYWdlcyAyIDAgUgo+PgplbmRvYmoKCjIgMCBvYmoKPDwKICAvVHlwZSAvUGFnZXMKICAv" +
    //     "TWVkaWFCb3ggWyAwIDAgMjAwIDIwMCBdCiAgL0NvdW50IDEKICAvS2lkcyBbIDMgMCBSIF0K" +
    //     "Pj4KZW5kb2JqCgozIDAgb2JqCjw8CiAgL1R5cGUgL1BhZ2UKICAvUGFyZW50IDIgMCBSCiAg" +
    //     "L1Jlc291cmNlcyA8PAogICAgL0ZvbnQgPDwKICAgICAgL0YxIDQgMCBSIAogICAgPj4KICA+" +
    //     "PgogIC9Db250ZW50cyA1IDAgUgo+PgplbmRvYmoKCjQgMCBvYmoKPDwKICAvVHlwZSAvRm9u" +
    //     "dAogIC9TdWJ0eXBlIC9UeXBlMQogIC9CYXNlRm9udCAvVGltZXMtUm9tYW4KPj4KZW5kb2Jq" +
    //     "Cgo1IDAgb2JqICAlIHBhZ2UgY29udGVudAo8PAogIC9MZW5ndGggNDQKPj4Kc3RyZWFtCkJU" +
    //     "CjcwIDUwIFRECi9GMSAxMiBUZgooSGVsbG8sIHdvcmxkISkgVGoKRVQKZW5kc3RyZWFtCmVu" +
    //     "ZG9iagoKeHJlZgowIDYKMDAwMDAwMDAwMCA2NTUzNSBmIAowMDAwMDAwMDEwIDAwMDAwIG4g" +
    //     "CjAwMDAwMDAwNzkgMDAwMDAgbiAKMDAwMDAwMDE3MyAwMDAwMCBuIAowMDAwMDAwMzAxIDAw" +
    //     "MDAwIG4gCjAwMDAwMDAzODAgMDAwMDAgbiAKdHJhaWxlcgo8PAogIC9TaXplIDYKICAvUm9v" +
    //     "dCAxIDAgUgo+PgpzdGFydHhyZWYKNDkyCiUlRU9G"
    // ),
    cMapPacked: true,
    useSystemFonts: true,
    stopAtErrors: true,
    disableRange: true,
  });
  loadingTask.promise.then((pdf) => {
    pdfDOC = pdf;
    data.value.pdfPages = pdfDOC.numPages;
    nextTick(() => {
      renderPage(data.value.cur_page, pdfDOC); // 表示渲染第 1 页
    });
  });
};

let renderPage = (num: number, pdfDoc: any) => {
  pdfDoc.getPage(num).then((page: any) => {
    const canvas: any = document.getElementById("pdf-canvas");
    const ctx: any = canvas.getContext("2d");
    const viewport = page.getViewport({ scale: data.value.pdfScale });
    canvas.width = viewport.width;
    canvas.height = viewport.height;
    canvas.style.width = "100%";
    const renderContext = {
      canvasContext: ctx,
      viewport: viewport,
    };
    page.render(renderContext);
  });
};

loadFile(prop.src);
</script>

<style lang="scss" scoped>
.pdf-container {
  .bottom-button {
    width: 100%;
    display: flex;
    justify-content: center;
    height: 40px;
    line-height: 40px;
    margin-bottom: 20px;
    p {
      margin: 0 20px;
      font-size: 20px;
    }
  }
}
</style>
