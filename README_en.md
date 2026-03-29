# 🐾 UNNC CatRec (Meow Moments)

**English Version** | [中文版](README.md)

> An AI-powered application designed for identifying and documenting stray cats on the University of Nottingham Ningbo China (UNNC) campus.

## 📖 Introduction

UNNC CatRec is a campus cat identification and documentation platform integrated with AI computer vision models. Whether you encounter an unknown campus cat and want to know its name, or you simply want to view their daily hotspots and photos remotely, this app provides the most heartwarming experience.

---

## 🌟 Core Features

### 🔍 AI Cat Identification
Powered by deep learning vision models (DINO-v2 feature embeddings), users can upload a photo of a cat to instantly retrieve the most likely matches from the campus registry in milliseconds.

| 📸 Upload Photo | ✨ Identify Result |
| :---: | :---: |
| ![Upload](assets/CatID0.png) | ![Result](assets/CatID1.png) |

### 📚 Campus Cat Registry
A complete archive of UNNC campus cats, including basic information (name, usual locations, personality tags) and TNR (Trap-Neuter-Return) status. Supports bilingual (English/Chinese) switching.

| 🐱 Cat Registry | 🏷️ Cat Profile |
| :---: | :---: |
| ![Registry](assets/CatRegistry.png) | ![Profile](assets/CatProfile.png) |

### 📸 Cat Moments (Social Feed)
A beautiful, WeChat Moments-style photo gallery. It uses randomized layout algorithms to transform static cat photos into vivid, timeline-based social feeds with dynamically generated comments and likes.

| 🐾 Moments Feed |
| :---: |
| ![Moment](assets/CatMoment.png) |

### 🗺️ Campus Map & Hotspots
A dynamic activity map pointing to the campus's physical coordinates, visually displaying cat density around landmarks like the Library, Building 17/18, and DB.

### ➕ Add New Cat
A form page for reporting new cats discovered on campus. Key API endpoints are secured by an admin passcode (e.g., `UNNC2026`) to maintain registry data integrity.

---

## 💻 Tech Stack

- **Frontend**: `Vue 3` + `Vite` + `UniApp` (Fully compatible with H5 Web and WeChat Mini Programs).
- **Backend**: `FastAPI` (Python) + `SQLite` (lightweight local database).
- **AI/Vision Model**: Built with `PyTorch`. Generates high-dimensional tensor embeddings from images and calculates cosine similarity matrices for predictions.

---

## 🚀 Quick Start (Local Dev)

### 1. Start Backend Server
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### 2. Start Frontend App
```bash
cd frontend-uniapp  # or frontend/
npm install
npm run dev:h5      # Preview in browser (Web H5)
npm run dev:mp-weixin # Preview in WeChat Developer Tools
```

---

## 🤝 Contributors & Support

This project is dedicated to combining technology with care for the natural environment. If you run into new campus cats or have code improvements (PR / Issues) for the AI precision or frontend rendering, we deeply appreciate it!

**Let's give every campus cat a name!** 🐾