
<template>
    <el-menu
        default-active="UserList"
        :unique-opened="true"
        class="el-menu-vertical-demo"
        :collapse="isCollapse"
    >
        <el-submenu v-for="item in nav_menu" :key="item.key" :index="item.key">
            <template #title>
                <i :class="item.icon"></i>
                <span>{{item.title}}</span>
            </template>
            <el-menu-item v-for="data in item.data" :key="data.index" :index="data.index">{{data.title}}</el-menu-item>
        </el-submenu>
    </el-menu>
</template>
    
    <script>

export default {
    props: {
        isCollapse: {
            type: Boolean,
            default: true
        }
    },
    data() {
        return {
            nav_menu: [
                {
                    'title': '用户管理',
                    'key': 'User',
                    'icon': 'el-icon-user-solid',
                    'data': [
                        {
                            'title': '用户列表',
                            'index': 'UserList'
                        }
                    ]
                },
                {
                    'title': '问题管理',
                    'key': 'Problem',
                    'icon': 'el-icon-question',
                    'data': [
                        {
                            'title': '问题列表',
                            'index': 'ProblemList'
                        },
                        {
                            'title': '问题管理',
                            'index': 'ProblemCon'
                        },
                        {
                            'title': '问题添加',
                            'index': 'AddProblem'
                        }
                    ]
                },
                {
                    'title': '竞赛管理',
                    'key': 'Contest',
                    'icon': 'el-icon-s-order',
                    'data': [
                        {
                            
                        }
                    ]
                },
                {
                    'title': '学校管理',
                    'key': 'school',
                    'icon': 'el-icon-school',
                    'data': [
                        {
                            'title': '学校添加',
                            'index': 'AddSchool'
                        }
                    ]
                },
                {
                    'title': '班级管理',
                    'key': 'class',
                    'icon': 'el-icon-s-management',
                    'data': [
                        {
                            
                        }
                    ]
                },
                {
                    'title': '判题机管理',
                    'key': 'Judger',
                    'icon': 'el-icon-s-flag',
                    'data': [
                        {
                            
                        }
                    ]
                }
            ]
        };
    },
    methods: {
    }
}

</script>
    
    <style>
.el-menu-vertical-demo:not(.el-menu--collapse) {
    width: 200px;
    height: 100%;
    background-color: aliceblue;
}
</style>
    