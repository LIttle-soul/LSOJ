<template>
    <div class="team-registration">
        <el-form>
            <el-form-item label="团队名称">
                <el-input></el-input>
            </el-form-item>
            <el-form-item label="团队介绍">
                <el-input></el-input>
            </el-form-item>
            <el-form-item label="成员1">
                <el-input></el-input>
            </el-form-item>
            <el-form-item label="成员2">
                <el-input></el-input>
            </el-form-item>
            <el-form-item label="成员3">
                <el-input></el-input>
            </el-form-item>
            <el-form-item label="指导老师">
                <el-input></el-input>
            </el-form-item>
        </el-form>
    </div>
</template>

<script>
export default {
    data() {
        return {
            teamData: {
                team_title: '',
                team_introduce: '',
                team_school: '',
                team_user1: '',
                team_user2: '',
                team_user3: '',
                team_teacher: '',
                team_type: ''
            }
        }
    }
}
</script>