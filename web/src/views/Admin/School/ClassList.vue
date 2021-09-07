<template>
    <div class="user-list">
        <div class="echart">
            <!-- 此处用于添加图表信息 -->
        </div>
        <div class="list">
            <UserList />
        </div>
    </div>
</template>

<script>
import UserList from '@/components/User/UserList.vue'

export default {
  components: {
      UserList: UserList
  },
    
}
</script>

<style scoped>
.user-list {
    width: 95%;
    max-width: 1200px;
    margin: 70px auto;
}
@media screen and (max-width: 1000px){
    .user-list {
        width: 100%;
    }
}
</style>