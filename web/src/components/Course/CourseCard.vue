<template>
  <div class="course">
    <el-tooltip placement="right-start" :visible-arrow="false">
      <template #content>
        <div style="height:180px">
          多行信息<br/>第二行信息
        </div>
      </template>
      
      <el-card class="content" shadow="hover" :body-style="{ padding: '0px' }">
        <p>图片</p>
      </el-card>
    
    </el-tooltip>
    <h1>课程标题</h1>
  </div>
</template>

<style>
  .course {
    width: 150px;
  }
  .course .content {
    width: 100%;
    height: 200px;
    /* border: 2px solid black; */
    /* background-color: #FCFFA1; */
  }
  .course h1 {
    line-height: 2rem;
  }
</style>