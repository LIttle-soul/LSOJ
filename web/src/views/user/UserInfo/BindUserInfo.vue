<template>
  <el-card class="bind-user-info">
    <h1 style="margin-bottom: 20px;">
      <i class="el-icon-s-tools"></i>用户信息绑定
    </h1>
    <div>
      <UpLoadIcon class="user-icon" />
      <h1 class="user-icon">头像上传</h1>
    </div>
    <el-form ref="form" :model="UserSchoolForm">
      <el-form-item label="省份选择">
        <el-select
          v-model="UserSchoolForm.province"
          @change="getMunicipality"
          :filterable="true"
          :allow-create="true"
          placeholder="请选择"
        >
          <el-option
            v-for="item in DataList.province_list"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          >
          </el-option>
        </el-select>
      </el-form-item>

      <el-form-item label="城市选择">
        <el-select
          v-model="UserSchoolForm.municipality"
          @change="getSchool"
          :filterable="true"
          :allow-create="true"
          placeholder="请选择"
        >
          <el-option
            v-for="item in DataList.municipality_list"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          >
          </el-option>
        </el-select>
      </el-form-item>

      <el-form-item label="学校选择">
        <el-select
          v-model="UserSchoolForm.school"
          placeholder="请选择"
          :filterable="true"
          :allow-create="true"
        >
          <el-option
            v-for="item in DataList.school_list"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          >
          </el-option>
        </el-select>
      </el-form-item>
    </el-form>
    <el-form ref="form" :model="UserSchoolForm">
      <el-form-item label="省份选择">
        <el-select
          v-model="UserSchoolForm.province"
          @change="getMunicipality"
          :filterable="true"
          :allow-create="true"
          placeholder="请选择"
        >
          <el-option
            v-for="item in DataList.province_list"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          >
          </el-option>
        </el-select>
      </el-form-item>
    </el-form>
  </el-card>
</template>

<script>
import { defineAsyncComponent } from "vue";

export default {
  components: {
    UpLoadIcon: defineAsyncComponent(() =>
      import("@/components/IconUpLoad.vue")
    ),
  },
  mounted() {
      this.getProvince();
  },
  setup() {},
  data() {
    return {
        UserEmail: '',
      UserSchoolForm: {
        province: null,
        municipality: null,
        school: null,
      },
      DataList: {
        province_list: [
            {
          value: '选项1',
          label: '黄金糕'
        }, {
          value: '选项2',
          label: '双皮奶'
        }, {
          value: '选项3',
          label: '蚵仔煎'
        }, {
          value: '选项4',
          label: '龙须面'
        }, {
          value: '选项5',
          label: '北京烤鸭'
        }
        ],
        municipality_list: [],
        school_list: [],
      },
    };
  },
  methods: {
    getProvince() {
      this.$http({
        url: "/api/addprovince/",
        methods: "get",
        params: {},
      }).then((res) => {
        console.log(res.data);
      });
    },
    getMunicipality() {
      this.$http({
        url: "/api/addmunicipality/",
        methods: "get",
        params: {
          province: this.UserSchoolForm.province,
        },
      }).then((res) => {
        console.log(res.data);
      });
    },
    getSchool() {
      this.$http({
        url: "/api/addschool/",
        methods: "get",
        params: {
          province: this.UserSchoolForm.province,
          municipality: this.UserSchoolForm.municipality,
        },
      }).then((res) => {
        console.log(res.data);
      });
    },
  },
};
</script>

<style scoped>
.user-icon {
  text-align: center;
  font: 20px "楷体";
}
</style>
