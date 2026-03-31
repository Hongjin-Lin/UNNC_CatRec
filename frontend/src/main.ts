import { createSSRApp } from "vue";
import App from "./App.vue";

const shareMixin = {
  // 必须加上这个方法，微信小程序才会点亮分享给朋友
  onShareAppMessage() {
    return {
      title: 'UNNC 校园猫咪图鉴',
      path: '/pages/identify/index'
    }
  },
  // 必须加上这个方法，微信小程序才会点亮分享到朋友圈
  onShareTimeline() {
    return {
      title: 'UNNC 校园猫咪图鉴',
      query: ''
    }
  }
}

export function createApp() {
  const app = createSSRApp(App);
  app.mixin(shareMixin);
  return {
    app,
  };
}
