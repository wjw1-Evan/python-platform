import type { ActionType, ProColumns } from '@ant-design/pro-components';
import { ProTable } from '@ant-design/pro-components';
import { Card, Col, Row, Statistic, Tag } from 'antd';
import React, { useEffect, useRef, useState } from 'react';
import { logAPI } from '@/services/api';
import type { Log } from '@/services/ant-design-pro/typings';

const LogList: React.FC = () => {
  const actionRef = useRef<ActionType>();
  const [statistics, setStatistics] = useState<any>({});

  useEffect(() => {
    // 获取统计信息
    const fetchStatistics = async () => {
      try {
        const response = await logAPI.getStatistics();
        setStatistics(response || {});
      } catch (error) {
        console.error('获取统计信息失败:', error);
      }
    };

    fetchStatistics();
  }, []);

  const columns: ProColumns<Log>[] = [
    {
      title: 'ID',
      dataIndex: 'id',
      hideInTable: true,
      hideInSearch: true,
    },
    {
      title: '日志类型',
      dataIndex: 'log_type',
      valueType: 'select',
      valueEnum: {
        api: { text: 'API', status: 'Default' },
        operation: { text: '操作', status: 'Processing' },
        system: { text: '系统', status: 'Success' },
        error: { text: '错误', status: 'Error' },
      },
      render: (_, record) => {
        const typeMap: Record<string, { color: string; text: string }> = {
          api: { color: 'blue', text: 'API' },
          operation: { color: 'green', text: '操作' },
          system: { color: 'orange', text: '系统' },
          error: { color: 'red', text: '错误' },
        };
        const type = typeMap[record.log_type || 'api'] || typeMap.api;
        return <Tag color={type.color}>{type.text}</Tag>;
      },
    },
    {
      title: '日志级别',
      dataIndex: 'log_level',
      valueType: 'select',
      valueEnum: {
        DEBUG: { text: 'DEBUG', status: 'Default' },
        INFO: { text: 'INFO', status: 'Processing' },
        WARNING: { text: 'WARNING', status: 'Warning' },
        ERROR: { text: 'ERROR', status: 'Error' },
        CRITICAL: { text: 'CRITICAL', status: 'Error' },
      },
      render: (_, record) => {
        const levelMap: Record<string, { color: string }> = {
          DEBUG: { color: 'default' },
          INFO: { color: 'blue' },
          WARNING: { color: 'orange' },
          ERROR: { color: 'red' },
          CRITICAL: { color: 'red' },
        };
        const level = levelMap[record.log_level || 'INFO'] || levelMap.INFO;
        return <Tag color={level.color}>{record.log_level || 'INFO'}</Tag>;
      },
    },
    {
      title: '消息',
      dataIndex: 'message',
      valueType: 'text',
      ellipsis: true,
    },
    {
      title: '用户ID',
      dataIndex: 'user_id',
      valueType: 'text',
      hideInSearch: true,
    },
    {
      title: '企业ID',
      dataIndex: 'company_id',
      valueType: 'text',
      hideInSearch: true,
    },
    {
      title: '创建时间',
      dataIndex: 'created_at',
      valueType: 'dateTime',
      hideInSearch: true,
      sorter: true,
    },
  ];

  return (
    <>
      <Card style={{ marginBottom: 16 }}>
        <Row gutter={16}>
          <Col span={6}>
            <Statistic
              title="总日志数"
              value={statistics.total || 0}
              valueStyle={{ color: '#1890ff' }}
            />
          </Col>
          <Col span={6}>
            <Statistic
              title="API日志"
              value={statistics.api_count || 0}
              valueStyle={{ color: '#52c41a' }}
            />
          </Col>
          <Col span={6}>
            <Statistic
              title="错误日志"
              value={statistics.error_count || 0}
              valueStyle={{ color: '#ff4d4f' }}
            />
          </Col>
          <Col span={6}>
            <Statistic
              title="今日日志"
              value={statistics.today_count || 0}
              valueStyle={{ color: '#faad14' }}
            />
          </Col>
        </Row>
      </Card>

      <ProTable<Log>
        headerTitle="日志列表"
        actionRef={actionRef}
        rowKey="id"
        search={{
          labelWidth: 120,
        }}
        request={async (params) => {
          try {
            const response = await logAPI.getLogs({
              page: params.current,
              page_size: params.pageSize,
              log_type: params.log_type,
              log_level: params.log_level,
              start_date: params.start_date,
              end_date: params.end_date,
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

export default LogList;
