import http from "@/utils/http";

export const getSchoolList = (data) => {
  return http({
    url: "/api/school/getschool/",
    method: "get",
    params: {
      municipality_id: data,
    },
  }).then((res) => {
    // console.log(res);
    return res.data;
  });
};
