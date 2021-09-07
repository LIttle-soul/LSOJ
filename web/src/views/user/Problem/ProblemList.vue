<template>
    <div class="problem-list">
        <div class="problem-left">
            <!-- <template #default> -->
                <problem-list />
            <!-- </template>
            <template #fallback>
                Loading...
            </template> -->
        </div>
        <div class="problem-right">
            <problem-nav />
        </div>
    </div>
</template>

<script>
import { defineAsyncComponent } from '@vue/runtime-core'

export default {
    components: {
        ProblemList: defineAsyncComponent(() => import('@/components/Problem/ProblemList.vue')),
        ProblemNav: defineAsyncComponent(() => import('@/components/Problem/ProblemNav.vue'))
    },
    beforeCreate() {
        this.$store.dispatch('problem/getProblemDataList');
    },
}
</script>

<style scoped>
.problem-list {
    width: 85%;
    max-width: 1400px;
    margin: 70px auto;
    position: relative;
}
.problem-left {
    width: 80%;
    float: left;
}
.problem-right {
    width: 18%;
    float: left;
    margin-left: 2%;
}
@media screen and (max-width: 1000px) {
    .problem-list {
      width: 100%;
    }
  }
@media screen and (max-width: 800px) {
    .problem-right {
      display: none;
    }
    .problem-left {
        width: 100%;
    }
  }
</style>