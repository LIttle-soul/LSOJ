---
title: vue-cookies常用操作
tags: [前端, Vue3]
categories: [前端, Vue3]
# index_img: /image/page_image/git1.jpg
banner_img: /image/background/background11.jpg
date: 2021-08-10 08:00:00
hide: false
---

### 1. 简介

> cookies 在前端开发项目中是常用的功能之一，几乎所有的浏览器都支持原生的 cookies，并且后端接口可以直接写入 cookies，这点相对于 localStore 来说算个小优势，而在大多数情况下项目开发会选择 vue 框架，因为 vue 框架开发效率高，也更易于后期的升级迭代和维护。vue-cookies 就是为 vue 框架打造的一款操作 cookies 的工具。

### 2. 安装

- 在终端中执行如下命令

```bash
$ npm install vue-cookies --save
```

> 此命令会将 vue-cookies 的文件包保存到正在开发项目的 node_models 目录下面

### 3. 引入

- 在项目文件中的 main.js 中设置

```javascript
// vue-cookies配置
import cookies from "vue-cookies";

// vue2中的设置方式
Vue.prototype.$cookies = cookies;

// vue3中的设置方式
app.config.globalProperties.$cookies = cookies;
```

### 4. 使用

1. 设置 cookies

```javascript
this.$cookies.set(keyName, value[, expireTimes[, path[, domain[, secure]]]])   //return this

// 简洁使用
this.$cookies.set('key','value', '过期时间,按秒计');

// 示例
this.$cookies.set('username',response.data.username, '7d');
```

2. 获取 cookies

```javascript
this.$cookies.get(keyName); // return value
```

3. 删除 cookies

```javascript
this.$cookies.remove("key");
```

4. 判断 cookies 中是否有指定的 key

```javascript
this.$cookies.isKey(keyName);
```

5. 获取所有的 cookies

```javascript
this.$cookies.keys();
```
