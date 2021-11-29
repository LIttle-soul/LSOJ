import http from "@/utils/http";

/**
 * Get Contest List Data
 * @param {Number} page - Current Page
 * @param {Number} total - The total of data size
 * @param {String} status - [search, status]
 * @param {String} text - The search content
 * @param {Number} contest_id - Get a contest data
 * @param {String} me - Get self's contest list [True, ""]
 * @param {String} time - Get the havn't end contest [True, ""]
 */

interface ContestData {
  page: number;
  total: number;
  status: string;
  text: string;
  contest_id: number;
  me: string;
  time: string;
}

export const getContestList = (data: ContestData) => {
  return http({
    url: "/api/contest/contestlist/",
    method: "get",
    params: data,
  }).then((res: any) => {
    return res.data;
  });
};

/**
 * Get contest problem
 * @param {Number} page - Current page
 * @param {Number} total - Page size
 * @param {Number} contest_id - Current contest
 * @param {Number} text - the search text
 */
interface contestProblemData {
  page: number;
  total: number;
  contest_id: number;
  text: string;
}
export const getContestProblem = (data: contestProblemData) => {
  return http({
    url: "/api/contest/contestproblemlist/",
    method: "get",
    params: data,
  }).then((res: any) => {
    return res.data;
  });
};

/**
 * Get contest rank data
 * @param {Number} page - Current page
 * @param {Number} total - Page size
 * @param {Number} contest_id - Current contest
 */
interface contestRankData {
  page: number;
  total: number;
  contest_id: number;
}
export const getContestRank = (data: contestRankData) => {
  return http({
    url: "/api/contest/ranklist/",
    method: "get",
    params: data,
  }).then((res: any) => {
    return res.data;
  });
};

/**
 * Get contest count data
 * @param {Number} page - Current page
 * @param {Number} total - Page size
 * @param {Number} contest_id - Current contest
 */
interface contestCountData {
  page: number;
  total: number;
  contest_id: number;
}
export const getContestCount = (data: contestCountData) => {
  return http({
    url: "/api/contest/conteststats/",
    method: "get",
    params: data,
  }).then((res: any) => {
    return res.data;
  });
};

/**
 * Add contest data
 *  @param {String} contest_title
 *  @param {String} start_time
 *  @param {String} end_time
 *  @param {String} problem_id
 *  @param {String} contest_language
 *  @param {String} contest_introduce
 *  @param {String} contest_province
 *  @param {String} contest_password
 *  @param {String} contest_status
 */
interface contestData {
  contest_title: string;
  start_time: string;
  end_time: string;
  problem_id: string;
  contest_language: string;
  contest_introduce: string;
  contest_province: number;
  contest_password: string;
  contest_status: number;
}
export const submitContestData = (data: any) => {
  return http({
    url: "/api/contest/contestlist/",
    method: "post",
    data: data,
  }).then((res: any) => {
    return res.data;
  });
};

/**
 * Change contest Data
 * @param {String} contest_id
 * @param {String} contest_title
 * @param {String} start_time
 * @param {String} end_time
 * @param {String} contest_language
 * @param {String} contest_introduce
 * @param {String} contest_province
 * @param {String} contest_password
 * @param {String} contest_status
 */
interface contestDataByChange {
  contest_id: number;
  contest_title: string;
  start_time: string;
  end_time: string;
  contest_language: string;
  contest_introduce: string;
  contest_province: number;
  contest_password: string;
  contest_status: number;
}
export const changeContestData = (data: any) => {
  return http({
    url: "/api/contest/contestlist/",
    method: "put",
    params: data,
  }).then((res: any) => {
    return res.data;
  });
};

/**
 * Delete contest data
 * @param {Number} contest_id
 */
export const deleteContestData = (data: { contest_id: number }) => {
  return http({
    url: "/api/contest/contestlist/",
    method: "delete",
    params: data,
  }).then((res: any) => {
    return res.data;
  });
};

/**
 * Change contest problem list
 * @param {Number} contest_id - Current contest
 * @param {String} problem_list - The new problem list
 */
export const changeProblemList = (data: {
  contest_id: number;
  problem_list: string;
}) => {
  return http({
    url: "/api/contest/contestproblemlist/",
    method: "put",
    params: data,
  }).then((res: any) => {
    return res.data;
  });
};

/**
 * Add contest problem
 * @param {Number} contest_id - Current contest
 * @param {Number} problem_id - The will add problem ID
 */
export const addProblem = (data: {
  contest_id: number;
  problem_id: number;
}) => {
  return http({
    url: "/api/contest/contestproblemlist/",
    method: "post",
    data: data,
  }).then((res: any) => {
    return res.data;
  });
};

/**
 * Delete contest problem
 * @param {Number} contest_id - Current contest
 * @param {Number} problem_id - The will delete problem ID
 */
export const deleteProblem = (data: {
  contest_id: number;
  problem_id: number;
}) => {
  return http({
    url: "/api/contest/contestproblemlist/",
    method: "delete",
    params: data,
  }).then((res: any) => {
    return res.data;
  });
};

/**
 * Get Contest User list
 * @param {Number} page - Current page
 * @param {Number} total - Current page's size
 * @param {Number} contest_id - Current contest
 * @param {String} text - The search text
 */
export const getContestUser = (data: {
  page: number;
  total: number;
  contest_id: number;
  text: string;
}) => {
  return http({
    url: "/api/contest/contestuserlist/",
    method: "get",
    params: data,
  }).then((res: any) => {
    return res.data;
  });
};

/**
 * 同意竞赛用户
 * contest_id
 * user_id
 */
export const agreeContestUser = (data: any) => {
  return http({
    url: "/api/contest/contestuserlist/",
    method: "put",
    params: data,
  }).then((res: any) => {
    return res.data;
  });
};

/**
 * 添加竞赛用户
 * contest_id
 * user_list
 */
export const addContestUser = (data: any) => {
  return http({
    url: "/api/contest/contestuserlist/",
    method: "post",
    data: data,
  }).then((res: any) => {
    return res.data;
  });
};

/**
 * 删除竞赛用户
 * contest_id
 * user_id
 */
export const deleteContestUser = (data: any) => {
  return http({
    url: "/api/contest/contestuserlist/",
    method: "delete",
    params: data,
  }).then((res: any) => {
    return res.data;
  });
};

export const refurbishContestRank = (data: any) => {
  /**
   * 刷新竞赛排名
   * contest_id
   */
  return http({
    url: "/api/contest/contestrank/",
    method: "get",
    params: data,
  }).then((res: any) => {
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
  }).then((res: any) => {
    return res.data;
  });
};

/**
 * Join contest by user
 * @param {Number} contest_id - Current contest ID
 */
export const joinContestByUser = (data: { contest_id: number }) => {
  return http({
    url: "/api/contest/singleSignUp/",
    method: "post",
    data: data,
  }).then((res: any) => {
    return res.data;
  });
};

/**
 * Join contest by team
 * @param {Number} contest_id - Current contest ID
 * @param {Number} team_id - My team id
 */
export const joinContestByTeam = (data: {
  contest_id: number;
  team_id: number;
}) => {
  return http({
    url: "/api/contest/teamSignUp/",
    method: "post",
    data: data,
  }).then((res: any) => {
    return res.data;
  });
};

/**
 * Join contest by password
 * @param {Number} contest_id - Current contest ID
 * @param {Number} password - My team id
 */
export const joinContestByPassword = (data: {
  contest_id: number;
  password: string;
}) => {
  return http({
    url: "/api/contest/signUp/",
    method: "post",
    data: data,
  }).then((res: any) => {
    return res.data;
  });
};
