import http from "@/utils/http";

/**
 * Get Home Count Data
 */

export const getCountData = () => {
  return http({
    url: "/api/user/countmessage/",
    method: "get",
  }).then((res: any) => {
    return res.data;
  });
};
