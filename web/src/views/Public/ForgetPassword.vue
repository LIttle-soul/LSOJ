<template>
  <el-card class="forget-password">
    <el-form ref="form" :model="form" :rules="rules" label-width="165px">
      <h3 class="header-font">
        忘记密码
      </h3>
      <el-form-item label="用户名" prop="username">
        <el-input
          v-model="form.username"
          maxlength="16"
          placeholder="用户名（学号）最长16位*"
          style="width: 290px;float: left;"
          prefix-icon="el-icon-user-solid"
        ></el-input>
      </el-form-item>
      <el-form-item label="新密码" prop="password">
        <el-input
          type="password"
          v-model="form.password"
          placeholder="密码"
          style="width: 290px;float: left;"
          show-password
          prefix-icon="el-icon-lock"
        ></el-input>
      </el-form-item>
      <el-form-item label="确认密码" prop="check_password">
        <el-input
          type="password"
          v-model="form.check_password"
          placeholder="确认密码"
          style="width: 290px;float: left;"
          show-password
          prefix-icon="el-icon-lock"
        ></el-input>
      </el-form-item>
      <el-form-item label="验证码" prop="verifycode" style="width:570px">
        <el-input
          v-model="form.verifycode"
          placeholder="验证码"
          style="width: 290px;float: left;"
          prefix-icon="el-icon-suitcase"
        >
          <template #append>
            <el-button
              @click="sendEmailCode"
              :disabled="send_email_button.status"
              >{{ send_email_button.text }}</el-button
            >
          </template>
        </el-input>
      </el-form-item>
      <el-button
        class="bottom-button"
        type="warning"
        @click="linkTo()"
        style="width: 180px;"
        >返回登录</el-button
      >
      <el-button
        class="bottom-button"
        type="primary"
        @click="onSubmit('form')"
        style="width: 180px;"
        >提交</el-button
      >
    </el-form>
  </el-card>
</template>

<script>
import { submitForgetPasswordForm, sendEmailCode } from "@/api/user";

export default {
  name: "ForgetPassword",
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
    var validateCheckPass = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请输入密码"));
      } else if (value !== this.form.password) {
        return callback(new Error("两次输入密码不一致"));
      } else {
        callback();
      }
    };
    return {
      isShow: false,
      button_text: "发送邮件",
      send_email_button: {
        status: false,
        text: "获取验证码",
      },
      form: {
        username: "",
        password: "",
        check_password: "",
        verifycode: "",
      },
      rules: {
        name: [{ validator: checkUser, trigger: "blur" }],
        password: [{ validator: validatePass, trigger: "blur" }],
        check_password: [{ validator: validateCheckPass, trigger: "blur" }],
      },
    };
  },
  methods: {
    onSubmit(formName) {
      this.$refs[formName].validate(async (valid) => {
        if (valid) {
          var val = await submitForgetPasswordForm(this.form);
          if (val.status) {
            this.$message({
              type: "success",
              message: val.message,
            });
            this.$router.push("/login");
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
    async sendEmailCode() {
      this.send_email_button.status = true;
      var data = await sendEmailCode({
        user_id: this.form.username,
      });
      if (data.status) {
        this.$message({
          type: "success",
          message: data.message,
        });
        let time_out = 60;
        let inter = setInterval(() => {
          this.send_email_button.text = "请在" + time_out + "秒后再试";
          time_out--;
          if (time_out <= 0) {
            this.send_email_button.status = false;
            this.send_email_button.text = "获取验证码";
            clearInterval(inter);
          }
        }, 1000);
      } else {
        this.$message({
          type: "error",
          message: data.message,
        });
      }
    },
    linkTo() {
      this.$router.push("/login");
    },
  },
};
</script>

<style scoped>
.header-font {
  margin-bottom: 30px;
  text-align: center;
  width: 100%;
  font-family: "楷体";
  font-size: 28px;
}

.forget-password {
  width: 600px;
  height: 450px;
  margin: 140px auto;
  border-radius: 15px;
}

.bottom-button {
  margin-left: 12%;
}
</style>
