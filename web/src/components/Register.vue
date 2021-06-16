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
    <el-form-item label="" prop="checkPass">
      <el-input
        prefix-icon="el-icon-lock"
        placeholder="重复密码"
        type="password"
        v-model="ruleForm.checkPass"
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
          <div
            class="login-code"
            @click="refreshCode"
            style="width: 90"
            key="two"
            v-if="isShow"
          >
            <Identify :identifyCode="ruleForm.true_code" />
          </div>
        </template>
      </el-input>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submitForm('ruleForm')">提交</el-button>
      <el-button @click="resetForm('ruleForm')">重置</el-button>
    </el-form-item>
  </el-form>
</template>

<script>
import Identify from "./identify.vue";

export default {
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
        return callback(new Error("用户账号不能为空"));
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
    var validatePass2 = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请输入密码"));
      } else if (value !== this.ruleForm.pass) {
        callback(new Error("两次输入密码不一致"));
      } else {
        callback();
      }
    };
    var checkCode = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请输入验证码"));
      } else if (value !== this.ruleForm.true_code) {
        callback(new Error("验证码输入错误"));
      } else {
        callback();
      }
    };
    return {
      ruleForm: {
        user: "",
        pass: "",
        checkPass: "",
        code: "",
        true_code: "1234",
      },
      rules: {
        user: [{ validator: checkUser, trigger: "blur" }],
        pass: [{ validator: validatePass, trigger: "blur" }],
        checkPass: [{ validator: validatePass2, trigger: "blur" }],
        code: [{ validator: checkCode, trigger: "blur" }],
      },
      identifyCodes: "1234567890",
    };
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          alert("submit!");
        } else {
          console.log("error submit!!");
          return false;
        }
      });
    },
    resetForm(formName) {
      this.$refs[formName].resetFields();
    },
    refreshCode() {
      this.ruleForm.true_code = "";
      this.makeCode(this.identifyCodes, 4);
    },
    randomNum(min, max) {
      return Math.floor(Math.random() * (max - min) + min);
    },
    makeCode(o, l) {
      for (let i = 0; i < l; i++) {
        this.ruleForm.true_code +=
          this.identifyCodes[this.randomNum(0, this.identifyCodes.length)];
      }
    },
  },
};
</script>

<style>
</style>
