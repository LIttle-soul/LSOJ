<template>
    <div class="problem-header">
        <div class="left">
            <i class="el-icon-s-management"></i>
            <div class="left-text">{{problem_title}}</div>
            <div class="left-info">
                <p>时间限制: {{time_limit}}ms</p>
                <p>空间限制：{{memory_limit}}mb</p>
            </div>
        </div>
        <div class="right">
            <el-button v-for="item in button_list" :key="item.title" type="text" @click="routerTo(item.index)">{{item.title}}</el-button>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        problem_title: {
            type: String,
            default: '背包问题'
        },
        time_limit: {
            type: Number,
            default: 1000
        },
        memory_limit: {
            type: Number,
            default: 128
        }
    },
    setup() {
        
    },
    data() {
        return {
            button_list: [
                {
                    title: '返回列表',
                    index: 'problemlist'
                },
                {
                    title: '我的提交',
                    index: 'problemlist'
                }
            ]
        }
    },
    methods: {
        routerTo(){
            this.$router.go(-1);
        }
    },
}
</script>

<style scoped>
.problem-header {
    width: 100%;
    height: 100%;
}
.left {
    width: 50%;
    height: 100%;
    line-height: 100%;
    float: left;
    /* background: rgba(126, 100, 251, 0.8); */
}
.left .el-icon-s-management::before {
    font-size: 35px;
    height: 50px;
    line-height: 50px;
    margin-left: 15px;
    color: aliceblue;
}
.left .el-icon-s-management {
    width: 60px;
    float: left;
}
.left-text {
    height: 50px;
    line-height: 50px;
    float: left;
    font-size: 20px;
    font-family: "宋体";
    color: aliceblue;
}
.left-info {
    float: right;
    height: 30px;
    margin: 10px;
    line-height: 15px;
    color: aliceblue;
    font-size: 15px;
    font-family: "楷体";
}
.right {
    width: 50%;
    height: 50px;
    float: left;
}
.right .el-button {
    float: right;
    height: 30px;
    margin: 5px 10px;
    font-size: 18px;
    font-family: "宋体";
    color: aliceblue;
}
</style>