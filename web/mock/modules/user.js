import { mock, Random } from "mockjs"

function getRankList() {
    const rank_list = []
    for(var i = 0; i < 135; i++){
        var text = {
            'user_rank': i + 1,
            'user_id': mock('@cname()'),
            'user_nick': mock('@cname()'),
            'true_submit': mock('@integer(100, 10000)'),
            'all_submit': mock('@integer(100, 10000)'),
        };
        // console.log(text);
        rank_list.push(text);
    }
    return rank_list
}

function getUserInfo() {
    const data = {
        'user_id': Random.id(),
        'registration_time': mock('@datetime()'),
        'user_icon': Random.image('100x100', '#50B347', '#fff', 'LiSoul'),
        'student_id': mock('@word(5)'),
        'user_name': mock('@cname()'),
        'user_nick': mock('@word(5)'),
        'user_introduce': Random.paragraph(),
        'user_power': mock('@integer(0, 4)'),
        'user_score': mock('@integer(100, 10000)'),
        'user_sex': mock('@integer(0, 1)'),
        'user_telephone': mock('@string("number", 11)'),
        'user_email': Random.email(),
        'user_birthday': mock('@datetime()'),
        'user_school': null,
        'user_address': mock('@county(true)')
    }
    return data
}

export default [
    {
        url: '/api/user/login/',
        method: 'get',
        data: mock('@string("number", 4)')
    },
    {
        url: '/api/user/login/',
        method: 'post',
        data: {
            message: '登陆成功',
            token: '@word(64)'
        }
    },
    {
        url: '/api/user/get_user_info/',
        method: 'get',
        data: getUserInfo()
    },
    {
        url: '/api/getrank/',
        method: 'get',
        data: getRankList()
    }
]