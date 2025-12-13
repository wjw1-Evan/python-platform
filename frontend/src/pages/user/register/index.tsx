import {
  LockOutlined,
  MailOutlined,
  UserOutlined,
  BankOutlined,
} from '@ant-design/icons';
import {
  ProForm,
  ProFormText,
} from '@ant-design/pro-components';
import {
  FormattedMessage,
  Helmet,
  SelectLang,
  useIntl,
  useModel,
  history,
} from '@umijs/max';
import { App, Card } from 'antd';
import { createStyles } from 'antd-style';
import React, { useState } from 'react';
import { Footer } from '@/components';
import { authAPI } from '@/services/api';
import Settings from '../../../../config/defaultSettings';

const useStyles = createStyles(({ token }) => {
  return {
    container: {
      display: 'flex',
      flexDirection: 'column',
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      position: 'relative',
      overflow: 'hidden',
      '&::before': {
        content: '""',
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        background:
          'radial-gradient(circle at 20% 50%, rgba(120, 119, 198, 0.3) 0%, transparent 50%), radial-gradient(circle at 80% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%)',
        pointerEvents: 'none',
      },
    },
    lang: {
      width: 42,
      height: 42,
      lineHeight: '42px',
      position: 'fixed',
      right: 24,
      top: 24,
      borderRadius: token.borderRadius,
      zIndex: 100,
      background: 'rgba(255, 255, 255, 0.2)',
      backdropFilter: 'blur(10px)',
      ':hover': {
        backgroundColor: 'rgba(255, 255, 255, 0.3)',
      },
    },
    content: {
      flex: 1,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '24px',
      position: 'relative',
      zIndex: 1,
      minHeight: 0,
    },
    footerWrapper: {
      position: 'relative',
      zIndex: 1,
      padding: '16px 24px',
      background: 'rgba(255, 255, 255, 0.1)',
      backdropFilter: 'blur(10px)',
    },
    card: {
      width: '100%',
      maxWidth: 480,
      borderRadius: '16px',
      boxShadow: '0 20px 60px rgba(0, 0, 0, 0.3)',
      background: 'rgba(255, 255, 255, 0.95)',
      backdropFilter: 'blur(10px)',
      border: '1px solid rgba(255, 255, 255, 0.2)',
      animation: '$slideUp 0.5s ease-out',
    },
    '@keyframes slideUp': {
      '0%': {
        opacity: 0,
        transform: 'translateY(30px)',
      },
      '100%': {
        opacity: 1,
        transform: 'translateY(0)',
      },
    },
    header: {
      textAlign: 'center',
      marginBottom: 32,
    },
    logo: {
      width: 64,
      height: 64,
      margin: '0 auto 16px',
      borderRadius: '12px',
      background: `linear-gradient(135deg, ${token.colorPrimary} 0%, #764ba2 100%)`,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      fontSize: 32,
      color: '#fff',
      boxShadow: '0 4px 12px rgba(102, 126, 234, 0.4)',
    },
    title: {
      fontSize: 28,
      fontWeight: 600,
      color: token.colorTextHeading,
      marginBottom: 8,
    },
    subtitle: {
      fontSize: 14,
      color: token.colorTextSecondary,
    },
    formItem: {
      marginBottom: 20,
    },
    footer: {
      textAlign: 'center',
      marginTop: 24,
      color: token.colorTextSecondary,
      fontSize: 14,
    },
    link: {
      color: token.colorPrimary,
      fontWeight: 500,
      textDecoration: 'none',
      '&:hover': {
        textDecoration: 'underline',
      },
    },
  };
});

const Lang = () => {
  const { styles } = useStyles();
  return (
    <div className={styles.lang} data-lang>
      {SelectLang && <SelectLang />}
    </div>
  );
};

const Register: React.FC = () => {
  const { styles } = useStyles();
  const { message } = App.useApp();
  const intl = useIntl();
  const [loading, setLoading] = useState(false);
  const { setInitialState } = useModel('@@initialState');

  const handleSubmit = async (values: any) => {
    setLoading(true);
    try {
      const response = await authAPI.register({
        username: values.username,
        email: values.email,
        password: values.password,
        company_name: values.company_name,
      });

      message.success('注册成功！请登录');
      setTimeout(() => {
        history.push('/user/login');
      }, 1000);
    } catch (error: any) {
      console.error('注册错误:', error);
      const errorMessage =
        error?.response?.data?.error || error?.message || '注册失败，请重试！';
      message.error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <Helmet>
        <title>
          {intl.formatMessage({
            id: 'menu.register',
            defaultMessage: '注册',
          })}
          {Settings.title && ` - ${Settings.title}`}
        </title>
      </Helmet>
      <Lang />
      <div className={styles.content}>
        <Card className={styles.card} bordered={false}>
          <div className={styles.header}>
            <div className={styles.logo}>
              <img
                alt="logo"
                src="/logo.svg"
                style={{ width: 40, height: 40 }}
                onError={(e) => {
                  const target = e.target as HTMLImageElement;
                  target.style.display = 'none';
                  if (target.parentElement) {
                    target.parentElement.innerHTML = '🚀';
                  }
                }}
              />
            </div>
            <div className={styles.title}>
              {intl.formatMessage({
                id: 'menu.register',
                defaultMessage: '创建账户',
              })}
            </div>
            <div className={styles.subtitle}>
              {intl.formatMessage({
                id: 'pages.layouts.userLayout.title',
                defaultMessage: '加入通用Admin平台',
              })}
            </div>
          </div>

          <ProForm
            onFinish={async (values) => {
              await handleSubmit(values);
            }}
            submitter={{
              searchConfig: {
                submitText: intl.formatMessage({
                  id: 'pages.register.submit',
                  defaultMessage: '注册',
                }),
              },
              resetButtonProps: {
                style: {
                  display: 'none',
                },
              },
              submitButtonProps: {
                loading,
                size: 'large',
                block: true,
                style: {
                  height: 48,
                  fontSize: 16,
                  fontWeight: 500,
                  borderRadius: '8px',
                  background: 'linear-gradient(135deg, #1890ff 0%, #764ba2 100%)',
                  border: 'none',
                  boxShadow: '0 4px 12px rgba(102, 126, 234, 0.4)',
                },
              },
              render: (_, dom) => {
                return (
                  <div>
                    {dom}
                    <div className={styles.footer} style={{ marginTop: 24 }}>
                      <FormattedMessage
                        id="pages.register.hasAccount"
                        defaultMessage="已有账户？"
                      />
                      <a
                        className={styles.link}
                        onClick={() => {
                          history.push('/user/login');
                        }}
                        style={{ marginLeft: 8 }}
                      >
                        <FormattedMessage
                          id="pages.register.login"
                          defaultMessage="立即登录"
                        />
                      </a>
                    </div>
                  </div>
                );
              },
            }}
          >
            <ProFormText
              name="username"
              fieldProps={{
                size: 'large',
                prefix: <UserOutlined style={{ color: '#667eea' }} />,
                style: {
                  borderRadius: '8px',
                  height: 48,
                },
              }}
              placeholder={intl.formatMessage({
                id: 'pages.register.username.placeholder',
                defaultMessage: '请输入用户名',
              })}
              rules={[
                {
                  required: true,
                  message: (
                    <FormattedMessage
                      id="pages.register.username.required"
                      defaultMessage="请输入用户名！"
                    />
                  ),
                },
                {
                  min: 3,
                  message: (
                    <FormattedMessage
                      id="pages.register.username.min"
                      defaultMessage="用户名至少3个字符！"
                    />
                  ),
                },
              ]}
              className={styles.formItem}
            />

            <ProFormText
              name="email"
              fieldProps={{
                size: 'large',
                prefix: <MailOutlined style={{ color: '#667eea' }} />,
                style: {
                  borderRadius: '8px',
                  height: 48,
                },
              }}
              placeholder={intl.formatMessage({
                id: 'pages.register.email.placeholder',
                defaultMessage: '请输入邮箱',
              })}
              rules={[
                {
                  required: true,
                  message: (
                    <FormattedMessage
                      id="pages.register.email.required"
                      defaultMessage="请输入邮箱！"
                    />
                  ),
                },
                {
                  type: 'email',
                  message: (
                    <FormattedMessage
                      id="pages.register.email.invalid"
                      defaultMessage="请输入有效的邮箱地址！"
                    />
                  ),
                },
              ]}
              className={styles.formItem}
            />

            <ProFormText.Password
              name="password"
              fieldProps={{
                size: 'large',
                prefix: <LockOutlined style={{ color: '#667eea' }} />,
                style: {
                  borderRadius: '8px',
                  height: 48,
                },
              }}
              placeholder={intl.formatMessage({
                id: 'pages.register.password.placeholder',
                defaultMessage: '请输入密码',
              })}
              rules={[
                {
                  required: true,
                  message: (
                    <FormattedMessage
                      id="pages.register.password.required"
                      defaultMessage="请输入密码！"
                    />
                  ),
                },
                {
                  min: 6,
                  message: (
                    <FormattedMessage
                      id="pages.register.password.min"
                      defaultMessage="密码至少6位！"
                    />
                  ),
                },
              ]}
              className={styles.formItem}
            />

            <ProFormText.Password
              name="confirm"
              dependencies={['password']}
              fieldProps={{
                size: 'large',
                prefix: <LockOutlined style={{ color: '#667eea' }} />,
                style: {
                  borderRadius: '8px',
                  height: 48,
                },
              }}
              placeholder={intl.formatMessage({
                id: 'pages.register.confirm.placeholder',
                defaultMessage: '请确认密码',
              })}
              rules={[
                {
                  required: true,
                  message: (
                    <FormattedMessage
                      id="pages.register.confirm.required"
                      defaultMessage="请确认密码！"
                    />
                  ),
                },
                ({ getFieldValue }) => ({
                  validator(_, value) {
                    if (!value || getFieldValue('password') === value) {
                      return Promise.resolve();
                    }
                    return Promise.reject(
                      new Error(
                        intl.formatMessage({
                          id: 'pages.register.confirm.mismatch',
                          defaultMessage: '两次输入的密码不一致！',
                        }),
                      ),
                    );
                  },
                }),
              ]}
              className={styles.formItem}
            />

            <ProFormText
              name="company_name"
              fieldProps={{
                size: 'large',
                prefix: <BankOutlined style={{ color: '#667eea' }} />,
                style: {
                  borderRadius: '8px',
                  height: 48,
                },
              }}
              placeholder={intl.formatMessage({
                id: 'pages.register.company.placeholder',
                defaultMessage: '企业名称（可选）',
              })}
              className={styles.formItem}
            />
          </ProForm>
        </Card>
      </div>
      <div className={styles.footerWrapper}>
        <Footer />
      </div>
    </div>
  );
};

export default Register;
