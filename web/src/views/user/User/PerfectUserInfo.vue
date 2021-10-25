<template>
  <div class="perfect">
    <!-- 基础信息修改完善 -->
    <el-card class="box-card">
      <h1 style="margin-bottom: 20px;">
        <i class="el-icon-s-tools"></i> {{ form_title }}
      </h1>
      <el-form ref="form" :model="user_form" label-width="80px" size="mini">
        <el-form-item label="真实姓名">
          <el-input
            placeholder="好汉，留名不杀"
            v-model="user_form.user_name"
            :disabled="activate"
          ></el-input>
        </el-form-item>
        <el-form-item label="个人昵称">
          <el-input
            placeholder="有趣的灵魂总能相遇"
            v-model="user_form.user_nick"
          ></el-input>
        </el-form-item>
        <el-form-item label="我的性别">
          <el-radio-group
            v-model="user_form.user_sex"
            size="medium"
            :disabled="activate"
          >
            <el-radio :label="0">男</el-radio>
            <el-radio :label="1">女</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="我的介绍">
          <el-input
            placeholder="此站是我开，此框是我管，要想我知你，留下自荐信"
            class="input-width"
            type="textarea"
            v-model="user_form.user_introduce"
          ></el-input>
        </el-form-item>
        <el-form-item label="我的电话">
          <el-input
            placeholder="怕我找你？切！懒得理你"
            v-model="user_form.user_telephone"
          ></el-input>
        </el-form-item>
        <el-form-item label="我的生日">
          <el-date-picker
            v-model="user_form.user_birthday"
            type="date"
            size="small"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            placeholder="成功完善生日信息有惊喜哦"
          >
          </el-date-picker>
        </el-form-item>
        <el-form-item label="我的地址">
          <el-cascader
            placeholder="别怕，这是你学校的地址"
            v-model="user_form.user_address"
            :options="city_list"
            :filterable="true"
            :clearable="true"
          >
          </el-cascader>
        </el-form-item>
        <el-form-item label="我的学校">
          <el-cascader
            placeholder="想知道你的校友有谁吗？"
            v-model="user_form.user_school"
            :options="school_list"
            :filterable="true"
            :clearable="true"
          >
          </el-cascader>
        </el-form-item>
        <el-form-item label="我的班级">
          <el-cascader
            placeholder="想知道和你同班的有谁吗？"
            v-model="user_form.user_class"
            :disabled="user_form.user_school == ''"
            :options="class_list"
            :filterable="true"
            :clearable="true"
          >
          </el-cascader>
        </el-form-item>
        <el-form-item size="large">
          <el-button type="primary" @click="onSubmit">提交</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { mapState } from "vuex";
import { submitUserInfoForm } from "@/api/user";

export default {
  computed: {
    ...mapState("address", {
      city_list: (state) =>
        state.address_list.map((item) => ({
          value: item.id,
          label: item.name,
          children: item.children.map((item2) => ({
            value: item2.id,
            label: item2.name,
          })),
        })),
    }),
    ...mapState("school", {
      school_list: (state) =>
        state.school_list.map((item) => ({
          value: item.school_id,
          label: item.school_name,
        })),
    }),
    ...mapState("user", {
      user_info: (state) => state.user_info,
    }),
  },
  watch: {
    user_info() {
      this.inputUserInfo(this.user_info);
    },
  },
  mounted() {
    this.inputUserInfo(this.user_info);
  },
  data() {
    return {
      form_title: "基础信息完善",
      activate: false,
      school_status: true,
      class_list: [],
      user_form: {
        user_name: "",
        user_nick: "",
        user_introduce: "",
        user_telephone: "",
        user_birthday: "2000-01-01",
        user_school: null,
        user_class: "",
        user_address: null,
        user_sex: 0,
      },
    };
  },
  methods: {
    inputUserInfo(val) {
      if (val != null && val != undefined) {
        this.user_form = {
          user_name: val.user_name,
          user_nick: val.user_nick,
          user_introduce: val.user_introduce,
          user_telephone: val.user_telephone,
          user_birthday: this.$dayJS(val.user_birthday).format("YYYY-MM-DD"),
          user_school: val.user_school ? val.user_school.school_id : null,
          user_class: val.user_class,
          user_address: val.user_address
            ? [
                Math.floor(val.user_address.address_id / 100),
                val.user_address.address_id,
              ]
            : null,
          user_sex: val.user_sex,
        };
      }
    },
    async onSubmit() {
      let back_data = await submitUserInfoForm(this.user_form);
      // console.log(back_data);
      if (back_data.status) {
        this.$message({
          type: "success",
          message: back_data.message,
        });
        this.$store.dispatch("user/getUserInfo");
      } else {
        this.$message({
          type: "success",
          message: back_data.message,
        });
      }
    },
  },
};
</script>

<style scoped>
.perfect {
  max-width: 500px;
  min-width: 350px;
  margin: 0 auto;
}
.box-card {
  margin: 40px auto;
}
.box-card:last-child {
  margin-top: 20px;
}
.box-card .el-input {
  max-width: 300px;
}

.box-card .input-width {
  width: 300px;
}
</style>
