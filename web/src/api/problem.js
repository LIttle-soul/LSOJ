import http from '@/utils/http'

// export const getProblemDataList = () => {
//     return http({
//         url: "/api/problem/getproblemlist/",
//         methods: "get",
//     }).then((res) => {
//         console.log(res.data);
//         return res.data.rank.map(item => ({
//             problem_id: item.problem_id,
//             problem_title: item.problem_title,
//             problem_degree: item.problem_difficult,
//             problem_tag: item.problem_tag,
//             problem_solved: item.problem_accepted,
//             problem_submit: item.problem_submit,
//             problem_status: true,
//             problem_source: "汉语言文学",
//             creation_time: "2020-01-01 08:00:00",
//             submit_status: 0,
//             centerDialogVisible: false,
//         }));
//     })
// }

// RSET 接口
export const getProblemDataList = () => {
    return http({
        url: "/api/problem/problem/",
        methods: "get",
    }).then((res) => {
        // console.log(res.data);
        return res.data.map(item => ({
            problem_id: item.problem_id,
            problem_title: item.problem_title,
            problem_degree: item.problem_difficult,
            problem_tag: item.problem_tag,
            problem_solved: item.problem_accepted,
            problem_submit: item.problem_submit,
            problem_description: item.problem_description,
            time_limit: item.time_limit,
            memory_limit: item.memory_limit,
            problem_status: item.problem_status,
            problem_source: item.problem_course,
            creation_time: item.creation_time,
            submit_status: item.submit_status,
            centerDialogVisible: false,
        }));
    })
}

