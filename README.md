# Title: Warranty Tracker App

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Description

The Warranty Tracker App allows you to store information about your purchased items and tracks their warranties.

On the **`vue` branch**, the app uses a **Vue 3** frontend and **FastAPI** backend with the same SQLite database schema as the original Flask app.

## Features

1. **Shops** — store information about the shops you purchase from
2. **Items** — store purchased goods and warranty length
3. **Database** — backup, restore, and purge the SQLite database
4. **Search** — search items and shops by name, comment, address, etc.

## Stack (vue branch)

| Layer    | Technology                           |
| -------- | ------------------------------------ |
| Frontend | Vue 3, Vite, Vue Router, Bootstrap 5 |
| Backend  | FastAPI, SQLAlchemy 2, Pydantic      |
| Database | SQLite (`instance/warranty.db`)      |

## Requirements

- **Docker** (recommended): https://www.docker.com/
- **Local development** (optional):
    - Python 3.12+
    - Node.js 20+

## Quick start with Docker

1. Clone the repository and switch to the `vue` branch:
    ```bash
    git clone https://github.com/tomasmuhr/Warranty-web2.git
    cd Warranty-web2
    git checkout vue
    ```
2. Copy environment file:
    ```bash
    cp .env-sample .env
    ```
3. Start services:
    ```bash
    docker compose up --build
    ```
4. Open the app:
    - **Frontend (Vue):** http://localhost:8080
    - **Backend API (FastAPI):** http://localhost:8000/api/health
    - **API docs:** http://localhost:8000/docs

The SQLite database is stored in `./instance/warranty.db` and is shared with the FastAPI container via a volume mount. Existing databases from the Flask app are compatible.

## Local development

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The Vite dev server runs on http://localhost:5173 and proxies `/api` requests to the FastAPI backend.

## API overview

| Method     | Endpoint                | Description              |
| ---------- | ----------------------- | ------------------------ |
| GET        | `/api/stats`            | Item and shop counts     |
| GET/POST   | `/api/items`            | List / create items      |
| PUT/DELETE | `/api/items/{id}`       | Update / delete item     |
| GET/POST   | `/api/shops`            | List / create shops      |
| PUT/DELETE | `/api/shops/{id}`       | Update / delete shop     |
| GET        | `/api/search?query=`    | Search items and shops   |
| GET        | `/api/database/export`  | Download DB backup       |
| POST       | `/api/database/restore` | Restore from backup file |
| POST       | `/api/database/purge`   | Purge orphaned records   |

## Contributing

- Fork the repository
- Create a new branch
- Make your changes
- Submit a pull request

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

- LinkedIn: https://www.linkedin.com/in/tomas-muhr/
