<template>
<div class="level">
    <el-card v-for="(item,index) in  LevelKind.slice(0,LevelKind.length-1)" :key="index" class="level-list">

      <!-- 关卡 -->
      <div class="header">
        <h1>{{item.kind_title}}</h1><!-- 关卡名称 -->
        <p>{{item.description}}</p><!-- 关卡描述 -->
      </div>
      
      <el-divider></el-divider>
      
      <!-- 关卡内容 -->
      <!-- 进度条 -->
      <div>
        <el-progress :text-inside="true" :stroke-width="8" :percentage="0"></el-progress>
      </div>
      <!-- 所有关卡点 -->
      <div>
        <!-- 关卡点 -->
        <el-col :span="8" v-for="(i,cindex) in LevelKind[index].Levels" :key="cindex">
          <el-card shadow="never" :body-style="{ padding: '0px' }" class="level-point">
            <!-- 关卡卡片头部 -->
            <template #header>
              <div class="header">
                <!-- 关卡卡片状态 -->
                <div v-if="showlogin==null" class="cart_status gray-background" title="请登录您的账号"></div>
                <div v-else class="after">
                  <div v-if="i.level_judge == 1" class="cart_status blue-background" title="该关卡已解锁"></div>
                  <div v-else-if="i.level_judge == 0" class="cart_status gray-background" title="该关卡未解锁"></div>
                  <div v-else class="cart_status green-background" title="该关卡已完成"></div>
                </div>
                <h3>{{i.title}}</h3>
                <p>{{i.pass_num}}题通关</p>
              </div>
            </template>
            <!-- 关卡卡片主体 -->
            <div class="main">{{i.description}}</div>
            <!-- 关卡卡片底部 -->
            <div class="footer">
              <el-popover placement="bottom" style="display: block;" trigger="click">
                <!-- 关卡卡片按钮 -->
                <template #reference>
                  <el-button  type="text" class="button" v-on:click="getLevel(i)">
                    <div v-if="showlogin==null" class="level_judges gray-background" title="请登录" @click="gotoLogin()"><i class="el-icon-user"></i></div>
                    <div v-else class="after">
                      <div v-if="i.level_judge == 1" class="level_judges blue-background" title="已解锁"><i class="el-icon-tickets"></i></div>
                      <div v-else-if="i.level_judge == 0" class="level_judges gray-background" title="未解锁"><i class="el-icon-close"></i></div>
                      <div v-else class="level_judges green-background" title="已完成"><i class="el-icon-check"></i></div>
                    </div>
                  </el-button>
                </template>
                <!-- 关卡卡片按钮内的内容 -->
                <div v-if="i.level_judge == 1">
                  <el-table :data="Proinfo" style="width: 100%;">
                    <el-table-column width="100" prop="problem_id" label="题目编号">
                      <template #default="scope" >
                        <div style="text-decoration:none;cursor:pointer;" @click="itemClick(scope.row)">{{ scope.row.problem_id }}</div>
                      </template>
                    </el-table-column>
                    <el-table-column width="200"  prop="title" label="题目">
                      <template #default="scope" >
                        <div style="text-decoration:none;cursor:pointer;" @click="itemClick(scope.row)">{{ scope.row.title }}</div>
                      </template>
                    </el-table-column>
                    <el-table-column width="100" property="solved" label="是否解决"></el-table-column>
                  </el-table>
                </div>
                <div v-if="i.level_judge == 0" >
                  <el-table :data="Preinfo" width="300">
                    <el-table-column width="300"  prop="title" label="请先完成"></el-table-column>
                  </el-table>
                </div>
              </el-popover>
            </div>

          </el-card>
        </el-col>
      </div>
      <div style="clear: both"></div>
    </el-card>
</div>
</template>

<script>
import axios from 'axios'
// import paintedEggshell from './fire'
export default {
  name: 'openclass',
  components: {
  },
  data () {
    return {
      LevelKind: [],
      Levels: {},
      level_id: '',
      level_judge: '',
      Proinfo: [],
      Preinfo: [],
      showlogin: localStorage.getItem('username'),
    }
  },
  mounted () {
    this.getLevelKinds()
    // this.getLevel()
    // this.itemClick()
  },
  methods: {
    itemClick (row) {
      this.$router.push({
        name: 'problem',
        query: {
          problem_id: row.problem_id
        }
      })
    },
    gotoLogin () {
      this.$router.push({
        name: 'login'
      })
    },
    getLevelKinds () {
      // this.user_id = localStorage.getItem('username')
      axios.get('http://182.92.71.47/takeoutLevelinfo/').then(res => {
        console.log(res.data)
        this.LevelKind = res.data.LevelKind
      })
    },
    getLevel (level) {
      this.level_id = level.level_id
      this.level_judge = level.level_judge
      axios({
        method: 'post',
        url: 'http://182.92.71.47/takeoutLevelpro/',
        data: {
          level_judge: this.level_judge,
          level_id: this.level_id
        },
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        transformRequest: function (obj) {
          var str = []
          for (var p in obj) {
            str.push(encodeURIComponent(p) + '=' + encodeURIComponent(obj[p]))
          }
          return str.join('&')
        }
      }).then((res) => {
        console.log(res)
        console.log(level)
        console.log(res.data.Proinfo)
        this.Proinfo = res.data.Proinfo
        this.Preinfo = res.data.Preinfo
      })
    }
  }
}
</script>

<style scoped>
  /* 页面 */
  .level {
    width: 80%;
    max-width: 1200px;
    margin: 0 auto;
    margin: 70px auto;

    font: 1em "楷体";
  }
  .level .level-list {
    margin-bottom: 30px;
  }
  .level .header > h1{
    font-size: 1.2em;
    letter-spacing: 3px;
    line-height: 2em;
  }

  /* 卡片 */
  
  .level .level-point {
    height: 210px;
  }
  /* header */
  .level .level-point .header {
    height: 40px;
  }
  .level .level-point .header h3 {
    font-size: 1.0em;
  }
  .level .level-point .header p {
    font-size: 0.8em;
  }
  /* main */
  .level .level-point .main {
    font-size: 0.9em;
    padding: 10px 20px;
    height: 80px;
  }
  /* footer */
  .level .level-point .footer {
    text-align: center;
    width: 100%;
    min-height: 28px;
  }

  .el-col {
    width: 29%;
    margin-top: 2%;
    margin-left: 3%;
    margin-bottom: 5%;
  }
  


  .level_judges{
    text-align: center;
    width: 100%;
    line-height: 40px;
    color: #000;
    font-size: 16px;
  }
  
  a{
    text-decoration: none;
    color: #000;
  }
  
  .button {
    border: none;
    padding: 0;
    width: 100%;
    height: 20px;
  }

  .cart_status {
    float: right;
    width: 20px;
    height: 20px;
    border: 1px solid fffffc;
    border-radius: 50%;
  }

/* 颜色类 */

  /* 背景色 */
  .gray-background {
    background-color: #eae4e9;
  }
  .red-background {
    background-color: #FFADAD;
  }
  .green-background {
    background-color: #CAFFBF;
  }
  .blue-background {
    background-color: #9BF6FF;
  }


  @media screen and (max-width: 600px) {
    .level {
      width: 100%;
    }
    .el-col {
      max-width: 100%;
      width: 95%;
      margin-top: 2%;
      margin-left: 3%;
      margin-bottom: 5%;
    }
  }
</style>
