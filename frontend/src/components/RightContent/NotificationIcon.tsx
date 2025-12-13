import { BellOutlined } from '@ant-design/icons';
import { Badge, Dropdown, List, message } from 'antd';
import React, { useEffect, useState } from 'react';
import { history } from '@umijs/max';
import { notificationAPI } from '@/services/api';
import { NotificationWebSocket } from '@/utils/websocket';
import type { Notification } from '@/services/ant-design-pro/typings';

const NotificationIcon: React.FC = () => {
  const [unreadCount, setUnreadCount] = useState(0);
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [ws, setWs] = useState<NotificationWebSocket | null>(null);

  useEffect(() => {
    // 获取未读数量和最新通知
    const fetchData = async () => {
      try {
        const [countResponse, listResponse] = await Promise.all([
          notificationAPI.getUnreadCount(),
          notificationAPI.getNotifications({ page: 1, page_size: 5 }),
        ]);
        setUnreadCount(countResponse.count || 0);
        setNotifications(listResponse.items || []);
      } catch (error) {
        console.error('获取通知失败:', error);
      }
    };

    fetchData();

    // 建立 WebSocket 连接
    const token = localStorage.getItem('access_token');
    if (token) {
      const websocket = new NotificationWebSocket(token);
      websocket.onMessage((data) => {
        if (data.type === 'notification') {
          // 收到新通知，更新列表和未读数量
          fetchData();
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

  const handleMarkRead = async (notificationId: string) => {
    try {
      await notificationAPI.markRead(notificationId);
      // 更新本地状态
      setNotifications((prev) =>
        prev.map((item) =>
          item.id === notificationId ? { ...item, is_read: true } : item,
        ),
      );
      setUnreadCount((prev) => Math.max(0, prev - 1));
    } catch (error) {
      message.error('操作失败');
    }
  };

  const handleViewAll = () => {
    history.push('/notification');
  };

  const notificationList = (
    <List
      dataSource={notifications}
      locale={{ emptyText: '暂无通知' }}
      style={{ width: 300, maxHeight: 400, overflow: 'auto' }}
      renderItem={(item) => (
        <List.Item
          style={{
            cursor: 'pointer',
            padding: '12px 16px',
            backgroundColor: item.is_read ? undefined : '#e6f7ff',
          }}
          onClick={() => {
            if (!item.is_read) {
              handleMarkRead(item.id!);
            }
          }}
        >
          <List.Item.Meta
            title={
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span>{item.title}</span>
                {!item.is_read && <Badge status="processing" />}
              </div>
            }
            description={
              <div>
                <div style={{ marginBottom: 4 }}>{item.content}</div>
                <div style={{ fontSize: 12, color: '#999' }}>
                  {item.created_at}
                </div>
              </div>
            }
          />
        </List.Item>
      )}
      footer={
        <div style={{ textAlign: 'center', padding: '8px 0' }}>
          <a onClick={handleViewAll}>查看全部</a>
        </div>
      }
    />
  );

  return (
    <Dropdown overlay={notificationList} placement="bottomRight" trigger={['click']}>
      <span style={{ cursor: 'pointer', padding: '0 12px' }}>
        <Badge count={unreadCount} size="small">
          <BellOutlined style={{ fontSize: 18 }} />
        </Badge>
      </span>
    </Dropdown>
  );
};

export default NotificationIcon;
