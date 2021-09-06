const MonacoWebpackPlugin = require("monaco-editor-webpack-plugin");
const webpack = require('webpack')

module.exports = {
  devServer: {
    open: true,
    host: "localhost",
    port: 8080,
    https: false,
    // proxy: {
    //     '/api': {
    //         target: 'http://serve.iqgb.py/eijmssmw/',
    //         ws: true,
    //         secure: false,
    //         changOrigin: true,
    //         pathRewrite: {
    //             '^/api': ''
    //         }
    //     }
    // }
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
        'windows.jQoery': 'jquery'
      })
    ],
  },
};
