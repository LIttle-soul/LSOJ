<template> 
  <div class="level-show">
        <div class="level-show-child"  v-for="i in Data" :key="i.level_id" v-show="i.status === true" style="margin-top:50px">
            <div class="title-header">
                <div class="card-title">{{ i.level_title }}</div>
                <div class="level-describe">{{ i.level_describe }}</div>
            </div> 
            <el-progress :text-inside="true"  :stroke-width="32" v-if="isNaN(((i.level_pass/i.level_numbers)*100).toFixed(2)) === false" :percentage="parseFloat(((i.level_pass/i.level_numbers)*100).toFixed(2))" class="progress-header" ></el-progress>
            <el-space wrap class="level-list"  v-for="j in i.level_list" :key="j.level_id" v-show="j.status === true">
                <el-card class="box-card"  @click="handleProblemClick({
                    level_id: j.level_id,
                })"> 
                    <template #header>
                        <div class="card-header" @click="i.current_level == j.level_id?i.current_level=-1:i.current_level=j.level_id">
                            <el-button class="panel-title" type="text" > {{ j.level_title }}</el-button>
                            <span class="Number-of-customs-clearance">{{ j.pass_numbers }}人过关</span>
                        </div>
                    </template>
                    <p>关卡{{ i.level_id }}-{{ j.num }}, {{ j.problem_numbers }}道题</p>
                    <div  class="Cleared" v-if="j.level_pass ">已通过</div ><div  class="Challenged" v-else>可挑战</div >
                    <p class="small-level-describe" > {{ j.level_describe }} </p>
                </el-card>
                <el-card class="box-card-two"  v-if="+j.level_id === +i.current_level " >
                    <template #header>
                    <div class="card-header-two">
                        <span class="title">要通过该关卡需要完成{{ j.problem_numbers }}道题，所有题目通过后点击底部“点击通关”按钮通过关卡</span> 
                    </div>
                    </template>
                    <div class="text" v-for="k in Problem_list" :key="k.problem_id"   >
                       
                        <el-button  type="text" @click="
                            handleLevelProblemClick({
                                memory_limit: k.memory_limit,
                                time_limit: k.time_limit,
                                problem_description: k.problem_description,
                                problem_title: k.problem_title,
                        })">
                        {{ k.problem_id }} {{ k.problem_title }}        
                       
                        </el-button>   
                        <span  class="Unadopted" v-if="k.problem_status === -1">未通过</span  >
                        <span  class="Adopted" v-if="k.problem_status === 1">通过</span>
                        <span  class="Unlogged" v-if="k.problem_status === 0">可挑战</span > 
                    </div>
                    <el-button class="button" type="text"  @click="handleclearanceclick({level_id: j.level_id})">点击通关</el-button>
                </el-card> 
            </el-space>
        </div> 
    </div>
   
</template>


<script lang="ts" setup>
import { onMounted, ref } from 'vue'
import { ElLoading,ElMessage } from "element-plus";
import { getLevelList } from "@/api/level";
import { levelCompletion,getProblem } from "@/api/level";
import { useRouter } from "vue-router";
import echarts from 'echarts/lib/echarts'
import 'echarts/lib/chart/line'
import 'echarts/lib/component/tooltip'
import 'echarts/lib/component/legendScroll'
let router = useRouter();
let  Data = ref({
    level_describe:"青铜玩家往往是最不受控制的爱好者，他们不熟悉规则，不明白什么时候该去提交，什么时候该去改代码，他们的特点就是“犟”。↵无论你在干什么，他们因为写不出这道代码，所以就会在简单的题目上找找快感，所以在周赛的时候，他总会一个人默默地写简单的题目，没有任何战绩可言。",
    level_id:"1",
    level_pass: 0,
    status: "N",
    level_title: "倔强青铜",
    level_numbers: 2,
    current_level: "-1",
    level_list: [
    {
        level_describe:"解决输入输出的问题",
        level_id: "10",
        level_pass: "false",
        num: "1",
        status: "N",
        level_title: "计算机开口说话",
        pass_numbers: 1,
        problem_numbers: 2,
        // level_passnum: 2,
    }
    ]
});
let Problem_list = ref([{
    problem_id: "1001",
    problem_status: "0",
    problem_title: "爬楼梯",
    memory_limit: 128,
    problem_description: "树老师爬楼梯，他可以每次走1级或者2级，输入楼梯的级数，求不同的走法数例如：楼梯一共有3级，他可以每次都走一级，或者第一次走一级，第二次走两级也可以第一次走两级，第二次走一级，一共3种方法.}",
    time_limit: "1000",
}])
let getlevellist = async () => {
    let loading = ElLoading.service({
        lock: true,
        text: "加载中...",
        background: "rgba(0,0,0,0.7)",
    });
    let level = await getLevelList();
    if (level.status) {
        Data.value = formatData(level.message);
        loading.close();
        console.log(Data.value);
    }
    console.log(level.message);
};
let formatData = (val: any) => {
    return val.map((item: any) => ({
        level_describe: item.description,
        level_id: item.level_id,
        level_pass: item.level_pass,
        status: item.status,
        level_title: item.title,
        level_numbers: item.level_numbers,
        level_list: item.level_list.map((it: any) => ({
            level_describe: it.description,
            level_id: it.level_id,
            level_pass: it.level_pass,
            num: it.num,
            pass_numbers: it.pass_numbers,
            status: it.status,
            level_title: it.title,
            problem_numbers: it.problem_numbers,
        }))
    }));
};
let handleclearanceclick = async (val: any) =>{
    let back_data = await levelCompletion(val);
    if (back_data.status){
        ElMessage({
            type: "success",
            message: back_data.message,
        });
    } 
    else {
        ElMessage.error(back_data.message);          
    }
};
let handleLevelProblemClick = async (val: any) => {
    router.push({
        path:"/showproblem",
        query: {
            memory_limit: val.memory_limit,
            time_limit:  val.time_limit,
            problem_description:  val.problem_description,
            problem_title:  val.problem_title,
        },
    });

};
let handleProblemClick = async (val: any) =>{
    let problem = await getProblem(val);
    if (problem.status){
        Problem_list.value = formatProblem(problem.message);
    }
     console.log(Problem_list.value);
};
let formatProblem = (val: any) =>{
    return val.map((item: any) =>({
        memory_limit: item.memory_limit,
        problem_description: item.problem_description,
        problem_id: item.problem_id,
        problem_status: item.problem_status,
        problem_title: item.problem_title,
        time_limit: item.time_limit,
    }))
};
onMounted(() => {
    getlevellist();
})
</script>
<style  lang="scss">
    .level-show{
        margin: 0 auto;
        max-width: 1800px;
        width: 100%;
        .level-show-child{
            border-radius: 15px;
            margin:auto;
            width:60%;
            height: auto;
            box-shadow: 10px 10px 20px 5px rgb(192, 240, 255);
            margin-bottom: 2%;
            .title-header{
                margin: 5px;
                .card-title {
                    font-size : 28px;
                    padding-top: 20px;
                }
                .level-describe{
                    font-size: 16px;
                    text-indent: 2em;
                    line-height: 25px;
                    margin-top: 10px;
                }
            }
            .progress-header{
                margin-left:5px;
                margin-right:5px;
            }
            
               
            .card-header {
                cursor: pointer; 
                height: 60px;
                margin: -20px -20px -20px  -20px ;
                background: rgba(193, 210, 240, 0.35);
                .panel-title {
                    font-size : 20px;
                    line-height :1.2;
                    margin-left: 10px;
                    margin-top: 10px;
                }
                .Number-of-customs-clearance{
                    color: rgb(0, 132, 255);
                    margin-left: 4px;
                }
            }
            .Cleared{
                float: right;
                text-align: center;
                color: azure;
                font-family: "微软雅黑";
                background: green;
                font-size: 14px;
                margin-top: -15px;
                width: 60px;
            }
            .Challenged{
                float: right;
                color: white;
                text-align: center;
                font-family: "微软雅黑";
                background: rgb(0, 162, 255);
                font-size: 14px;
                margin-top: -15px;
                width: 60px;
            }
            .small-level-describe{
                margin-top: 10px;   
                font-size: 14px;
                color: grey;
                margin-top: 12%;
            }
        }
        .box-card-two {
            margin-top: 2px;
            margin-left: -60px;
            width: 490px;
            .card-header-two {
                display: flex; 
                justify-content: space-between;
                align-items: center;
                .title{
                    font-size: 12px;
                }
            }
            .text {
                font-size: 12px;
                margin-top: -21px;
                margin-left: 10px;
                .Unlogged{
                    font-size: 12px;
                    float: right;
                    margin-top: 7px;
                    font-family: "微软雅黑";
                }
                .Adopted{
                    font-size: 12px;
                    float: right;
                    font-family: "微软雅黑";
                    margin-top: 6px;
                
                }
                .Unadopted{
                    font-size: 12px;
                    float: right;
                    font-family: "微软雅黑";
                    margin-top: 7px;
                }
            }
        }
    }   
    .level-list{
        width: 24%;
        margin-left: 70px;
        margin-top: 10px;
        padding-bottom: 8px;
    }
    .box-card {
        height: auto;
        width: 300px;
    }
    *{
        padding:0;
        margin:0;
    }
    @media screen and (max-width: 1800px) {
        .level-list{
            margin-left: 10px;
            width: 30%;
            // border: solid 2px red; 
        }
        .box-card{
            width: 250px;
        }
    }
    @media screen and (max-width: 1400px) {
        .level-list{
            margin-left: 30px;
            width: 45%;
            // border: solid 2px rgb(0, 162, 255); 
        }
        .box-card{
            width: 300px;
        }
    }
</style>