<template>
  <div class="level-list-child">
    <el-card>
      <template #header>
        <div class="table-header">
          <i class="el-icon-date"></i>
          关卡列表
        </div>
        <el-input placeholder="请输入内容" size="mini" v-model="search_data" class="input-with-select">
          <template #append>
            <el-button icon="el-icon-search" @click="search_all_data"></el-button>
          </template>
        </el-input>
      </template>
      <div>
        <el-table :data="
            Data.slice(
              (current_page - 1) * page_sizes,
              current_page * page_sizes
            )
          " size="mini" :stripe="false" :fit="true" row-key="id" style="width: 100%;"
          :default-sort="{ prop: 'id', order: 'descending' }"
          :tree-props="{children: 'children', hasChildren: 'hasChildren'}">
          <el-table-column prop="id" label="关卡编号"> </el-table-column>
          <el-table-column prop="level_title" label="关卡标题"> </el-table-column>
          <el-table-column prop="level_description" label="关卡描述"> </el-table-column>
          <el-table-column prop="level_pre" label="前置关卡"> </el-table-column>
          <el-table-column prop="level_belong" label="属于"> </el-table-column>
          <el-table-column prop="level_creator" label="创建者"> </el-table-column>
          <el-table-column prop="level_status" fixed="right" width="50px" label="状态">
            <template #default="scope">
              <el-switch v-model="scope.row.level_status" active-color="#13ce66" inactive-color="#ff4949"></el-switch>
            </template>
          </el-table-column>
          <el-table-column fixed="right" width="125px" label="操作">
            <template #default="scope">
              <el-button size="mini" type="primary" circle icon="el-icon-edit" @click="handleEditClick(scope.row)">
              </el-button>
              <el-button size="mini" type="success" circle icon="el-icon-check" @click="handleCheckClick(scope.row)">
              </el-button>
              <el-button size="mini" type="danger" circle icon="el-icon-delete" @click="handleDeleteClick(scope.row)">
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
      <el-pagination class="pagination-1" @size-change="handleSizeChange" @current-change="handleCurrentChange"
        :current-page="current_page" :page-sizes="[20, 50, 100, 200]" :page-size="page_sizes"
        layout="total, sizes, prev, pager, next, jumper" :total="Data.length" :hide-on-single-page="true">
      </el-pagination>
      <el-pagination class="pagination-2" @size-change="handleSizeChange" @current-change="handleCurrentChange"
        :current-page="current_page" :page-sizes="[20, 50, 100, 200]" :page-size="page_sizes" layout="prev, pager, next"
        :total="Data.length" :hide-on-single-page="true">
      </el-pagination>
    </el-card>
  </div>
</template>

<script>
import { mapState, mapGetters } from 'vuex';

export default {
  name: "LevelListChild",
  mounted () { },
  computed: {
    listenSoreMsg () {
      return this.$store.state.search_data;
    },
    ...mapState('level', {
      Data: state => state.level_list
    }),
    ...mapGetters('level', {
      filterProvince: 'filterLevelData'
    })
  },
  watch: {
    listenSoreMsg () {
      this.search_data = this.listenSoreMsg;
      this.search_all_data();
    },
  },
  props: {
    admin: {
      type: Boolean,
      default: false,
    },
  },
  data () {
    return {
      search_data: "",
      current_page: 1,
      page_sizes: 50,
      Data: [
        {
          id: 1,
          level_title: "大关卡",
          level_description: "125",
          level_creator: "123",
          children: [
            {
              id: 2,
              level_title: "大关卡",
              level_description: "125",
              level_pre: 123,
              level_belong: "大关卡",
              level_creator: "123",
            }
          ]
        },
        {
          id: 3,
          level_title: "大关卡",
          level_description: "125",
          level_creator: "123",
          children: [
            {
              id: 4,
              level_title: "大关卡",
              level_description: "125",
              level_pre: 123,
              level_belong: "大关卡",
              level_creator: "123",
            }
          ]
        },
      ],
      total: 3,
      listQuery: {
        page: 1,
        limit: 10,
      },
    };
  },
  methods: {
    handleSizeChange (val) {
      this.page_sizes = val;
    },
    handleCurrentChange (val) {
      this.current_page = val;
    },
    search_all_data () {
      this.Data = this.filterProvince(this.search_data);
    },
    handleEditClick (val) {
      console.log(val);
    },
    handleCheckClick (val) {
      console.log(val);
    },
    handleDeleteClick (val) {
      console.log(val);
    },
  },
};
</script>

<style>
.level-list-child .table-header {
  font: 1.2em "楷体";
  letter-spacing: 3px;
  height: 30px;
  width: 50%;
  min-width: 210px;
  float: left;
}
.level-list-child .el-card__header {
  height: 60px;
}
.level-list-child .input-with-select {
  width: 205px;
  float: right;
  margin-right: 10px;
  transform: translateY(-1px);
}
.level-list-child .current-time {
  font-size: 10px;
  color: darkturquoise;
  letter-spacing: 1px;
}
.level-list-child .pagination-2 {
  display: none;
}
@media screen and (max-width: 600px) {
  .level-list-child .input-with-select {
    display: none;
  }
  .level-list-child .pagination-2 {
    display: block;
  }
  .level-list-child .pagination-1 {
    display: none;
  }
}
</style>
<template>
  <div class="level-list-child">
    <el-card>
      <template #header>
        <div class="table-header">
          <i class="el-icon-date"></i>
          关卡列表
          <!-- <div class="current-time">当前时间:{{ current_time }}</div> -->
        </div>
        
        <el-input 
          placeholder="请输入内容" 
          size="mini" 
          v-model="search_data" 
          class="input-with-select"
        >
          <template #append>
            <el-button
              icon="el-icon-search" 
              @click="search_all_data(search_data)"
            ></el-button>
          </template>
        </el-input>
      </template>
      <div>
        <el-table :data="
        Data.slice((current_page - 1) * page_sizes, current_page * page_sizes)
      " size="mini" :stripe="false" :fit="true" row-key="num" style="width: 100%;"
          :default-sort="{ prop: 'num', order: 'ascending' }"
          :tree-props="{children: 'level_list', hasChildren: 'problem_list'}"
          :default-expand-all="false"
          lazy:="true"
           >
          <el-table-column prop="level_id" label="关卡编号"> </el-table-column>
          <el-table-column prop="level_title" label="关卡标题"> </el-table-column>
          <el-table-column prop="level_describe" label="关卡描述"> </el-table-column>
          <el-table-column prop="type" label="类型"> </el-table-column>
          <el-table-column prop="front_id" label="前置关卡"> </el-table-column>
          <el-table-column prop="creator" label="创建者"> </el-table-column>
          <el-table-column prop="status" fixed="right" width="50px" label="状态">
            <template #default="scope">
              <el-switch v-model="scope.row.status" active-color="#13ce66" inactive-color="#ff4949" @click="handleStatusChange(scope.row.level_id,scope.row.status)"></el-switch>
            </template>
          </el-table-column>
          <el-table-column fixed="right" width="125px" label="操作">
            <template #default="scope">
              <div>
              <el-button size="mini" type="primary" circle icon="el-icon-edit" @click="handleEditClick({  
                level_id: scope.row.level_id,
                level_title: scope.row.level_title,
                creator: scope.row.creator,
                level_describe: scope.row.level_describe,
                front_id: scope.row.front_id,
                type: scope.row.type,
                problem_list: scope.row.problem_list,
              })">
              </el-button>
              <el-button size="mini" type="success" circle icon="el-icon-add-location" @click="handleAddlevelClick({
                type: scope.row.type,
                status: scope.row.status,
              })">
              </el-button>
              <el-button size="mini" type="danger" circle icon="el-icon-delete" @click="open(scope.row.level_id)">
              </el-button>
              </div>
              <el-button size="mini" type="primary" circle icon="el-icon-arrow-up" @click="handleUpClick({
                level_id: scope.row.level_id,
                type: scope.row.type,
                move: 1,
                front_id: scope.row.front_id,
              })">
              </el-button>
               <el-button class="downbutton" size="mini" type="primary" circle icon="el-icon-arrow-down" @click="handleDownClick({
                level_id: scope.row.level_id,
                type: scope.row.type,
                move: 2,
                front_id: scope.row.front_id,
              })">
              </el-button>
             
            </template>
          </el-table-column>
        </el-table>
      </div>
      <el-pagination class="pagination-1" @size-change="handleSizeChange" @current-change="handleCurrentChange"
        :current-page="current_page" :page-sizes="[20, 50, 100, 200]" :page-size="page_sizes"
        layout="total, sizes, prev, pager, next, jumper" :total="Data.length" :hide-on-single-page="true">
      </el-pagination>
      <el-pagination class="pagination-2" @size-change="handleSizeChange" @current-change="handleCurrentChange"
        :current-page="current_page" :page-sizes="[20, 50, 100, 200]" :page-size="page_sizes" layout="prev, pager, next"
        :total="Data.length" :hide-on-single-page="true">
      </el-pagination>
    </el-card>
  </div>
</template>

<script >
import {  deleteLevel } from "@/api/level";
import {  edithideLevel,levelMove,screenLevel } from "@/api/level";
// import {  editLevel } from "@/api/level";
export default {
  name: "LevelListChild",
  props: {
    admin: {
      type: Boolean,
      default: false,
    },
     Data: {
       default: [
              {
              creator:"admin",
              level_describe:"青铜玩家往往是最不受控制的爱好者，他们不熟悉规则，不明白什么时候该去提交，什么时候该去改代码，他们的特点就是“犟”。↵无论你在干什么，他们因为写不出这道代码，所以就会在简单的题目上找找快感，所以在周赛的时候，他总会一个人默默地写简单的题目，没有任何战绩可言。",
              front_id:"0",
              level_id:"1",
              level_pass: 0,
              level_pre: "",
              nick: "admin",
              num: "1",
              pass_num: "0",
              status: "N",
              level_title: "倔强青铜",
              type: "2",
              current_level: "-1",
              level_list: [
              {
                  creator:"admin",
                  level_describe:"解决输入输出的问题",
                  front_id: "1",
                  level_id: "10",
                  level_pass: "false",
                  level_pre: "",
                  nick:"admin",
                  num: "1",
                  pass_num:"5",
                  status: "N",
                  level_title: "计算机开口说话",
                  type: 1,
                  
                  // level_passnum: 2,
                  problem_list:[
                  {
                      level_id:"10",
                      num:1,
                      problem_id:"1001",
                      problem_status:"0",
                      problem_title:"爬楼梯",

                  }
                  ]

              }
              ]
          }
       ],
     },
  },
  // created() {
  //   deleteLevel();
  //   editLevel();
  // },
  data () {
    return {
      search_data: "",
      current_page: 1,
      page_sizes: 50,
      // Data: [
      //   {
      //     creator:"admin",
      //     level_describe:"青铜玩家往往是最不受控制的爱好者，他们不熟悉规则，不明白什么时候该去提交，什么时候该去改代码，他们的特点就是“犟”。↵无论你在干什么，他们因为写不出这道代码，所以就会在简单的题目上找找快感，所以在周赛的时候，他总会一个人默默地写简单的题目，没有任何战绩可言。",
      //     front_id:"0",
      //     level_id:"1",
      //     level_pass: 0,
      //     level_pre: "",
      //     nick: "admin",
      //     num: "1",
      //     pass_num: "0",
      //     status: "N",
      //     level_title: "倔强青铜",
      //     type: 2,
      //     level_list: [
      //     {
      //         creator:"admin",
      //         level_describe:"解决输入输出的问题",
      //         front_id: "1",
      //         level_id: "10",
      //         level_pass: "false",
      //         level_pre: "",
      //         nick:"admin",
      //         num: "1",
      //         pass_num:"5",
      //         status: "N",
      //         level_title: "计算机开口说话",
      //         type: 1,
      //         // level_passnum: 2,
      //         // problem_list:[
      //         // {
      //         //     level_id:"10",
      //         //     num:1,
      //         //     problem_id:"1001",
      //         //     problem_status:"0",
      //         //     problem_title:"爬楼梯",

      //         // }
      //         // ]

      //     }
      //     ]
      // }
      
      // ],
 
    };
  },
  methods: {
    async handleUpClick(val){
      console.log(val)
      let back_data = await levelMove(val);
      if (back_data.status === false){
        this.$message({
            type: "error",
            message: back_data.err,
        });
      }
    },
    async handleDownClick(val){
      console.log(val)
      let back_data = await levelMove(val);
      if (back_data.status === false){
        this.$message({
            type: "error",
            message: back_data.err,
        });
      }
    },
    handleAddlevelClick(val){
      console.log(val);
      if (val.type === 1){
        this.$router.push({
          path:"/admin/SmallLevelAdd",
          query: {
              type: val.type,
          }
        })
      }
      else{
          this.$router.push({
          path:"/admin/LevelAdd",
          query: {
              type: val.type,
              status: val.status,
          }
        })
      }
      
    },
    handleEditClick(val){
          console.log(val)
          if (val.type === 1){
              this.$router.push({
                path:"/admin/SmallLevelEdit",
                query: {
                  type: val.type,
                  level_title: val.level_title,
                  creator: val.creator,
                  level_describe: val.level_describe,
                  front_id: val.front_id,
                  level_id: val.level_id,
                  problem_list: val.problem_list,
                },
            });
          }
          else{
            this.$router.push({
                path:"/admin/BigLevelEdit",
                query: {
                  type: val.type,
                  level_title: val.level_title,
                  creator: val.creator,
                  level_describe: val.level_describe,
                  front_id: val.front_id,
                  level_id: val.level_id,
                },
            });
          }

      },
    handleStatusChange(val,value){
      this.status =!this.status
      this.handleStatuschange({ level_id: val, defunct: value })
    },
    async handleStatuschange(val){
      console.log(val)
      let back_data = await edithideLevel(val);
      if (back_data.status === false){
        this.$message({
            type: "error",
            message: back_data.err,
        });
      }
    },
    async handleDeleteClick(val) {
      console.log(val)
      let back_data = await deleteLevel(val);
      if  (back_data.status){
        this.$message({
            type: "success",
            message: back_data.err,
        });
      }else{
        this.$message({
            type: "error",
            message: back_data.err,
        });
        }
    },
    open(val) {
        this.$confirm(
          '你确定要删除此关卡吗？',
          '确认信息',
          {
            distinguishCancelAndClose: true,
            confirmButtonText: '确认',
            cancelButtonText: '取消', 
          }
        )
          .then(() => {
            this.handleDeleteClick({level_id: val})
          })
      //     .catch((action) => {
      //       this.$message({
      //         type: 'info',
      //         message:
      //           action === 'cancel' ? '放弃保存并离开页面' : '停留在当前页面',
      //     })
      // })
    },
    async search_All_Data(val){
      console.log(val)
      let back_data = await screenLevel(val);
        if (back_data.status) {
          this.data = this.formatLevel(back_data.message);
          console.log(this.data);
          // this.$message({
          //   type: "success",
          //     message: back_data.message,
          //   });
        }else {
          this.$message({
            type: "error",
              message: back_data.message,
          });   
        } 
        
    },
    formatLevel(val){
      console.log(val)
      return  val.map((item) =>({
          creator: item.creator,  
          level_describe: item.description,
          level_id: item.level_id,
          front_id: item.front_id,
          level_title: item.title,
          type: item.type,
      }));
    },
    search_all_data(val){
      this.search_data = val;
      this.search_All_Data({ text: val });
    },

    handleSizeChange (val) {
      this.page_sizes = val;
    },
    handleCurrentChange (val) {
      this.current_page = val;
    },

  

    // handleDeleteClick (val) {
    //   console.log(val);
    // },
    // async handleDeleteClick(row) {
    //   let back_data = await deleteLevel(row.level_id);
    //   if (back_data.status) {
    //     this.$message({
    //       type: "success",
    //       message: back_data.message,
    //     });
    //     this.$store.dispatch("level/getLevelList");
    //   } else {
    //     this.$message({
    //       type: "error",
    //       message: back_data.message,
    //     });
    //   }
    // },
    
  },
};
</script>

<style>
.level-list-child .table-header {
  font: 1.2em "楷体";
  letter-spacing: 3px;
  height: 30px;
  width: 50%;
  min-width: 210px;
  float: left;
}
.level-list-child .el-card__header {
  height: 60px;
}
.level-list-child .input-with-select {
  width: 205px;
  float: right;
  margin-right: 10px;
  transform: translateY(-1px);
}
.level-list-child .current-time {
  font-size: 10px;
  color: darkturquoise;
  letter-spacing: 1px;
}
.level-list-child .pagination-2 {
  display: none;
}
.downbutton{
  margin-top: 10px;
  margin-left: 10px;
}
@media screen and (max-width: 600px) {
  .level-list-child .input-with-select {
    display: none;
  }
  .level-list-child .pagination-2 {
    display: block;
  }
  .level-list-child .pagination-1 {
    display: none;
  }
}
  
</style>
