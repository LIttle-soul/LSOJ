<template>
  <div class="login-register">
    <div class="container" :class="{ 'right-panel-active': signUpMode }">
      <!-- Sign Up -->
      <div class="container__form container__signup">
        <el-form class="form" id="form1">
          <h2 class="form__title">注册</h2>
          <el-form-item label="" class="input">
            <el-input
              prefix-icon="el-icon-user-solid"
              type="text"
              maxlength="20"
              minlength="5"
              placeholder="User"
            ></el-input>
          </el-form-item>
          <el-form-item label="" class="input">
            <el-input
              prefix-icon="el-icon-lock"
              type="password"
              show-password="true"
              minlength="8"
              maxlength="16"
              placeholder="Password"
            ></el-input>
          </el-form-item>
          <el-form-item label="" class="input">
            <el-input
              prefix-icon="el-icon-circle-check"
              type="password"
              placeholder="Reply"
            ></el-input>
          </el-form-item>
          <el-form-item label="" class="input">
            <el-input
              v-model="loginForm.captcha_code"
              prefix-icon="el-icon-circle-check"
              maxlength="6"
              type="text"
              placeholder="Code"
              style="float: left; width: 140px"
            ></el-input>
            <div class="captcha_code">
              <img src="" ref="code" @click="changeCode" alt="" />
            </div>
          </el-form-item>

          <el-form-item label="">
            <el-button class="btn">注册</el-button>
          </el-form-item>
        </el-form>
      </div>
      <!-- Sign In -->
      <div class="container__form container__signin">
        <el-form class="form" id="form2">
          <h2 class="form__title">登录</h2>
          <el-form-item label="" class="input">
            <el-input type="text" placeholder="User"></el-input>
          </el-form-item>
          <el-form-item label="" class="input">
            <el-input type="password" placeholder="Password"></el-input>
          </el-form-item>
          <el-form-item label="" class="input">
            <el-input
              v-model="loginForm.captcha_code"
              prefix-icon="el-icon-circle-check"
              maxlength="6"
              type="text"
              placeholder="Code"
              style="float: left; width: 140px"
            ></el-input>
            <div class="captcha_code">
              <img src="" ref="code" @click="changeCode" alt="" />
            </div>
          </el-form-item>
          <el-form-item label="">
            <el-button class="btn">登录</el-button>
          </el-form-item>
        </el-form>
      </div>
      <!-- Overlay -->
      <div class="container__overlay">
        <div class="overlay">
          <div class="overlay__panel overlay__left">
            <el-button
              @click="signUpMode = !signUpMode"
              class="btn"
              type="primary"
              round
            >
              登录
            </el-button>
          </div>
          <div class="overlay__panel overlay__right">
            <el-button
              @click="signUpMode = !signUpMode"
              class="btn"
              type="primary"
              round
            >
              注册
            </el-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// import { ref } from '@vue/runtime-core'
export default {
  name: "LoginRegister",
  setup() {},
  data() {
    return {
      signUpMode: false,
      loginForm: {
        username: "",
        password: "",
        captcha_key: "",
        captcha_code: "",
      },
    };
  },
  mounted() {
    this.changeCode();
  },
  methods: {
    getCaptchaKey() {
      let captchaKey = Math.random().toString(36).substring(2);
      return captchaKey;
    },
    changeCode() {
      let captcha_key = this.getCaptchaKey();
      this.$refs.code.setAttribute(
        "src",
        process.env.VUE_APP_API_URL +
          "auth/get_captcha?captcha_key=" +
          captcha_key
      );
    },
  },
};
</script>

<style sass scoped>
div {
  /* COLORS */
  --white: #e9e9e9;
  --gray: #333;
  --blue: #0367a6;
  --lightblue: #008997;

  /* RADII */
  --button-radius: 0.7rem;

  /* SIZES */
  --max-width: 758px;
  --max-height: 480px;

  font-size: 16px;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen,
    Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
}

.login-register {
  align-items: center;
  background-color: var(--white);
  background: url("~@/assets/img/640.jpg");
  background-attachment: fixed;
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
  display: grid;
  height: 100vh;
  place-items: center;
  z-index: 1;
}

.form__title {
  font-size: 18pt;
  font-weight: 800;
  color: #07539be8;
  margin: 0;
  margin-bottom: 1.25rem;
}

.link {
  color: var(--gray);
  font-size: 0.9rem;
  margin: 1.5rem 0;
  text-decoration: none;
}

.container {
  /* background-color: var(--white); */
  border-radius: var(--button-radius);
  box-shadow: 0 0.9rem 1.7rem rgba(0, 0, 0, 0.25),
    0 0.7rem 0.7rem rgba(0, 0, 0, 0.22);
  height: var(--max-height);
  max-width: var(--max-width);
  overflow: hidden;
  position: relative;
  width: 100%;
}

.container__form {
  height: 100%;
  position: absolute;
  top: 0;
  transition: all 0.6s ease-in-out;
}

.container__signin {
  left: 0;
  width: 50%;
  z-index: 2;
}

.container.right-panel-active .container__signin {
  transform: translateX(100%);
}

.container__signup {
  left: 0;
  opacity: 0;
  width: 50%;
  z-index: 1;
}

.container.right-panel-active .container__signup {
  -webkit-animation: show 0.6s;
  animation: show 0.6s;
  opacity: 1;
  transform: translateX(100%);
  z-index: 5;
}

.container__overlay {
  height: 100%;
  left: 50%;
  overflow: hidden;
  position: absolute;
  top: 0;
  transition: transform 0.6s ease-in-out;
  width: 50%;
  z-index: 100;
}

.container.right-panel-active .container__overlay {
  transform: translateX(-100%);
}

.overlay {
  height: 100%;
  left: -100%;
  position: relative;
  transform: translateX(0);
  transition: transform 0.6s ease-in-out;
  width: 200%;
}

.container.right-panel-active .overlay {
  transform: translateX(50%);
}

.overlay__panel {
  align-items: center;
  display: flex;
  flex-direction: column;
  height: 100%;
  justify-content: center;
  position: absolute;
  text-align: center;
  top: 0;
  transform: translateX(0);
  transition: transform 0.6s ease-in-out;
  width: 50%;
}

.overlay__left {
  transform: translateX(-20%);
}

.container.right-panel-active .overlay__left {
  transform: translateX(0);
}

.overlay__right {
  right: 0;
  transform: translateX(0%);
}

.container.right-panel-active .overlay__right {
  transform: translateX(20%);
}

.btn {
  background-color: var(--blue);
  background-image: linear-gradient(
    90deg,
    var(--blue) 0%,
    var(--lightblue) 74%
  );
  border-radius: 20px;
  border: 1px solid var(--blue);
  color: var(--white);
  cursor: pointer;
  font-size: 0.8rem;
  font-weight: bold;
  letter-spacing: 0.1rem;
  padding: 0.9rem 4rem;
  text-transform: uppercase;
  transition: transform 80ms ease-in;
}

.form > .btn {
  margin-top: 1.5rem;
}

.btn:active {
  transform: scale(0.95);
}

.btn:focus {
  outline: none;
}

.form {
  background-color: var(--white);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  padding: 0 3rem;
  height: 100%;
  text-align: center;
}

.input {
  border: none;
  padding: 0.7rem 0.9rem;
  margin: 0.2rem 0;
  width: 100%;
}

@-webkit-keyframes show {
  0%,
  49.99% {
    opacity: 0;
    z-index: 1;
  }

  50%,
  100% {
    opacity: 1;
    z-index: 5;
  }
}

@keyframes show {
  0%,
  49.99% {
    opacity: 0;
    z-index: 1;
  }

  50%,
  100% {
    opacity: 1;
    z-index: 5;
  }
}
</style>