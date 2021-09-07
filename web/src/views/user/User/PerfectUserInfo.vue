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
            :readonly="!activate"
            placeholder="成功完善生日信息有惊喜哦"
          >
          </el-date-picker>
        </el-form-item>
        <el-form-item label="我的地址">
          <el-cascader
            @change="getSchoolList"
            placeholder="别怕，这是你学校的地址"
            v-model="user_form.user_address"
            :props="city_list"
            :filterable="false"
            :clearable="true"
          >
          </el-cascader>
        </el-form-item>
        <el-form-item label="我的学校">
          <el-cascader
            placeholder="地址可缩小学校范围哦"
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
export default {
  data() {
    let self = this;
    return {
      form_title: "基础信息完善",
      activate: false,
      school_status: true,
      city_list: {
        lazy: true,
        lazyLoad(node, resolve) {
          // console.log(node, resolve);
          const { level, value } = node;
          setTimeout(() => {
            if(level == 0) {
              self.getProvinceList().then((res) => {
                // console.log(res);
                resolve(res);
              });
            } else if(level == 1) {
              self.getMunicipalityList(value).then((res) => {
                resolve(res);
              });
            } else {
              resolve([]);
            }
          }, 100);
        }
      },
      school_list: [
      ],
      class_list: [
      ],
      user_form: {
        user_name: '',
        user_nick: '',
        user_introduce: '',
        user_telephone: '',
        user_birthday: "2000-01-01",
        user_school: '',
        user_class: '',
        user_address: '',
        user_sex: 0,
      },
    };
  },
  mounted() {
    this.InputUserInfo();
    this.getSchoolList();
  },
  methods: {
    InputUserInfo() {
      this.$http({
        url: "/api/user/perfectinfo/",
        methods: "get",
        params: {
          token: this.$cookies.get("token"),
        },
      }).then((res) => {
        // console.log(res.data);
        if (res.data.status) {
          this.user_form.user_name = res.data.data.user_name;
          this.user_form.user_nick = res.data.data.user_nick;
          this.user_form.user_introduce = res.data.data.user_introduce;
          this.user_form.user_telephone = res.data.data.user_telephone;
          this.user_form.user_birthday = this.$dayJS(res.data.data.user_birthday).format('YYYY-MM-DD');
          this.user_form.user_school = res.data.data.user_school.school_id;
          this.user_form.user_class = res.data.data.user_class;
          let user_address = res.data.data.user_address.municipality_id;
          this.user_form.user_sex = res.data.data.user_sex;
          this.user_form.user_address = [Math.floor(user_address/100), user_address];
          this.activate = true;
          this.form_title = "基础信息修改";
        }
      });
    },
    onSubmit() {
      let address = this.user_form.user_address;
      address = address?address[1]:null;
      let school = this.user_form.user_school
      school = school?school[0]:null
      this.$http({
        url: "/api/user/perfectinfo/",
        method: "post",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        transformRequest: [
          function(data) {
            let ret = "";
            for (let it in data) {
              ret +=
                encodeURIComponent(it) +
                "=" +
                encodeURIComponent(data[it]) +
                "&";
            }
            return ret;
          },
        ],
        params: {},
        data: {
          token: this.$cookies.get("token"),
          user_name: this.user_form.user_name,
          user_nick: this.user_form.user_nick,
          user_introduce: this.user_form.user_introduce,
          user_telephone: this.user_form.user_telephone,
          user_birthday: this.user_form.user_birthday,
          user_school: school,
          user_class: this.user_form.user_class,
          user_address: address,
          user_sex: this.user_form.user_sex,
        },
      }).then((res) => {
        // console.log('res=>', res.data);
        alert(res.data.err);
      });
    },
    getProvinceList() {
      return this.$http({
        url: "/api/address/getprovince/",
        methods: "get",
        params: {
        },
      }).then((res) => {
        // console.log(res.data.data);
        return res.data.data.map(item => ({
          value: item.province_id,
          label: item.province_name
        }));
      });
    },
    getMunicipalityList(province_id) {
      return this.$http({
        url: "/api/address/getmunicipality/",
        methods: "get",
        params: {
          province_id: province_id
        },
      }).then((res) => {
        // console.log(res.data.data);
        return res.data.data.map(item => ({
          value: item.municipality_id,
          label: item.municipality_name,
          leaf: true
        }));
      });
    },
    getSchoolList() {
      let value = this.user_form.user_address;
      this.$http({
        url: "/api/school/getschool/",
        methods: "get",
        params: {
          municipality_id: value?value[1]:null
        },
      }).then((res) => {
        // console.log(res.data.data);
        this.school_list = res.data.data.map(item => ({
          value: item.school_id,
          label: item.school_name
        }));
      });
    }
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
