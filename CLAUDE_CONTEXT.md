# UNNC CatRec — Claude 上手文档

> 本文档记录项目全貌，供 Claude 在新对话中快速上手。

---

## 项目简介

**UNNC CatRec** 是宁波诺丁汉大学校园猫咪识别与社区 App，30 小时 Hackathon 项目，3 人团队。

核心功能：
- 上传猫咪照片 → SigLIP2 AI 识别 → 返回匹配猫咪信息
- 地图展示校园猫咪热点
- 猫咪名册（网格浏览所有猫）
- 添加新猫咪（表单 + 照片上传）

前端采用 uni-app（Vue 3），一套代码编译到 H5 和微信小程序。`frontend/`（Next.js）为早期原型，不再维护。

---

## 技术栈

| 层 | 技术 |
|---|---|
| 前端 | Vue 3 + uni-app + Vite |
| 后端 | FastAPI + Uvicorn (Python) |
| AI | DINO-v2 (`nateraw/dino-v2-small-for-animal-identification`) via HuggingFace transformers |
| 数据库 | NocoDB (REST API) |
| 向量库 | 本地 `backend/data/cat_profiles.pkl` |

---

## 项目结构

```
CatRec/
├── .gitignore
├── README.md
├── claude_context.md           # 本文件
├── cat_registry.pt             # CatRec.py 原型用的 torch 注册档案
├── cats.json                   # 从 NocoDB 导出的原始猫咪数据
├── backend/
│   ├── main.py                 # FastAPI app 入口，CORS 配置
│   ├── CatRec.py               # 早期原型 CatRecognizer 类（注册/识别/is_same_cat）
│   ├── download.py             # 从 cats.json 批量下载猫咪照片到 campus_cats_library/
│   ├── profile.py              # 下载 SigLIP2 模型到 model_save/（hf-mirror）
│   ├── requirements.txt        # Python 依赖
│   ├── .env.example            # 环境变量模板
│   ├── data/                   # (gitignored) cat_profiles.pkl 放这里
│   ├── routers/
│   │   ├── identify.py         # POST /identify — 图片识别
│   │   ├── cats.py             # GET /cats, GET /cats/map-data
│   │   └── add_cat.py          # POST /cats/add — 添加新猫
│   ├── services/
│   │   ├── siglip_service.py   # SigLIP2 推理 + pkl 向量匹配
│   │   └── nocodb_service.py   # NocoDB REST API 客户端
│   └── shared/
│       └── cats_schema.json    # 猫咪数据结构 JSON Schema
├── frontend-uniapp/            # uni-app 前端（支持微信小程序和 H5）
│   ├── src/
│   │   ├── api/
│   │   │   └── index.ts        # 后端请求封装 + TypeScript 类型
│   │   ├── pages/
│   │   │   ├── index/index.vue       # / 识别页
│   │   │   ├── profiles/index.vue    # /profiles 猫册页
│   │   │   ├── map/index.vue         # /map 地图页
│   │   │   └── add/index.vue         # /add 添加猫咪页
│   │   ├── static/             # 静态资源
│   │   ├── App.vue             # 全局应用入口
│   │   ├── main.ts             # Vue 实例挂载
│   │   ├── manifest.json       # uni-app 和微信小程序配置文件
│   │   ├── pages.json          # 路由配置 + 底部 TabBar 导航
│   │   └── uni.scss            # 样式变量
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── .env                    # VITE_API_URL 生产环境
│   └── .env.development        # VITE_API_URL=http://localhost:8000 
├── images/                     # CatRec.py 原型训练用图（卷卷/橙子/粑粑柑/黄苹果）
├── model_save/                 # 下载的 SigLIP2 模型权重（safetensors，约 3GB）
└── campus_cats_library/        # 从 NocoDB 下载的完整猫咪照片库（按猫名分文件夹）
    ├── 卷卷/
    ├── 井盖/
    ├── 二胖/
    ├── 墨墨-竖竖/
    └── ...
```

---

## 环境变量

### 后端 `backend/.env`
```env
NOCODB_BASE_URL=https://你的nocodb地址
NOCODB_API_TOKEN=你的token
NOCODB_TABLE_ID=你的表ID
CORS_ORIGINS=http://localhost:3000
```

### 前端 `frontend-uniapp/.env.development`
```env
VITE_API_URL=http://localhost:8000
```
### 前端 `frontend-uniapp/.env`
```env
VITE_API_URL=https://catrec.thirtysixstudio.net
```

---

## 启动方式

### 后端
```bash
cd backend
pip install -r requirements.txt
# 首次运行需先构建数据库和向量库
python profile.py            # 下载猫咪图片
python build_profile.py      # 生成 data/cats.db（猫咪名册）
python build_embeddings.py   # 生成 data/cat_profiles.pkl（识别向量库）
# 启动服务
python -m uvicorn main:app --reload --port 8000
```

### 前端 — H5 网页端
```bash
cd frontend-uniapp
npm install
npm run dev:h5
# 访问 http://localhost:5173
```

### 前端 — 微信小程序
```bash
cd frontend-uniapp
npm install
npm run dev:mp-weixin
# 用微信开发者工具打开 dist/dev/mp-weixin/
# 需先在 src/manifest.json 的 mp-weixin.appid 填入小程序 AppID
```

---

## API 接口一览

| Method | Path | 说明 |
|--------|------|------|
| GET | `/health` | 健康检查 |
| POST | `/identify` | 上传图片识别猫咪（multipart/form-data, field: `image`）|
| GET | `/cats` | 获取所有猫咪列表 |
| GET | `/cats/map-data` | 获取地图热点数据 |
| POST | `/cats/add` | 添加新猫咪（multipart/form-data）|

### POST /identify 返回格式
```json
// 匹配成功
{"no_match": false, "match": {"name": "小花", "location": "#23", "personality": ["亲人"], "tnr_status": true, "confidence": 0.87}}
// 未匹配
{"no_match": true, "match": null, "confidence": 0.42}
```

### POST /cats/add 表单字段
```
name        string  必填
location    string  例如 #23
personality string  逗号分隔，例如 "亲人,怕生"
tnr_status  bool
notes       string  可选
image       file    图片文件
```

---

## 核心模块说明

### `backend/services/siglip_service.py`
- 懒加载 DINO-v2 模型（首次调用时从 HuggingFace 下载）
- `embed_image(bytes)` → L2 归一化的向量 (numpy)
- `find_best_match(bytes)` → 与 `cat_profiles.pkl` 做余弦相似度比较，阈值 0.50 左右
- pkl 格式：`{"profiles": [dict, ...], "embeddings": [[float, ...], ...]}`
- pkl 路径：`backend/data/cat_profiles.pkl`（被 .gitignore 忽略）

### `backend/routers/cats.py`
- MAP_DATA 直接访问 `data/cats.db` 缓存而不是访问 NOCDB 云端。
- 位置标签 → GPS 坐标硬编码分布在 `LOCATION_COORDS` 字典中
- 新增位置时在该字典中按地点关键字添加即可

### `frontend/src/api/index.ts`
- 所有请求统一走 `VITE_API_URL`
- 导出类型：`CatProfile`, `Hotspot`, `IdentifyResult`
- 导出函数：`identifyCat()`, `getCats()`, `getMapData()`, `addCat()`

### `frontend/src/pages/map/index.vue`
- 原生地图组件 `<map>` 支持微信小程序
- 地图中心：UNNC 校园 `[29.80002, 121.56351]`，zoom 16
- 热点用 `<map>` Marker 渲染

---

## 设计规范

**调色板（Tailwind 自定义色）：**

| 名称 | 色值 | 用途 |
|------|------|------|
| `cream-50` | #FFF8F0 | 页面背景 |
| `cream-100` | #FEF3E2 | 卡片背景色块 |
| `cream-200` | #FDE8C8 | 标签背景 |
| `brand` | #F97316 | 主色（按钮、激活态）|
| `brand-light` | #FDBA74 | 次要强调 |
| `paw-dark` | #1C1917 | 主文字 |
| `paw-soft` | #78716C | 次要文字 |

**布局原则：**
- 移动端优先，`max-w-md mx-auto` 居中
- 底部固定导航栏，高度 `h-16`，留 `pb-20` 给内容区
- 圆角统一用 `rounded-2xl` / `rounded-3xl`

---

## NocoDB 表结构（期望字段名）

| 字段 | 类型 | 说明 |
|------|------|------|
| `Name` | Text | 猫咪名字 |
| `Location` | Text | 位置标签，如 #23 |
| `Personality` | Text | 逗号分隔性格标签 |
| `TNR_Status` | Checkbox | 是否已绝育 |
| `Notes` | Text | 备注 |
| `Image` | Attachment | 猫咪照片 |

如果你的 NocoDB 列名不同，只需修改 `backend/services/nocodb_service.py` 中 `create_cat()` 的 payload 字段名，以及 `get_all_cats()` 的返回处理。

---

## 已知限制 / 待完善

1. **NocoDB API 版本**：代码用 v1 API（`xc-auth` 头）。若用新版 NocoDB（v2），需改为 `xc-token` 头，路径改为 `/api/v2/tables/{tableId}/records`。
2. **cat_profiles.pkl 需手动维护**：添加新猫后需重新生成 pkl（调用 `build_embeddings.py`），目前没有自动化脚本。
3. **地图位置硬编码**：`LOCATION_COORDS` 在 `backend/routers/cats.py` 里，新地址或不确定的地址标签需要加映射关键字。
4. **添加猫咪鉴权**：只进行简单前端验证限制（`UNNC2026` 后门）。
5. **图片存储**：图片上传到 NocoDB attachment，不是独立对象存储。
