<template>
    <div class="zong">
        <div class="heard">
            <div class="title">
                <h1>批阅列表</h1>
                <el-button type="primary" plain size="small">返回</el-button>
            </div>
        </div>
        <div class="set">
            <h2>2021年数据结构重考</h2>
            <div class="seta">
                <p>题量：</p>
                <p>|满分：</p>
                <p>|涉及人数：</p>
                <p>|已交：</p>
            </div>
            <div class="setb">
                <p>创建人：</p>
                <p>|发送对象：</p>
                <p>|有效时间段：</p>
            </div>
            <div class="setleft"><span>0</span>份待批</div>
        </div>
        <div class="sousuo">
            <el-input
            placeholder="请输入学号或姓名"
            class="input-with-select"
            size="mini"
            >
            <template>
                <el-button :icon="Search"></el-button>
            </template>
            </el-input>
        </div>
        <div class="student">
            <el-table :data="tableData" style="width: 100%" border>
                <el-table-column prop="name" label="姓名" width="90" />
                <el-table-column prop="id" label="学号/工号" width="100" />
                <el-table-column prop="state" label="状态" width="90" />
                <el-table-column prop="time" label="领取时间" width="90" />
                <el-table-column prop="time" label="提交时间" />
                <el-table-column prop="id" label="IP" width="90" />
                <el-table-column prop="true" label="客观题正确率" width="90" />
                <el-table-column prop="time" label="批阅时间" />
                <el-table-column prop="sorce" label="分数" width="90" />
                <el-table-column prop="name" label="批阅人" width="90" />
                <el-table-column prop="id" label="批阅IP" />
                <el-table-column prop="operate" label="操作" width="90" />
            </el-table>
        </div>
    </div>
</template>

<style scoped lang="scss">
.zong{
    width: 70%;
    margin-left: 15%;
}
.heard{
    width: 100%;
    height:50px;
    border-bottom: solid rgb(194, 184, 184) 2px;
    margin-top: 20px;
}
.title{
    margin-left: 10px;
}
.title h1{
    font-size: 18px;
    padding-top: 30px;
}
.el-button{
    margin-left: 600px;
    float: right;
    margin-top: -30px;
}
.set{
    width: 100%;
    height: 100px;
    border: solid 1px rgb(194, 184, 184);
    margin-top: 10px;
    color: rgb(165, 165, 165);
}
.set h2{
    font-size: 20px;
    color: grey;
    margin-top: 20px;
    margin-left: 20px;
}
.seta p{
    float: left;
    margin-left: 10px;
    font-size: 13px;
}
.seta{
    margin-top: 10px;
    margin-left: 10px;
    width: 90%;
}
.setb{
    margin-top: 25px;
    margin-left: 10px;
}
.setb p{
    float: left;
    margin-left: 10px;
    font-size: 13px;
}
.setleft{
    color: rgb(126, 122, 122);
    font-size: 13px;
    margin-top: -40px;
    margin-left: 900px;
}
.setleft span{
    color: red;
    font-size: 40px;
}
.sousuo{
    margin-top: 10px;
}
.student{
    margin-top: 10px;
}

</style>