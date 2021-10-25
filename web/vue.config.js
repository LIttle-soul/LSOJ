const MonacoWebpackPlugin = require("monaco-editor-webpack-plugin");
const webpack = require("webpack");

module.exports = {
  devServer: {
    open: true,
    host: "0.0.0.0",
    port: 8080,
    https: false,
    proxy: {
      "/api": {
        // target: "http://124.71.143.224:8080/",
        target: "http://10.46.3.131:8081/",
        // target: "http://127.0.0.1:8081/",
        ws: true,
        secure: false,
        changOrigin: true,
        pathRewrite: {
          "^/api": "",
        },
      },
    },
  },
  // publicPath: process.env.NODE_ENV === "production" ? "./" : "/",
  configureWebpack: {
    module: {
      rules: [
        {
          test: /\.md$/,
          use: "text-loader",
        },
      ],
    },
    plugins: [
      new MonacoWebpackPlugin(),
      new webpack.ProvidePlugin({
        $: "jquery",
        jQuery: "jquery",
        "windows.jQuery": "jquery",
      }),
    ],
  },
};
