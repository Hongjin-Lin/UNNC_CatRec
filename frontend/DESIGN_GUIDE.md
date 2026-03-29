# 🐱 喵友圈圈 - 品牌视觉规范 (Design Language)

## 1. 核心设计理念 (The Vibe)

- **温暖与安全**：模拟沐浴在阳光下的校园角落，消除传统社交软件的冰冷感。
- **治愈与宁静**：通过低饱和度的色彩，缓解压力，营造亲近友好的社区氛围。
- **好奇与连接**：以猫咪的视角观察世界，强调人与猫、人与人之间的情感纽带。

---

## 2. 色彩系统 (Color Palette)

所有页面必须严格遵循以下十六进制色值，以确保视觉连贯性：

| 维度 | 颜色名称 | 十六进制 (Hex) | RGB | 应用场景示例 |
|------|---------|---------------|-----|------------|
| 主背景 | 奶油黄 (Creamy Yellow) | #FFF8DC | 255, 248, 220 | 全页面底色、高光区域 |
| 功能/图标 | 淡蓝绿 (Sage Green-Blue) | #B7C9C0 | 183, 201, 192 | 交互图标、导航栏按钮、日期文字 |
| 辅助/情绪 | 薰衣草紫 (Lavender Mist) | #D8BFD8 | 216, 191, 216 | 次要说明文字、阴影处理、底部加载提示 |
| 情感/连接 | 柔和粉 (Soft Coral Pink) | #F4A460 | 244, 164, 96 | 列表分割线、地点标签背景、亲密交互提示 |
| 核心焦点 | 圆眼睛金 (Goldeneye Amber) | #F0C350 | 240, 195, 80 | 点赞激活态、收藏星标、猫咪眼睛特写 |
| 文本 | 偏蓝绿深灰 (Deep Gray) | #7A8A80 | 122, 138, 128 | 列表标题、正文内容（非纯黑以减少突兀感） |
| 标题 | 深灰 (Dark Gray) | #1C1917 | 28, 25, 23 | 页面标题、卡片名称 |

---

## 3. UI 组件规范 (Component Standards)

### 容器与间距

**大圆角策略**：
- 头像：8px 圆角 (16rpx)
- 动态图片和内容卡片：12px+ 圆角 (16rpx 及以上)
- 增加视觉亲和力

**区块分割**：
- 弃用粗重的边线，改用颜色分割
- 改用颜色分割（如奶油黄背景上的白色卡片）或 1px 的柔和粉 (#F4A460) 细线
- 卡片间距：20-24rpx

### 交互动效

**反馈色**：
- 所有的点击反馈应倾向于变亮而非变暗，模拟阳光感
- 使用 `:active` 状态改变背景或透明度

**情感反馈**：
- 点赞动作应伴随圆眼睛金 (#F0C350) 的色彩变换
- 象征"眼神的对视"

### 排版系统

**字体**：
- 优先使用系统默认无衬线字体 (`-apple-system`)
- 保持简洁

**层级**：
- 通过字号大小而非字重 (Weight) 来区分层级
- 保持整体线条的纤细与柔和
- 主标题：48rpx, 700 weight
- 副标题：26rpx, 500 weight
- 正文：26-28rpx, 400 weight
- 辅助文字：22-24rpx, 400 weight

---

## 4. 页面适配逻辑 (Page Adapting Logic)

当在编写新页面（如 Cat-Moments 或其他新页面）时，请遵循以下逻辑流程：

### Step 1: 注入底色
```css
background-color: #FFF8DC;
```
这是所有页面的第一步。

### Step 2: 元素染色
- 将原本习惯使用的灰色（#888, #ccc）全部替换为薰衣草紫或淡蓝绿调和后的灰度色
- 避免使用纯黑色纯白色，保持温暖调性

### Step 3: 视觉锚点
- 每个页面必须有一个圆眼睛金 (#F0C350) 的元素作为视觉中心
- 可以是按钮、点赞图标、强调标签等

### Step 4: 情感化文案
- 所有的提示语（如加载中、空状态）需带有猫咪语感
- 例子：
  - "加载中喵~" 而不是 "Loading..."
  - "没有更多猫片了喵~" 而不是 "No more data"
  - "还没有喵友圈内容呢" 而不是 "No content"
- 配合薰衣草紫 (#D8BFD8) 显示

---

## 5. 样式编码规范

### Rem 单位对照
- 设计稿基准：375px 宽度 = 750rpx
- 实际转换：1rpx = 0.5px
- 常用尺寸对照：
  - 16rpx = 8px
  - 20rpx = 10px
  - 24rpx = 12px
  - 32rpx = 16px
  - 48rpx = 24px

### CSS 类命名
- 使用 BEM 命名法：`.block__element--modifier`
- 例子：`.card__body`, `.btn--primary`, `.tag--active`

### 响应式设计
- 基础断点：
  - 小屏 (< 375px)：特殊处理
  - 中屏 (375-414px)：默认标准
  - 大屏 (> 414px)：微调间距

---

## 6. 文件结构建议

```
frontend-uniapp/src/
├── pages/
│   ├── identify/          # 识别页面
│   │   └── index.vue
│   ├── profiles/          # 猫咪名册
│   │   ├── index.vue
│   │   └── self-profile/  # 猫咪详情
│   │       ├── self-profile.vue
│   │       └── cat-moment/    # 喵友圈
│   │           └── cat-moment.vue
│   ├── map/               # 地图页面
│   │   └── index.vue
│   └── add/               # 添加猫咪
│       └── index.vue
├── api/
│   └── index.ts           # API 接口
├── assets/
│   └── colors.ts          # 颜色常量
└── App.vue
```

---

## 7. 常用组件变体

### 按钮样式
```typescript
// 主要按钮 (Primary CTA)
background: linear-gradient(135deg, #B7C9C0 0%, #D8BFD8 100%);
color: white;

// 次要按钮 (Secondary)
background: #B7C9C0;
color: white;

// 强调按钮 (Focus/Active)
background: #F0C350;
color: white;

// 文字链接 (Link)
color: #B7C9C0;
```

### 卡片样式
```css
background: white;
border: 1px solid #F4A460;
border-radius: 16rpx;
padding: 24rpx;
```

### 标签样式
```css
background: #F4A460;
color: white;
padding: 8rpx 16rpx;
border-radius: 8rpx;
font-size: 20rpx;
```

---

## 8. 开发检查清单

- [ ] 所有页面背景色为 #FFF8DC
- [ ] 所有文本使用 #1C1917 (标题) 或 #7A8A80 (正文)
- [ ] 没有使用纯黑或纯灰色
- [ ] 每个页面有至少一个 #F0C350 视觉锚点
- [ ] 所有空状态和加载提示带有猫咪语感，使用 #D8BFD8
- [ ] 卡片使用 #F4A460 边框或背景分割
- [ ] TAB栏选中色为 #F0C350，未选中为 #7A8A80
- [ ] 没有使用渐变以外的装饰
- [ ] 所有圆角都不小于 12rpx（头像除外，可用 8rpx）

---

## 9. 更新日志

- **v1.0** (2024-03-28)：初始版本，包含核心色彩系统和组件规范

