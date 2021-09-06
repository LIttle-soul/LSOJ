<template>
    <div class="contest-card">
        <el-card class="content">
            <template #header>
                <span class="header">近期比赛</span>
                <el-button type="text">more</el-button>
            </template>
            <el-card shadow="hover" class="container" v-for="item in 8" :key="item">
                <template #header>
                    <span class="content-header">竞赛{{item}}</span>
                    <el-tag type="success" size="mini" class="content-tag">公开</el-tag>
                </template>
                <div class="container-text">
                    <p><span>状态: 比赛中</span><span>2020-01-02 12:12:00</span></p>
                    <p><span>命题: LiSoul</span><span>2020-01-02 12:12:00</span></p>
                </div>
            </el-card>
        </el-card>
        <el-card class="content">
            <template #header>
                <span class="header">其他比赛</span>
            </template>
            <el-card shadow="hover" class="container" v-for="item in 6" :key="item">
                <template #header>
                    <span class="content-header">竞赛{{item}}</span>
                    <el-tag type="success" size="mini" class="content-tag">公开</el-tag>
                </template>
                <div class="container-text">
                    <p><span>状态: 比赛中</span><span>2020-01-02 12:12:00</span></p>
                    <p><span>命题: LiSoul</span><span>2020-01-02 12:12:00</span></p>
                </div>
            </el-card>
        </el-card>
    </div>
</template>

<script>
export default {
    setup() {
        
    },
}
</script>

<style>
.contest-card {
    width: 100%;
}
.contest-card .content {
    width: 100%;
    min-height: 400px;
    margin: 20px 0;
    position: relative;
}
.contest-card .content .el-button {
    position: absolute;
    right: 20px;
    top: 6px;
}
.contest-card .header {
    font-weight: 800;
    max-width: 50%;
}
.contest-card .el-card__body {
    padding: 0;
}
.contest-card .container {
    width: 45%;
    margin: 15px 0;
    min-height: 120px;
    position: relative;
}
.contest-card .container:nth-child(2n-1) {
    float: left;
    margin-left: 3%;
}
.contest-card .container:nth-child(2n) {
    float: right;
    margin-right: 3%;
}
.contest-card .container .el-card__header {
    padding: 0;
    height: 35px;
    line-height: 30px;
}
.contest-card .content-header {
    font-size: 12px;
    margin-left: 12px;
}
.contest-card .content-tag {
    position: absolute;
    right: 10px;
    top: 6px;
}
.contest-card .container-text{
    font-size: 8px;
    height: 100%;
    width: 95%;
    margin: 0 auto;
}
.contest-card .container-text p{
    line-height: 40px;
}
.contest-card .container-text p span:last-child{
    float: right;
}
</style>