import http from "@/utils/http";
import axios from "axios";
import { helperNameMap } from "@vue/compiler-core";
import { computeStyles } from "@popperjs/core";

/**
 * 获取课程列表
 * @author LiSoul
 * @param {Number} page - Current Page
 * @param {Number} total - 每次请求多少条数据
 * @param {String} sort_by - 排序类型
 * @param {String} key - 搜索类型
 * @param {String} text - 搜索关键词
 * @param {String} subject - 课程标签
 * @param {Boolean} me - 是否获取我的课程
 */

export const getCourseList = (data: {
  page: number;
  total: number;
  sort_by: string;
  key: string;
  text: string;
  subject: string;
  me: boolean;
}) => {
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
 * 获取课程列表管理端
 * @author LiSoul
 * @param {Number} page - Current Page
 * @param {Number} total - 每次请求多少条数据
 * @param {String} text - 搜索关键词
 */
interface courseDate {
  page: number;
  total: number;
  text: string;
}

export const getCourseData = (data: courseDate) => {
  return http({
    url: "/api/course/coursemanage/",
    method: "get",
    params: data,
  }).then((res: any) => {
    return res.data;
  });
};

/**
 * 删除课程
 * @param {Number} course_id - 已发布的课程标题
 */
interface deleteCourseData {
  course_id: number;
}
export const deleteCourse = (data: deleteCourseData) => {
  console.log(data);
  return http({
    url: "/api/course/getcoursedetails/",
    method: "delete",
    params: data,
  }).then((res: any) => {
    return res.data;
  });
};
/**
 * 是否显示课程
 * @param {Number} course_id - 已发布的课程标题
 */
interface CourseShow {
  course_id: number;
}
export const showCourse = (data: CourseShow) => {
  console.log(data);
  return http({
    url: "/api/course/coursemanage/",
    method: "put",
    params: data,
  }).then((res: any) => {
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
 * @author LiSoul
 * @param {Number} course_id - 课程id
 */
interface courseChapter {
  course_id: number;
  class_id: string;
}

export const getCourseChapter = (data: courseChapter) => {
  return http({
    url: "/api/course/chapterlist/",
    method: "get",
    params: data,
  }).then((res: any) => {
    return res.data;
  });
};

/**
 * 添加课程章节
 * @author LiSoul
 * @param {Number} course_id - 课程id
 * @param {String} chapter_title - 章节类型
 * @param {Number} pre_chapter - 前置关卡
 */

export const addCourseChapter = (data: {
  course_id: number;
  chapter_title: string;
  pre_chapter: number;
}) => {
  return http({
    url: "/api/course/chapterlist/",
    method: "post",
    data: data,
  }).then((res: any) => {
    return res.data;
  });
};

/**
 * 删除课程章节
 * @author LiSoul
 * @param {Number} chapter_id - 章节编号
 */

export const deleteCourseChapter = (data: { chapter_id: number }) => {
  return http({
    url: "/api/course/chapterlist/",
    method: "delete",
    params: data,
  }).then((res: any) => {
    return res.data;
  });
};

/**
 * 添加章节内容
 * @author LiSoul
 * @param {Number} chapter_id - 章节ID
 * @param {String} chapter_content  - 章节内容
 */

export const addChapterContent = (data: {
  chapter_id: number;
  course_id: number;
  chapter_content: string;
}) => {
  return http({
    url: "/api/course/coursechapter/",
    method: "post",
    data: data,
  }).then((res: any) => {
    return res.data;
  });
};

/**
 * 获取课程的所有数据
 * @param {Number} course_id - 课程id
 */

interface courseAll {
  course_id: number;
}

export const getCourseAllData = (data: courseAll) => {
  return http({
    url: "/api/course/getcoursealldata/",
    method: "get",
    param: data,
  }).then((res: any) => {
    return res.data;
  });
};

// /**
//  * 获取考试数据
//  * @param {Number} course_id - 课程id
//  */

interface courseExam {
  course_id: number;
}
export const getcourseExam = (data: courseExam) => {
  return http({
    url: "/api/course/viewcourseassignmentexam/",
    method: "get",
    param: data,
  }).then((res: any) => {
    return res.data;
  });
};

/**
 * 获取我的作业数据
 * @param {Number} course_id - 课程id
 * @param {Number} task_type - 作业类型
 * @param {Number} page - 页数
 * @param {Number} total - 每次请求多少条数据
 * @param {Number} key - 搜索类型
 */

interface homeWorkData {
  course_id: number;
  task_type: number;
  page: number;
  total: number;
  key: number;
}

export const getTaskData = (data: homeWorkData) => {
  return http({
    url: "/api/course/mytask/",
    method: "get",
    params: data,
  }).then((res: any) => {
    return res.data;
  });
};

/**
 * 加入课程
 * @param {Number} course_id - 课程id
 */
interface joinData {
  course_id: number;
}
export const joinCourse = (data: joinData) => {
  return http({
    url: "/api/class/joincourse/",
    method: "post",
    data: data,
  }).then((res: any) => {
    return res.data;
  });
};

/**
 * 获取题单
 * @author LiSoul
 * @param {Number} task_id - 题单编号
 * @param {Boolean} is_see - 试看状态
 */
export const getOneTask = (data: { task_id: number; is_see: boolean }) => {
  return http({
    url: "/api/course/createtask/",
    method: "get",
    params: data,
  }).then((res: any) => {
    return res.data;
  });
};

/**
 * 添加题单
 * @author LiSoul
 * @param {number} course_id - 课程编号
 * @param {string} task_title - 作业标题
 * @param {number} task_type - 作业类型 {0-测试|1-作业|2-考试}
 * @param {number} total_score - 总分
 * @param {string} problem_content - 作业单内容 JSON格式
 */
interface addTaskData {
  course_id: number;
  task_title: string;
  task_type: number;
  total_score: number;
  problem_content: string;
}
export const addTaskData = (data: addTaskData) => {
  return http({
    url: "/api/course/createtask/",
    method: "post",
    data: data,
  }).then((res: any) => {
    return res.data;
  });
};

/**
 * 提交答题结果
 * @author LiSoul
 * @param {Number} task_id - 作业编号
 * @param {Number} user_score - 用户得分
 * @param {String} problem_content - 作业题单（JSON格式）
 */
interface AnswerData {
  task_id: number;
  user_score: number;
  problem_content: string;
}
export const submitAnswerData = (data: AnswerData) => {
  return http({
    url: "/api/course/submittask/",
    method: "post",
    data: data,
  }).then((res: any) => {
    return res.data;
  });
};

/**
 * 获取课程班级
 * @param {Number} course_id - 课程id
 */
interface courseClassData {
  course_id: number;
}
export const getCourseClass = (data: courseClassData) => {
  return http({
    url: "/api/class/createclass/",
    method: "get",
    params: data,
  }).then((res: any) => {
    return res.data;
  });
};

/**
 * 获取课程统计
 * @param {Number} course_id - 课程id
 * @param {Number} class_id - 班级id
 */
interface statisticsData {
  course_id: number;
}
export const getCourseStatistics = (data: statisticsData) => {
  return http({
    url: "/api/course/settlement/",
    method: "get",
    params: data,
  }).then((res: any) => {
    return res.data;
  });
};

/**
 * 获取作业
 * @param {Number} course_id - 课程id
 * @param {Number} task_type - 类型
 * @param {Number} key - 筛选类型
 */
interface workData {
  course_id: number;
  task_type: number;
  key: number;
}
export const getHomeWork = (data: workData) => {
  console.log(data.key);
  return http({
    url: "/api/course/mytask/",
    method: "get",
    params: data,
  }).then((res: any) => {
    return res.data;
  });
};
/**
 * 获取作业库数据
 * @param {Number} course_id - 课程id
 * @param {Number} task_type - 类型 0作业2考试
 */
interface taskData {
  course_id: number;
  task_type: number;
}
export const gettask = (data: taskData) => {
  return http({
    url: "/api/course/allcoursetask/",
    method: "get",
    params: data,
  }).then((res: any) => {
    return res.data;
  });
};
/**
 * 上传发放作业数据
 * @param {Number} course_id -课程id
 * @param {Number} task_type - 类型
 * @param {Number} task_id - 作业id
 * @param {String} title - 作业标题
 * @param {Object} time - 时间
 * @param {Object} class_lists - 班级列表
 * @param {Boolean} task_judge - 是否自动判题
 */
interface releseData {
  course_id: number;
  task_type: number;
  task_id: number;
  title: string;
  time: object;
  class_lists: object;
  task_judge: boolean;
}
export const postreleaseTaskData = (data: releseData) => {
  console.log(data);
  return http({
    url: "/api/course/allcoursetask/",
    method: "post",
    data: data,
  }).then((res: any) => {
    return res.data;
  });
};
/**
 * 删除作业/考试
 * @param {Number} task_id - 类型0作业2考试
 */
interface deleteTaskData {
  task_id: number;
}
export const deleteTask = (data: deleteTaskData) => {
  return http({
    url: "/api/course/allcoursetask/",
    method: "delete",
    params: data,
  }).then((res: any) => {
    return res.data;
  });
};
/**
 * 删除已发布的作业/考试
 * @param {Number} work_id - 已发布的作业/考试id
 */
interface deleteWorkData {
  release_id: number;
}
export const deleteWork = (data: deleteWorkData) => {
  console.log(data);
  return http({
    url: "/api/course/allcoursetask/",
    method: "delete",
    params: data,
  }).then((res: any) => {
    return res.data;
  });
};
/**
 * 获取用户在课程中的身份
 * @param {Number} course_id - 课程id
 */
interface powerData {
  course_id: number;
}
export const getUserPower = (data: powerData) => {
  return http({
    url: "/api/course/coursepower/",
    method: "get",
    params: data,
  }).then((res: any) => {
    return res.data;
  });
};
/**
 * 获取课程题库
 * @param {Number} course_id - 课程id
 * @param {String} text - 搜索数据
 */
interface QuestionData {
  course_id: number;
  text: string;
}
export const getQuestionList = (data: QuestionData) => {
  return http({
    url: "/api/course/allcoursequestions/",
    methon: "get",
    params: data,
  }).then((res: any) => {
    return res.data;
  });
};
/**
 * 删除题目
 * @param {Number} question_id - 题目id
 */
interface deleteQuestionData {
  question_id: number;
}
export const deleteProblem = (data: deleteQuestionData) => {
  console.log(data);
  return http({
    url: "/api/course/deletequestion//",
    methon: "get",
    params: data,
  }).then((res: any) => {
    return res.data;
  });
};

/**
 * 获取课程班级
 * @param {Number} course_id - 课程id
 */
interface classData {
  course_id: number;
}
export const getClassList = (data: classData) => {
  return http({
    url: "/api/class/createclass/",
    method: "get",
    params: data,
  }).then((res: any) => {
    return res.data;
  });
};

/**
 * 添加学生
 * @param {Number} course_id - 课程id
 * @param {Number} class_id - 班级id
 * @param {String} user_list - 学生id
 * @param {Number} add_class_id -添加班级id
 */
interface addStudentData {
  course_id: number;
  class_id: number;
  user_list: string;
  add_class_id: number;
}
export const addStudent = (data: addStudentData) => {
  return http({
    url: "/api/class/admincatchstudent/",
    method: "post",
    data: data,
  }).then((res: any) => {
    return res.data;
  });
};
/**
 * 删除学生
 * @param {Number} course_id - 课程id
 * @param {Number} class_id - 班级id
 * @param {String} user_list - 学生id
 */
interface deleteStudentData {
  course_id: number;
  class_id: number;
  user_id: string;
}
export const deleteStudent = (data: deleteStudentData) => {
  return http({
    url: "/api/class/admincatchstudent/",
    method: "delete",
    params: data,
  }).then((res: any) => {
    return res.data;
  });
};
/**
 * 获取资料信息
 * @param {Number} course_id - 课程id
 * @param {String} text - 搜索数据
 */
interface getDatumData {
  course_id: number;
  text: string;
}
export const getDatum = (data: getDatumData) => {
  return http({
    url: "/api/course/coursechapter/",
    methon: "get",
    params: data,
  }).then((res: any) => {
    return res.data;
  });
};
/**
 * 删除资料信息
 * @param {Number} file_id - 文件id
 */
interface deleteFileData {
  file_id: number;
}
export const deleteFile = (data: deleteFileData) => {
  return http({
    url: "/api/course/uploadfile/",
    method: "delete",
    params: data,
  }).then((res: any) => {
    return res.data;
  });
};
/**
 * 获取所有的班级
 */
export const allClass = () => {
  return http({
    url: "/api/class/createclass/",
    method: "get",
  }).then((res: any) => {
    return res.data;
  });
};
/**
 * 添加班级
 * @param {Number} course_id - 课程id
 * @param {String} class_name - 班级名称
 */
interface AddClassData {
  course_id: number;
  class_id: string;
}
export const addClss = (data: AddClassData) => {
  return http({
    url: "/api/class/addcourseclass/",
    method: "post",
    data: data,
  }).then((res: any) => {
    return res.data;
  });
};
/**
 * 下载资料
 * @param {Number} file_id - 文件id
 */
interface downFileData {
  file_id: number;
}
export const downLoad = (data: downFileData) => {
  return http({
    url: "/api/course/uploadfile/",
    method: "patch",
    params: data,
    responseType: "json",
  }).then((res: any) => {
    return res.data;
  });
};

/**
 * Add course data
 *  @param {String} course_name - 课程名字
 *  @param {String} course_school - 学校
 *  @param {String} course_credits -学分
 *  @param {Number} course_cost -价格
 *  @param {String} start_time -开始时间
 *  @param {String} end_time - 结束时间
 *  @param {String} course_introduce - 课程介绍
 *  @param {String} course_cover -课程封面
 */
interface courseData {
  course_name: string;
  course_school: string;
  course_credits: string;
  course_cost: number;
  start_time: string;
  end_time: string;
  course_introduce: string;
  course_cover: string;
  course_form: FormData;
}
export const submitCourseData = (data: any) => {
  console.log(data)
  return http({
    url: "/api/course/getcoursedetails/",
    method: "post",
    data: data,
    // Headers: {
    //   'Content-Type': 'multipart/form-data'
    // }
  }).then((res: any) => {
    return res.data;
  });
};

/**
 * Change course Data
 *  @param {Number} course_id
 *  @param {String} course_name
 *  @param {String} course_school
 *  @param {String} course_credits
 *  @param {Number} course_cost
 *  @param {String} start_time
 *  @param {String} end_time
 *  @param {String} course_introduce
 *  @param {String} course_cover
 */
interface courseDataByChange {
  course_id: number;
  course_name: string;
  course_school: string;
  course_credits: string;
  course_cost: number;
  start_time: string;
  end_time: string;
  course_introduce: string;
  course_cover: string;
}
export const changeCourseData = (data: courseDataByChange) => {
  console.log(data);
  return http({
    url: "/api/course/getcoursedetails/",
    method: "post",
    data: data,
  }).then((res: any) => {
    return res.data;
  });
};
/**
 * 上传图片
 * @param {File} course_cover - 课程封面
 */
interface ImgData {
  course_cover: string;
  course_id: number
}
export const submitCourseImg = (data: ImgData) => {
  console.log(data);
  return http({
    url: "/api/course/submitcoursecover/",
    method: "post",
    data: data,
  }).then((res: any) => {
    return res.data;
  });
};

/** 修改课程数据
 * @param {Number} course_id - 课程id
 */
interface modifyCourseData {
  course_id: number,
}
export const getcoursemessage = (data: modifyCourseData) => {
  return http({
    url: "/api/course/getcoursedetails/",
    method: "get",
    params: data,
  }).then((res: any) => {
    return res.data;
  });
};