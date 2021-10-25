import axios from "axios";

export const upLoadImages = (files) => {
  console.log(files);
  var data = new FormData();
  data.append("images", files[0]);
  return axios.post("/api/problem/upimage/", data).then((res) => {
    console.log(res.data);
    return res.data;
  });
};
