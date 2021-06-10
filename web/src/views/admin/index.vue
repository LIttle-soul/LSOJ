<template>
    <div class='admin'>
        <el-container>
            <el-aside class="aside" @open="handleOpen" @close="handleClose" :collapse="isCollapse">
                <el-menu default-active="1" class="el-menu-vertical-demo">
                    <el-submenu index="1">
                        <template #title>
                            <i class="el-icon-location"></i>
                            <span>导航一</span>
                        </template>
                        <el-menu-item-group>
                            <template #title>分组一</template>
                            <el-menu-item index="1-1">选项1</el-menu-item>
                            <el-menu-item index="1-2">选项2</el-menu-item>
                        </el-menu-item-group>
                         <el-menu-item-group title="分组2">
                            <el-menu-item index="1-3">选项3</el-menu-item>
                        </el-menu-item-group>
                        <el-submenu index="1-4">
                            <template #title>选项4</template>
                            <el-menu-item index="1-4-1">选项1</el-menu-item>
                        </el-submenu>
                    </el-submenu>
                    <el-menu-item index="2">
                        <i class="el-icon-menu"></i>
                            <template #title>导航二</template>
                    </el-menu-item>
                    <el-menu-item index="3" disabled>
                        <i class="el-icon-document"></i>
                        <template #title>导航三</template>
                    </el-menu-item>
                    <el-menu-item index="4">
                        <i class="el-icon-setting"></i>
                        <template #title>导航四</template>
                    </el-menu-item>
                </el-menu>
            </el-aside>
            <el-container>
                <el-header height="60px">
                    <el-radio-group v-model="isCollapse">
                        <el-radio-button :label="false">展开</el-radio-button>
                        <el-radio-button :label="true">收起</el-radio-button>
                    </el-radio-group>
                    <el-row type="flex" justify="end">
                        <el-col :xs="0" :sm="0" :md="6" :lg="4" :xl="2">
                            <el-input placeholder="请输入内容" v-model="input" size="mini">
                                <template #append>
                                    <el-button icon="el-icon-search"></el-button>
                                </template>
                            </el-input>
                        </el-col>
                        <el-col :xs="1" :sm="1" :md="1" :lg="1" :xl="1" class="tag_header">
                            2
                        </el-col>
                    </el-row>
                </el-header>
                <el-main>
                    content
                </el-main>
                <el-footer height="40px">
                    footer
                </el-footer>
            </el-container>
        </el-container>
    </div>
</template>

<script>
export default {
    name: 'Admin',
    setup() {
        
    },
    data() {
        return {
            isCollapse: true,
        }
    },
    methods: {
        handleOpen(key, keyPath) {
            console.log(key, keyPath);
        },
        handleClose(key, keyPath) {
            console.log(key, keyPath);
        }
    },
}
</script>

<style scoped>
.el-header, .el-footer {
    background-color: blanchedalmond;
}
.el-aside {
    background-color: aquamarine;
}
.tag_header {
    text-align: right;
}
.el-menu-vertical-demo:not(.el-menu--collapse) {
    width: 200px;
    min-height: 400px;
  }
</style>