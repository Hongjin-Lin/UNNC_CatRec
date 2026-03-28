# UNNC CatRec — Claude 上手文档

> 本文档由原项目对话自动生成，供迁移到新仓库后的 Claude 快速理解项目全貌。

---

## 项目简介

**UNNC CatRec** 是宁波诺丁汉大学校园猫咪识别与社区 App，30 小时 Hackathon 项目，3 人团队。

核心功能：
- 上传猫咪照片 → SigLIP2 AI 识别 → 返回匹配猫咪信息
- 地图展示校园猫咪热点
- 猫咪名册（网格浏览所有猫）
- 添加新猫咪（表单 + 照片上传到 NocoDB）

未来计划迁移到微信小程序，因此前端采用移动端优先设计。

---

## 技术栈

| 层 | 技术 |
|---|---|
| 前端 | Next.js 14 (App Router) + Tailwind CSS + Lucide Icons + Leaflet.js |
| 后端 | FastAPI + Uvicorn (Python) |
| AI | SigLIP2-Giant (`google/siglip2-giant-patch16-384`) via HuggingFace transformers |
| 数据库 | NocoDB (REST API) |
| 向量库 | 本地 `backend/data/cat_profiles.pkl` |

---

## 项目结构

```
AICatRec/
├── .gitignore                  # 忽略模型权重、pkl、.env
├── CLAUDE_CONTEXT.md           # 本文件
├── backend/
│   ├── main.py                 # FastAPI app 入口，CORS 配置
│   ├── requirements.txt        # Python 依赖
│   ├── .env.example            # 环境变量模板
│   ├── data/                   # (gitignored) cat_profiles.pkl 放这里
│   ├── routers/
│   │   ├── identify.py         # POST /identify — 图片识别
│   │   ├── cats.py             # GET /cats, GET /cats/map-data
│   │   └── add_cat.py          # POST /cats/add — 添加新猫
│   └── services/
│       ├── siglip_service.py   # SigLIP2 推理 + pkl 向量匹配
│       └── nocodb_service.py   # NocoDB REST API 客户端
├── frontend/
│   ├── package.json
│   ├── next.config.js
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── .env.local              # NEXT_PUBLIC_API_URL=http://localhost:8000
│   ├── app/
│   │   ├── layout.tsx          # 全局布局 + 底部导航栏
│   │   ├── globals.css         # Tailwind + 设计 token CSS 变量
│   │   ├── page.tsx            # / 识别页
│   │   ├── profiles/page.tsx   # /profiles 猫册页
│   │   ├── map/page.tsx        # /map 地图页
│   │   └── add/page.tsx        # /add 添加猫咪页
│   ├── components/
│   │   ├── NavBar.tsx          # 底部四标签导航
│   │   ├── CatCard.tsx         # 猫咪卡片（用于网格）
│   │   ├── MapView.tsx         # Leaflet 地图（client-only dynamic import）
│   │   └── LoadingSpinner.tsx  # 通用加载动画
│   └── lib/
│       └── api.ts              # 所有后端请求封装 + TypeScript 类型
└── shared/
    └── cats_schema.json        # 猫咪数据结构 JSON Schema（文档用途）
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

### 前端 `frontend/.env.local`
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 启动方式

### 前端
```bash
cd frontend
npm install
npm run dev
# 访问 http://localhost:3000
```

### 后端
```bash
cd backend
python -m venv .venv
source .venv/Scripts/activate  # Windows Git Bash
# 或 .venv\Scripts\activate    # Windows CMD
pip install -r requirements.txt
cp .env.example .env            # 然后填写真实值
uvicorn main:app --reload --port 8000
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
- 懒加载 SigLIP2-Giant 模型（首次调用时从 HuggingFace 下载，约 3GB）
- `embed_image(bytes)` → L2 归一化的向量 (numpy)
- `find_best_match(bytes)` → 与 `cat_profiles.pkl` 做余弦相似度比较，阈值 0.70
- pkl 格式：`{"profiles": [dict, ...], "embeddings": [[float, ...], ...]}`
- pkl 路径：`backend/data/cat_profiles.pkl`（被 .gitignore 忽略）

### `backend/services/nocodb_service.py`
- 使用 NocoDB v1 API：`/api/v1/db/data/noco/{TABLE_ID}`
- 认证头：`xc-auth: {API_TOKEN}`
- 位置标签 → GPS 坐标硬编码在 `LOCATION_COORDS` 字典中，目前有 `#23`, `#01`, `#05`
- 新增位置时在该字典添加即可

### `frontend/lib/api.ts`
- 所有请求统一走 `NEXT_PUBLIC_API_URL`
- 导出类型：`CatProfile`, `Hotspot`, `IdentifyResult`
- 导出函数：`identifyCat()`, `getCats()`, `getMapData()`, `addCat()`

### `frontend/components/MapView.tsx`
- Leaflet 地图，必须通过 `dynamic(() => import(...), { ssr: false })` 加载
- 地图中心：UNNC 校园 `[31.8315, 121.6832]`，zoom 16
- 热点用 `CircleMarker` 表示，半径随猫数量增大

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
2. **cat_profiles.pkl 需手动维护**：添加新猫后需重新生成 pkl（嵌入向量库），目前没有自动化脚本。
3. **地图位置硬编码**：`LOCATION_COORDS` 在 `nocodb_service.py` 里，新增位置要手动加。
4. **无鉴权**：所有 API 均公开，Hackathon 阶段够用。
5. **图片存储**：图片上传到 NocoDB attachment，不是独立对象存储。
