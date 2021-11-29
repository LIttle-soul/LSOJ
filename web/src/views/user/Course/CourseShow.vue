<template>
  <div class="course-show">
    <el-container>
      <el-header>
        <el-image></el-image>
        <el-descriptions title="课程标题" :column="2">
          <el-descriptions-item label="开课时间" width="22.5%">2021/08/01 至 2022/01/31</el-descriptions-item>
          <el-descriptions-item label="开课状态" width="22.5%">正在开课</el-descriptions-item>
          <el-descriptions-item label="开课院校" width="22.5%">金华职业技术学院</el-descriptions-item>
          <el-descriptions-item label="授课老师" width="22.5%">梅旭时</el-descriptions-item>
          <el-descriptions-item label="课程学分" width="22.5%">2分</el-descriptions-item>
          <el-descriptions-item label="学习人数" width="22.5%">0/41人</el-descriptions-item>
        </el-descriptions>
        <el-button type="warning" plain size="medium" class="course-join">立即参加</el-button>
      </el-header>
      <el-main>
        <el-tabs v-model="activeName" @tab-click="handleClick">
          <el-tab-pane label="课程详情" name="first">
            <div>
              <div class="title">课程简介</div>
              <div class="content-text">
                <div style="text-indent: 2em; line-height: 28px;">
                  企业法律风险防范课程讲授企业法律风险管理体系、企业法律风险分类、宪法法律风险、行政法律风险、民商法律
                  风险、刑事法律风险、经济法律风险、社会法律风险、国际法律风险、诉讼法律风险、企业法律风险防范对策。
                </div>
              </div>
              <div class="title">课程概述</div>
              <div class="content-text">
                <div style="text-indent: 2em;">
                  <p>
                    一、本课程共有105个教学微视频，共八章节，视频总时长达1200分钟。
                    <br>
                    二、本课程共32个学时，2学分。
                    <br>
                    三、教学计划如下:
                    <br>
                    第一章 法律风险管理&nbsp;&nbsp; 2个学时
                    <br>
                    第二章 法律风险分类&nbsp;&nbsp; 2个学时
                    <br>
                    第三章 宪法法律风险&nbsp;&nbsp; 3个学时
                    <br>
                    第四章 行政法律风险&nbsp;&nbsp; 3个学时
                    <br>
                    第五章 民商法律风险&nbsp;&nbsp; 3个学时
                    <br>
                    第六章 经济法律风险&nbsp;&nbsp; 4个学时
                    <br>
                    第七章 刑事法律风险&nbsp;&nbsp; 3个学时
                    <br>
                    第八章 社会法律风险&nbsp;&nbsp; 4个学时
                    <br>
                    第九章 国际法律风险&nbsp;&nbsp; 2个学时
                    <br>
                    第十章 诉讼法律风险&nbsp;&nbsp; 3个学时
                    <br>
                    第十一章 企业法律风险防范对策&nbsp;&nbsp; 3个学时
                    <br>
                    四、授课方式介绍
                    <br>
                    每次课前发布任务，网上观看微课，然后做作业、测验和考试，讨论区互动答疑，线下课堂案例分析和解答问题。
                    <br>
                    五、成绩评价:线上和线下融合、过程性评价与终结性评价相结合的多元化课程评价体系;
                    <br>
                    线上成绩是以“视频观看时长、完成测试、考试、作业情况及论坛发帖”之成绩为计算依据，各项目占比如下:
                    <br>
                    (1)视频观看占20%（最终以任课教师系统设置为准）;
                    <br>
                    (2)作业成绩占10%（最终以任课教师系统设置为准）;
                    <br>
                    (3)测验成绩占50%（最终以任课教师系统设置为准）;
                    <br>
                    (4)考试成绩占10%（最终以任课教师系统设置为准）;
                    <br>
                    (5)发帖讨论成绩占5%,普通帖子0.5分一个,精华帖子1分一个（最终以任课教师系统设置为准）;
                    <br>
                    (6)笔记成绩占5%,普通笔记0.5分一个,精华笔记1分一个（最终以任课教师系统设置为准）;
                    <br>
                    本课程最终成绩 = 线上成绩70%权重值+线下成绩30%权重值（最终以任课教师系统设置为准）。
                  </p>
                </div>
              </div>
            </div>
          </el-tab-pane>
          <el-tab-pane label="课程目录" name="second">
            <div class="course-outline" style="position: relative;">
              <div v-for="item in 5" :key="item">
                <h5 class="item">
                  第一章  企业法概述
                </h5>
                <ul>
                  <li class="outline" v-for="item in 5" :key="item">
                    <span class="sb-border" >
                      第一节  企业法概述
                    </span>
                  </li>
                </ul>
              </div>
            </div>
          </el-tab-pane>
        </el-tabs>
      </el-main>
    </el-container>
  </div>
</template>

<script>
export default {
  data() {
    console.log(this)
    return {
      activeName: 'first',
    }
  },
  methods: {
    handleClick(tab, event) {
      console.log(tab, event)
    },
  }
}
</script>

<style scoped>
.el-header {
  height: 200px;
}
.el-image{
  width: 40%;
  height: 200px;
  float: left;
}
.el-descriptions {
  width: 54%;
  float:left;
  margin-left: 2%;
}
.el-button{
  margin-left: 2%;
  float: left;
}
.el-main {
  max-width: 1200px;
  width: 1200px;
  margin: 0 auto;
}
.title {
  border: 0;
  display: block;
  width: 100%;
  background: #e2efff;
  height: 42px;
  line-height: 42px;
  font-size: 16px;
  font-weight: 550;
  color: #1d7ffd;
  letter-spacing: 5px;
  text-align: center;
}
.content-text {
    padding: 20px 24px;
    color: #666;
    font-size: 14px;
    line-height: 28px;
    max-width: 800px;
}
.course-outline ul.outline {
    padding-left: 20px;
    padding-right: 20px;
}
li {
    display: flex;
    font-family: 'Arial', 'Microsoft Yahei' !important;
    font-size: 14px;
    color: #666666;
    letter-spacing: 0.88px;
    height: 35px;
    line-height: 35px;
}
.course-outline .item {
    padding-left: 20px;
    padding-right: 20px;
    border: none;
    display: block;
    width: 100%;
    background: #f1faff;
    height: 42px;
    line-height: 42px;
    font-size: 16px;
    font-weight: 550;
    color: #418fbe;
    letter-spacing: 3px;
}
h5 {
  padding: 0;
  margin: 0;
  display: block;
  font-size: 0.83em;
  margin-block-start: 1.67em;
  margin-block-end: 1.67em;
  margin-inline-start: 0px;
  margin-inline-end: 0px;
  font-weight: bold;
}
ul, li {
    list-style: none;
    padding: 0;
    margin: 0;
}
ul {
    display: block;
    list-style-type: disc;
    margin-block-start: 1em;
    margin-block-end: 1em;
    margin-inline-start: 0px;
    margin-inline-end: 0px;
    padding-inline-start: 40px;
}
.course-show{
  max-width: 1200px;
  width: 1200px;
  margin: 50px auto;
}
</style>