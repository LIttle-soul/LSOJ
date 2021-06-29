<template>
    <el-card class="user-info">
        <el-descriptions 
        class="margin-top" 
        :column="3" 
        :size="medium" 
        border>
    <template #title>
        <i class="el-icon-user-solid"></i>
        个人信息
    </template>
    <el-descriptions-item>
      <template #label>
        <i class="el-icon-user"></i>
        用户账号
      </template>
      201910101600040
    </el-descriptions-item>
    <el-descriptions-item>
      <template #label>
        <i class="el-icon-s-flag"></i>
        用户昵称
      </template>
      一只无趣的小灵魂
    </el-descriptions-item>
    <el-descriptions-item>
      <template #label>
        <i class="el-icon-s-custom"></i>
        真实姓名
      </template>
      任成辉
    </el-descriptions-item>
    <el-descriptions-item>
      <template #label>
        <i class="el-icon-star-off"></i>
        用户积分
      </template>
      1280
    </el-descriptions-item>
    <el-descriptions-item>
      <template #label>
        <i class="el-icon-time"></i>
        注册时间
      </template>
      2019-10-10 04:05:25
    </el-descriptions-item>
    <el-descriptions-item>
      <template #label>
        <i class="el-icon-school"></i>
        学校
      </template>
      金华职业技术学院
    </el-descriptions-item>
    <el-descriptions-item>
      <template #label>
        <i class="el-icon-male"></i>
        性别
      </template>
      男
    </el-descriptions-item>
    <el-descriptions-item>
      <template #label>
        <i class="el-icon-mobile-phone"></i>
        用户手机
      </template>
      17693535183
    </el-descriptions-item>
    <el-descriptions-item>
      <template #label>
        <i class="el-icon-message"></i>
        用户邮箱
      </template>
      2833896014@qq.com
    </el-descriptions-item>
  </el-descriptions>

  <el-descriptions class="margin-top" :column="1" :size="size">
      <template #title>
        <i class="el-icon-s-tools"></i>
        信息修改
    </template>
    <el-descriptions-item label="用户名">kooriookami</el-descriptions-item>
    <el-descriptions-item label="手机号">18100000000</el-descriptions-item>
    <el-descriptions-item label="居住地">苏州市</el-descriptions-item>
    <el-descriptions-item label="备注">
      <el-tag size="small">学校</el-tag>
    </el-descriptions-item>
    <el-descriptions-item label="联系地址">江苏省苏州市吴中区吴中大道 1188 号</el-descriptions-item>
  </el-descriptions>
    </el-card>
</template>

<script>
export default {

    name: "UserInfo",
    setup() {
        
    },
}
</script>

<style scoped>
.user-info {
    width: 80%;
    margin: 40px auto;
}


</style>