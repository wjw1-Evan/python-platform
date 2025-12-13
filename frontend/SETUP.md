# 前端项目设置指南

## 使用 Ant Design Pro CLI 创建项目

### 1. 安装 Pro CLI

```bash
npm install -g @ant-design/pro-cli
```

### 2. 创建项目

在 `frontend` 目录下执行：

```bash
cd frontend
pro create platform
```

### 3. 选择配置选项

当提示时，请选择以下配置：

- **模板**: 选择 `umi` (Umi Max)
- **语言**: 选择 `TypeScript`
- **包管理器**: 选择 `npm` 或 `yarn`
- **功能**: 选择完整功能（包括 ProLayout、ProTable 等）

### 4. 安装依赖

```bash
cd platform
npm install
```

### 5. 配置 API 代理

创建或编辑 `config/config.ts`，添加以下配置：

```typescript
export default {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true,
      pathRewrite: { '^/api': '/api' },
    },
  },
};
```

### 6. 配置路由

在 `config/routes.ts` 或 `src/app.tsx` 中添加路由配置：

```typescript
export default [
  {
    path: '/',
    redirect: '/user',
  },
  {
    name: '用户管理',
    path: '/user',
    component: './User',
  },
  {
    name: '企业管理',
    path: '/company',
    component: './Company',
  },
  {
    name: '通知',
    path: '/notification',
    component: './Notification',
  },
  {
    name: '日志',
    path: '/log',
    component: './Log',
  },
];
```

### 7. 配置请求拦截器

在 `src/app.tsx` 中添加：

```typescript
export const request = {
  requestInterceptors: [
    (config: any) => {
      const token = localStorage.getItem('token');
      if (token) {
        config.headers = {
          ...config.headers,
          Authorization: `Bearer ${token}`,
        };
      }
      return config;
    },
  ],
};
```

### 8. 启动开发服务器

```bash
npm start
```

项目将在 http://localhost:8000 启动（如果端口被占用，会自动使用其他端口）

## 项目结构说明

创建后的项目结构：

```
frontend/
└── platform/
    ├── src/
    │   ├── pages/          # 页面组件
    │   ├── services/       # API 服务
    │   ├── components/     # 公共组件
    │   └── utils/          # 工具函数
    ├── config/             # 配置文件
    ├── package.json
    └── .umirc.ts
```

## 注意事项

1. 确保后端 API 网关运行在 `http://localhost:8000`
2. 确保 WebSocket 服务运行在 `ws://localhost:8005`
3. Token 存储在 localStorage 中，key 为 `token`
4. 用户信息存储在 localStorage 中，key 为 `userInfo`
