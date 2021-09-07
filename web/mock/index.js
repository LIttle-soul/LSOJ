const Mock = require('mockjs')   //引入mock
import { test } from './test.js'
import { problem } from './problem.js'

Mock.setup({
  timeout: 2000
})

var data = [
  ...test,
  ...problem
]

// console.log(data);
data.forEach(val => {
    // console.log(val);
    Mock.mock(val.url, val.method, val.data);
})

export default Mock