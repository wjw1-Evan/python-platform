/**
 * @name 代理的配置
 * @see 在生产环境 代理是无法生效的，所以这里没有生产环境的配置
 * -------------------------------
 * The agent cannot take effect in the production environment
 * so there is no configuration of the production environment
 * For details, please see
 * https://pro.ant.design/docs/deploy
 *
 * @doc https://umijs.org/docs/guides/proxy
 */
export default {
  /**
   * @name 开发环境代理配置
   * @description 将 /api/ 请求代理到后端API网关
   */
  dev: {
    '/api/': {
      target: 'http://localhost:8000',
      changeOrigin: true,
      // 不重写路径，直接转发 /api/ 到后端
    },
  },
  /**
   * @name 详细的代理配置
   * @doc https://github.com/chimurai/http-proxy-middleware
   */
  test: {
    '/api/': {
      target: 'http://localhost:8000',
      changeOrigin: true,
      // 不重写路径，直接转发 /api/ 到后端
    },
  },
  pre: {
    '/api/': {
      target: 'http://localhost:8000',
      changeOrigin: true,
      // 不重写路径，直接转发 /api/ 到后端
    },
  },
};
