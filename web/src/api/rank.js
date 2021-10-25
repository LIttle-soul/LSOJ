import http from "@/utils/http";

// 获取排名列表
export const getRankList = (data) => {
  return http({
    url: "/api/user/getranklist/",
    methods: "get",
    params: {
      sort_by: data,
    },
  }).then((res) => {
    // console.log(res.data);
    return res.data;
  });
};
