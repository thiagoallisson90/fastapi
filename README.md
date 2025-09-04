# FastAPI Project

## 🎵 Based on the [Playlist](https://www.youtube.com/playlist?list=PLpdAy0tYrnKy3TvpCT-x7kGqMQ5grk1Xq)

## 🚀 Project Setup

This project uses **FastAPI** with authentication, database support, migrations, and schemas.

---

## 📦 Dependencies

Install all required packages with:

```bash
pip install fastapi uvicorn sqlalchemy passlib[bcrypt] python-jose[cryptography] python-dotenv python-multipart sqlalchemy_utils alembic requests
```

## ▶️ Run

To start the FastAPI server using **Uvicorn**, run:

### Standard structure (`main.py`):

```bash
uvicorn app.main:app --reload
```
