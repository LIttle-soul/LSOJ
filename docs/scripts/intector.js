hexo.extend.injector.register(
  "body_end",
  `<script
        src='https://cdn.bootcdn.net/ajax/libs/canvas-nest.js/2.0.4/canvas-nest.js'
        color='183,20,147'
        pointColor='160,0,100'
        opacity='0.8'
        zIndex='-1'
        count='500'
    ></script>`
);

hexo.extend.injector.register(
  "head_end",
  `<script src='/js/FunnyTitle.js'></script>`
);

hexo.extend.injector.register(
  "head_end",
  `<script src='/live2d-widget/autoload.js'></script>`
);

// hexo.extend.injector.register(
//   "head_end",
//   `<link rel="stylesheet" href='/css/mouse.css'>`
// );

hexo.extend.injector.register(
  "head_end",
  `<link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/font-awesome@4.7.0/css/font-awesome.min.css'>
  <link rel='stylesheet' href='/css/live2d.css'>`
);

hexo.extend.injector.register(
  "head_end",
  `<script src='/js/WaifuMove.js'></script>`
);
