window.onload = () => {
  //元素鼠标按下事件
  //当鼠标在这个元素身上按下的时候 就会触发回调函数
  var box = document.getElementById("waifu");
  if (box) {
    box.onmousedown = function (e) {
      let disx = e.pageX - box.offsetLeft;
      let disy = e.pageY - box.offsetTop;
      document.onmousemove = function (e) {
        box.style.left = e.pageX - disx + "px";
        box.style.top = e.pageY - disy + "px";
      };
      //释放鼠标按钮，将事件清空，否则始终会跟着鼠标移动
      document.onmouseup = function () {
        document.onmousemove = document.onmouseup = null;
      };
    };
  }
};
