<template>
  <el-card class="user-info">
    <el-descriptions class="margin-top" :column="3" size="medium" border>
      <template #title>
        <i class="el-icon-user-solid"></i>
        个人信息
      </template>
      <el-descriptions-item>
        <template #label>
          <i class="el-icon-user"></i>
          用户账号
        </template>
        {{user_data.user_id}}
      </el-descriptions-item>
      <el-descriptions-item>
        <template #label>
          <i class="el-icon-s-flag"></i>
          用户昵称
        </template>
        {{user_data.user_nick}}
      </el-descriptions-item>
      <el-descriptions-item>
        <template #label>
          <i class="el-icon-s-custom"></i>
          真实姓名
        </template>
        {{user_data.user_name}}
      </el-descriptions-item>
      <el-descriptions-item>
        <template #label>
          <i class="el-icon-star-off"></i>
          用户积分
        </template>
        {{user_data.user_score}}
      </el-descriptions-item>
      <el-descriptions-item>
        <template #label>
          <i class="el-icon-time"></i>
          注册时间
        </template>
        {{user_data.registration_time}}
      </el-descriptions-item>
      <el-descriptions-item>
        <template #label>
          <i class="el-icon-school"></i>
          学校
        </template>
        {{user_data.user_school}}
      </el-descriptions-item>
      <el-descriptions-item>
        <template #label>
          <i class="el-icon-male"></i>
          性别
        </template>
        {{user_data.user_sex}}
      </el-descriptions-item>
      <el-descriptions-item>
        <template #label>
          <i class="el-icon-mobile-phone"></i>
          用户手机
        </template>
        {{user_data.user_telephone}}
      </el-descriptions-item>
      <el-descriptions-item>
        <template #label>
          <i class="el-icon-message"></i>
          用户邮箱
        </template>
        {{user_data.user_email}}
      </el-descriptions-item>
    </el-descriptions>
  </el-card>
</template>

<script>
export default {
  name: "UserInfo",
  setup() {},
  mounted() {
    this.InputUserInfo();
  },
  data() {
    return {
      user_data: {
        user_id: null,
        user_nick: null,
        user_name: null,
        user_score: 0,
        registration_time: null,
        user_school: null,
        user_sex: '保密',
        user_telephone: null,
        user_email: null
      }
    }
  },
  methods: {
    InputUserInfo() {
      this.$http({
        url: '/api/perfectinfo/',
        methods: 'get',
        params: {
          'token': this.$cookies.get('token')
        }
      }).then( res => {
        // console.log(res.data)
        if(res.data.status){
          this.user_data.user_id = res.data.data.user_id_id
          this.user_data.user_nick = res.data.data.nick
          this.user_data.user_name = res.data.data.real_name
          this.user_data.user_score = res.data.data.score
          this.user_data.registration_time = res.data.data.reg_time
          this.user_data.user_school = res.data.data.school_id
          this.user_data.user_sex = res.data.data.sex === 0 ? '男' : '女'
          this.user_data.user_telephone = res.data.data.telephone
          this.user_data.user_email = res.data.data.enail
        } else {
          alert(res.data.err)
        }
      })
    }
  }
};
</script>

<style scoped>
.user-info {
  width: 80%;
  margin: 40px auto;
}
</style>
