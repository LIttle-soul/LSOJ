<template>
  <div class="login-container" :style="bg">
    <h4 class="login-title">
      <img :src="logo" alt="" class="logo" />高密度空气质量监测原型系统
    </h4>
    <el-form
      ref="loginForm"
      :model="loginForm"
      :rules="loginRules"
      class="login-form"
      autocomplete="on"
      label-position="left"
    >
      <div class="title-container">
        <h3 class="title">系统登录</h3>
      </div>
      <el-form-item prop="username">
        <span class="svg-container">
          <svg-icon icon-class="user" />
        </span>
        <el-input
          ref="username"
          v-model="loginForm.username"
          placeholder="用户名"
          name="username"
          type="text"
          tabindex="1"
          autocomplete="on"
        />
      </el-form-item>

      <el-tooltip
        v-model="capsTooltip"
        content="Caps lock is On"
        placement="right"
        manual
      >
        <el-form-item prop="password">
          <span class="svg-container">
            <svg-icon icon-class="password" />
          </span>
          <el-input
            :key="passwordType"
            ref="password"
            v-model="loginForm.password"
            :type="passwordType"
            placeholder="密码"
            name="password"
            tabindex="2"
            autocomplete="on"
            @keyup.enter="checkCapslock"
            @blur="capsTooltip = false"
            @keydown.enter="handleLogin"
          />
          <span class="show-pwd" @click="showPwd">
            <svg-icon
              :icon-class="passwordType === 'password' ? 'eye' : 'eye-open'"
            />
          </span>
        </el-form-item>
      </el-tooltip>
      <el-form-item prop="validateCode" style="border: none">
        <div
          style="
            width: 160px;
            border: 1px solid #889aa4;
            border-radius: 5px;
            display: inline-block;
          "
        >
          <span class="svg-container">
            <svg-icon icon-class="message" />
          </span>
          <el-input
            ref="validateCode"
            v-model="loginForm.validateCode"
            placeholder="验证码"
            name="validateCode"
            type="text"
            tabindex="1"
            autocomplete="on"
            style="width: 78%"
          />
        </div>
        <div class="yzm_picture_div">
          <img :src="codeImg" />
        </div>
        <div class="yzm_text_div">
          <a href="javascript:void(0);" @click="loadCode">看不清,换一张？</a>
        </div>
      </el-form-item>
      <el-form-item style="background: #fff; border: none">
        <div class="tips">
          <p>
            <a @click="finduser">忘记用户名？</a
            ><a @click="findpass">忘记密码？</a>
          </p>
        </div>
      </el-form-item>
      <el-form-item style="background: #fff; border: none">
        <el-button
          :loading="loading"
          type="primary"
          @click.enter.prevent="handleLogin"
          style="width: 47%"
          >登录</el-button
        >
        <el-button @click="register" type="primary" style="width: 47%"
          >注册</el-button
        >
      </el-form-item>
    </el-form>
  </div>
</template>
<script>

 export default {
   name: 'Login',
   data() {
     const validateUsername = (rule, value, callback) => {
       if (value =='') {
         callback(new Error('请输入登录名'))
       } else {
         if (value.length > 20) {
           callback(new Error('请输入小于20位登录名'))
         } else {
           callback()
         }
       }
     }
     const validatePassword = (rule, value, callback) => {
       if (value.length < 6 ||value.length > 20) {
         callback(new Error('请输入6-20位密码'))
       } else {
         callback()
       }
     }
     return {
       backgroundImage,
       logo,
       codeImg:'',
       bg:{
         background:`url(${backgroundImage})`,
         backgroundSize:'100% 100%'
       },
       loginForm: {
         validateCode:'',
         username: '',
         password: '' //BKa531*$%_6
       },
       loginRules: {
         validateCode:  [{ required: true, message: '请输入验证码', trigger: 'blur' },
         { min: 4, max: 4, message: '请输入右侧4位数验证码', trigger: 'blur' }],
         username: [{ required: true, trigger: 'blur', validator: validateUsername }],
         password: [{ required: true, trigger: 'blur', validator: validatePassword }]
       },
       passwordType: 'password',
       capsTooltip: false,
       loading: false,
       showDialog: false,
       redirect: undefined,
       otherQuery: {}
     }
   },
   created() {
       this.loadCode();
     // window.addEventListener('storage', this.afterQRScan)
   },
   mounted() {
     if (this.loginForm.username == '') {
       this.$refs.username.focus()
     } else if (this.loginForm.password == '') {
       this.$refs.password.focus()
     }
     else if (this.loginForm.validateCode == '') {
       this.$refs.validateCode.focus()
     }
   },
   methods: {
     register(){
       this.$router.push({path: '/register'});
     },
     loadCode() {
       getCode().then(res => {  //获取验证码
         this.codeImg=window.URL.createObjectURL(res);
         })
     }
   }
 }
</script>