<template>
<div>
    <el-header class="home-header">
        <Header />
    </el-header>
    <el-main class="home-main">
        <router-view />
    </el-main>
    <el-footer class="home-footer">
        <Footer />
    </el-footer>
</div>
</template>

<script>
import { defineAsyncComponent } from '@vue/runtime-core'

export default {
    name: "User",
    components: {
        Header: defineAsyncComponent(() => import('./Header/Header.vue')),
        Footer: defineAsyncComponent(() => import('./Footer/Footer.vue')),
    },
    data() {
        return {
            count: 0
        }
    },
    methods: {
        load() {
            this.count += 2
            if(this.count > 100){
                this.count = 100
            }
        }
    }
}
</script>

<style>
a {
  text-decoration: none;
}
.home-header {
    width: 100%;
    position: fixed;
    top: 10px;
    z-index: 5;
}
.home-main {
    margin: 50px auto;
    max-width: 1800px;
    min-width: 400px;
    position: relative;
}
.router-link-active {
  text-decoration: none;
}
</style>