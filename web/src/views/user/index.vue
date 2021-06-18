<template>
<div>
    <el-header>
        <Header />
    </el-header>
    <el-main>
        <router-view />
    </el-main>
    <el-footer>
        <Footer />
    </el-footer>
</div>
</template>

<script>
import { defineAsyncComponent } from '@vue/runtime-core'

export default {
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
 
.router-link-active {
  text-decoration: none;
}
</style>