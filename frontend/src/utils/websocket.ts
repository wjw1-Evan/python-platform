/**
 * WebSocket 通知工具类
 * 用于管理与后端通知服务的 WebSocket 连接
 */

export class NotificationWebSocket {
  private ws: WebSocket | null = null;
  private url: string;
  private token: string;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 3000;
  private messageHandlers: ((data: any) => void)[] = [];
  private onConnectHandlers: (() => void)[] = [];
  private onDisconnectHandlers: (() => void)[] = [];

  constructor(token: string, wsUrl?: string) {
    this.token = token;
    // 从环境变量获取 WebSocket URL，默认使用 localhost:8005
    const defaultUrl = process.env.REACT_APP_WS_URL || 'ws://localhost:8005';
    this.url = `${wsUrl || defaultUrl}/ws/notifications/?token=${token}`;
  }

  /**
   * 连接 WebSocket
   */
  connect(): void {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      console.log('WebSocket 已连接');
      return;
    }

    try {
      this.ws = new WebSocket(this.url);

      this.ws.onopen = () => {
        console.log('WebSocket 连接已建立');
        this.reconnectAttempts = 0;
        this.onConnectHandlers.forEach((handler) => handler());
      };

      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          this.messageHandlers.forEach((handler) => handler(data));
        } catch (error) {
          console.error('解析 WebSocket 消息失败:', error);
        }
      };

      this.ws.onerror = (error) => {
        console.error('WebSocket 错误:', error);
      };

      this.ws.onclose = () => {
        console.log('WebSocket 连接已关闭');
        this.onDisconnectHandlers.forEach((handler) => handler());
        this.attemptReconnect();
      };
    } catch (error) {
      console.error('WebSocket 连接失败:', error);
      this.attemptReconnect();
    }
  }

  /**
   * 尝试重连
   */
  private attemptReconnect(): void {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      console.log(
        `尝试重连 (${this.reconnectAttempts}/${this.maxReconnectAttempts})...`,
      );
      setTimeout(() => {
        this.connect();
      }, this.reconnectDelay);
    } else {
      console.error('WebSocket 重连次数已达上限');
    }
  }

  /**
   * 断开连接
   */
  disconnect(): void {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
    this.reconnectAttempts = 0;
  }

  /**
   * 添加消息处理器
   */
  onMessage(handler: (data: any) => void): void {
    this.messageHandlers.push(handler);
  }

  /**
   * 移除消息处理器
   */
  offMessage(handler: (data: any) => void): void {
    this.messageHandlers = this.messageHandlers.filter((h) => h !== handler);
  }

  /**
   * 添加连接成功处理器
   */
  onConnect(handler: () => void): void {
    this.onConnectHandlers.push(handler);
  }

  /**
   * 添加断开连接处理器
   */
  onDisconnect(handler: () => void): void {
    this.onDisconnectHandlers.push(handler);
  }

  /**
   * 获取连接状态
   */
  getState(): number | null {
    return this.ws?.readyState ?? null;
  }

  /**
   * 检查是否已连接
   */
  isConnected(): boolean {
    return this.ws?.readyState === WebSocket.OPEN;
  }
}
