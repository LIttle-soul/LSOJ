<template>
  <div class="perfect">
      <!-- 基础信息修改完善 -->
    <el-card class="box-card">
        <h1 style="margin-bottom: 20px;"><i class="el-icon-s-tools"></i> {{form_title}}</h1>
      <el-form ref="form" :model="user_form" label-width="80px" size="mini">
        <el-form-item label="真实姓名">
          <el-input v-model="user_form.user_name" :disabled="activate"></el-input>
        </el-form-item>
        <el-form-item label="个人昵称">
          <el-input v-model="user_form.user_nick"></el-input>
        </el-form-item>
        <el-form-item label="电话号码">
          <el-input v-model="user_form.user_telephone"></el-input>
        </el-form-item>
        <el-form-item label="个人宣言">
          <el-input type="textarea" v-model="user_form.user_maxim" class="textarea"></el-input>
        </el-form-item>
        <el-form-item label="性别">
          <el-radio-group v-model="user_form.user_sex" size="medium" :disabled="activate">
            <el-radio label="男"></el-radio>
            <el-radio label="女"></el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="个人生日">
            <el-date-picker 
            :disabled="activate"
            type="date" 
            placeholder="选择日期" 
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            v-model="user_form.user_birthday">
            </el-date-picker>
         </el-form-item>
        <el-form-item size="large">
          <el-button type="primary" @click="onSubmit">提交</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    <UserInfoBind />
  </div>
</template>

<script>
import { defineAsyncComponent } from 'vue'

export default {
  components: {
    UserInfoBind: defineAsyncComponent(() => import('@/views/user/UserInfo/BindUserInfo.vue'))
  },
  data() {
    return {
      form_title: '基础信息完善',
      activate: false,
      user_form: {
        user_name: '',
        user_nick: '',
        user_maxim: '',
        user_sex: '男',
        user_birthday: "2000-01-01",
        user_telephone: null,
      },
    };
  },
  mounted() {
    this.InputUserInfo();
  },
  methods: {
    InputUserInfo()  {
     this.$http({
        url: '/api/perfectinfo/',
        methods: 'get',
        params: {
          'token': this.$cookies.get('token')
        }
      }).then( res => {
        // console.log(res.data)
        if(res.data.status){
          this.user_form.user_nick = res.data.data.user_nick
          this.user_form.user_maxim = res.data.data.user_maxim
          this.user_form.user_name = res.data.data.user_name
          this.user_form.user_sex = res.data.data.user_sex === 0 ? '男' : '女'
          this.user_form.user_birthday = this.$dayJS(res.data.data.user_birthday).format('YYYY-MM-DD')
          this.user_form.user_telephone = res.data.data.user_telephone
          this.activate = true
          this.form_title = '基础信息修改'
        }
      })
    },
      onSubmit(){
        //   console.log(this.user_form);
          this.$http({
            url: '/api/perfectinfo/',
            method: 'post',
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded'
            },
            transformRequest: [function(data) {
              let ret = ''
              for (let it in data) {
                ret += encodeURIComponent(it) + '=' + encodeURIComponent(data[it]) + '&'
              }
              return ret
            }],
            params: {},
            data: {
              'token': this.$cookies.get('token'),
              'user_name': this.user_form.user_name,
              'user_nick': this.user_form.user_nick,
              'user_maxim': this.user_form.user_maxim,
              'user_sex': this.user_form.user_sex,
              'user_birthday': this.user_form.user_birthday,
              'user_telephone': this.user_form.user_telephone,
            }
          }).then( res => {
            // console.log('res=>', res.data.err);
            alert(res.data.err);
          })
      }
  },
};
</script>

<style scoped>
.perfect {
    max-width: 500px;
    min-width: 350px;
    margin: 0 auto;
}
.box-card {
  
  margin: 40px auto;
}
.box-card:last-child {
    margin-top: 20px;
}
.box-card .el-input {
    max-width: 300px;
}

.box-card .textarea {
    width: 300px;
}
</style>
