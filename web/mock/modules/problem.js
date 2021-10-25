import { mock, Random } from "mockjs"


function getProblemDescription() {
    const problem_list = []
    for(var i = 0; i < 235; i++){
        var con = `
### 题目描述
    
${mock('@cparagraph(10, 20)')}
![${mock('@word')}](${Random.image()})
        
### 输入格式
        
${mock('@cparagraph')}
        
### 输出格式
        
${mock('@cparagraph')}
        
### 数据范围
        
$0 \\lt N,V \\le 1000$
$0 \\lt v_i,w_i \\le1000$
        
### 输入样例
        
\`\`\`
1 2
3 4
5 6
7 8
\`\`\`
        
### 输出样例
        
\`\`\`
8
\`\`\`
        
::: tip
${mock('@cparagraph(3, 8)')}
:::
    `
        var text = {
            problem_id: i + 1000,
            problem_title: mock('@ctitle(3,8)'),
            problem_difficult: mock('@integer(1, 5)'),
            problem_tag: mock('@cword(3, 5)'),
            problem_accepted: mock('@integer(100, 10000)'),
            problem_submit: mock('@integer(60, 5000)'),
            problem_description: con,
            time_limit: mock('@integer(60, 100)'),
            memory_limit: mock('@integer(60, 100)'),
            problem_status: mock('@boolean'),
            problem_course: mock('@word(5)'),
            creation_time: mock('@datetime()'),
            submit_status: mock('@integer(-1, 1)'),
            problem_creator: mock('@cname()'),
        };
        // console.log(text);
        problem_list.push(text);
    }
    return problem_list
}


export default [
    {
        url: "/api/problem/problem/",
        method: "get",
        data: getProblemDescription()
    }
]