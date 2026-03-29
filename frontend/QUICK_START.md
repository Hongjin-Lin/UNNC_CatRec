# 🐱 喵友圈圈 - 快速参考指南

## 快速查找

### 核心色值（复制粘贴）
```css
/* 背景 */
background-color: #FFF8DC;

/* 按钮/导航 */
background: linear-gradient(135deg, #B7C9C0 0%, #D8BFD8 100%);

/* 强调色（点赞/激活） */
color: #F0C350;

/* 文字 */
color: #1C1917;          /* 标题 */
color: #7A8A80;          /* 正文 */
color: #D8BFD8;          /* 辅助/placeholder */

/* 边框/分割线 */
border: 1px solid #F4A460;
```

---

## 路由导航

### 四个主TAB页面
| 页面 | 路径 | 标题 |
|------|------|------|
| 识别 | `/pages/identify/index` | 🔍 猫咪识别 |
| 猫册 | `/pages/profiles/index` | 🐱 猫咪名册 |
| 地图 | `/pages/map/index` | 🗺️ 校园地图 |
| 添加 | `/pages/add/index` | 🐱 添加新猫咪 |

### 详情页面
| 页面 | 路径 | 用途 |
|------|------|------|
| 猫咪详情 | `/pages/profiles/self-profile?id={catId}` | 查看单只猫咪完整档案 |
| 喵友圈 | `/pages/profiles/self-profile/cat-moment` | 该猫咪的момент/动态 |

---

## 页面结构速查

### `profiles/index.vue` - 猫咪名册
```
头部 (标题 + 副标题)
  ↓
加载/错误/空状态处理
  ↓
网格卡片列表 (2列)
  ↓
点击卡片 → 进入 self-profile
```

### `profiles/self-profile.vue` - 猫咪详情
```
返回按钮 + 标题
  ↓
圆形头像 (240rpx)
  ↓
基本信息卡片
  │ ├─ 名字 + TNR状态
  │ ├─ 📍 位置
  │ ├─ 🎭 性格标签
  │ └─ 📝 备注
  ↓
喵友圈入口按钮
  ↓
感情反馈栏 (关注/评论/收藏)
```

### `profiles/self-profile/cat-moment.vue` - 喵友圈
```
Sticky 导航栏
  ↓
加载/空状态
  ↓
信息流卡片
  │ ├─ 用户头像 + 名字 + 时间
  │ ├─ 内容文本
  │ ├─ 图片 (可选)
  │ ├─ 互动栏 (关注/评论/收藏)
  │ └─ 评论预览 (最多2条)
  ↓
加载更多 / 结束提示
```

### `identify/index.vue` - 猫咪识别
```
头部说明
  ↓
图片选择/预览区
  ↓
识别按钮
  ↓
结果展示 (两种)
  ├─ 未匹配 → 建议添加
  └─ 匹配 → 显示详情 + 查看详情按钮
```

### `map/index.vue` - 校园地图
```
标题 + 地图组件
  ↓
热点列表卡片
  ├─ 热点名称
  ├─ 🐱 猫咪列表
  └─ 📍 坐标 (可选)
```

### `add/index.vue` - 添加新猫咪
```
成功状态 (if success)
  └─ 继续添加按钮
或
上传图片区
  ↓
表单字段
  ├─ 名字 *
  ├─ 位置
  ├─ 性格
  ├─ 性别 (单选)
  ├─ TNR状态 (复选)
  └─ 备注
  ↓
提交按钮
```

---

## 组件尺寸参考

| 元素 | 尺寸 | rpx |
|------|------|-----|
| 页面padding | 上下40 | 左右24 |
| 标题字号 | 48rpx | 24px |
| 副标题字号 | 26rpx | 13px |
| 正文字号 | 26-28rpx | 13-14px |
| 辅助文字 | 22-24rpx | 11-12px |
| 卡片border-radius | 16rpx | 8px |
| 头像圆角 | 8rpx | 4px (小) / 120rpx 圆形 (大) |
| 标签padding | 8rpx 16rpx | 4px 8px |
| 标签圆角 | 8~20rpx |  |
| 间距 | 20-24rpx | 10-12px |

---

## 常见交互模式

### 卡片点击反馈
```vue
<view class="card" @tap="handleTap">
  <!-- content -->
</view>

<style scoped>
.card {
  transition: all 0.3s ease;
}
.card:active {
  transform: translateY(-4rpx);
  box-shadow: 0 8rpx 20rpx rgba(240, 195, 80, 0.15);
}
</style>
```

### 按钮点击反馈
```vue
<button class="btn" @tap="handleClick">确认</button>

<style scoped>
.btn {
  background: linear-gradient(135deg, #B7C9C0 0%, #D8BFD8 100%);
  transition: opacity 0.2s;
}
.btn:active {
  opacity: 0.9;
}
.btn[disabled] {
  opacity: 0.6;
}
</style>
```

### 切换状态
```vue
<view class="toggle" :class="{ active: isActive }" @tap="toggle">
  {{ isActive ? '已关注' : '关注' }}
</view>

<style scoped>
.toggle {
  color: #7A8A80;
  border: 2px solid #B7C9C0;
}
.toggle.active {
  background: #F0C350;
  color: white;
  border-color: #F0C350;
}
</style>
```

---

## 猫咪语感文案例句

| 情景 | 表达 |
|------|------|
| 加载中 | 加载中喵~ |
| 没有数据 | 没有更多猫片了喵~ / 还没有喵友圈内容呢 |
| 识别失败 | 没找到匹配的猫咪 / 这只猫可能很特别呢！ |
| 成功提示 | 添加成功喵！/ 这只小可爱已经加入名册了 |
| 空状态 | 还没有猫咪档案喵~ / 没有更多内容呢 |
| 提示语 | 让更多人认识这位校园小明星 |
| 行为邀请 | 快来诰一下这只猫咪吧~ |

---

## 常见问题排查

### 颜色不对？
1. 检查 `pages.json` 中的 `globalStyle.backgroundColor`
2. 检查具体页面的 `.page { background: #FFF8DC; }`
3. 检查 `uni.scss` 中的 SCSS 变量是否更新

### 页面打不开？
1. 确认 `pages.json` 中的路由路径是否正确
2. 确认文件是否存在（路径大小写敏感）
3. 确认 `<navigator>` 路径是否正确

### 样式不生效？
1. 检查 `<style scoped>` 是否正确关闭
2. 检查 class 名称是否拼写正确
3. 清除缓存重新编译

### API 调用失败？
1. 后端服务是否启动？
2. `.env` 中 `VITE_API_URL` 是否配置正确？
3. 检查 API 路径和参数是否匹配

---

## 开发流程

```mermaid
新增功能需求
    ↓
在 DESIGN_GUIDE.md 中查找设计规范
    ↓
新建页面遵循 4-step 适配逻辑
    ↓
更新 pages.json 中的路由
    ↓
编写页面逻辑 (Composition API + TS)
    ↓
按照色彩系统设置样式
    ↓
添加猫咪语感文案
    ↓
测试各设备屏幕适配
    ↓
更新本文档
```

---

## 链接检查

- 📖 完整设计规范：[DESIGN_GUIDE.md](./DESIGN_GUIDE.md)
- 📋 重构详细说明：[REFACTOR_NOTES.md](./REFACTOR_NOTES.md)

---

**最后更新**：2024-03-28  
**版本**：v1.0

