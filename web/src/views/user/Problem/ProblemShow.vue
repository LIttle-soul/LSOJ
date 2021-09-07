<template>
  <div class="problem-show">
    <div class="header">
      <ProblemHeader 
        :problem_title="problem_data.problem_title"
        :time_limit="problem_data.time_limit"
        :memory_limit="problem_data.memory_limit"
      />
    </div>
    <div class="container">
      <div class="left">
        <ProblemChild mode="preview" height="100%" :content="problem_data.problem_description" />
      </div>
      <div class="right">
        <CodeEditor />
      </div>
    </div>
  </div>
</template>

<script>
import { defineAsyncComponent } from "@vue/runtime-core";
import ProblemModel from '@/assets/markdown/问题模板.md';
import { mapGetters } from 'vuex';

export default {
  components: {
    ProblemHeader: defineAsyncComponent(() =>
      import("@/components/Problem/ProblemHeader.vue")
    ),
    ProblemChild: defineAsyncComponent(() =>
      import("@/components/Editor/MarkdownEditor.vue")
    ),
    CodeEditor: defineAsyncComponent(() =>
      import("@/components/Editor/CodeEditor.vue")
    ),
  },
  created() {
    this.setData(this.$route.params.problem_id);
  },
  computed: {
    ...mapGetters('problem', {
      getProblemData: 'getProblemData'
    })
  },
  setup() {},
  data() {
    return {
      problem_data: {
        problem_title: 'Hello, World',
        problem_description: ProblemModel,
        time_limit: 1000,
        memory_limit: 128
      }
    };
  },
  methods: {
    setData(data) {
      let val = this.getProblemData(data);
      // console.log(val, data);
      this.problem_data.problem_title = val.problem_title
      this.problem_data.problem_description = val.problem_description
      this.problem_data.time_limit = val.time_limit
      this.problem_data.memory_limit = val.memory_limit
    },
  }
};
</script>


<style scoped>
.problem-show {
  width: 100%;
  min-width: 800px;
  min-height: 600px;
  height: 100vh;
}
.header {
  width: 100%;
  height: 50px;
  position: absolute;
  top: 0;
  background-color: rgba(0, 25, 35, 0.9);
}
.container {
  width: 100%;
  position: absolute;
  top: 50px;
  bottom: 0;
}
.left {
  width: 50%;
  height: 100%;
  float: left;

}
.right {
  width: 50%;
  height: 100%;
  float: left;
}
</style>
