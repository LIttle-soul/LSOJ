<template>
<div>
    <el-header>
        <NavTop />
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
import NavTop from '@/components/NavTop.vue'
import Footer from '@/components/Footer.vue'

export default {
    components: {
        NavTop,
        Footer
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