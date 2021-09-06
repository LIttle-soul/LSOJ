<template>
  <div class="problem-nav">
    <el-card class="box-card" v-for="card in card_data" :key="card.key">
      <template #header>
        <div class="card-header">
          <span>{{card.title}}</span>
        </div>
      </template>
      <a v-for="item in card.data" :key="item.value" href="#" class="text">
        {{ item.title }}
      </a>
    </el-card>
  </div>
</template>

<script>
export default {
  setup() {},
  data() {
      return {
          card_data: [
              {
                  title: '题目标签',
                  key: 1,
                  data: [
                      {
                          title: '基础题',
                          value: 1
                      },
                      {
                          title: '普通题',
                          value: 2
                      },
                      {
                          title: '提高题',
                          value: 3
                      }
                  ]
              },
              {
                  title: '题目来源',
                  key: 2,
                  data: [
                      {
                          title: '金华职业技术学院',
                          value: 1
                      },
                      {
                          title: '浙师大',
                          value: 2
                      },
                      {
                          title: '浙江大学',
                          value: 3
                      }
                  ]
              }
          ]
      }
  }
};
</script>

<style>
.problem-nav .box-card {
    min-height: 250px;
    text-align: center;
}

.problem-nav .box-card .el-card__header {
    font-size: 16px;
    height: 30px;
    line-height: 30px;
    text-align: center;
    padding: 0;
    font-family: '楷体';
}
.problem-nav .box-card .el-card__body {
    padding: 0;
}
.problem-nav .box-card:nth-child(1) {
    margin-bottom: 40px;
}
.problem-nav .text {
    margin: 4px;
    padding: 4px;
    border: 1px solid rgba(243, 225, 166, 0.8);
    background-color: rgba(243, 225, 166, 0.6);
    box-shadow: 3px 3px rgba(243, 225, 166, 0.4);
    border-radius: 10px;
    text-align: center;
    white-space:nowrap;
    font-size: 12px;
    line-height: 40px;
}
</style>
