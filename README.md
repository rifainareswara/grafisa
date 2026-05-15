# Grafisa — Template Canva Store

E-commerce untuk menjual template Canva siap pakai. Dibangun dengan **FastAPI** (backend) dan **SvelteKit** (frontend).

---

## Daftar Isi

- [Tech Stack](#tech-stack)
- [Fitur](#fitur)
- [Menjalankan Secara Lokal](#menjalankan-secara-lokal)
- [Menjalankan dengan Docker](#menjalankan-dengan-docker)
- [Deploy ke Google Cloud Run](#deploy-ke-google-cloud-run)
- [Konfigurasi Midtrans](#konfigurasi-midtrans)
- [Admin Panel](#admin-panel)
- [Struktur Project](#struktur-project)

---

## Tech Stack

| Layer | Teknologi |
|---|---|
| Backend | Python 3.12, FastAPI, SQLAlchemy, SQLite |
| Frontend | SvelteKit 2, Svelte 5, TailwindCSS v4 |
| Payment | Midtrans Snap |
| Container | Docker, Docker Compose |
| Deploy | Google Cloud Run |

---

## Fitur

- Landing page dengan showcase produk
- Halaman daftar & detail produk
- Keranjang belanja (disimpan di localStorage)
- Checkout & pembayaran via Midtrans (QRIS, GoPay, OVO, Transfer Bank)
- Halaman sukses setelah pembayaran
- Admin panel: statistik, kelola produk (CRUD), lihat semua order

---

## Menjalankan Secara Lokal

### Prasyarat

- Python 3.10+
- Node.js 18+

### 1. Clone & masuk folder

```bash
git clone <repo-url>
cd technocrat
```

### 2. Setup Backend

```bash
cd backend

# Buat virtual environment
python3 -m venv venv
source venv/bin/activate          # Mac/Linux
# venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt

# Konfigurasi environment
cp .env.example .env
# Edit .env sesuai kebutuhan (lihat bagian Konfigurasi)

# Jalankan server
uvicorn app.main:app --reload --port 8000
# API tersedia di http://localhost:8000
# Docs: http://localhost:8000/docs
```

### 3. Setup Frontend

```bash
cd frontend

# Install dependencies
npm install

# Konfigurasi (opsional)
cp .env.example .env

# Jalankan dev server
npm run dev
# Frontend tersedia di http://localhost:5173
```

### Shortcut: gunakan script

```bash
# Terminal 1
./start-backend.sh

# Terminal 2
./start-frontend.sh
```

---

## Menjalankan dengan Docker

### Prasyarat

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) terinstall

### Langkah

```bash
# 1. Buat file .env di root project
cp backend/.env.example .env
# Edit .env — isi MIDTRANS_SERVER_KEY, MIDTRANS_CLIENT_KEY, dll

# 2. Build & jalankan semua service
docker compose up --build

# Frontend: http://localhost:3000
# Backend:  http://localhost:8000
```

### Perintah Docker berguna

```bash
# Jalankan di background
docker compose up -d --build

# Lihat log
docker compose logs -f

# Stop
docker compose down

# Stop dan hapus data (database)
docker compose down -v
```

---

## Deploy ke Google Cloud Run

### Prasyarat

1. Akun [Google Cloud](https://console.cloud.google.com/) dengan billing aktif
2. [Google Cloud CLI](https://cloud.google.com/sdk/docs/install) terinstall
3. [Docker](https://www.docker.com/) terinstall

### Langkah 1 — Persiapan GCP

```bash
# Login ke Google Cloud
gcloud auth login

# Set project (buat project baru jika belum ada)
gcloud config set project NAMA_PROJECT_KAMU

# Aktifkan service yang diperlukan
gcloud services enable \
  run.googleapis.com \
  artifactregistry.googleapis.com \
  cloudbuild.googleapis.com

# Buat Artifact Registry repository
gcloud artifacts repositories create grafisa \
  --repository-format=docker \
  --location=asia-southeast2 \
  --description="Grafisa container images"

# Login ke registry
gcloud auth configure-docker asia-southeast2-docker.pkg.dev
```

### Langkah 2 — Build & Push Image Backend

```bash
cd backend

# Build image
docker build -t asia-southeast2-docker.pkg.dev/NAMA_PROJECT_KAMU/grafisa/backend:latest .

# Push ke Artifact Registry
docker push asia-southeast2-docker.pkg.dev/NAMA_PROJECT_KAMU/grafisa/backend:latest
```

### Langkah 3 — Deploy Backend ke Cloud Run

```bash
gcloud run deploy grafisa-backend \
  --image asia-southeast2-docker.pkg.dev/NAMA_PROJECT_KAMU/grafisa/backend:latest \
  --region asia-southeast2 \
  --platform managed \
  --allow-unauthenticated \
  --port 8000 \
  --memory 512Mi \
  --set-env-vars "SECRET_KEY=GANTI_DENGAN_SECRET_PANJANG" \
  --set-env-vars "ADMIN_USERNAME=admin" \
  --set-env-vars "ADMIN_PASSWORD=GANTI_PASSWORD_AMAN" \
  --set-env-vars "MIDTRANS_SERVER_KEY=SB-Mid-server-xxxxx" \
  --set-env-vars "MIDTRANS_CLIENT_KEY=SB-Mid-client-xxxxx" \
  --set-env-vars "MIDTRANS_IS_PRODUCTION=false" \
  --set-env-vars "FRONTEND_URL=https://DOMAIN_FRONTEND_KAMU"
```

> Setelah deploy, catat **URL backend** yang diberikan (bentuknya: `https://grafisa-backend-xxxx-et.a.run.app`)

### Langkah 4 — Build & Push Image Frontend

```bash
cd frontend

# Build image (PUBLIC_API_URL di-set saat runtime, bukan build time)
docker build \
  -t asia-southeast2-docker.pkg.dev/NAMA_PROJECT_KAMU/grafisa/frontend:latest .

# Push
docker push asia-southeast2-docker.pkg.dev/NAMA_PROJECT_KAMU/grafisa/frontend:latest
```

### Langkah 5 — Deploy Frontend ke Cloud Run

```bash
gcloud run deploy grafisa-frontend \
  --image asia-southeast2-docker.pkg.dev/NAMA_PROJECT_KAMU/grafisa/frontend:latest \
  --region asia-southeast2 \
  --platform managed \
  --allow-unauthenticated \
  --port 3000 \
  --memory 256Mi \
  --set-env-vars "PUBLIC_API_URL=https://grafisa-backend-xxxx-et.a.run.app"
```

### Langkah 6 — Update CORS Backend

Setelah mendapat URL frontend, update `FRONTEND_URL` di backend:

```bash
gcloud run services update grafisa-backend \
  --region asia-southeast2 \
  --update-env-vars "FRONTEND_URL=https://grafisa-frontend-xxxx-et.a.run.app"
```

### Langkah 7 — Setup Midtrans Notification URL

Di [dashboard Midtrans](https://dashboard.sandbox.midtrans.com):
1. Buka **Settings → Configuration**
2. Set **Payment Notification URL** ke:
   ```
   https://grafisa-backend-xxxx-et.a.run.app/api/payment/notification
   ```

---

## Konfigurasi Midtrans

### Mendapatkan API Key (Sandbox / Testing)

1. Daftar di [sandbox.midtrans.com](https://sandbox.midtrans.com)
2. Login → **Settings → Access Keys**
3. Salin **Server Key** dan **Client Key**

### Konfigurasi di `.env`

```env
MIDTRANS_SERVER_KEY=SB-Mid-server-xxxxxxxxxxxxxxxxxxxxxx
MIDTRANS_CLIENT_KEY=SB-Mid-client-xxxxxxxxxxxxxxxxxxxxxx
MIDTRANS_IS_PRODUCTION=false
```

### Testing Pembayaran (Sandbox)

Gunakan kartu test Midtrans:
- **VISA**: `4811 1111 1111 1114` — CVV: `123` — Exp: `01/25`
- **Mastercard**: `5211 1111 1111 1117`
- **GoPay / QRIS**: Scan dengan [Midtrans Simulator](https://simulator.sandbox.midtrans.com)

---

## Admin Panel

Akses: `http://localhost:5173/admin` (atau URL production)

| Fitur | Keterangan |
|---|---|
| Dashboard | Statistik revenue, order paid/pending, jumlah produk |
| Kelola Produk | Tambah, edit, hapus produk + link Canva |
| Semua Order | Lihat semua order, filter by status |

**Kredensial default**: `admin` / `admin123`

> Ganti password di `backend/.env` sebelum deploy ke production!

---

## Environment Variables

### Backend (`backend/.env`)

| Variable | Keterangan | Default |
|---|---|---|
| `SECRET_KEY` | JWT signing key — **wajib diganti** di production | `dev-secret...` |
| `ADMIN_USERNAME` | Username admin panel | `admin` |
| `ADMIN_PASSWORD` | Password admin panel | `admin123` |
| `MIDTRANS_SERVER_KEY` | Server key dari Midtrans | — |
| `MIDTRANS_CLIENT_KEY` | Client key dari Midtrans | — |
| `MIDTRANS_IS_PRODUCTION` | `true` untuk live, `false` untuk sandbox | `false` |
| `FRONTEND_URL` | URL frontend (untuk CORS) | `http://localhost:5173` |
| `DB_PATH` | Path file SQLite | `./grafisa.db` |

### Frontend (`frontend/.env`)

| Variable | Keterangan | Default |
|---|---|---|
| `PUBLIC_API_URL` | URL backend API | `http://localhost:8000` |

---

## Struktur Project

```
technocrat/
├── backend/
│   ├── app/
│   │   ├── main.py          # Entry point FastAPI
│   │   ├── database.py      # SQLAlchemy setup
│   │   ├── models.py        # Database models
│   │   ├── schemas.py       # Pydantic schemas
│   │   ├── auth.py          # JWT admin auth
│   │   ├── config.py        # App settings
│   │   ├── seed.py          # Seed data produk
│   │   └── routers/
│   │       ├── products.py  # CRUD produk
│   │       ├── orders.py    # Buat & lihat order
│   │       ├── payment.py   # Midtrans integration
│   │       └── admin.py     # Login & statistik
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── lib/
│   │   │   ├── api.js           # API client
│   │   │   └── stores/
│   │   │       └── cart.js      # Cart store (Svelte)
│   │   └── routes/
│   │       ├── +layout.svelte   # Navbar & Footer
│   │       ├── +page.svelte     # Landing page
│   │       ├── products/        # Daftar & detail produk
│   │       ├── cart/            # Keranjang
│   │       ├── checkout/        # Form checkout
│   │       ├── payment/success/ # Halaman sukses
│   │       └── admin/           # Admin panel
│   ├── Dockerfile
│   ├── svelte.config.js
│   └── .env.example
│
├── docker-compose.yml
├── .gitignore
├── start-backend.sh
├── start-frontend.sh
└── README.md
```

---

## API Endpoints

| Method | Endpoint | Keterangan |
|---|---|---|
| `GET` | `/api/products/` | Daftar semua produk |
| `GET` | `/api/products/{id}` | Detail produk |
| `POST` | `/api/products/` | Tambah produk (admin) |
| `PUT` | `/api/products/{id}` | Update produk (admin) |
| `DELETE` | `/api/products/{id}` | Hapus produk (admin) |
| `POST` | `/api/orders/` | Buat order baru |
| `GET` | `/api/orders/{order_id}` | Detail order |
| `GET` | `/api/orders/` | Semua order (admin) |
| `POST` | `/api/payment/create/{order_id}` | Buat transaksi Midtrans |
| `POST` | `/api/payment/notification` | Webhook Midtrans |
| `POST` | `/api/admin/login` | Login admin |
| `GET` | `/api/admin/stats` | Statistik dashboard (admin) |

Dokumentasi interaktif tersedia di: `http://localhost:8000/docs`
