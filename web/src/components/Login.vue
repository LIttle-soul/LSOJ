<template>
  <el-form
    :model="ruleForm"
    status-icon="true"
    :rules="rules"
    ref="ruleForm"
    label-position="left"
    class="demo-ruleForm"
  >
    <el-form-item label="" prop="user">
      <el-input
        prefix-icon="el-icon-user"
        placeholder="学号/工号"
        type="text"
        v-model="ruleForm.user"
        autocomplete="off"
      ></el-input>
    </el-form-item>
    <el-form-item label="" prop="pass">
      <el-input
        prefix-icon="el-icon-lock"
        placeholder="密码"
        type="password"
        v-model="ruleForm.pass"
        autocomplete="off"
      ></el-input>
    </el-form-item>
    <el-form-item label="" prop="code">
      <el-input
        prefix-icon="el-icon-box"
        placeholder="验证码"
        v-model="ruleForm.code"
      >
        <template #append>
          <div class="login-code" @click="getCode" key="one" v-if="isShow">
            <Identify :identifyCode="ruleForm.true_code"></Identify>
          </div>
        </template>
      </el-input>
    </el-form-item>
    <!-- 按钮实现 -->
    <el-form-item>
      <el-button type="primary" @click="submitForm('ruleForm')">提交</el-button>
      <el-button @click="resetForm('ruleForm')">重置</el-button>
    </el-form-item>
  </el-form>
</template>

<script>
import Identify from "./identify.vue";

export default {
  name: 'Login',
  components: {
    Identify,
  },
  props: {
    isShow: {
      type: Boolean,
      default: true,
    },
  },
  data() {
    var checkUser = (rule, value, callback) => {
      if (!value) {
        return callback(new Error("用户名不能为空"));
      }
      setTimeout(() => {
        if (value.length < 5 || value.length > 20) {
          return callback(new Error("用户账号必须在5-20个字符之间"));
        } else {
          callback();
        }
      }, 1000);
    };
    var validatePass = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请输入密码"));
      } else {
        if (this.ruleForm.checkPass !== "") {
          this.$refs.ruleForm.validateField("checkPass");
        }
        callback();
      }
    };
    var checkCode = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请输入验证码"));
      } else if (value.toLowerCase() !== this.ruleForm.true_code.toLowerCase()) {
        callback(new Error("验证码输入错误"));
      } else {
        callback();
      }
    };
    return {
      ruleForm: {
        user: "",
        pass: "",
        code: "",
        true_code: "",
      },
      rules: {
        user: [{ validator: checkUser, trigger: "blur" }],
        pass: [{ validator: validatePass, trigger: "blur" }],
        code: [{ validator: checkCode, trigger: "blur" }],
      },
    };
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.$http.post(
            '/api/login/',
            this.$qs.stringify({
              'user_id': this.ruleForm.user,
              'password': this.ruleForm.pass,
              'code': this.ruleForm.code,
            }
          )).then( res => {
            console.log('res=>', res);
            alert(res.data.err);
            if(res.data.status){
              this.$cookies.set('token', res.data.token)
              this.$router.push('/home');
            }
          })
        } else {
          console.log("error submit!!");
          return false;
        }
      });
    },
    resetForm(formName) {
      this.$refs[formName].resetFields();
    },
    getCode() {
      this.$http.get('/api/login/').then(response => (
          this.ruleForm.true_code = response.data.capture,
          console.log(response.data.capture)
      ));
    }
  },
};
</script>

<style>
</style>
