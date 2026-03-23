# 🧠 AI Lab — From Zero to AI Architect

An **interactive AI learning platform** built with Django — inspired by KafkaLab.  
Learn AI through simulations and visualizers, not static documentation.

---

## 🚀 Quick Start (Local)

```bash
# 1. Clone / navigate into project
cd AL_ML_TECH_DASHBOARD

# 2. Create & activate virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy environment file
cp .env .env.local  # already has AWS Bedrock credentials

# 5. Run migrations
python manage.py migrate

# 6. Seed AI modules (7 modules, 19 sections, 55 concepts)
python manage.py seed_data

# 7. Create admin user (already created: admin@ailab.com / admin123)
python manage.py createsuperuser

# 8. Start server (with WebSocket support)
./start.sh
# OR manually:
daphne -b 0.0.0.0 -p 8000 ailab.asgi:application
```

Open → **http://localhost:8000**

---

## 📁 Project Structure

```
AL_ML_TECH_DASHBOARD/
├── ailab/                  # Django project config
│   ├── settings.py         # All settings (Bedrock, JWT, Channels)
│   ├── urls.py             # Root URL routing
│   └── asgi.py             # ASGI + WebSocket routing
│
├── users/                  # Auth app
│   ├── models.py           # CustomUser (email login, roles)
│   ├── views.py            # Register, Login, Logout, Profile
│   └── urls.py             # /api/auth/*
│
├── modules/                # Learning content app
│   ├── models.py           # Module, Section, Concept, UserProgress, Quiz
│   ├── views.py            # Module list/detail, progress, quiz
│   ├── admin.py            # Django admin
│   └── management/
│       └── commands/
│           └── seed_data.py  # Seeds all 7 AI modules
│
├── simulations/            # Simulation engine app
│   ├── engine.py           # 8 simulators (NN, GD, RAG, Agent, etc.)
│   ├── views.py            # REST endpoints for each simulator
│   ├── consumers.py        # WebSocket streaming consumer
│   └── routing.py          # WS URL: ws://localhost:8000/ws/simulation/
│
├── ai_service/             # AWS Bedrock LLM app
│   ├── bedrock.py          # Bedrock Claude client + streaming
│   ├── views.py            # Chat, Explain, Quiz Gen, Code Review
│   ├── consumers.py        # WebSocket LLM streaming
│   └── routing.py          # WS URL: ws://localhost:8000/ws/ai/chat/
│
├── core/                   # Frontend pages app
│   ├── views.py            # Renders all HTML templates
│   └── urls.py             # Page URL routing
│
├── templates/
│   ├── base.html           # Dark theme sidebar layout
│   └── core/
│       ├── home.html           # Landing + module grid
│       ├── module_learn.html   # Module lesson viewer
│       ├── rag_visualizer.html # RAG pipeline animation
│       ├── agent_visualizer.html  # Agent flow simulator
│       ├── llm_params_lab.html # LLM parameter playground
│       ├── neural_network_lab.html # Canvas NN visualizer
│       ├── ai_chat.html        # Claude live chat
│       └── playground.html     # Lab launcher hub
│
├── .env                    # AWS Bedrock + Django config
├── requirements.txt        # Python dependencies
└── start.sh                # One-command startup script
```

---

## 🌐 Pages & URLs

| Page | URL |
|------|-----|
| Homepage | `http://localhost:8000/` |
| AI Basics | `http://localhost:8000/learn/ai-basics/` |
| Machine Learning | `http://localhost:8000/learn/machine-learning-deep-dive/` |
| Deep Learning | `http://localhost:8000/learn/deep-learning-lab/` |
| Generative AI | `http://localhost:8000/learn/generative-ai/` |
| LLM Systems | `http://localhost:8000/learn/llm-systems/` |
| Agentic AI | `http://localhost:8000/learn/agentic-ai/` |
| Neural Network Lab | `http://localhost:8000/neural-network/` |
| RAG Visualizer | `http://localhost:8000/rag-visualizer/` |
| Agent Visualizer | `http://localhost:8000/agent-visualizer/` |
| LLM Params Lab | `http://localhost:8000/llm-params/` |
| AI Chat (Claude) | `http://localhost:8000/ai-chat/` |
| Playground | `http://localhost:8000/playground/` |
| Django Admin | `http://localhost:8000/admin/` |

---

## 🔌 REST API Endpoints

### Auth — `/api/auth/`
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | Create account |
| POST | `/api/auth/login/` | Login → JWT tokens |
| POST | `/api/auth/logout/` | Logout |
| GET/PATCH | `/api/auth/profile/` | User profile |
| POST | `/api/auth/token/refresh/` | Refresh JWT |

### Modules — `/api/modules/`
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/modules/` | List all modules |
| GET | `/api/modules/<slug>/` | Module detail + sections |
| GET | `/api/modules/dashboard/` | User dashboard stats |
| POST | `/api/modules/<slug>/progress/` | Update progress |
| GET | `/api/modules/<slug>/quiz/` | Get quiz questions |
| POST | `/api/modules/<slug>/quiz/submit/` | Submit answers |

### Simulations — `/api/simulations/`
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/simulations/neural-network/` | Run NN simulation |
| POST | `/api/simulations/gradient-descent/` | Run gradient descent |
| GET | `/api/simulations/activation-functions/` | Activation fn data |
| POST | `/api/simulations/bias-variance/` | Bias-variance sim |
| POST | `/api/simulations/llm-params/` | LLM params simulator |
| POST | `/api/simulations/rag-pipeline/` | RAG pipeline sim |
| POST | `/api/simulations/agent-flow/` | Agent flow sim |
| POST | `/api/simulations/tokenizer/` | Tokenizer visualizer |

### AI Service — `/api/ai/`
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/ai/chat/` | Chat with Claude |
| POST | `/api/ai/explain/` | Explain a concept |
| POST | `/api/ai/quiz/generate/` | Generate quiz via AI |
| POST | `/api/ai/code-review/` | AI code review |

### WebSocket
| URL | Description |
|-----|-------------|
| `ws://localhost:8000/ws/ai/chat/` | Streaming Claude chat |
| `ws://localhost:8000/ws/simulation/` | Real-time simulation |

---

## ⚙️ Environment Variables (`.env`)

```env
DEBUG=True
SECRET_KEY=your-secret-key

# AWS Bedrock (Claude Opus 4.5)
AWS_ACCESS_KEY_ID=AKIA53QGATJFQZPL6DUO
AWS_SECRET_ACCESS_KEY=...
AWS_DEFAULT_REGION=ap-south-1
BEDROCK_MODEL_ID=arn:aws:bedrock:ap-south-1:...

# Database (SQLite for local, Postgres for prod)
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=ailab_db
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 5.2 + DRF |
| WebSocket | Django Channels + Daphne |
| Auth | JWT (djangorestframework-simplejwt) |
| AI/LLM | AWS Bedrock (Claude Opus 4.5) |
| Database | SQLite (local) / PostgreSQL (prod) |
| Frontend | Django Templates + Vanilla JS + Canvas |
| Fonts | Google Fonts (Inter + JetBrains Mono) |

---

## 🚀 Deployment (Netlify / Cloud)

For production deployment, update `.env`:
```env
DEBUG=False
DB_ENGINE=django.db.backends.postgresql
DB_NAME=ailab_prod
DB_HOST=your-rds-host
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=your-password
REDIS_URL=redis://your-redis:6379/0
ALLOWED_HOSTS=yourdomain.com
```

Then:
```bash
pip install psycopg2-binary gunicorn
python manage.py collectstatic
daphne -b 0.0.0.0 -p 8000 ailab.asgi:application
```

---

## 👤 Admin Credentials (Local)
- **Email:** `admin@ailab.com`  
- **Password:** `admin123`
- **Admin Panel:** http://localhost:8000/admin/
