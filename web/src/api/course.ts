import http from "@/utils/http";

/**
 * 获取课程列表
 * @param {Number} page - Current Page
 * @param {Number} total - 每次请求多少条数据
 * @param {String} sort_by - 排序类型
 * @param {String} key - 搜索类型
 * @param {String} text - 搜索关键词
 * @param {String} subject - 课程标签
 */

interface courseData {
  page: number;
  total: number;
  sort_by: string;
  key: string;
  text: string;
  subject: string;
}

export const getCourseList = (data: courseData) => {
  return http({
    url: "/api/course/coursehome/",
    method: "get",
    params: data,
  }).then((res: any) => {
    // console.log(res.data);
    return res.data;
  });
};
/**
 * 获取课程标签
 */

export const getCourseTag = () => {
  return http({
    url: "/api/course/getcoursetag/",
    method: "get",
  }).then((res: any) => {
    return res.data;
  });
};

/**
 * 获取课程详情
 * @param {Number} course_id - 课程id
 */
interface courseDetailsData {
  course_id: number;
}

export const getCourseDetails = (data: courseDetailsData) => {
  return http({
    url: "/api/course/getcoursedetails/",
    method: "get",
    params: data,
  }).then((res: any) => {
    return res.data;
  });
};

/**
 * 获取课程章节
 * @param {Number} course_id - 课程id
 */
interface courseChapter {
  course_id: number;
}

export const getCourseChapter = (data: courseChapter) => {
  return http({
    url: "/api/course/coursechapter/",
    method: "get",
    params: data,
  }).then((res: any) => {
    return res.data;
  });
};
