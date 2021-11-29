import http from "@/utils/http";

/**
 * Get Address Info
 * @author LiSoul
 * @param {String} father - [province, municipality, area, township, village]
 * @param {Number} father_id - The father's id
 * @param {String} child - [province, municipality, area, township, village]
 * @param {Number} page - The begin of request id
 * @param {Number} total - The total of request number
 * @returns {Array} - The callback list
 * @example
 * let data = await getAddressInfo({
 *  father: "province",
 *  father_id: 0,
 *  child: "city",
 *  page: 0,
 *  total: 0
 * })
 */
interface requestData {
  father: string;
  father_id: string;
  child: string;
  page: number;
  total: number;
}
export const getAddressList = (data: requestData) => {
  return http({
    url: "/api/address/getaddressmessage/",
    method: "get",
    params: data,
  }).then((res: any) => {
    return res.data;
  });
};
