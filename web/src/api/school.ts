import http from "@/utils/http";

/**
 * Get school list data
 * @param {Number} page - Current page
 * @param {Number} total - Current page total
 * @param {String} text - The search text
 * @param {String} municipality_id - Get list from this municipality
 */
interface schoolListData {
  page: number;
  total: number;
  text: string;
  municipality_id: string;
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
 */

interface collegeListData {
  page: number;
  total: number;
  text: string;
  school_id: string;
}

export const getCollegeList = (data: collegeListData) => {
  return http({
    url: "/api/school/getcollege/",
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
  college_id: string;
}

export const getClassList = (data: classListData) => {
  return http({
    url: "/api/school/getclass/",
    method: "get",
    params: data,
  }).then((res: any) => {
    return res.data;
  });
};
