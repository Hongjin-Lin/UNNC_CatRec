# 喵友圈圈 (CatRec)

> UNNC 校园猫咪识别与社区 App — Hackathon 项目
> Campus Cat Recognition & Community App for UNNC — Hackathon Project

一款帮助宁波诺丁汉大学师生认识、记录、关爱校园流浪猫的移动应用。拍一张照片，AI 帮你认出是哪只猫，并查看它的档案、位置和 TNR 状态。

A mobile app that helps UNNC students and staff identify, record, and care for campus stray cats. Take a photo — AI tells you which cat it is and shows its profile, location, and TNR status.

---

## 功能 / Features

- **AI 猫咪识别 / AI Cat Identification**：上传照片，DINOv2 模型与向量库比对，返回 top-3 匹配候选及置信度 / Upload a photo; DINOv2 matches it against the vector database and returns top-3 candidates with confidence scores
- **猫咪名册 / Cat Registry**：浏览所有 51 只校园猫咪，搜索、查看详情 / Browse all 51 campus cats, search by name, view full profiles
- **相册 / Photo Album**：每只猫的详情页内置滑动相册，点击可全屏放大 / Swipeable photo album on each cat's profile, tap to preview full-screen
- **校园地图 / Campus Map**：热点标注猫咪常出没区域 / Map markers showing cat hotspots across campus
- **添加新猫 / Add New Cat**：管理员可通过 App 上传照片、填写信息注册新猫 / Admins can register new cats via the app with photo upload
- **中英双语 / Bilingual**：支持中/英文界面切换，状态持久化 / Switch between Chinese and English UI, preference saved locally

---

## 技术栈 / Tech Stack

| 层 / Layer | 技术 / Technology |
|---|---|
| 前端 / Frontend | Vue 3 + uni-app + Vite (H5 & WeChat Mini Program) |
| 后端 / Backend | FastAPI + Uvicorn (Python) |
| AI | DINOv2-small (`AvitoTech/DINO-v2-small-for-animal-identification`) |
| 数据库 / Database | SQLite (`data/cats.db`) |
| 向量库 / Vector Store | `data/cat_profiles.pkl` (numpy cosine similarity) |
| 图片托管 / Image Hosting | FastAPI StaticFiles → `campus_cats_library/` |

---

## 快速开始 / Quick Start

### 后端 / Backend

```bash
cd backend
pip install -r requirements.txt

# First run: build the database and vector store
# 首次运行：构建数据库和向量库
python build_profile.py      # cats.json → data/cats.db
python build_embeddings.py   # campus_cats_library/ → data/cat_profiles.pkl

# Start server / 启动服务
python -m uvicorn main:app --reload --port 8000
```

### 前端 H5 / Frontend (H5)

```bash
cd frontend
npm install
npm run dev:h5
# Visit / 访问 http://localhost:5173
```

### 前端微信小程序 / Frontend (WeChat Mini Program)

```bash
cd frontend
npm run build:mp-weixin
# Import frontend/dist/dev/mp-weixin in WeChat DevTools
# 用微信开发者工具导入 frontend/dist/dev/mp-weixin
```

---

## 项目结构 / Project Structure

```
CatRec/
├── cats.json                   # Raw cat data (data source) / 原始猫咪数据
├── product_brief.md            # Hackathon product brief / 产品简报
├── backend/
│   ├── main.py                 # FastAPI entry point / 入口
│   ├── build_profile.py        # Generate cats.db / 生成数据库
│   ├── build_embeddings.py     # Generate cat_profiles.pkl / 生成向量库
│   ├── routers/
│   │   ├── identify.py         # POST /identify/
│   │   ├── cats.py             # GET /cats/, /cats/{id}, /cats/map-data
│   │   └── add_cat.py          # POST /cats/add/
│   └── services/
│       └── identify_service.py # DINOv2 inference + vector matching
├── frontend/                   # uni-app frontend / 前端
│   └── src/
│       ├── composables/
│       │   ├── useLocale.ts    # Bilingual state / 双语切换
│       │   └── catCache.ts     # List preload cache / 预加载缓存
│       ├── locales/zh.ts & en.ts
│       ├── components/LangToggle.vue
│       └── pages/
│           ├── identify/
│           ├── profiles/
│           ├── map/
│           └── add/
└── campus_cats_library/        # Cat photo library (~51 cats) / 猫咪照片库
```

---

## API

| Method | Path | Description / 说明 |
|--------|------|------|
| GET | `/health` | Health check / 健康检查 |
| POST | `/identify/` | Identify cat from photo / 图片识别 |
| GET | `/cats/` | All cats list / 所有猫咪列表 |
| GET | `/cats/{id}` | Single cat detail + photos[] / 单猫详情 |
| GET | `/cats/map-data` | Map hotspots / 地图热点 |
| POST | `/cats/add/` | Add new cat / 添加新猫 |

---

## 设计规范 / Design System

基于 Happy Hues Palette 15，温暖插画风 / Based on Happy Hues Palette 15, warm illustration style:

| 色值 / Color | 用途 / Usage |
|------|------|
| `#faeee7` | 主背景 / Main background |
| `#33272a` | 标题 / Headlines |
| `#594a4e` | 正文 / Body text |
| `#ff8ba7` | 主按钮 / Primary button & highlight |
| `#ffc6c7` | 边框 / Borders & secondary |
| `#c3f0ca` | TNR / 成功状态 / Success state |
| `#fffffe` | 卡片背景 / Card surface |

---

## 已知限制 / Known Limitations

1. **向量库需手动重建 / Manual vector rebuild required**：添加新猫后需重新运行 `build_embeddings.py` / Must re-run `build_embeddings.py` after adding new cats
2. **位置坐标硬编码 / Hardcoded GPS coordinates**：`backend/routers/cats.py` 的 `LOCATION_COORDS` 需手动维护 / `LOCATION_COORDS` dict must be updated manually
3. **管理员鉴权简单 / Simple admin auth**：仅前端密码验证，无后端鉴权 / Frontend-only password check, no real backend auth
4. **识别阈值固定 / Fixed similarity threshold**：余弦相似度阈值 0.70，未经大规模测试 / Cosine similarity threshold of 0.70, not validated at scale
