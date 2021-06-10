<template>
    <div class="layui-row layui-col-space5">
        <div class="layui-col-md5">
            <div class="layui-row grid-demo">
                <div class="layui-col-md3">
                    内部列
                </div>
                <div class="layui-col-md9">
                    内部列
                </div>
                <div class="layui-col-md12">
                    内部列
                </div>
            </div>
        </div>
        <div class="layui-col-md7">
            <div class="layui-row grid-demo grid-demo-bg1">
                <div class="layui-col-md12">
                    内部列
                </div>
                <div class="layui-col-md9">
                    内部列
                </div>
                <div class="layui-col-md3">
                    内部列
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "Nav",
    data() {
        return {
            nav_list: [],
        }
    }
}
</script>

<style scoped>
.grid-demo {
    background: #663355;
}
</style>