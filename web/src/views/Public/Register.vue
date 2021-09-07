<template>
  <div class="login_box">
    <el-form ref="form" :model="form" :rules="rules" label-width="80px">
      <h1 class="login_title">欢迎注册</h1>
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
          placeholder="输入密码"
          prefix-icon="el-icon-key"
          show-password
          clearable
          class="t1"
        ></el-input>
      </el-form-item>
        <el-form-item label="确认密码" prop="checkpassword">
        <el-input
          type="password"
          v-model="form.checkpassword"
          placeholder="再次输入密码"
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
        <router-link :to="{ path: '/login' }">
          <el-link type="primary" :underline="false" class="txt1">登录</el-link>
        </router-link>
        <el-button type="text" class="txt2" @click="on">忘记密码？</el-button>

        <br />
        <el-button
          type="primary"
          @click="onSubmit('form')"
          class="btn"
          icon="el-icon-switch-button"
          >注册</el-button
        >
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { ElMessage } from "element-plus";
import { defineAsyncComponent } from "vue";

export default {
  name: "Register",
  components: {
    SIdentify: defineAsyncComponent(() =>
      import("@/components/User/Verification.vue")
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
    var validateCheckPass = (rule, value, callback) => {
        if (value === "") {
        callback(new Error("请输入密码"));
      } else if(value !== this.form.password) {
          return callback(new Error("两次输入密码不一致"))
      } else {
        callback();
      }
    }
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
        checkpassword: "",
        verifycode: "",
      },
      rules: {
        username: [{ validator: checkUser, trigger: "blur" }],
        password: [{ validator: validatePass, trigger: "blur" }],
        checkpassword: [{ validator: validateCheckPass, trigger: "blur"}],
        verifycode: [{ validator: checkCode, trigger: "blur" }],
      },
    };
  },
  mounted() {
    // 初始化验证码
    this.identifyCode = "";
    this.makeCode(this.identifyCodes, 4);
  },
  methods: {
    onSubmit(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
        //   console.log(this.form);
          this.$http({
            url: "/api/user/register/",
            method: "post",
            headers: {
              "Content-Type": "application/x-www-form-urlencoded",
            },
            transformRequest: [
              function(data) {
                let ret = "";
                for (let it in data) {
                  ret +=
                    encodeURIComponent(it) +
                    "=" +
                    encodeURIComponent(data[it]) +
                    "&";
                }
                return ret;
              },
            ],
            params: {},
            data: {
              user_id: this.form.username,
              password: this.form.password,
              check_pass: this.form.checkpassword,
              code: this.form.verifycode,
            },
          }).then((res) => {
            // console.log('res=>', res);
            if(res.data.status){
              ElMessage.success(res.data.err);
              this.$router.push("/login");
            } else {
              ElMessage.error(res.data.err);
            }
          });
        } else {
          ElMessage.error("请正确填写表单信息！！！");
          return false;
        }
      });
    },
    on() {
      this.$router.push("/forgetpassword"); // 返回登录界面
    },
    // 获取四位随机验证码
    makeCode() {
      this.$http.get("/api/user/register/").then((res) => {
        this.identifyCode = res.data.capture;
      });
    },
  },
};
</script>

<style scoped>
.login_box {
  width: 500px;
  height: 450px;
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
