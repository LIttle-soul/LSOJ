import http from "@/utils/http";

export const getCourseList = () => {
  return http({
    url: "/api/course/viewallcourse/",
    method: "get",
  }).then((res: any) => {
    // console.log(res.data);
    return res.data;
  });
};
