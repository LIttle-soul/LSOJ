<template>
    <el-container>
        <el-affix :offset="0">
        <el-aside width="auto">
            <LeftNav :isCollapse='IsShow'/>
        </el-aside>
    </el-affix>
        <el-container>
            <el-header>
                <el-button @click="IsShow = !IsShow" :round="true" icon="el-icon-apple"></el-button>
                header
            </el-header>
            <el-main>
                <!-- <Home /> -->
                <HelloWorld />
            </el-main>
        </el-container>
        <el-backtop target=""></el-backtop>
    </el-container>
</template>

<script>
import { defineAsyncComponent } from '@vue/runtime-core'
export default {
    name: "Admin",
    components: {
        LeftNav:  defineAsyncComponent(() => import('@/components/LeftNav.vue')),
        // Home: defineAsyncComponent(() => import('@/views/user/Home/Home.vue')),
        HelloWorld: defineAsyncComponent(() => import('@/components/HelloWorld.vue'))
    },
    props: {
    },
    setup() {
        
    },
    data() {
        return {
            IsShow: false
        }
    }
}
</script>