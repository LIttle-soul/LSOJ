<template>
  <div class="login">
    <div class="container" :class="panel_active">
			<!-- Sign Up -->
			<div class="container__form container--signup">
				<form action="#" class="form" id="form1">
					<h2 class="form__title">Sign Up</h2>
					<input type="text" placeholder="User" class="input" v-model="user_name"/>
					<input type="email" placeholder="Email" class="input" v-model="email"/>
					<input type="password" placeholder="Password" class="input" v-model="password"/>
					<button class="btn" @click="sign_up">Sign Up</button>
				</form>
			</div>

			<!-- Sign In -->
			<div class="container__form container--signin">
				<form action="#" class="form" id="form2">
					<h2 class="form__title">Sign In</h2>
					<input type="email" placeholder="Email" class="input" v-model="email"/>
					<input type="password" placeholder="Password" class="input" v-model="password"/>
					<a href="#" class="link">Forgot your password?</a>
					<button class="btn" @click="sign_in">Sign In</button>
				</form>
			</div>

			<!-- Overlay -->
			<div class="container__overlay">
				<div class="overlay">
					<div class="overlay__panel overlay--left">
						<button class="btn" id="signIn" @click="changeClass('sign_in')">Sign In</button>
					</div>
					<div class="overlay__panel overlay--right">
						<button class="btn" id="signUp" @click="changeClass('sign_up')">Sign Up</button>
					</div>
				</div>
			</div>
		</div>
  </div>
</template>

<script>
// import axios from "axios";
export default {
  name: "Login",
  data() {
    return {
      panel_active: 'left-panel-active',
      user_name: '',
      email: '',
      password: ''
    }
  },
  methods: {
    changeClass(event) {
      if(event === "sign_in"){
        this.panel_active = 'left-panel-active';
      } else {
        this.panel_active = 'right-panel-active';
      }
    },
    sign_in() {
      console.log(this.email, this.password);
      if(this.email === '' || this.password === ''){
        alert('表单填写不完整');
      } else {
        this.axios({
          method: 'post',
          url: '/login/',
          data: {
            email: this.email,
            password: this.password,
          },
          headers: {'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'},
          transformRequest(obj) {
            let str = [];
            let p;
            for (p in obj) {
              str.push(encodeURIComponent(p) + '=' + encodeURIComponent(obj[p]));
            }
            return str.join('&')
          }
        }).then((res) => {
          console.log(res);
          alert(res.data.status);
        }).catch(err => {
          console.log(err);
          alert('Error');
        })
      }
    },
    sign_up() {
      console.log(this.user_name, this.email, this.password);
      if(this.user_name === '' || this.email === '' || this.password === ''){
        alert('表单填写不完整');
      } else {
        this.axios({
          method: 'post',
          url: '/register/',
          data: {
            name: this.user_name,
            password: this.password,
            email: this.email
          },
          headers: {'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'},
          transformRequest(obj) {
            let str = [];
            let p;
            for (p in obj) {
              str.push(encodeURIComponent(p) + '=' + encodeURIComponent(obj[p]));
            }
            return str.join('&')
          }
        }).then((res) => {
          console.log(res);
          alert(res.data.status);
        }).catch(err => {
          console.log(err);
          alert('Error');
        })
      }
    },
  }
}
</script>

<style scoped>
@import "../assets/normalize.css";
.login{
  align-items: center;
  background: url("../assets/background_oeuhe7.jpg") no-repeat fixed center;
  background-size: cover;
	display: grid;
	height: 100vh;
	place-items: center;
}
.form__title {
  font-weight: 300;
  margin: 0 0 1.25rem;
}

.link {
  color: #333333;
  font-size: 0.9rem;
  margin: 1.5rem 0;
  text-decoration: none;
}

.container {
  background-color: #e9e9e9;
  border-radius: 0.7rem;
  box-shadow: 0 0.9rem 1.7rem rgba(0,0,0,0.25),
      0 0.7rem 0.7rem rgba(0,0,0,0.22);
  height: 420px;
  max-width: 758px;
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

.container--signin {
  left: 0;
  width: 50%;
  z-index: 2;
}

.container.right-panel-active .container--signin {
  transform: translateX(100%);
}

.container--signup {
  left: 0;
  opacity: 0;
  width: 50%;
  z-index: 1;
}

.container.right-panel-active .container--signup {
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
  background: url("../assets/background_oeuhe7.jpg") no-repeat fixed center;
  background-size: cover;
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

.overlay--left {
	transform: translateX(-20%);
}

.container.right-panel-active .overlay--left {
	transform: translateX(0);
}

.overlay--right {
	right: 0;
	transform: translateX(0);
}

.container.right-panel-active .overlay--right {
	transform: translateX(20%);
}

.btn {
	background-color: #0367a6;
	background-image: linear-gradient(90deg, #0367a6 0%, #008997 74%);
	border-radius: 20px;
	border: 1px solid #0367a6;
	color: #e9e9e9;
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
	background-color: #e9e9e9;
	display: flex;
	align-items: center;
	justify-content: center;
	flex-direction: column;
	padding: 0 3rem;
	height: 100%;
	text-align: center;
}

.input {
	background-color: #fff;
	border: none;
	padding: 0.9rem 0.9rem;
	margin: 0.5rem 0;
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