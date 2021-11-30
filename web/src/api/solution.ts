import http from "@/utils/http";

/**
 * Get solution data list
 * @param {Number} page - Current page
 * @param {Number} total - A page size
 * @param {String} key - [solution_id, user, problem_id]
 * @param {String} text - The search text
 * @param {String} run_result - filter result data
 * @param {String} language - filter language data
 * @param {Number} contest_id - Get a contest's solution data list
 * @param {String} me - [True, False]
 */

interface solutionData {
  page: number;
  total: number;
  key: string;
  text: string;
  run_result: string;
  language: string;
  contest_id: number;
  me: string;
}

export const getSolutionDataList = (data: solutionData) => {
  return http({
    url: "/api/solution/statussubmit/",
    method: "get",
    params: data,
  }).then((res: any) => {
    return res.data;
  });
};

/**
 * Get a solution data
 * @param {String} solution_id - Current solution's ID
 */
interface solutionData {
  solution_id: string;
}
export const getSolutionData = (data: solutionData) => {
  return http({
    url: "/api/solution/onesolutionstatus/",
    method: "get",
    params: data,
  }).then((res: any) => {
    return res.data;
  });
};

/**
 * Submit Code
 * @param {Number} problem_id - The submit problem_id
 * @param {Number} solution_language - The solution language ID
 * @param {String} solution_code - The solution Code text
 * @param {String} level_id - The solution level id
 * @param {String} contest_id - The solution contest id
 */

interface submitCodeData {
  problem_id: number;
  solution_language: number;
  solution_code: string;
  level_id: string;
  contest_id: string;
}
export const submitCode = (data: submitCodeData) => {
  return http({
    url: "/api/solution/problemSubmission/",
    method: "post",
    data: data,
  }).then((res: any) => {
    return res.data;
  });
};

/**
 * Afresh judge solution
 * @param {Number} solution_id - which solution will afresh judger
 * @param {Number} problem_id - which problem will afresh judger
 * @param {Number} contest_id - which contest will afresh judger
 * @param {String} user_id - which user will afresh judger
 */
interface afreshJudgerData {
  solution_id: number;
  problem_id: number;
  contest_id: number;
  user_id: string;
}
export const afreshJudgerSolution = (data: afreshJudgerData) => {
  return http({
    url: "/api/solution/rejudgesolution/",
    method: "post",
    data: data,
  }).then((res: any) => {
    return res.data;
  });
};
