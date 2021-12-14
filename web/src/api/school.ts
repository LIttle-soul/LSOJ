import http from "@/utils/http";

/**
 * Get school list data
 * @param {Number} page - Current page
 * @param {Number} total - Current page total
 * @param {String} text - The search text
 * @param {String} municipality_id - Get list from this municipality
 * @param {String} school_id - Get a school data
 */
interface schoolListData {
  page: number;
  total: number;
  text: string;
  municipality_id: string;
  school_id: string;
}

export const getSchoolList = (data: schoolListData) => {
  return http({
    url: "/api/school/getschool/",
    method: "get",
    params: data,
  }).then((res: any) => {
    return res.data;
  });
};

/**
 * Get college list data
 * @param {Number} page - Current page
 * @param {Number} total - Current page size
 * @param {String} text - The search text
 * @param {String} school_id - Get list from this school
 * @param {Number} college_id - Get a college data by college ID
 */

interface collegeListData {
  page: number;
  total: number;
  text: string;
  college_id: string;
  school_id: string;
}

export const getCollegeList = (data: collegeListData) => {
  return http({
    url: "/api/school/managecollege/",
    method: "get",
    params: data,
  }).then((res: any) => {
    return res.data;
  });
};

/**
 * Get class list data
 * @param {Number} page - Current page
 * @param {Number} total - Current page size
 * @param {String} text - The search text
 * @param {String} college_id - Get list from this college
 */
interface classListData {
  page: number;
  total: number;
  text: string;
  college_id: number;
  school_id: string;
  class_id: number;
  course_id: number;
}

export const getClassList = (data: classListData) => {
  return http({
    url: "/api/class/createclass/",
    method: "get",
    params: data,
  }).then((res: any) => {
    return res.data;
  });
};

interface schoolData {
  school_id: string;
  school_name: string;
  school_describe: string;
  school_municipality: string;
  school_department: string;
  school_rank: string;
  school_remark: string;
}

export const addSchoolData = (data: schoolData) => {
  return http({
    url: "/api/school/getschool/",
    method: "post",
    data: data,
  }).then((res: any) => {
    return res.data;
  });
};

interface collegeData {
  school_id: string;
  college_name: string;
  college_describe: string;
  college_remark: string;
}

export const addCollegeData = (data: collegeData) => {
  return http({
    url: "/api/school/managecollege/",
    method: "post",
    data: data,
  }).then((res: any) => {
    return res.data;
  });
};

interface classData {
  class_name: string;
  class_introduce: string;
  class_note: string;
  course_id: number;
  class_school: string;
  class_college: string;
  class_teacher: string[];
  class_student: string[];
}

export const addClassData = (data: classData) => {
  return http({
    url: "/api/class/createclass/",
    method: "post",
    data: data,
  }).then((res: any) => {
    return res.data;
  });
};

export const deleteSchoolData = (data: any) => {
  return http({
    url: "/api/school/",
    method: "delete",
    data: data,
  }).then((res: any) => {
    return res.data;
  });
};

export const deleteCollegeData = (data: any) => {
  return http({
    url: "/api/school/",
    method: "delete",
    data: data,
  }).then((res: any) => {
    return res.data;
  });
};

export const deleteClassData = (data: any) => {
  return http({
    url: "/api/school/",
    method: "delete",
    data: data,
  }).then((res: any) => {
    return res.data;
  });
};
