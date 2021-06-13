<template>
<div>
    <el-header>
        <Header></Header>
    </el-header>
    <el-main>
        <ul 
        class="infinite-list" 
        v-infinite-scroll="load" 
        style="overflow:auto">
            <li 
            v-for="i in count" 
            :key="i" 
            class="infinite-list-item">
                {{ i }}
            </li>
        </ul>
    </el-main>
    <el-footer>
        Footer
    </el-footer>
</div>
</template>

<script>
// import Header from './Header/Header.vue'

export default {
    components: {
        // Header
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