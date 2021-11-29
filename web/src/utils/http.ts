// axios 拦截器配置
import axios from "axios";

// 创建axios实例
const service = axios.create({
  // timeout: 10000,
  headers: {
    "Content-Type": "application/x-www-form-urlencoded",
    "Access-Control-Allow-Origin": "*",
  },
  transformRequest: [
    function (data) {
      let ret = "";
      for (let it in data) {
        ret +=
          encodeURIComponent(it) + "=" + encodeURIComponent(data[it]) + "&";
      }
      return ret;
    },
  ],
});

// 添加请求拦截器
service.interceptors.request.use(
  (config) => {
    return config;
  },
  (err) => {
    console.log(err);
  }
);

// 添加响应拦截器
interface responseData {
  status: number;
  data: any;
}

service.interceptors.response.use(
  (response) => {
    let res = <responseData>{};
    res.status = response.status;
    res.data = response.data;
    return res;
  },
  (err) => {
    console.log(err);
  }
);

export default service;
