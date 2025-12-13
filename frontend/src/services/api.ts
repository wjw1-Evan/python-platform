import { request } from '@umijs/max';

const API_BASE = '/api';

// 认证相关API
export const authAPI = {
  /**
   * 用户登录
   */
  login: (data: { username: string; password: string; company_id?: string }) => {
    return request<{
      message: string;
      user_id: string;
      company_id: string;
      access: string;
      refresh: string;
    }>(`${API_BASE}/auth/login/`, {
      method: 'POST',
      data,
    });
  },

  /**
   * 用户注册
   */
  register: (data: {
    username: string;
    email: string;
    password: string;
    company_name?: string;
  }) => {
    return request<{
      message: string;
      user_id: string;
      company_id: string;
    }>(`${API_BASE}/auth/register/`, {
      method: 'POST',
      data,
    });
  },

  /**
   * 刷新Token
   */
  refreshToken: (refresh: string) => {
    return request<{
      access: string;
      refresh?: string;
    }>(`${API_BASE}/auth/refresh/`, {
      method: 'POST',
      data: { refresh },
    });
  },
};

// 用户相关API
export const userAPI = {
  /**
   * 获取用户列表
   */
  getUsers: (params?: {
    page?: number;
    page_size?: number;
    search?: string;
  }) => {
    return request<{
      items: any[];
      total: number;
      page: number;
      page_size: number;
    }>(`${API_BASE}/users/`, {
      method: 'GET',
      params,
    });
  },

  /**
   * 获取用户详情
   */
  getUser: (userId: string) => {
    return request<any>(`${API_BASE}/users/${userId}/`, {
      method: 'GET',
    });
  },

  /**
   * 更新用户信息
   */
  updateUser: (userId: string, data: any) => {
    return request<any>(`${API_BASE}/users/${userId}/`, {
      method: 'PUT',
      data,
    });
  },

  /**
   * 删除用户
   */
  deleteUser: (userId: string) => {
    return request<{ message: string }>(`${API_BASE}/users/${userId}/`, {
      method: 'DELETE',
    });
  },
};

// 企业相关API
export const companyAPI = {
  /**
   * 获取企业列表
   */
  getCompanies: (params?: { page?: number; page_size?: number }) => {
    return request<{
      items: any[];
      total: number;
      page: number;
      page_size: number;
    }>(`${API_BASE}/companies/`, {
      method: 'GET',
      params,
    });
  },

  /**
   * 获取企业详情
   */
  getCompany: (companyId: string) => {
    return request<any>(`${API_BASE}/companies/${companyId}/`, {
      method: 'GET',
    });
  },

  /**
   * 更新企业信息
   */
  updateCompany: (companyId: string, data: any) => {
    return request<any>(`${API_BASE}/companies/${companyId}/`, {
      method: 'PUT',
      data,
    });
  },

  /**
   * 用户加入企业
   */
  joinCompany: (companyId: string, data: { user_id: string }) => {
    return request<{ message: string }>(`${API_BASE}/companies/${companyId}/join/`, {
      method: 'POST',
      data,
    });
  },

  /**
   * 用户退出企业
   */
  leaveCompany: (companyId: string) => {
    return request<{ message: string }>(`${API_BASE}/companies/${companyId}/leave/`, {
      method: 'POST',
    });
  },
};

// 通知相关API
export const notificationAPI = {
  /**
   * 获取通知列表
   */
  getNotifications: (params?: { page?: number; page_size?: number }) => {
    return request<{
      items: any[];
      total: number;
      page: number;
      page_size: number;
    }>(`${API_BASE}/notifications/`, {
      method: 'GET',
      params,
    });
  },

  /**
   * 获取未读通知数量
   */
  getUnreadCount: () => {
    return request<{ count: number }>(`${API_BASE}/notifications/unread_count/`, {
      method: 'GET',
    });
  },

  /**
   * 标记通知为已读
   */
  markRead: (notificationId: string) => {
    return request<{ message: string }>(
      `${API_BASE}/notifications/${notificationId}/mark_read/`,
      {
        method: 'POST',
      },
    );
  },

  /**
   * 标记所有通知为已读
   */
  markAllRead: () => {
    return request<{ message: string }>(`${API_BASE}/notifications/mark_all_read/`, {
      method: 'POST',
    });
  },
};

// 日志相关API
export const logAPI = {
  /**
   * 获取日志列表
   */
  getLogs: (params?: {
    page?: number;
    page_size?: number;
    log_type?: string;
    log_level?: string;
    start_date?: string;
    end_date?: string;
  }) => {
    return request<{
      items: any[];
      total: number;
      page: number;
      page_size: number;
    }>(`${API_BASE}/logs/`, {
      method: 'GET',
      params,
    });
  },

  /**
   * 获取日志统计
   */
  getStatistics: () => {
    return request<any>(`${API_BASE}/logs/statistics/`, {
      method: 'GET',
    });
  },
};
