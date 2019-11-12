const path = require('path');

module.exports = {
  assetsDir: '../static',
  baseUrl: '',
  publicPath: undefined,
  outputDir: path.resolve(__dirname, '../app/templates'),
  runtimeCompiler: undefined,
  productionSourceMap: undefined,
  parallel: undefined,
  css: undefined
};




// module.exports = {
//     devServer: {
//          proxy: "http://localhost:5000"
//     }
// }