import http from "@/utils/http";

/**
 * get Rank List
 * @param page - Current page
 * @param total - The request data total
 * @param sort_by - [year, month, week, day]
 * @param text - The search keyword
 * @returns Response
 */
interface rankData {
  page: number;
  total: number;
  sort_by: string;
  text: string;
}
export const getRankList = (data: rankData) => {
  return http({
    url: "/api/user/getranklist/",
    methods: "get",
    params: data,
  }).then((res: any) => {
    return res.data;
  });
};
