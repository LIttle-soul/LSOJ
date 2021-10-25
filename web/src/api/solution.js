import http from "@/utils/http";

export const getSolutionDataList = () => {
  return http({
    url: "/api/solution/statussubmit/",
    method: "get",
  }).then((res) => {
    // console.log(res.data);
    return res.data;
  });
};

export const getSolutionData = (data) => {
  return http({
    url: "/api/solution/onesolutionstatus/",
    method: "get",
    params: data,
  }).then((res) => {
    return res.data;
  });
};

export const submitCode = (data) => {
  // console.log(data);
  return http({
    url: "/api/solution/problemSubmission/",
    method: "post",
    data: {
      problem_id: data.problem_id,
      solution_language: data.solution_language,
      solution_code: data.solution_code,
      level_id: data.level_id,
      contest_id: data.contest_id,
    },
  }).then((res) => {
    // console.log(res.data);
    return res.data;
  });
};
