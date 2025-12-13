import { GithubOutlined } from '@ant-design/icons';
import { DefaultFooter } from '@ant-design/pro-components';
import React from 'react';

const Footer: React.FC = () => {
  return (
    <DefaultFooter
      style={{
        background: 'none',
        color: 'rgba(255, 255, 255, 0.8)',
      }}
      copyright={
        <span style={{ color: 'rgba(255, 255, 255, 0.8)' }}>
          Powered by Ant Design Pro
        </span>
      }
      links={[
        {
          key: 'Ant Design Pro',
          title: (
            <span style={{ color: 'rgba(255, 255, 255, 0.8)' }}>
              Ant Design Pro
            </span>
          ),
          href: 'https://pro.ant.design',
          blankTarget: true,
        },
        {
          key: 'github',
          title: (
            <GithubOutlined style={{ color: 'rgba(255, 255, 255, 0.8)' }} />
          ),
          href: 'https://github.com/ant-design/ant-design-pro',
          blankTarget: true,
        },
        {
          key: 'Ant Design',
          title: (
            <span style={{ color: 'rgba(255, 255, 255, 0.8)' }}>
              Ant Design
            </span>
          ),
          href: 'https://ant.design',
          blankTarget: true,
        },
      ]}
    />
  );
};

export default Footer;
