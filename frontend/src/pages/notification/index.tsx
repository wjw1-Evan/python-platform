import { BellOutlined } from '@ant-design/icons';
import type { ActionType, ProColumns } from '@ant-design/pro-components';
import { ProTable } from '@ant-design/pro-components';
import { Badge, Button, message, Space, Tag } from 'antd';
import React, { useEffect, useRef, useState } from 'react';
import { notificationAPI } from '@/services/api';
import { NotificationWebSocket } from '@/utils/websocket';
import type { Notification } from '@/services/ant-design-pro/typings';

const NotificationList: React.FC = () => {
  const actionRef = useRef<ActionType>();
  const [unreadCount, setUnreadCount] = useState(0);
  const [ws, setWs] = useState<NotificationWebSocket | null>(null);

  useEffect(() => {
    // 获取未读数量
    const fetchUnreadCount = async () => {
      try {
        const response = await notificationAPI.getUnreadCount();
        setUnreadCount(response.count || 0);
      } catch (error) {
        console.error('获取未读数量失败:', error);
      }
    };

    fetchUnreadCount();

    // 建立 WebSocket 连接
    const token = localStorage.getItem('access_token');
    if (token) {
      const websocket = new NotificationWebSocket(token);
      websocket.onMessage((data) => {
        // 收到新通知，刷新列表和未读数量
        if (data.type === 'notification') {
          message.info(`收到新通知: ${data.title}`);
          actionRef.current?.reload();
          fetchUnreadCount();
        }
      });
      websocket.connect();
      setWs(websocket);
    }

    return () => {
      if (ws) {
        ws.disconnect();
      }
    };
  }, []);

  const handleMarkRead = async (record: Notification) => {
    try {
      await notificationAPI.markRead(record.id!);
      message.success('已标记为已读');
      actionRef.current?.reload();
      // 刷新未读数量
      const response = await notificationAPI.getUnreadCount();
      setUnreadCount(response.count || 0);
    } catch (error) {
      message.error('操作失败');
    }
  };

  const handleMarkAllRead = async () => {
    try {
      await notificationAPI.markAllRead();
      message.success('已全部标记为已读');
      actionRef.current?.reload();
      setUnreadCount(0);
    } catch (error) {
      message.error('操作失败');
    }
  };

  const columns: ProColumns<Notification>[] = [
    {
      title: 'ID',
      dataIndex: 'id',
      hideInTable: true,
      hideInSearch: true,
    },
    {
      title: '标题',
      dataIndex: 'title',
      valueType: 'text',
    },
    {
      title: '内容',
      dataIndex: 'content',
      valueType: 'text',
      ellipsis: true,
    },
    {
      title: '类型',
      dataIndex: 'notification_type',
      valueType: 'select',
      valueEnum: {
        info: { text: '信息', status: 'Default' },
        success: { text: '成功', status: 'Success' },
        warning: { text: '警告', status: 'Warning' },
        error: { text: '错误', status: 'Error' },
      },
      render: (_, record) => {
        const typeMap: Record<string, { color: string; text: string }> = {
          info: { color: 'blue', text: '信息' },
          success: { color: 'green', text: '成功' },
          warning: { color: 'orange', text: '警告' },
          error: { color: 'red', text: '错误' },
        };
        const type = typeMap[record.notification_type || 'info'] || typeMap.info;
        return <Tag color={type.color}>{type.text}</Tag>;
      },
    },
    {
      title: '状态',
      dataIndex: 'is_read',
      valueType: 'select',
      valueEnum: {
        true: {
          text: '已读',
          status: 'Default',
        },
        false: {
          text: '未读',
          status: 'Processing',
        },
      },
      render: (_, record) => (
        <Badge
          status={record.is_read ? 'default' : 'processing'}
          text={record.is_read ? '已读' : '未读'}
        />
      ),
    },
    {
      title: '创建时间',
      dataIndex: 'created_at',
      valueType: 'dateTime',
      hideInSearch: true,
      sorter: true,
    },
    {
      title: '操作',
      valueType: 'option',
      key: 'option',
      render: (_, record) => [
        !record.is_read && (
          <a
            key="markRead"
            onClick={() => {
              handleMarkRead(record);
            }}
          >
            标记已读
          </a>
        ),
      ],
    },
  ];

  return (
    <>
      <ProTable<Notification>
        headerTitle={
          <Space>
            <BellOutlined />
            <span>通知中心</span>
            {unreadCount > 0 && (
              <Badge count={unreadCount} showZero={false} />
            )}
          </Space>
        }
        actionRef={actionRef}
        rowKey="id"
        search={{
          labelWidth: 120,
        }}
        toolBarRender={() => [
          <Button key="markAll" onClick={handleMarkAllRead}>
            全部标记为已读
          </Button>,
        ]}
        request={async (params) => {
          try {
            const response = await notificationAPI.getNotifications({
              page: params.current,
              page_size: params.pageSize,
            });
            return {
              data: response.items || [],
              success: true,
              total: response.total || 0,
            };
          } catch (error) {
            return {
              data: [],
              success: false,
              total: 0,
            };
          }
        }}
        columns={columns}
      />
    </>
  );
};

export default NotificationList;
