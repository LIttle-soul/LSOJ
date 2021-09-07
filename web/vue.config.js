const MonacoWebpackPlugin = require("monaco-editor-webpack-plugin");
const webpack = require('webpack')

module.exports = {
  devServer: {
    open: true,
    host: "localhost",
    port: 8080,
    https: false,
    // proxy: {
    //   "/api": {
    //     // target: "http://81.70.218.179:8081/",
    //     // target: 'http://192.168.123.83:8081/',
    //     target: 'http://127.0.0.1:8081/',
    //     ws: true,
    //     secure: false,
    //     changOrigin: true,
    //     pathRewrite: {
    //       "^/api": "",
    //     },
    //   },
    // },
  },
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
        $: 'jquery',
        jQuery: 'jquery',
        'windows.jQuery': 'jquery'
      })
    ],
  },
};
