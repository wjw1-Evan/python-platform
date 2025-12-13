import { LockOutlined, UserOutlined } from '@ant-design/icons';
import {
  ProForm,
  ProFormCheckbox,
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
import { Alert, App, Card } from 'antd';
import { createStyles } from 'antd-style';
import React, { useState } from 'react';
import { flushSync } from 'react-dom';
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
      maxWidth: 440,
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
    submitButton: {
      height: 48,
      fontSize: 16,
      fontWeight: 500,
      borderRadius: '8px',
      background: `linear-gradient(135deg, ${token.colorPrimary} 0%, #764ba2 100%)`,
      border: 'none',
      boxShadow: '0 4px 12px rgba(102, 126, 234, 0.4)',
      transition: 'all 0.3s',
      '&:hover': {
        transform: 'translateY(-2px)',
        boxShadow: '0 6px 16px rgba(102, 126, 234, 0.5)',
      },
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

const LoginMessage: React.FC<{
  content: string;
}> = ({ content }) => {
  return (
    <Alert
      style={{
        marginBottom: 24,
        borderRadius: '8px',
      }}
      message={content}
      type="error"
      showIcon
    />
  );
};

const Login: React.FC = () => {
  const [userLoginState, setUserLoginState] = useState<API.LoginResult>({});
  const [loading, setLoading] = useState(false);
  const { initialState, setInitialState } = useModel('@@initialState');
  const { styles } = useStyles();
  const { message } = App.useApp();
  const intl = useIntl();

  const fetchUserInfo = async () => {
    const userInfo = await initialState?.fetchUserInfo?.();
    if (userInfo) {
      flushSync(() => {
        setInitialState((s) => ({
          ...s,
          currentUser: userInfo,
        }));
      });
    }
  };

  const handleSubmit = async (values: API.LoginParams) => {
    setLoading(true);
    try {
      // 调用后端登录API
      const response = await authAPI.login({
        username: values.username || '',
        password: values.password || '',
        company_id: values.company_id,
      });

      // 保存token
      if (response.access) {
        localStorage.setItem('access_token', response.access);
        if (response.refresh) {
          localStorage.setItem('refresh_token', response.refresh);
        }
      }

      const defaultLoginSuccessMessage = intl.formatMessage({
        id: 'pages.login.success',
        defaultMessage: '登录成功！',
      });
      message.success(defaultLoginSuccessMessage);

      // 获取用户信息
      await fetchUserInfo();

      // 跳转
      const urlParams = new URL(window.location.href).searchParams;
      window.location.href = urlParams.get('redirect') || '/';
    } catch (error: any) {
      const defaultLoginFailureMessage = intl.formatMessage({
        id: 'pages.login.failure',
        defaultMessage: '登录失败，请重试！',
      });
      console.error('登录错误:', error);
      const errorMessage =
        error?.response?.data?.error || error?.message || defaultLoginFailureMessage;
      message.error(errorMessage);
      setUserLoginState({
        status: 'error',
        type: 'account',
      });
    } finally {
      setLoading(false);
    }
  };

  const { status } = userLoginState;

  return (
    <div className={styles.container}>
      <Helmet>
        <title>
          {intl.formatMessage({
            id: 'menu.login',
            defaultMessage: '登录页',
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
                id: 'menu.login',
                defaultMessage: '欢迎登录',
              })}
            </div>
            <div className={styles.subtitle}>
              {intl.formatMessage({
                id: 'pages.layouts.userLayout.title',
                defaultMessage: '通用Admin平台',
              })}
            </div>
          </div>

          {status === 'error' && (
            <LoginMessage
              content={intl.formatMessage({
                id: 'pages.login.accountLogin.errorMessage',
                defaultMessage: '账户或密码错误，请重试',
              })}
            />
          )}

          <ProForm
            onFinish={async (values) => {
              await handleSubmit(values as API.LoginParams);
            }}
            submitter={{
              searchConfig: {
                submitText: intl.formatMessage({
                  id: 'pages.login.submit',
                  defaultMessage: '登录',
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
                        id="pages.login.registerAccount"
                        defaultMessage="还没有账户？"
                      />
                      <a
                        className={styles.link}
                        onClick={() => {
                          history.push('/user/register');
                        }}
                        style={{ marginLeft: 8 }}
                      >
                        <FormattedMessage
                          id="pages.login.register"
                          defaultMessage="立即注册"
                        />
                      </a>
                    </div>
                  </div>
                );
              },
            }}
            initialValues={{
              autoLogin: true,
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
                id: 'pages.login.username.placeholder',
                defaultMessage: '请输入用户名',
              })}
              rules={[
                {
                  required: true,
                  message: (
                    <FormattedMessage
                      id="pages.login.username.required"
                      defaultMessage="请输入用户名!"
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
                id: 'pages.login.password.placeholder',
                defaultMessage: '请输入密码',
              })}
              rules={[
                {
                  required: true,
                  message: (
                    <FormattedMessage
                      id="pages.login.password.required"
                      defaultMessage="请输入密码！"
                    />
                  ),
                },
              ]}
              className={styles.formItem}
            />

            <div
              style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                marginBottom: 24,
              }}
            >
              <ProFormCheckbox noStyle name="autoLogin">
                <FormattedMessage
                  id="pages.login.rememberMe"
                  defaultMessage="记住我"
                />
              </ProFormCheckbox>
              <a
                style={{
                  color: '#667eea',
                  textDecoration: 'none',
                }}
              >
                <FormattedMessage
                  id="pages.login.forgotPassword"
                  defaultMessage="忘记密码？"
                />
              </a>
            </div>
          </ProForm>
        </Card>
      </div>
      <div className={styles.footerWrapper}>
        <Footer />
      </div>
    </div>
  );
};

export default Login;
