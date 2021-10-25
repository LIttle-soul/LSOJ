function getContestList() {
  const data = [];
  for (var i = 0; i < 238; i++) {
    var text = {
      contest_id: 238 - i,
      contest_title: "@ctitle",
      contest_time: "@datetime",
      contest_type: '@integer(0,3)',
      contest_creator: "@cname",
      contest_status: '@boolean',
      contest_content: "@paragraph",
      duration: "5小时",
      join_people: '@integer(0,1000)',
      contest_power: '@boolean',
    };
    data.push(text);
  }
  return data;
}

export default [
  {
    url: "/api/contest/contest/",
    method: "get",
    data: getContestList(),
  },
];
