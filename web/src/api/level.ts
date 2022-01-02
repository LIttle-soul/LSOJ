import http from '@/utils/http'

export const getLevelList = () => {
    return http({
        url: '/api/level/getlevellist/',
        method: 'get',
    }).then((res: any) => {
        console.log(res.data);
        return res.data;
    });
};

export const levelCompletion = (data: any) => {
    return http({
        url: '/api/level/levelcompletion/',
        method: 'post',
        data: data
    }).then((res: any) => {
        console.log(res.data);
        return res.data;
    }); 
};

export const addLevel = (data: any) => {
    return http({
        url: '/api/level/addlevel/',
        method: 'post',
        data: data
    }).then((res: any) => {
        console.log(res.data);
        return res.data;
    });
};
export const editLevel = (data: any) => {
    return http({
        url: '/api/level/editlevel/',
        method: 'post',
        data: data
    }).then((res: any) => {
        console.log(res.data);
        return res.data;
    });
};
export const deleteLevel = (data: any) => {
    return http({
        url: '/api/level/deletelevel/',
        method: 'post',
        data: data
    }).then((res: any) => {
        console.log(res.data);
        return res.data;
    });
};
export const editHideLevel = (data: any) => {
    return http({
        url: '/api/level/edithidelevel/',
        method: 'get',
        params: data
    }).then((res: any) => {
        console.log(res.data);
        return res.data;
    });
};
export const edithideLevel = (data: any) => {
    return http({
        url: '/api/level/edithidelevel/',
        method: 'post',
        data: data
    }).then((res: any) => {
        console.log(res.data);
        return res.data;
    });
};
export const levelMove = (data: any) => {
    return http({
        url: '/api/level/levelmove/',
        method: 'post',
        data: data
    }).then((res: any) => {
        console.log(res.data);
        return res.data;
    });
};

export const smallLevelMove = (data: any) => {
    return http({
        url: '/api/level/smalllevelmove/',
        method: 'get',
        params: data
    }).then((res: any) => {
        // console.log(res.data);
        return res.data;
    });
};

export const levelProblem = (data: any) => {
    return http({
        url: '/api/level/levelproblem/',
        method: 'get',
        params: data
    }).then((res: any) => {
        // console.log(res.data);
        return res.data;
    }); 
};
export const searchLevel = (data: any) => {
    return http({
        url: '/api/level/searchlevel/',
        method: 'get',
        params: data
    }).then((res: any) => {
        console.log(res.data);
        return res.data;
    });
};
export const searchProblem = (data: any) => {
    return http({
        url: '/api/level/searchproblem/',
        method: 'get',
        params: data
    }).then((res: any) => {
        console.log(res.data);
        return res.data;
    });
};
export const getProblem = (data: any) => {
    return http({
        url: '/api/level/getproblem/',
        method: 'get',
        params: data
    }).then((res: any) => {
        console.log(res.data);
        return res.data;
    });
};