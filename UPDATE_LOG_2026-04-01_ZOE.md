# 2026.4.1 Zoe 更新日志（供 Merge 审阅）

本文用于汇总 2026-04-01 当天代码侧的主要更新，帮助合并同学快速把握范围、影响面与回归重点。

## 1. 前端功能与页面结构更新

### 1.1 新增个人中心 Account 体系
- 新增页面：`frontend/src/pages/account/index.vue`
- 新增子页面：
  - `frontend/src/pages/account/my-cats.vue`
  - `frontend/src/pages/account/my-moments.vue`
  - `frontend/src/pages/account/bookmarks.vue`
  - `frontend/src/pages/account/settings.vue`
- 路由配置更新：`frontend/src/pages.json`
  - Tab 从「添加」调整为「我的」
  - 增加 Account 及其子页面路由

### 1.2 名册页重构（全部/收藏/搜索）
- 文件：`frontend/src/pages/profiles/index.vue`
- 主要改动：
  - 增加顶部模式切换：全部 / 收藏 / 搜索
  - 增加筛选面板：性别、绝育状态、当前状态
  - 增加排序：默认 / 热度 / 类别
  - 增加本地收藏交互与空状态文案

### 1.3 详情页信息扩展
- 文件：`frontend/src/pages/profiles/self-profile.vue`
- 展示字段扩展：性别、类别/品种、毛色、当前状态、年龄/体重
- 收藏按钮改为可切换星标（本地持久化）

### 1.4 添加页字段扩展与交互优化
- 文件：`frontend/src/pages/add/index.vue`
- 新增字段：物种、品种、毛色、估计年龄、体重、当前状态、是否亲人
- 品种支持下拉选择 + 手动输入
- 上传提示文案优化，表单输入高度和可读性优化

### 1.5 识别页补充纠错入口
- 文件：`frontend/src/pages/identify/index.vue`
- 在无匹配和结果区增加“信息有误 -> 联系我们”入口
- 非 H5 端补充复制链接逻辑

## 2. 国际化（中英）与导航文案更新

- 文件：
  - `frontend/src/locales/zh.ts`
  - `frontend/src/locales/en.ts`
  - `frontend/src/composables/useLocale.ts`
- 主要改动：
  - 增加 account 全套中英文文案
  - 调整 identify、profiles、map、add 文案
  - map 副标题改为准确性提示文本
  - tab 文案中英文同步（含 `👤 Me`）
  - TabBar 更新策略优化，减少页面切换时的 setTabBarItem 异常

## 3. 前端 API 与本地能力扩展

### 3.1 API 类型与查询能力增强
- 文件：`frontend/src/api/index.ts`
- `CatProfile` 扩展字段：species/breed/color/gender/estimated_age/weight/status/计数等
- `getCats` 支持查询参数（sort / gender / neutered / status / category）
- 新增点击计数接口：`incrementCatClick`
- `addCat` 增加扩展表单字段透传

### 3.2 收藏能力封装
- 新增文件：`frontend/src/composables/catFavorites.ts`
- 提供收藏读写、切换与状态判断方法

## 4. 后端数据模型与接口更新

### 4.1 猫数据表结构与构建流程升级
- 文件：`backend/build_profile.py`
- 将 cats 表重建为扩展结构，新增：
  - species, breed, color, gender, estimated_age, weight, status, is_friendly
  - click_count, likes_count, comments_count, favorites_count
  - default_rank
- 增加 pinned 默认顺序（橙子/森森/馒头/黄苹果/小话痨 等）

### 4.2 猫接口增强
- 文件：`backend/routers/cats.py`
- 新增与改动：
  - 运行时 schema 补齐（兼容旧库）
  - `GET /cats/` 支持排序与筛选参数
  - `GET /cats/{id}` 返回扩展字段
  - 新增 `POST /cats/{id}/click` 点击计数

### 4.3 添加猫流程改造
- 文件：
  - `backend/routers/add_cat.py`
  - `backend/services/local_cat_service.py`（新增）
- 优先本地落库（sqlite + cats.json + 本地图片），NocoDB 同步改为 best-effort，不阻塞主流程

### 4.4 数据管线补充
- 新增：
  - `backend/sync_cats_json.py`（从 NocoDB 同步 cats.json）
  - `backend/DATA_PIPELINE.md`（三步数据流文档）
- 更新：`backend/profile_script.py` 增加数据流程说明注释
- `backend/requirements.txt` 增加 `requests`

## 5. 用户/论坛标准结构预留（后端骨架）

- 新增：
  - `backend/routers/users.py`
  - `backend/services/user_service.py`
  - `backend/shared/users_schema.json`
  - `backend/shared/forum_schema.json`
- `backend/main.py` 注册 users router

## 6. 依赖与工程更新

- `frontend/package.json` 增加 `sass`
- `frontend/package-lock.json` 已同步变更（依赖树更新较大）

## 7. 当日验证情况（记录）

- 前端类型检查：`npm run type-check` 通过（Exit Code 0）
- 后端曾可启动并完成模型预加载；过程中出现过 watch reload 与进程被系统 kill（Exit 137）记录
- `build_embeddings.py` 在 `/usr/local/bin/python3` 环境下执行成功

## 8. Merge 关注点（建议）

1. 此次改动跨前后端、接口与文案，建议按模块拆分审阅：Account、Profiles、Add、Backend Cats。
2. `frontend/package-lock.json` 体积变更较大，建议重点关注是否仅由 `sass` 引入触发。
3. 后端 cats 表已扩展，若线上已有历史库，请优先验证迁移兼容（已在 router 层加补齐逻辑）。
4. 如果本地页面文案未即时刷新，需重启前端 dev server + 浏览器硬刷新后再验。
