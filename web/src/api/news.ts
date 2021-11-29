import http from "@/utils/http";

/**
 * Get News List
 * @param {Number} page - Current page
 * @param {Number} total - Current page total
 * @param {String} text - The search text
 * @param {Number} news_id - Get a news data
 */
interface newsListData {
  page: number;
  total: number;
  text: string;
  news_id: number;
}
export const getNewsList = (data: newsListData) => {
  return http({
    url: "/api/news/getnewslist/",
    method: "get",
    params: data,
  }).then((res: any) => {
    return res.data;
  });
};

/**
 * Submit news data
 * @param {String} news_title - the news title
 * @param {String} news_introduce - the news introduce
 * @param {String} news_type - The news Type
 * @param {Number} news_importance - The news importance
 */
interface newsData {
  news_title: string;
  news_introduce: string;
  news_type: string;
  news_importance: number;
}
export const submitNewsData = (data: newsData) => {
  return http({
    url: "/api/news/addnews/",
    method: "post",
    data: data,
  }).then((res: any) => {
    return res.data;
  });
};

/**
 * Change news data
 * @param {String} news_id - the news ID
 * @param {String} news_title - the news title
 * @param {String} news_introduce - the news introduce
 * @param {String} news_type - The news Type
 * @param {Number} news_importance - The news importance
 */
interface newsDatabyChange {
  news_id: number;
  news_title: string;
  news_introduce: string;
  news_type: string;
  news_importance: number;
}
export const changeNewsData = (data: newsDatabyChange) => {
  return http({
    url: "/api/news/addnews/",
    method: "put",
    params: data,
  }).then((res: any) => {
    return res.data;
  });
};

/**
 * Delete news data
 * @param {String} news_id - the news ID
 */
export const deleteNewsData = (data: { news_id: number }) => {
  return http({
    url: "/api/news/addnews/",
    method: "delete",
    params: data,
  }).then((res: any) => {
    return res.data;
  });
};
