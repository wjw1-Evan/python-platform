import type { ActionType, ProColumns } from '@ant-design/pro-components';
import { ProTable } from '@ant-design/pro-components';
import { Button, message, Modal } from 'antd';
import React, { useRef } from 'react';
import { companyAPI } from '@/services/api';
import type { Company } from '@/services/ant-design-pro/typings';

const CompanyList: React.FC = () => {
  const actionRef = useRef<ActionType>();

  const handleJoin = async (record: Company) => {
    Modal.confirm({
      title: '确认加入',
      content: `确定要加入企业 ${record.name} 吗？`,
      onOk: async () => {
        try {
          // 这里需要获取当前用户ID，暂时使用提示
          message.warning('请先选择要加入的用户');
        } catch (error) {
          message.error('加入失败');
        }
      },
    });
  };

  const handleLeave = async (record: Company) => {
    Modal.confirm({
      title: '确认退出',
      content: `确定要退出企业 ${record.name} 吗？`,
      onOk: async () => {
        try {
          await companyAPI.leaveCompany(record.id!);
          message.success('退出成功');
          actionRef.current?.reload();
        } catch (error) {
          message.error('退出失败');
        }
      },
    });
  };

  const columns: ProColumns<Company>[] = [
    {
      title: 'ID',
      dataIndex: 'id',
      hideInTable: true,
      hideInSearch: true,
    },
    {
      title: '企业名称',
      dataIndex: 'name',
      tip: '企业名称',
      formItemProps: {
        rules: [
          {
            required: true,
            message: '企业名称为必填项',
          },
        ],
      },
    },
    {
      title: '描述',
      dataIndex: 'description',
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
    {
      title: '更新时间',
      dataIndex: 'updated_at',
      valueType: 'dateTime',
      hideInSearch: true,
      sorter: true,
    },
    {
      title: '操作',
      valueType: 'option',
      key: 'option',
      render: (_, record) => [
        <a
          key="join"
          onClick={() => {
            handleJoin(record);
          }}
        >
          加入
        </a>,
        <a
          key="leave"
          onClick={() => {
            handleLeave(record);
          }}
        >
          退出
        </a>,
      ],
    },
  ];

  return (
    <ProTable<Company>
      headerTitle="企业列表"
      actionRef={actionRef}
      rowKey="id"
      search={{
        labelWidth: 120,
      }}
      request={async (params) => {
        try {
          const response = await companyAPI.getCompanies({
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
  );
};

export default CompanyList;
