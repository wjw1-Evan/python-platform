# 前端 API 集成指南

本文档说明如何将创建的前端项目与后端 API 集成。

## 1. API 服务配置

在 `src/services/` 目录下创建 `api.ts` 文件：

```typescript
import { request } from '@umijs/max';

const API_BASE = '/api';

// 认证相关API
export const authAPI = {
  login: (data: { username: string; password: string; company_id?: string }) => {
    return request(`${API_BASE}/auth/login/`, {
      method: 'POST',
      data,
    });
  },
  
  register: (data: { username: string; email: string; password: string; company_name?: string }) => {
    return request(`${API_BASE}/auth/register/`, {
      method: 'POST',
      data,
    });
  },
  
  refreshToken: (refresh: string) => {
    return request(`${API_BASE}/auth/refresh/`, {
      method: 'POST',
      data: { refresh },
    });
  },
};

// 用户相关API
export const userAPI = {
  getUsers: (params?: { page?: number; page_size?: number; search?: string }) => {
    return request(`${API_BASE}/users/`, {
      method: 'GET',
      params,
    });
  },
  
  getUser: (userId: string) => {
    return request(`${API_BASE}/users/${userId}/`, {
      method: 'GET',
    });
  },
  
  updateUser: (userId: string, data: any) => {
    return request(`${API_BASE}/users/${userId}/`, {
      method: 'PUT',
      data,
    });
  },
  
  deleteUser: (userId: string) => {
    return request(`${API_BASE}/users/${userId}/`, {
      method: 'DELETE',
    });
  },
};

// 企业相关API
export const companyAPI = {
  getCompanies: () => {
    return request(`${API_BASE}/companies/`, {
      method: 'GET',
    });
  },
  
  getCompany: (companyId: string) => {
    return request(`${API_BASE}/companies/${companyId}/`, {
      method: 'GET',
    });
  },
  
  updateCompany: (companyId: string, data: any) => {
    return request(`${API_BASE}/companies/${companyId}/`, {
      method: 'PUT',
      data,
    });
  },
  
  joinCompany: (companyId: string, data: { user_id: string }) => {
    return request(`${API_BASE}/companies/${companyId}/join/`, {
      method: 'POST',
      data,
    });
  },
  
  leaveCompany: (companyId: string) => {
    return request(`${API_BASE}/companies/${companyId}/leave/`, {
      method: 'POST',
    });
  },
};

// 通知相关API
export const notificationAPI = {
  getNotifications: (params?: { page?: number; page_size?: number }) => {
    return request(`${API_BASE}/notifications/`, {
      method: 'GET',
      params,
    });
  },
  
  getUnreadCount: () => {
    return request(`${API_BASE}/notifications/unread_count/`, {
      method: 'GET',
    });
  },
  
  markRead: (notificationId: string) => {
    return request(`${API_BASE}/notifications/${notificationId}/mark_read/`, {
      method: 'POST',
    });
  },
  
  markAllRead: () => {
    return request(`${API_BASE}/notifications/mark_all_read/`, {
      method: 'POST',
    });
  },
};

// 日志相关API
export const logAPI = {
  getLogs: (params?: { 
    page?: number; 
    page_size?: number; 
    log_type?: string; 
    log_level?: string;
    start_date?: string;
    end_date?: string;
  }) => {
    return request(`${API_BASE}/logs/`, {
      method: 'GET',
      params,
    });
  },
  
  getStatistics: () => {
    return request(`${API_BASE}/logs/statistics/`, {
      method: 'GET',
    });
  },
};
```

## 2. 配置请求拦截器

在 `src/app.tsx` 中添加：

```typescript
import { RequestConfig } from '@umijs/max';
import { message } from 'antd';

export const request: RequestConfig = {
  timeout: 10000,
  errorConfig: {
    errorHandler: (error: any) => {
      const { response } = error;
      if (response && response.status) {
        switch (response.status) {
          case 401:
            message.error('未授权，请重新登录');
            localStorage.removeItem('token');
            window.location.href = '/login';
            break;
          case 403:
            message.error('没有权限访问');
            break;
          case 500:
            message.error('服务器错误');
            break;
          default:
            message.error(response.data?.error || '请求失败');
        }
      }
    },
  },
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

## 3. WebSocket 连接

创建 `src/utils/websocket.ts`：

```typescript
export class NotificationWebSocket {
  private ws: WebSocket | null = null;
  private url: string;
  private token: string;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;

  constructor(token: string, wsUrl: string = 'ws://localhost:8005/ws/notifications/') {
    this.token = token;
    this.url = `${wsUrl}?token=${token}`;
  }

  connect(): void {
    this.ws = new WebSocket(this.url);
    
    this.ws.onopen = () => {
      console.log('WebSocket连接已建立');
      this.reconnectAttempts = 0;
    };

    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      // 处理通知消息
    };

    this.ws.onerror = (error) => {
      console.error('WebSocket错误:', error);
    };

    this.ws.onclose = () => {
      if (this.reconnectAttempts < this.maxReconnectAttempts) {
        this.reconnectAttempts++;
        setTimeout(() => this.connect(), 3000);
      }
    };
  }

  disconnect(): void {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }
}
```

## 4. 页面组件示例

### 登录页面 (`src/pages/Login/index.tsx`)

```typescript
import { Form, Input, Button, Card } from 'antd';
import { authAPI } from '@/services/api';
import { history } from '@umijs/max';

export default function Login() {
  const onFinish = async (values: any) => {
    const response = await authAPI.login(values);
    localStorage.setItem('token', response.access);
    history.push('/user');
  };

  return (
    <Card title="登录">
      <Form onFinish={onFinish}>
        <Form.Item name="username">
          <Input placeholder="用户名" />
        </Form.Item>
        <Form.Item name="password">
          <Input.Password placeholder="密码" />
        </Form.Item>
        <Form.Item>
          <Button type="primary" htmlType="submit" block>登录</Button>
        </Form.Item>
      </Form>
    </Card>
  );
}
```

### 用户管理页面 (`src/pages/User/index.tsx`)

```typescript
import { ProTable } from '@ant-design/pro-components';
import { userAPI } from '@/services/api';

export default function UserPage() {
  return (
    <ProTable
      request={async (params) => {
        const response = await userAPI.getUsers(params);
        return {
          data: response.items,
          success: true,
          total: response.total,
        };
      }}
      columns={[
        { title: '用户名', dataIndex: 'username' },
        { title: '邮箱', dataIndex: 'email' },
        { title: '全名', dataIndex: 'full_name' },
      ]}
    />
  );
}
```

## 5. 路由配置

在 `config/routes.ts` 中添加：

```typescript
export default [
  {
    path: '/login',
    component: './Login',
    layout: false,
  },
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

## 6. 环境变量配置

创建 `.env` 文件：

```env
API_BASE_URL=http://localhost:8000
WS_URL=ws://localhost:8005
```

## 7. 代理配置

在 `config/config.ts` 中配置：

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

## 注意事项

1. 确保后端服务运行在正确的端口
2. Token 存储在 localStorage，key 为 `token`
3. 所有 API 请求会自动添加 Authorization 头
4. WebSocket 连接需要 token 作为查询参数
5. 401 错误会自动跳转到登录页
