<template>
  <div class="login-register">
    <div class="container" :class="{ 'right-panel-active': signUpMode }">
      <!-- Sign Up -->
      <div class="container__form container__signup">
        <Register :isShow="signUpMode"/>
      </div>
      <!-- Sign In -->
      <div class="container__form container__signin">
        <Login :isShow="!signUpMode"/>
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
import { defineAsyncComponent } from 'vue'

export default {
  name: "LoginRegister",
  components: {
    Login: defineAsyncComponent(() => import('../../components/Login.vue')),
    Register: defineAsyncComponent(() => import('../../components/Register.vue')),
  },
  setup() {},
  data() {
    return {
      signUpMode: false,
    };
  },
  mounted() {
  },
  methods: {
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
  opacity: 0;
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

.btn:active {
  transform: scale(0.85);
}

.btn:focus {
  outline: none;
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