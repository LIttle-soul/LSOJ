import http from "@/utils/http";
import { AxiosResponseTransformer } from "axios";

/**
 * Check user login status
 * @author LiSoul
 */
export const checkUserLoginStatus = () => {
  return http({
    url: "/api/user/extendtokentime/",
    method: "get",
  }).then((res: any) => {
    return res.data;
  });
};

/**
 * Login
 * @author LiSoul
 * @example
 * ```typescript
 * const back_data = submitLoginForm({
 *  user_id: xxxx,
 *  password: *******
 * });
 * ```
 */
export const submitLoginForm = (data: {
  /** User Id */
  user_id: string;
  /** User Password */
  password: string;
}): AxiosResponseTransformer => {
  return http({
    url: "/api/user/login/",
    method: "post",
    data: data,
  }).then((res: any) => {
    return res.data;
  });
};

/**
 * Register
 * @author LiSoul
 * @param {{string}} user_id - User ID
 * @param {{string}} password - User Password
 * @param {{string}} check_password - User Password second
 */
export const submitRegisterForm = (data: {
  user_id: string;
  password: string;
  check_password: string;
}) => {
  return http({
    url: "/api/user/register/",
    method: "post",
    data: data,
  }).then((res: any) => {
    return res.data;
  });
};

interface forgetpasswordData {
  user_id: string;
  new_password: string;
  check_password: string;
  email_code: string;
}
/**
 * Submit Forget Password Form
 * @author LiSoul
 * when user forget password, we can use this founction to change it
 * @param {{string}} user_id - the user id value
 * @param {{string}} new_password - the new password
 * @param {{string}} check_password - the check password
 * @param {{string}} email_code - the callback email code
 */
export const submitForgetPasswordForm = (data: forgetpasswordData) => {
  return http({
    url: "/api/user/forgetpassword/",
    method: "post",
    data: data,
  }).then((res: any) => {
    return res.data;
  });
};

interface sendEmailData {
  user_id: String;
  email: String;
}
/**
 * Send email code
 * @author LiSoul
 * @param {{string}} user_id - when user forget password, user need this keyword to find it;
 * @param {{email}} email - when user bind email need it;
 */
export const sendEmailCode = (data: sendEmailData) => {
  return http({
    url: "/api/user/sendemail/",
    method: "get",
    params: data,
  })
    .then((res: any) => {
      return res.data;
    })
    .catch((res: any) => {
      return {
        status: false,
        message: "网络连接超时",
      };
    });
};

/***
 * Get has login userinfo
 * @author LiSoul
 */

export const getUserInfo = () => {
  return http({
    url: "/api/user/perfectinfo/",
    method: "get",
  }).then((res: any) => {
    return res.data;
  });
};

interface bindEmailData {
  email: string;
  code: string;
}
/***
 * Bind user email
 * @author LiSoul
 * @param {{email}} email - user will bind email
 * @param {{string}} code - the callback email code
 * @returns {JSON} - Action status
 *
 * @example
 * console.log(bindUserEmail({
 *  email: "xxxxxx@qq.com",
 *  code: "123456"
 * }))
 */
export const bindUserEmail = (data: bindEmailData) => {
  return http({
    url: "/api/user/sendemail/",
    method: "post",
    data: data,
  }).then((res: any) => {
    return res.data;
  });
};

interface userInfoData {
  user_name: string;
  user_nick: string;
  user_introduce: string;
  user_telephone: string;
  user_birthday: Date;
  user_school: [number, string];
  user_class: [number, string];
  user_address: [number, string];
  user_sex: number;
}
/**
 * Submit User Info
 * @author LiSoul
 * @param {{string}} user_name - User Name
 * @param {{string}} user_nick - User Nick
 * @param {{string}} user_introduce - User Introduce
 * @param {{string}} user_telephone - User Telephone Number
 * @param {{Date}}   user_birthday - User Birthday
 * @param {{string, number}} user_school - User School ID
 * @param {{string, number}} user_class - User Class ID
 * @param {{string, number}} user_address - User Address ID
 * @param {{number}} user_sex - 0:man 1:woman
 * @returns
 */
export const submitUserInfoForm = (data: userInfoData) => {
  // console.log(data);
  return http({
    url: "/api/user/perfectinfo/",
    method: "post",
    data: data,
  }).then((res: any) => {
    // console.log(res.data);
    return res.data;
  });
};

interface userStatusData {
  user_id: string;
}
/**
 * Get User Status
 * @author LiSoul
 * @param {{string}} user_id - If has user_id, it will search the user's info, else it search self info.
 * @returns
 */
export const getUserStatus = (data: userStatusData) => {
  return http({
    url: "/api/user/userstatus/",
    method: "get",
    params: data,
  }).then((res: any) => {
    return res.data;
  });
};

interface userListData {
  page: number;
  total: number;
  text: string;
  user_id: string;
}
/**
 * Get user list
 * @author LiSoul
 * @param {{Number}} page - Current page
 * @param {{Number}} total - Current page size
 * @param {{String}} text - The search text
 * @param {{String}} user_id - Get a user's userinfo
 */
export const getUserList = (data: userListData) => {
  return http({
    url: "/api/user/getuserlist/",
    methods: "get",
    params: data,
  }).then((res: any) => {
    return res.data;
  });
};

interface changeUserInfoData {
  user_id: string;
  user_power: string;
  user_status: boolean;
  user_password: string;
}
/**
 * The admin change userinfo
 * @author LiSoul
 * @param {{String}} user_id -  The user's ID will change
 * @param {{String}} user_power - The user's power
 * @param {{Boolean}} user_status - The user's status
 * @param {{String}} user_password - The user's password
 */
export const changeUserInfo = (data: any) => {
  return http({
    url: "/api/user/getuserlist/",
    method: "put",
    params: data,
  }).then((res: any) => {
    return res.data;
  });
};

interface deleteUserInfoData {
  user_id: string;
}
/**
 * The admin delete other user
 * @author LiSoul
 * @param {{String}} user_id - The will delete user
 */
export const deleteUserInfo = (data: deleteUserInfoData) => {
  return http({
    url: "/api/user/getuserlist/",
    method: "delete",
    params: data,
  }).then((res: any) => {
    return res.data;
  });
};

interface teamListData {
  page: number;
  total: number;
  text: string;
  mode: string;
}
/**
 * Get team list
 * @author LiSoul
 * @param {{Number}} page - Current page
 * @param {{Number}} total - Current page size
 * @param {{String}} text - The search text
 * @param {{String}} mode - ['', join, create] Return all team, my join team and my creator team
 */
export const getTeamList = (data: teamListData) => {
  return http({
    url: "/api/team/getteamlist/",
    method: "get",
    params: data,
  }).then((res: any) => {
    return res.data;
  });
};

/**
 * Delete Team List
 * @author LiSoul
 * @param {Number} team_id - The team's ID will delete
 */
export const deleteTeamData = (data: { team_id: number }) => {
  return http({
    url: "/api/team/getteamlist/",
    method: "delete",
    params: data,
  }).then((res: any) => {
    return res.data;
  });
};

interface teamUserData {
  team_id: number;
  user_id: string;
}
/**
 * Delete team user
 * @author LiSoul
 * @param {{Number}} team_id - which team
 * @param {{String}} user_id - which user
 */
export const deleteTeamUser = (data: teamUserData) => {
  return http({
    url: "/api/team/jointeam/",
    method: "delete",
    params: data,
  }).then((res: any) => {
    return res.data;
  });
};

interface teamRegistrationData {
  team_nick: string;
  team_introduce: string;
  team_school: string;
  team_teacher: string;
}
/**
 * Team registration
 * @author LiSoul
 * @param {{String}} team_nick - The team's name
 * @param {{String}} team_introduce - The team's introduce
 * @param {{String}} team_school - Which school that this team brlong to
 * @param {{String}} team_teacher - The tutor about this team
 */
export const teamRegistration = (data: any) => {
  // console.log(data);
  return http({
    url: "/api/team/getteamlist/",
    method: "post",
    data: data,
    responseType: "json",
  }).then((res: any) => {
    return res.data;
  });
};

/**
 * Get team invitation code
 * @author LiSoul
 * @param {Number} team_id - The team's ID
 */
export const getInvitationCode = (data: { team_id: number }) => {
  return http({
    url: "/api/team/createcode/",
    method: "get",
    params: data,
  }).then((res: any) => {
    return res.data;
  });
};

/**
 * Join team by invitation code
 * @author LiSoul
 * @param {String} code - The invitation code
 */

export const joinTeamByCode = (data: { code: string }) => {
  return http({
    url: "/api/team/jointeam/",
    method: "post",
    data: data,
  }).then((res: any) => {
    return res.data;
  });
};
