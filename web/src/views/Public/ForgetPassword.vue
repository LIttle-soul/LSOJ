<template>
  <el-card class="forget-password">
    <el-form
      :model="ruleForm"
      :rules="rules"
      ref="ruleForm"
      label-width="165px"
    >
      <h3 class="header-font">
        忘记密码
      </h3>
      <el-form-item label="用户名" prop="name">
        <el-input
          v-model="ruleForm.name"
          maxlength="16"
          placeholder="用户名（学号）最长16位*"
          style="width: 290px;float: left;"
          prefix-icon="el-icon-user-solid"
        ></el-input>
      </el-form-item>
      <el-form-item label="新密码" prop="password">
        <el-input
          type="password"
          v-model="ruleForm.password"
          placeholder="密码"
          style="width: 290px;float: left;"
          show-password
          prefix-icon="el-icon-lock"
        ></el-input>
      </el-form-item>
      <el-form-item label="确认密码" prop="checkpassword">
        <el-input
          type="password"
          v-model="ruleForm.checkpassword"
          auto-complete="off"
          placeholder="确认密码"
          style="width: 290px;float: left;"
          show-password
          prefix-icon="el-icon-lock"
        ></el-input>
      </el-form-item>
      <div class="check" v-if="!isShow">
        <el-form-item label="验证码" prop="verifycode" style="width:570px">
          <el-input
            v-model="ruleForm.verifycode"
            placeholder="验证码"
            size="small"
            style="width: 170px;float: left;"
            prefix-icon="el-icon-suitcase"
          ></el-input>
        </el-form-item>
        <!-- 验证码 -->
        <el-form-item>
          <div class="identifybox">
            <div @click="makeCode">
              <SIdentify :identifyCode="identifyCode"></SIdentify>
            </div>
            <el-button @click="makeCode" type="text" class="textbtn"
              >看不清，换一张</el-button
            >
          </div>
        </el-form-item>
      </div>
      <el-button @click="verifyEmail" style="width: 180px;">邮箱验证</el-button>
      <el-button
        type="primary"
        @click="submitForm('ruleForm')"
        style="width: 180px;"
        >提交</el-button
      >
    </el-form>
  </el-card>
</template>

<script>
import { ElMessage } from "element-plus";
import { defineAsyncComponent } from "vue";

export default {
  name: "ForgetPassword",
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
      } else if (value !== this.ruleForm.password) {
        return callback(new Error("两次输入密码不一致"));
      } else {
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
      ruleForm: {
        name: "",
        password: "",
        checkpassword: "",
        verifycode: "",
      },
      rules: {
        name: [{ validator: checkUser, trigger: "blur" }],
        password: [{ validator: validatePass, trigger: "blur" }],
        checkpassword: [{ validator: validateCheckPass, trigger: "blur" }],
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
    verifyEmail() {
       if(this.getEmailCode()){
        this.$prompt("请输入邮箱验证码", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消"
      })
        .then(({ value }) => {
          this.postEmailCode(value);
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "取消输入",
          });
        });
     }
    },
    onSubmit(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          //   console.log(this.form);
          this.$http({
            url: "/api/user/forgetpassword/",
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
              user_id: this.ruleForm.name,
              new_password: this.ruleForm.password,
              check_password: this.ruleForm.checkpassword,
              code: this.ruleForm.verifycode,
            },
          }).then((res) => {
            // console.log('res=>', res);
            if (res.data.status) {
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
    getEmailCode() {
        this.$http({
            url: "/api/user/sendemail/",
            method: "get",
            params: {
                user_id: this.ruleForm.name
            },
          }).then((res) => {
            // console.log('res=>', res);
            if (res.data.status) {
              ElMessage.success(res.data.err);
              return true;
            } else {
              alert(res.data.err);
              return false;
            }
          });
    },
    postEmailCode(value) {
        this.$http({
            url: "/api/user/sendemail/",
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
              user_id: this.ruleForm.name,
              code: value,
            },
          }).then((res) => {
            // console.log('res=>', res);
            if (res.data.status) {
              ElMessage.success(res.data.err);
            } else {
              ElMessage.error(res.data.err);
            }
          });
    },
    // 获取四位随机验证码
    makeCode() {
      this.$http.get("/api/user/forgetpassword/").then((res) => {
        this.identifyCode = res.data.capture;
      });
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
  margin: 100px auto;
  border-radius: 15px;
}

.el-button {
  margin-left: 15%;
}

.identifybox {
  float: right;
  margin-right: 25%;
  margin-top: -15%;
}
</style>
