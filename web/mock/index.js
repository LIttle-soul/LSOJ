const Mock = require('mockjs')   //引入mock
import problem from './modules/problem.js'
import user from './modules/user.js'
import solution from './modules/solution'
import contest from './modules/contest'

Mock.setup({
  timeout: 2000
})

var data = [
  ...problem,
  ...user,
  ...solution,
  ...contest
]

// console.log(data);
data.forEach(val => {
    // console.log(val);
    Mock.mock(val.url, val.method, val.data);
})

export default Mock