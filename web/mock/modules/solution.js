import { mock } from "mockjs";

function getSolutionList() {
  const data = [];
  for (var i = 236; i >= 0; i--) {
    var text = {
      solution_id: i + 1,
      user_id: mock('@id'),
      problem_id: mock('@integer(1000, 9999)'),
      solution_result: mock('@integer(0, 10)'),
      solution_memory: mock('@integer(0, 3000)'),
      solution_consuming: mock('@integer(0, 1000)'),
      solution_language: mock('@integer(0, 6)'),
      solution_length: "125B",
      solution_time: mock('@datetime'),
    };
    data.push(text);
  }
  return data;
}

export default [
  {
    url: "/api/solution/get_solution_list/",
    method: "get",
    data: getSolutionList(),
  },
];
