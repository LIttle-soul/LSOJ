import http from "@/utils/http";

export const getForumList = (data: any) => {
  return http({
    url: "/api/forum/getforumlist/",
    method: "get",
    params: data,
  }).then((res: any) => {
    console.log(res.data);
    return res.data;
  });
};

export const getReplyPage = (data: any) => {
  return http({
    url: "/api/forum/getreplypage/",
    method: "get",
    params: data,
  }).then((res: any) => {
    // console.log(res.data);
    return res.data;
  });
};

export const createForum = (data: any) => {
  return http({
    url: "/api/forum/createforum/",
    method: "post",
    data: data,
  }).then((res: any) => {
    // console.log(res.data);
    return res.data;
  });
};

export const putForum = (data: any) => {
  return http({
    url: "/api/forum/createforum/",
    method: "put",
    params: data,
  }).then((res: any) => {
    // console.log(res.data);
    return res.data;
  });
};

export const createReply = (data: any) => {
  return http({
    url: "/api/forum/addreply/",
    method: "post",
    data: data,
  }).then((res: any) => {
    // console.log(res.data);
    return res.data;
  });
};

export const setForumData = (data: any) => {
  return http({
    url: "/api/forum/setforumdata/",
    method: "put",
    params: data,
  }).then((res: any) => {
    // console.log(res.data);
    return res.data;
  });
};

export const deleteForum = (data: any) => {
  return http({
    url: "/api/forum/deleteforum/",
    method: "delete",
    params: data,
  }).then((res: any) => {
    // console.log(res.data);
    return res.data;
  });
};

export const deleteReply = (data: any) => {
  return http({
    url: "/api/forum/deletereply/",
    method: "delete",
    params: data,
  }).then((res: any) => {
    // console.log(res.data);
    return res.data;
  });
};

export const upForum = (data: any) => {
  return http({
    url: "/api/forum/forumtop/",
    method: "put",
    params: data,
  }).then((res: any) => {
    // console.log(res.data);
    return res.data;
  });
};

export const upReply = (data: any) => {
  return http({
    url: "/api/forum/replytop/",
    method: "put",
    params: data,
  }).then((res: any) => {
    // console.log(res.data);
    return res.data;
  });
};

export const putForumStatus = (data: any) => {
  return http({
    url: "/api/forum/forumstatus/",
    method: "put",
    params: data,
  }).then((res: any) => {
    // console.log(res.data);
    return res.data;
  });
};

export const getWord = (data: any) => {
  return http({
    url: "/api/forum/addword/",
    method: "get",
    params: data,
  }).then((res: any) => {
    console.log(res.data);
    return res.data;
  });
};

export const upWord = (data: any) => {
  return http({
    url: "/api/forum/addword/",
    method: "post",
    data: data,
  }).then((res: any) => {
    console.log(res.data);
    return res.data;
  });
};

export const deleteWord = (data: any) => {
  return http({
    url: "/api/forum/deleteword/",
    method: "delete",
    params: data,
  }).then((res: any) => {
    console.log(res.data);
    return res.data;
  });
};
