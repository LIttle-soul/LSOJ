<template>
  <el-card class="login-box">
    <div class="login-header">欢迎登录</div>
    <el-form
      ref="form_ref"
      :model="form"
      :rules="rules"
      label-width="80px"
      class="login-main"
    >
      <el-form-item label="帐号" prop="user_id">
        <el-input
          v-model="form.user_id"
          placeholder="学号"
          :clearable="true"
          class="input-text"
        >
          <template #prefix>
            <el-icon style="font-size: 1.4rem; transform: translateY(8px)"
              ><user-filled
            /></el-icon>
          </template>
        </el-input>
      </el-form-item>
      <el-form-item label="密码" prop="password">
        <el-input
          type="password"
          v-model="form.password"
          placeholder="密码"
          :show-password="true"
          :clearable="true"
          class="input-text"
        >
          <template #prefix>
            <el-icon style="font-size: 1.4rem; transform: translateY(8px)"
              ><key
            /></el-icon> </template
        ></el-input>
      </el-form-item>
      <div class="check-code">
        <el-form-item label="验证码" prop="code">
          <el-input
            v-model="form.code"
            placeholder="请输入验证码"
            :clearable="true"
            class="input-text"
            @keydown.enter="onSubmit()"
          >
            <template #prefix>
              <el-icon style="font-size: 1.4rem; transform: translateY(8px)"
                ><circle-check
              /></el-icon> </template
          ></el-input>
        </el-form-item>
        <div class="identifybox">
          <div @click="makeCode" class="identifybox-item">
            <s-identify
              :identifyCode="true_code"
              :contentWidth="100"
              :contentHeight="40"
            ></s-identify>
          </div>
          <div @click="makeCode" type="text" class="text-btn">看不清，换一张</div>
        </div>
      </div>
    </el-form>
    <div class="login-footer">
      <router-link :to="{ path: '/register' }">
        <el-link type="primary" :underline="false" class="txt1">注册</el-link>
      </router-link>
      <router-link :to="{ path: '/forgetpassword' }">
        <el-link type="info" :underline="false" class="txt2">忘记密码？</el-link>
      </router-link>
      <el-button type="primary" @click="onSubmit()" class="btn"
        ><el-icon style="font-size: 1.6rem; transform: translateY(2px)"
          ><switch-button /></el-icon
        >登录</el-button
      >
    </div>
  </el-card>
</template>

<script lang="ts" setup>
import { submitLoginForm } from "@/api/user";
import SIdentify from "@/components/Other/Verification.vue";
import { onMounted, reactive, ref, unref } from "vue";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";
import cookies from "vue-cookies";
import store from "@/store";
import { Key, UserFilled, CircleCheck, SwitchButton } from "@element-plus/icons";

// 表单类型限制
interface loginData {
  user_id: String;
  password: String;
  code: String;
}

// 构建表单数据
let form = ref<loginData>({
  user_id: "",
  password: "",
  code: "",
});
let true_code = ref("");
let form_ref = ref();

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
let checkCode = (rule: any, value: any, callback: any) => {
  if (value.toLowerCase() !== true_code.value.toLowerCase()) {
    callback(new Error("验证码输入错误"));
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
  code: [
    { requried: true, message: "验证码不能为空", trigger: "blur" },
    { validator: checkCode, trigger: "blur" },
  ],
});

// 随机验证码生成
let makeCode = () => {
  let s = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
  let code = "";
  for (let i = 0; i < 4; i++) {
    let index = Math.floor(Math.random() * 62);

    code += s.charAt(index);
  }
  true_code.value = "0000";
};

// 初始化验证码生成
onMounted(() => {
  makeCode();
});

// 数据提交
let router = useRouter();

let onSubmit = () => {
  let form_temp = unref(form_ref);
  form_temp.validate(async (valid: any) => {
    if (valid) {
      let val = await submitLoginForm({
        user_id: form.value.user_id,
        password: form.value.password,
      });
      if (val.status) {
        store.dispatch("user/getUserInfo");
        ElMessage({
          type: "success",
          message: val.message,
        });
        cookies.set("token", val.token);
        router.push("/home");
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
    padding-top: 40px;
    width: 100%;
    height: 250px;
    // background-color: #00776566;
    .input-text {
      width: calc(100% - 80px);
    }
    .check-code {
      width: calc(100% - 80px);
      display: flex;
      // background-color: #939393;
      .el-form-item {
        width: calc(100% - 110px);
        .input-text {
          width: 100%;
        }
      }

      .identifybox {
        padding-left: 10px;
        .identifybox-item {
          border-radius: 5px;
          width: 100px;
          height: 40px;
          overflow: hidden;
          cursor: pointer;
        }
        .text-btn {
          height: 16px;
          font-size: 14px;
          color: #409eff;
          cursor: pointer;
        }
      }
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
