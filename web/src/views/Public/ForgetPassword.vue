<template>
  <el-card class="login-box">
    <div class="login-header">忘记密码</div>
    <el-form
      ref="form_ref"
      :model="form"
      :rules="rules"
      label-width="80px"
      class="login-main"
    >
      <el-form-item label="用户名" prop="user_id">
        <el-input
          v-model="form.user_id"
          maxlength="16"
          placeholder="用户名（学号）最长16位"
          class="input-text"
          ><template #prefix>
            <el-icon style="font-size: 1.4rem; transform: translateY(8px)"
              ><user-filled
            /></el-icon> </template
        ></el-input>
      </el-form-item>
      <el-form-item label="新密码" prop="password">
        <el-input
          type="password"
          v-model="form.password"
          placeholder="密码"
          :show-password="true"
          :clearable="true"
          class="input-text"
          ><template #prefix>
            <el-icon style="font-size: 1.4rem; transform: translateY(8px)"
              ><key
            /></el-icon> </template
        ></el-input>
      </el-form-item>
      <el-form-item label="确认密码" prop="checkpassword">
        <el-input
          type="password"
          v-model="form.checkpassword"
          placeholder="确认密码"
          :show-password="true"
          :clearable="true"
          class="input-text"
          ><template #prefix>
            <el-icon style="font-size: 1.4rem; transform: translateY(8px)"
              ><key
            /></el-icon> </template
        ></el-input>
      </el-form-item>
      <el-form-item label="验证码" prop="code">
        <el-input v-model="form.code" placeholder="验证码" class="input-text">
          <template #prefix>
            <el-icon style="font-size: 1.4rem; transform: translateY(8px)"
              ><circle-check
            /></el-icon>
          </template>
          <template #append>
            <el-button @click="sendEmail" :disabled="send_email_button.status">{{
              send_email_button.text
            }}</el-button>
          </template>
        </el-input>
      </el-form-item>
    </el-form>
    <div class="login-footer">
      <router-link :to="{ path: '/login' }">
        <el-link type="primary" :underline="false" class="txt1">登录</el-link>
      </router-link>
      <router-link :to="{ path: '/register' }">
        <el-link type="info" :underline="false" class="txt2">注册</el-link>
      </router-link>
      <el-button type="primary" @click="onSubmit()" class="btn"
        ><el-icon style="font-size: 1.6rem; transform: translateY(2px)"
          ><switch-button /></el-icon
        >提交</el-button
      >
    </div>
  </el-card>
</template>

<script lang="ts" setup>
import { submitForgetPasswordForm, sendEmailCode } from "@/api/user";
import { onMounted, reactive, ref, unref } from "vue";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";
import { Key, UserFilled, CircleCheck, SwitchButton, Lock } from "@element-plus/icons";

// 表单类型限制
interface forgetpasswordData {
  user_id: String;
  password: String;
  checkpassword: String;
  code: String;
}

interface sendEmailButtonData {
  status: Boolean;
  text: String;
}

// 构建表单数据
let form = ref<forgetpasswordData>({
  user_id: "",
  password: "",
  checkpassword: "",
  code: "",
});
let form_ref = ref();

// 获取验证码按钮
let send_email_button = ref<sendEmailButtonData>({
  status: false,
  text: "获取验证码",
});

// 自定义效验规则
let checkPassword = (rule: any, value: any, callback: any) => {
  let reg = /^[A-Za-z][A-Za-z0-9_.]{7,19}$/;
  // console.log("reg", value, value.match(reg));
  if (!value.match(reg)) {
    callback(new Error("密码由字母或开头，且只能为字母,数字,下划线及（.）"));
  } else {
    callback();
  }
};
let checkPassword2 = (rule: any, value: any, callback: any) => {
  let reg = /^[A-Za-z][A-Za-z0-9_.]{7,19}$/;
  // console.log("reg", value, value.match(reg));
  if (!value.match(reg)) {
    callback(new Error("密码由字母或开头，且只能为字母,数字,下划线及（.）"));
  } else if (value != form.value.password) {
    callback(new Error("密码输入不一致"));
  } else {
    callback();
  }
};

// 构建验证规则
let rules = reactive({
  user_id: [
    { required: true, message: "账号不能为空", trigger: "blur" },
    {
      min: 5,
      max: 20,
      message: "用户账号必须在5-20个字符之间",
      trigger: "blur",
    },
  ],
  password: [
    { required: true, message: "密码不能为空", trigger: "blur" },
    { min: 8, max: 20, message: "密码必须在8-20个字符之间", trigger: "blur" },
    { validator: checkPassword, trigger: "blur" },
  ],
  checkpassword: [
    { required: true, message: "密码不能为空", trigger: "blur" },
    { min: 8, max: 20, message: "密码必须在8-20个字符之间", trigger: "blur" },
    { validator: checkPassword2, trigger: "blur" },
  ],
});

// 数据提交
let router = useRouter();

let onSubmit = () => {
  let form_temp = unref(form_ref);
  form_temp.validate(async (valid: any) => {
    if (valid) {
      let val = await submitForgetPasswordForm({
        user_id: form.value.user_id,
        new_password: form.value.password,
        check_password: form.value.checkpassword,
        email_code: form.value.code,
      });
      if (val.status) {
        ElMessage({
          type: "success",
          message: val.message,
        });
        router.push("/login");
      } else {
        ElMessage({
          type: "error",
          message: val.message,
        });
      }
    } else {
      ElMessage({
        type: "error",
        message: "请正确填写表单信息！！！",
      });
      return false;
    }
  });
};

// 获取验证码
let sendEmail = () => {
  let form_temp = unref(form_ref);
  form_temp.validate(async (valid: any) => {
    if (valid) {
      send_email_button.value.status = true;
      send_email_button.value.text = "邮箱验证中";
      let data = await sendEmailCode({
        user_id: form.value.user_id,
      });
      if (data.status) {
        ElMessage({
          type: "success",
          message: data.message,
        });
        let time_out = 60;
        let inter = setInterval(() => {
          send_email_button.value.text = "请在" + time_out + "秒后再试";
          time_out--;
          if (time_out <= 0) {
            send_email_button.value.status = false;
            send_email_button.value.text = "获取验证码";
            clearInterval(inter);
          }
        }, 1000);
      } else {
        send_email_button.value.status = false;
        send_email_button.value.text = "获取验证码";
        ElMessage({
          type: "error",
          message: data.message,
        });
      }
    } else {
      ElMessage({
        type: "error",
        message: "请正确填写表单信息！！！",
      });
      return false;
    }
  });
};
</script>

<style lang="scss">
@media screen and (max-width: 450px) {
  .login-box {
    .el-card__body {
      padding: 20px 0;
    }
  }
}
</style>

<style scoped lang="scss">
.login-box {
  width: 100%;
  max-width: 600px;
  min-width: 360px;
  height: 450px;
  margin: 150px auto 0 auto;
  border-radius: 20px;
  .login-header {
    height: 60px;
    width: 100%;
    line-height: 60px;
    font-size: 35px;
    font-family: "STKaiti";
    color: #409eff;
    text-align: center;
    // background-color: #700056;
  }
  .login-main {
    padding-top: 20px;
    width: 100%;
    height: 250px;
    // background-color: #00776566;
    .input-text {
      width: calc(100% - 80px);
    }
  }
  .login-footer {
    width: 100%;
    height: 60px;
    // background-color: #55770033;
    position: relative;
    .txt1 {
      width: 100px;
      position: absolute;
      top: 20px;
      left: calc(50% + 80px);
      font-size: 18px;
      // background-color: #409eff;
    }
    .txt2 {
      width: 100px;
      position: absolute;
      top: 20px;
      left: calc(50% - 160px);
      font-size: 18px;
      // background-color: #409eff;
    }
    .btn {
      position: absolute;
      top: 10px;
      font-size: 20px;
      left: calc(50% - 45px);
      cursor: pointer;
    }
  }
}
@media screen and (max-width: 450px) {
  .login-box {
    margin: 20px auto 0 auto;
  }
}
</style>
