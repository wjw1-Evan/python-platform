# 前端项目说明

## 创建Ant Design Pro项目

使用以下命令创建Ant Design Pro项目：

```bash
# 安装umi
npm install -g umi

# 创建项目
pro create platform

# 或使用npx
npx @ant-design/pro-cli create platform
```

## 项目结构

创建后的项目结构应该类似：

```
platform/
├── config/              # 配置文件
├── src/
│   ├── components/      # 组件
│   ├── pages/           # 页面
│   ├── services/        # API服务
│   ├── utils/           # 工具函数
│   ├── app.tsx          # 应用入口
│   └── ...
├── package.json
└── ...
```

## 配置API地址

在 `config/config.ts` 或 `.umirc.ts` 中配置后端API地址：

```typescript
export default {
  // ...
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true,
    },
  },
};
```

## 配置认证

在 `src/app.tsx` 中配置认证：

```typescript
export const request = {
  // 请求拦截器
  requestInterceptors: [
    (url: string, options: any) => {
      const token = localStorage.getItem('token');
      if (token) {
        options.headers = {
          ...options.headers,
          Authorization: `Bearer ${token}`,
        };
      }
      
      // 添加企业ID
      const companyId = localStorage.getItem('currentCompanyId');
      if (companyId) {
        options.headers = {
          ...options.headers,
          'X-Company-Id': companyId,
        };
      }
      
      return { url, options };
    },
  ],
};
```

## 主要功能页面

需要创建以下页面：

1. **用户登录/注册** (`src/pages/user/login/`)
2. **企业管理** (`src/pages/companies/`)
3. **用户管理** (`src/pages/users/`)
4. **通知中心** (`src/pages/notifications/`)
5. **日志查看** (`src/pages/logs/`)

## API服务示例

在 `src/services/api.ts` 中定义API：

```typescript
import { request } from '@umijs/max';

export async function login(data: { username: string; password: string }) {
  return request('/api/auth/login/', {
    method: 'POST',
    data,
  });
}

export async function getCompanies() {
  return request('/api/companies/');
}
```

## 环境变量

创建 `.env` 文件：

```
REACT_APP_API_URL=http://localhost:8000/api
```
