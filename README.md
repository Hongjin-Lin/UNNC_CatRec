# 🐾 喵友圈圈 (UNNC CatRec)

> 一个专门为宁波诺丁汉大学（UNNC）校园流浪猫打造的 AI 识别与图鉴小程序。

## 📖 项目简介

UNNC CatRec（喵友圈圈）是一个集成了人工智能视觉模型的校园猫咪识别与档案记录平台。无论是偶遇了不知名的校园猫咪，还是想随时“云吸猫”、查看猫咪们的日常热点地图，“喵友圈圈”都能为你提供最贴心、最治愈的体验。

---

## 🌟 核心功能

- **🔍 AI 猫咪识别 (Identify)**
  - 基于深度学习视觉模型（支持 DINO-v2 特征嵌入算法），一键上传猫咪照片，系统即可在几十毫秒内智能比对图库，高精度告诉你这是哪位校园“大明星”。
- **📚 校园猫咪名册 (Cat Registry)**
  - 完整收录 UNNC 校园内的猫咪档案，包含基础信息（名字、常出没地点、性格标签）、健康情况（绝育 TNR 状态标记）。支持双语（中/英）自由切换。
- **📸 喵友圈 (Cat Moments)**
  - 内置精美的类“微信朋友圈”风格猫片画廊。利用随机排版算法引擎，将静态猫图秒变为生动的专属社交动态时间线，配合动态生成的热评与点赞，让你沉浸式看猫。
- **🗺️ 校园地图与热点 (Campus Map)**
  - 基于校园物理坐标系映射的动态活动热点地图，直观显示图书馆、17/18号楼、DB楼等地点的猫主子驻扎密度。
- **➕ 加入新成员 (Add New Cat)**
  - 提供表单页用于报告校园新发现的猫咪成员。关键接口由管理员口令（如 `UNNC2026`）严格把控，维护图鉴的整洁与安全。

---

## 💻 技术栈

### 前端 (Frontend)
- **核心框架**: `Vue 3` (Options/Composition API) + `Vite`
- **跨端方案**: `UniApp` (完美兼容 H5 静态网页与微信小程序多端编译)
- **主要特性**: 响应式温馨暖色调排版 (Grid/Flex Layout)，内置轻量级 i18n 国际化引擎机制。

### 后端 (Backend)
- **Web 服务**: `FastAPI` (Python)
- **数据库**: `SQLite` 轻量级本地数据持久化层，快速执行地理映射与属性存储。
- **AI/图像模型**: `PyTorch` 构建。由图像文件解码提取高维向量 Tensor Embeddings，运算欧弦相似度矩阵来给出结果预测。

---

## 🚀 快速启动（本地开发）

### 准备工作
确保你的电脑已安装 `Node.js` 以及 `Python 3.10+`。

### 1. 启动后端服务器
```bash
cd backend
# 安装相关依赖 (建议在此前创建并激活 pip venv)
pip install -r requirements.txt
# 启动 FastAPI 服务，默认运行在 8000 端口
uvicorn main:app --reload
```

### 2. 启动前端页面
```bash
cd frontend-uniapp  # 或者是前端根目录 frontend/
npm install

# 浏览器预览 (Web H5)
npm run dev:h5

# 微信开发者工具预览 (Mini Program)
npm run dev:mp-weixin 
```
> **环境变量提示**: 前端网络请求会在本地开发时默认指向 `.env.development` 中配置的 `http://localhost:8000`。若你使用 Cloudflare Tunnel 或 SakuraFrp 等进行内外网穿透，请对应修改线上 `.env` 配置中的 `VITE_API_URL`。

---

## 📁 主要目录结构

```text
📦 UNNC_CatRec
 ┣ 📂 backend                     # Python FastAPI AI / 数据后端
 ┃ ┣ 📂 data                      # SQLite 数据库文件 (cats.db等)
 ┃ ┣ 📂 routers                   # 后端路由分离 (获取列表, 识别照片, 地图分配)
 ┃ ┣ 📜 CatRec.py               # 核心 AI 特征匹配运算
 ┃ ┗ 📜 main.py                 # FastAPI 入口配置及静态目录挂载
 ┣ 📂 campus_cats_library         # 完整的高清本地猫咪图像库 (按名字分类夹存档)
 ┣ 📂 frontend (frontend-uniapp)  # 移动端/多端 UI 框架
 ┃ ┣ 📂 src
 ┃ ┃ ┣ 📂 api               # 环境隔离的异步请求拦截/封装接口
 ┃ ┃ ┣ 📂 pages             # 各核心页面展示 (名册, 独立主页, 识别相机等)
 ┃ ┃ ┗ 📂 locales           # 国际化英汉双语映射文件 (en.ts, zh.ts)
 ┃ ┣ 📜 vite.config.ts        # 打包配置及代理设定
 ┃ ┗ 📜 package.json
 ┗ 📜 README.md                   # 项目概要 (You are here)
```

---

## 🤝 感谢与支持 (Contributors)

本项目致力于连接科技与自然环境的关爱。如果你在宁诺校园偶遇新猫片，或对于该系统的 AI 精准度与前端渲染体验有改善代码（PR / Issues），我们表示最真诚的感谢！

**Let's give every campus cat a name!** 🐾
