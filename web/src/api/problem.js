import http from "@/utils/http";

export const getProblemDataList = () => {
  return http({
    url: "/api/problem/getproblemlist/",
    method: "get",
  }).then((res) => {
    // console.log(res.data);
    return res.data;
  });
};

export const getProblemTagAndCourse = () => {
  return http({
    url: "/api/problem/getproblemtag/",
    method: "get",
  }).then((res) => {
    // console.log(res.data);
    return res.data;
  });
};

export const submitProblemData = (data) => {
  return http({
    url: "/api/problem/addproblem/",
    method: "post",
    data: {
      problem_id: data.problem_id,
      problem_title: data.problem_title,
      problem_description: data.problem_content,
      problem_spj: data.problem_spj,
      problem_course: data.problem_course,
      time_limit: data.time_limit,
      memory_limit: data.memory_limit,
      problem_tag: data.problem_tag,
      problem_difficult: data.problem_difficult,
      problem_status: data.problem_status,
    },
  }).then((res) => {
    // console.log(res);
    return res.data;
  });
};

export const changeProblemData = (data) => {
  return http({
    url: "/api/problem/addproblem/",
    method: "put",
    params: {
      problem_id: data.problem_id,
      problem_title: data.problem_title,
      problem_description: data.problem_content,
      problem_spj: data.problem_spj,
      problem_course: data.problem_course,
      time_limit: data.time_limit,
      memory_limit: data.memory_limit,
      problem_tag:
        data.problem_tag != undefined ? data.problem_tag.join(",") : undefined,
      problem_difficult: data.problem_difficult,
      problem_status: data.problem_status,
    },
  }).then((res) => {
    return res.data;
  });
};

export const deleteProblemData = (data) => {
  return http({
    url: "/api/problem/addproblem/",
    method: "delete",
    params: {
      problem_id: data,
    },
  }).then((res) => {
    return res.data;
  });
};

export const getProblemTestData = (problem_id) => {
  return http({
    url: "/api/problem/problemsample/",
    method: "get",
    params: {
      problem_id: problem_id,
    },
  }).then((res) => {
    // console.log(res);
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

export const changeProblemTestData = (data) => {
  console.log(data);
  return http({
    url: "/api/problem/problemsample/",
    method: "put",
    params: {
      problem_id: data.problem_id,
      files_name: data.data_title,
      files_text: data.data_text,
    },
  }).then((res) => {
    console.log(res);
    return res.data;
  });
};

export const changeProblemTestName = (data) => {
  return http({
    url: "/api/problem/problemsample/",
    method: "patch",
    params: {
      problem_id: data.problem_id,
      files_name: data.data_title,
      new_name: data.new_title,
    },
  }).then((res) => {
    console.log(res);
    return res.data;
  });
};

export const deleteProblemTestData = (data) => {
  return http({
    url: "/api/problem/problemsample/",
    method: "delete",
    params: {
      problem_id: data.problem_id,
      files_name: data.data_title,
    },
  }).then((res) => {
    console.log(res);
    return res.data;
  });
};
