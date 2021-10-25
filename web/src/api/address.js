import http from "@/utils/http";

export const getAddressList = () => {
  return http({
    url: "/api/address/getaddresslist/",
    method: "get",
  }).then((res) => {
    // console.log(res);
    return res.data;
  });
};

export const getProvinceList = () => {
  return http({
    url: "/api/address/getprovince/",
    method: "get",
  }).then((res) => {
    // console.log(res);
    return res.data;
  });
};

export const getMunicipalityList = () => {
  return http({
    url: "/api/address/getmunicipality/",
    method: "get",
  }).then((res) => {
    // console.log(res);
    return res.data;
  });
};
