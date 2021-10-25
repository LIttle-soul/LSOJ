<template>
  <div class="login_box">
    <el-form ref="form" :model="form" :rules="rules" label-width="80px">
      <h1 class="login_title">欢迎登录</h1>
      <el-form-item label="帐号" prop="username">
        <el-input
          v-model="form.username"
          placeholder="学号"
          prefix-icon="el-icon-user-solid"
          clearable
          class="t1"
        ></el-input>
      </el-form-item>
      <el-form-item label="密码" prop="password">
        <el-input
          type="password"
          v-model="form.password"
          placeholder="密码"
          prefix-icon="el-icon-key"
          show-password
          clearable
          class="t1"
        ></el-input>
      </el-form-item>

      <!-- 验证码 -->
      <div class="check" v-if="!isShow">
        <el-form-item label="验证码" prop="verifycode" style="width:570px">
          <el-input
            v-model="form.verifycode"
            placeholder="请输入验证码"
            size="small"
            style="width: 170px;float: left;"
            clearable
          ></el-input>
        </el-form-item>
        <el-form-item>
          <div class="identifybox">
            <div @click="makeCode">
              <s-identify :identifyCode="identifyCode"></s-identify>
            </div>
            <el-button @click="makeCode" type="text" class="textbtn"
              >看不清，换一张</el-button
            >
          </div>
        </el-form-item>
      </div>

      <el-form-item>
        <router-link :to="{ path: '/register' }">
          <el-link type="primary" :underline="false" class="txt1">注册</el-link>
        </router-link>
        <el-button type="text" class="txt2" @click="on">忘记密码？</el-button>

        <br />
        <el-button
          type="primary"
          @click="onSubmit('form')"
          class="btn"
          icon="el-icon-switch-button"
          >登录</el-button
        >
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { defineAsyncComponent } from "vue";
import { submitLoginForm } from "@/api/user";
import { loadData } from "@/utils/loadData";

export default {
  name: "Login",
  components: {
    SIdentify: defineAsyncComponent(() =>
      import("@/components/Other/Verification.vue")
    ),
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
        if (this.form.password !== "") {
          this.$refs.form.validateField("checkPass");
        }
        callback();
      }
    };
    var checkCode = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请输入验证码"));
      } else if (value.toLowerCase() !== this.identifyCode.toLowerCase()) {
        callback(new Error("验证码输入错误"));
      } else {
        callback();
      }
    };
    return {
      isShow: false,
      identifyCode: "",
      form: {
        username: "",
        password: "",
        verifycode: "",
      },
      rules: {
        username: [{ validator: checkUser, trigger: "blur" }],
        password: [{ validator: validatePass, trigger: "blur" }],
        verifycode: [{ validator: checkCode, trigger: "blur" }],
      },
    };
  },
  mounted() {
    // 初始化验证码
    this.identifyCode = "";
    this.makeCode();
  },
  methods: {
    onSubmit(formName) {
      this.$refs[formName].validate(async (valid) => {
        if (valid) {
          var val = await submitLoginForm(this.form);
          if (val.status) {
            this.$store.dispatch("user/getUserInfo");
            loadData();
            this.$message({
              type: "success",
              message: val.message,
            });
            this.$Cookies.set("token", val.token);
            this.$router.push("/home");
          } else {
            this.$message({
              type: "error",
              message: val.message,
            });
          }
        } else {
          this.$message({
            type: "error",
            message: "请正确填写表单信息！！！",
          });
          return false;
        }
      });
    },
    on() {
      this.$router.push("/forgetpassword"); // 返回登录界面
    },
    // 获取四位随机验证码
    makeCode() {
      var s = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
      var code = "";
      for (var i = 0; i < 4; i++) {
        var index = Math.floor(Math.random() * 62);

        code += s.charAt(index);
      }
      this.identifyCode = code;
    },
  },
};
</script>

<style scoped>
.login_box {
  width: 500px;
  height: 400px;
  border: 1px solid gray;
  margin: 150px auto;
  padding: 20px 60px 20px 30px;
  border-radius: 20px;
  box-shadow: 5px 5px 5px gray;
}

.login_title {
  text-align: center;
  margin-right: -35px;
  margin-bottom: 40px;
  font-family: "楷体";
  font-size: 35px;
  color: #409eff;
}
.t1 {
  width: 400px;
}

.txt1 {
  font-size: 18px;
  float: left;
}

.txt2 {
  font-size: 18px;
  float: right;
  color: grey;
}

.btn {
  margin: -50px 125px;
  text-align: left;
  height: 50px;
  width: 110px;
  font-size: 20px;
  position: absolute;
}

.checkCode {
  color: #409eff;
  margin-left: 20px;
  font-size: 20px;
  cursor: pointer;
}

.log-input {
  width: 320px;
  float: left;
}

.identifybox {
  float: right;
  margin-right: 25%;
  margin-top: -15%;
}
</style>
