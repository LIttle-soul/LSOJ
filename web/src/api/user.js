import http from "@/utils/http";

// 登陆接口
export const submitLoginForm = (data) => {
  return http({
    url: "/api/user/login/",
    method: "post",
    data: {
      user_id: data.username,
      password: data.password,
    },
  }).then((res) => {
    // console.log(res);
    return res.data;
  });
};

// 注册接口
export const submitRegisterForm = (data) => {
  return http({
    url: "/api/user/register/",
    method: "post",
    data: {
      user_id: data.username,
      password: data.password,
      check_password: data.checkpassword,
    },
  }).then((res) => {
    // console.log(res);
    return res.data;
  });
};

/**
 * Submit Forget Password Form
 * when user forget password, we can use this founction to change it
 * @param {string} user_id - the user id value
 * @param {string} new_password - the new password
 * @param {string} check_password - the check password
 * @param {string} email_code - the callback email code
 */
export const submitForgetPasswordForm = (data) => {
  return http({
    url: "/api/user/forgetpassword/",
    method: "post",
    data: {
      user_id: data.username,
      new_password: data.password,
      check_password: data.check_password,
      email_code: data.verifycode,
    },
  }).then((res) => {
    // console.log(res);
    return res.data;
  });
};

/**
 * Send email code
 * @param {string} user_id - when user forget password, user need this keyword to find it;
 * @param {email} email - when user bind email need it;
 */
export const sendEmailCode = (data) => {
  return http({
    url: "/api/user/sendemail/",
    method: "get",
    params: data,
  }).then((res) => {
    return res.data;
  });
};

/***
 * Get has log in userinfo
 */
export const getUserInfo = () => {
  return http({
    url: "/api/user/perfectinfo/",
    method: "get",
  }).then((res) => {
    return res.data;
  });
};

/***
 * Bind user email
 * @param {email} email - user will bind email
 * @param {string} code - the callback email code
 *
 * @example
 * console.log(bindUserEmail({
 *  email: "xxxxxx@qq.com",
 *  code: "123456"
 * }))
 */
export const bindUserEmail = (data) => {
  return http({
    url: "/api/user/sendemail/",
    method: "post",
    data: data,
  }).then((res) => {
    return res.data;
  });
};

// 提交用户信息表
export const submitUserInfoForm = (data) => {
  // console.log(data);
  return http({
    url: "/api/user/perfectinfo/",
    method: "post",
    data: {
      user_name: data.user_name,
      user_nick: data.user_nick,
      user_introduce: data.user_introduce,
      user_telephone: data.user_telephone,
      user_birthday: data.user_birthday,
      user_school: data.user_school,
      user_class: data.user_class,
      user_address: data.user_address,
      user_sex: data.user_sex,
    },
  }).then((res) => {
    // console.log(res.data);
    return res.data;
  });
};

// 获取用户列表
export const getUserList = () => {
  return http({
    url: "/api/user/getuserlist/",
    methods: "get",
  }).then((res) => {
    // console.log(res);
    return res.data;
  });
};

// 管理员修改用户信息
export const changeUserInfo = (data) => {
  return http({
    url: "/api/user/getuserlist/",
    method: "put",
    params: {
      user_id: data.user_id,
      user_power: data.user_power,
      user_status: data.user_status,
      user_password: data.user_password,
    },
  }).then((res) => {
    // console.log(res.data);
    return res.data;
  });
};

// 删除用户
export const deleteUserInfo = (data) => {
  return http({
    url: "/api/user/getuserlist/",
    method: "delete",
    params: {
      user_id: data,
    },
  }).then((res) => {
    // console.log(res.data);
    return res.data;
  });
};

// 获取团队列表
export const getTeamList = () => {
  return http({
    url: "/api/class/createTeam/",
    method: "get",
  }).then((res) => {
    // console.log(res.data);
    return res.data;
  });
};

// 删除团队列表
/**
 * Delete Team List
 * @param {*} data
 * @returns
 */
export const deleteTeamData = (data) => {
  return http({
    url: "/api/class/createTeam/",
    method: "delete",
    params: data,
  }).then((res) => {
    // console.log(res.data);
    return res.data;
  });
};

// 删除团队用户
export const deleteTeamUser = (data) => {
  return http({
    url: "/api/class/classusers/",
    method: "delete",
    params: data,
  }).then((res) => {
    return res.data;
  });
};

// 团队注册
export const teamRegistration = (data) => {
  // console.log(data);
  return http({
    url: "/api/class/createTeam/",
    method: "post",
    data: {
      team_name: data.team_title,
      team_introduce: data.team_introduce,
      team_school: data.team_school,
      team_member: data.team_user_list.map((item) => {
        return item.user_id;
      }),
      team_teacher: data.team_teacher,
    },
    responseType: "json",
  }).then((res) => {
    // console.log(res.data);
    return res.data;
  });
};

// 获取用户状态
export const getUserStatus = (data) => {
  return http({
    url: "/api/user/userstatus/",
    method: "get",
    params: data,
  }).then((res) => {
    return res.data;
  });
};
