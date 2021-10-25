<template>
    <div class="code-header">
        <el-select
        v-model="temp_language"
        size="mini"
        @change="changeLanguage">
            <el-option
            v-for="item in language"
            :key="item.value"
            :label="item.text"
            :value="item"></el-option>
        </el-select>
    </div>
</template>

<script>
import { mapState } from 'vuex'
export default {
    computed: {
        ...mapState('code', {
            language: state => state.filter_language_data
        })
    },
    data() {
        return {
            temp_language: {value: 0, text: 'C', code: "c"}
        }
    },
    methods: {
        changeLanguage(val) {
            // console.log(val, text);
            this.$emit('changeLanguage', val);
        } 
    }
}
</script>

<style scoped>
.code-header {
    width: 100%;
    height: 100%;
    position: relative;
}
.el-select {
    float: left;
    max-width: 120px;
    height: 25px;
    position: absolute;
    left: 10px;
    top: 8px;
}
</style>