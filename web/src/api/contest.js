import http from "@/utils/http";

export const getContestList = () => {
  return http({
    url: "/api/contest/contestlist/",
    method: "get",
  }).then((res) => {
    return res.data;
  });
};

/**
 * 添加竞赛数据
 * @param {*} data {
 *  contest_title
 *  start_time
 *  end_time
 *  problem_id
 *  contest_language
 *  contest_introduce
 *  contest_province
 *  contest_password
 *  contest_status
 * }
 * @returns
 */
export const submitContestData = (data) => {
  return http({
    url: "/api/contest/contestlist/",
    method: "post",
    data: {
      contest_title: data.contest_title,
      start_time: data.start_time,
      end_time: data.end_time,
      problem_id: data.contest_problem,
      contest_language: data.contest_language,
      contest_introduce: data.contest_content,
      contest_province: data.contest_type,
      contest_password: data.contest_password,
      contest_status: data.contest_status,
    },
  }).then((res) => {
    console.log(res.data);
    return res.data;
  });
};

/**
 * 修改竞赛数据
 * contest_id
 * contest_title
 * start_time
 * end_time
 * contest_language
 * contest_introduce
 * contest_province
 * contest_password
 * contest_status
 */
export const changeContestData = (data) => {
  return http({
    url: "/api/contest/contestlist/",
    method: "put",
    params: {
      contest_id: data.contest_id,
      contest_title: data.contest_title,
      start_time: data.start_time,
      end_time: data.end_time,
      contest_language:
        data.contest_language === undefined
          ? data.contest_language
          : data.contest_language.join(","),
      contest_introduce: data.contest_content,
      contest_province: data.contest_type,
      contest_password: data.contest_password,
      contest_status: data.contest_status,
    },
  }).then((res) => {
    console.log(res.data);
    return res.data;
  });
};
/**
 * 删除竞赛数据
 * contest_id
 */
export const deleteContestData = (contest_id) => {
  return http({
    url: "/api/contest/contestlist/",
    method: "delete",
    params: {
      contest_id: contest_id,
    },
  }).then((res) => {
    console.log(res.data);
    return res.data;
  });
};

export const joinContestByUser = (data) => {
  return http({
    url: "/api/contest/singleSignUp/",
    method: "post",
    data: {
      contest_id: data.contest_id,
    },
  }).then((res) => {
    // console.log(res.data);
    return res.data;
  });
};

/**
 * 获取竞赛问题
 * contest_id
 */
export const getContestProblem = (data) => {
  return http({
    url: "/api/contest/contestproblemlist/",
    method: "get",
    params: data,
  }).then((res) => {
    // console.log(res.data);
    return res.data;
  });
};

/**
 * 修改竞赛问题列表里
 * contest_id
 * problem_list
 */
export const changeProblemList = (data) => {
  return http({
    url: "/api/contest/contestproblemlist/",
    method: "put",
    params: data,
  }).then((res) => {
    return res.data;
  });
};

/**
 * 添加竞赛问题
 * contest_id
 * problem_id
 */
export const addProblem = (data) => {
  return http({
    url: "/api/contest/contestproblemlist/",
    method: "post",
    data: data,
  }).then((res) => {
    return res.data;
  });
};

/**
 * 删除竞赛问题
 * contest_id
 * problem_id
 */
export const deleteProblem = (data) => {
  return http({
    url: "/api/contest/contestproblemlist/",
    method: "delete",
    params: data,
  }).then((res) => {
    return res.data;
  });
};

/**
 * 获取竞赛用户
 * contest_id
 */
export const getContestUser = (data) => {
  return http({
    url: "/api/contest/contestuserlist/",
    method: "get",
    params: data,
  }).then((res) => {
    return res.data;
  });
};

/**
 * 同意竞赛用户
 * contest_id
 * user_id
 */
export const agreeContestUser = (data) => {
  return http({
    url: "/api/contest/contestuserlist/",
    method: "put",
    params: data,
  }).then((res) => {
    return res.data;
  });
};

/**
 * 添加竞赛用户
 * contest_id
 * user_list
 */
export const addContestUser = (data) => {
  return http({
    url: "/api/contest/contestuserlist/",
    method: "post",
    data: data,
  }).then((res) => {
    return res.data;
  });
};

/**
 * 删除竞赛用户
 * contest_id
 * user_id
 */
export const deleteContestUser = (data) => {
  return http({
    url: "/api/contest/contestuserlist/",
    method: "delete",
    params: data,
  }).then((res) => {
    return res.data;
  });
};

/**
 * 获取竞赛状态
 * contest_id
 */
export const getContestSolution = (data) => {
  return http({
    url: "/api/solution/statussubmit/",
    method: "get",
    params: data,
  }).then((res) => {
    // console.log(res.data);
    return res.data;
  });
};

/**
 * 获取竞赛排名数据
 * contest_id
 */
export const getContestRank = (data) => {
  return http({
    url: "/api/contest/ranklist/",
    method: "get",
    params: data,
  }).then((res) => {
    // console.log(res.data);
    return res.data;
  });
};

/**
 * 获取竞赛统计信息
 * contest_id
 */
export const getContestCount = (data) => {
  return http({
    url: "/api/contest/conteststats/",
    method: "get",
    params: data,
  }).then((res) => {
    return res.data;
  });
};

export const refurbishContestRank = (data) => {
  /**
   * 刷新竞赛排名
   * contest_id
   */
  return http({
    url: "/api/contest/contestrank/",
    method: "get",
    params: data,
  }).then((res) => {
    return res.data;
  });
};

/**
 * 我的比赛
 */
export const getMyContest = () => {
  return http({
    url: "/api/user/mycontest/",
    method: "get",
  }).then((res) => {
    return res.data;
  });
};

// export const joinContestByTeam = (data) => {
//   return http({
//     url: "/api/contest/",
//     method: "",
//     params: {},
//   }).then((res) => {
//     console.log(res.data);
//     return res.data;
//   });
// };

// export const joinContestByPassword = (data) => {
//   return http({
//     url: "/api/contest/",
//     method: "",
//     params: {},
//   }).then((res) => {
//     console.log(res.data);
//     return res.data;
//   });
// };
