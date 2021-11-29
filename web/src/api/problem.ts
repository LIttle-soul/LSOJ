import http from "@/utils/http";

/**
 * Get problem data list
 * @param {Number} page - Current page
 * @param {Number} total - Page size
 * @param {String} key - The search key [search, id, tag, difficult, ]
 * @param {String} text - The search Content
 */

interface problemTableData {
  page: number;
  total: number;
  key: string;
  text: string;
}

export const getProblemDataList = (data: problemTableData) => {
  return http({
    url: "/api/problem/getproblemlist/",
    method: "get",
    params: data,
  }).then((res: any) => {
    return res.data;
  });
};

/**
 * Get problem's tag and course
 */
export const getProblemTagAndCourse = () => {
  return http({
    url: "/api/problem/getproblemtag/",
    method: "get",
  }).then((res: any) => {
    return res.data;
  });
};

/**
 * Submit problem data
 * @param {Number} problem_id -
 * @param {Number} problem_title -
 * @param {Number} problem_description -
 * @param {Number} problem_spj -
 * @param {Number} problem_course -
 * @param {Number} time_limit -
 * @param {Number} memory_limit -
 * @param {Number} problem_tag -
 * @param {Number} problem_difficult -
 * @param {Number} problem_status -
 */
interface problemData {
  problem_id: number;
  problem_title: string;
  problem_description: string;
  problem_spj: boolean;
  problem_course: string;
  time_limit: number;
  memory_limit: number;
  problem_tag: string;
  problem_difficult: number;
  problem_status: boolean;
}
export const submitProblemData = (data: problemData) => {
  return http({
    url: "/api/problem/addproblem/",
    method: "post",
    data: data,
  }).then((res: any) => {
    return res.data;
  });
};

/**
 * Change problem data
 * @param {Number} problem_id -
 * @param {Number} problem_title -
 * @param {Number} problem_description -
 * @param {Number} problem_spj -
 * @param {Number} problem_course -
 * @param {Number} time_limit -
 * @param {Number} memory_limit -
 * @param {Number} problem_tag -
 * @param {Number} problem_difficult -
 * @param {Number} problem_status -
 */
export const changeProblemData = (data: problemData) => {
  return http({
    url: "/api/problem/addproblem/",
    method: "put",
    params: data,
  }).then((res: any) => {
    return res.data;
  });
};

/**
 * Delete problem data
 * @param {Number} problem_id - Delete problem by problem's ID
 */
export const deleteProblemData = (data: { problem_id: number }) => {
  return http({
    url: "/api/problem/addproblem/",
    method: "delete",
    params: data,
  }).then((res: any) => {
    return res.data;
  });
};

/**
 * Get problem test data
 * @param {Number} problem_id - Get test data by problem's ID
 */
export const getProblemTestData = (data: { problem_id: number }) => {
  return http({
    url: "/api/problem/problemsample/",
    method: "get",
    params: data,
  }).then((res: any) => {
    return res.data;
  });
};

// export const submitProblemTestData = (data) => {
//     return http({
//         url: "/api/problem/problemsample/",
//         method: "post",
//         data: {
//             problem_id: data.problem_id
//         }
//     }).then((res) => {
//         console.log(res);
//         return res.data;
//     })
// }

/**
 * Change problem test data
 * @param {String} problem_id - Current problem
 * @param {String} files_name - Current file's name
 * @param {String} files_text - Current file's content
 */
export const changeProblemTestData = (data: {
  problem_id: number;
  files_name: string;
  files_text: string;
}) => {
  // console.log(data);
  return http({
    url: "/api/problem/problemsample/",
    method: "put",
    params: data,
  }).then((res: any) => {
    return res.data;
  });
};

/**
 * Change problem test data
 * @param {String} problem_id - Current problem
 * @param {String} files_name - Current file's name
 * @param {String} news - new file's name
 */
export const changeProblemTestName = (data: {
  problem_id: number;
  files_name: string;
  news: string;
}) => {
  return http({
    url: "/api/problem/problemsample/",
    method: "patch",
    params: data,
  }).then((res: any) => {
    return res.data;
  });
};

/**
 * Change problem test data
 * @param {String} problem_id - Current problem
 * @param {String} files_name - Current file's name
 */
export const deleteProblemTestData = (data: {
  problem_id: number;
  files_name: string;
}) => {
  return http({
    url: "/api/problem/problemsample/",
    method: "delete",
    params: data,
  }).then((res: any) => {
    return res.data;
  });
};
