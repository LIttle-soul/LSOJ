<template>
    <div class="container">
        <!-- form表单容器 -->
        <div class="forms-container">
            <div class="signin-signup">
                <!-- 登陆 -->
                <h1>登陆</h1>
                <!-- 注册 -->
                <h1>注册</h1>
            </div>
        </div>
        <div class="panels-container">
            <div class="panel left-panel">
                <div class="content">
                    <h3>学习是为了有更多的选择,让生活变得更美貌</h3>
                    <p>何以解忧,唯有女修</p>
                    <button class="btn transparent">注册</button>
                </div>
                <img src="" alt="">
            </div>
            <div class="panel right-panel">

            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "LoginRegister",
    setup() {
        
    },
    data() {
        return {

        }
    }
}
</script>

<style scoped>
.container {
    position: relative;
    width: 100%;
    background-color: #fff;
    min-height: 100vh;
    overflow: hidden;
}

.forms-container {
    position: absolute;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
}

.signin-signup {
    position: absolute;
    top: 50%;
    transform: translate(-50%, -50%);
    left: 75%;
    width: 44%;
    transition: 1s 0.7s ease-in-out;
    display: grid;
    grid-template-columns: 1fr;
    z-index: 5;
}
</style>