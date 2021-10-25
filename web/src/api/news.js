import http from "@/utils/http";

export const getNewsList = () => {
  return http({
    url: "/api/news/getnewslist/",
    method: "get",
  }).then((res) => {
    // console.log(res.data);
    return res.data;
  });
};

export const submitNewsData = (data) => {
  return http({
    url: "/api/news/addnews/",
    method: "post",
    data: {
      news_title: data.news_title,
      news_introduce: data.news_content,
      news_type: data.news_type,
      news_importance: data.news_importance,
    },
  }).then((res) => {
    // console.log(res.data);
    return res.data;
  });
};

export const changeNewsData = (data) => {
  console.log(data);
  return http({
    url: "/api/news/addnews/",
    method: "put",
    params: {
      news_id: data.news_id,
      news_title: data.news_title,
      news_introduce: data.news_content,
      news_type: data.news_type,
      news_importance: data.news_importance,
    },
  }).then((res) => {
    // console.log(res.data);
    return res.data;
  });
};

export const deleteNewsData = (data) => {
  return http({
    url: "/api/news/addnews/",
    method: "delete",
    params: {
      news_id: data,
    },
  }).then((res) => {
    // console.log(res.data);
    return res.data;
  });
};
