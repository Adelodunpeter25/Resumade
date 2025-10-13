# Resumade 📄

A modern resume builder with ATS optimization, multiple export formats, and real-time preview.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.13-blue.svg)
![React](https://img.shields.io/badge/react-18.3-blue.svg)

## ✨ Features

### Core Features
- 🎨 **Multiple Professional Templates** - Choose from modern, professional designs
- 📝 **Real-time Preview** - See changes instantly as you type
- 🤖 **ATS Optimization** - Automated scoring and feedback for applicant tracking systems
- 📊 **Skill Validation** - 127+ validated technical and soft skills
- 📄 **Multiple Export Formats** - PDF, DOCX, and TXT
- 📤 **PDF Upload & Parse** - Extract data from existing resumes
- 📜 **Version History** - Track and restore previous versions (Authenticated user)
- 🎨 **Template Customization** - Customize colors, fonts, and layout
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile

### Authentication & Security
- 🔐 **Email/Password Authentication**
- 🔑 **Google OAuth Integration**
- 🔒 **Password Reset via Email**
- 👤 **Guest Mode** - Create resumes without signing up


---

## 🏗️ Tech Stack

### Frontend
- **React 18.3** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Tailwind CSS 4** - Styling
- **React Router 7** - Routing
- **Lucide React** - Icons
- **React Quill** - Rich text editor

### Backend
- **FastAPI** - Python web framework
- **SQLAlchemy** - ORM
- **PostgreSQL** - Database
- **Alembic** - Database migrations
- **WeasyPrint** - PDF generation
- **python-docx** - DOCX generation
- **Resend** - Email service
- **Supabase** - File storage

### Infrastructure
- **Asyncpg** - Async PostgreSQL driver
- **JWT** - Authentication
- **Bcrypt** - Password hashing
- **Pydantic** - Data validation

---

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- Node.js 18+
- PostgreSQL 14+
- npm or yarn

### Installation

#### 1. Clone the repository
```bash
git clone https://github.com/Adelodunpeter25/resumade.git
cd resumade
```

#### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env with your configuration
# DATABASE_URL, SECRET_KEY, etc.

# Run migrations
alembic upgrade head

# Start backend server
uvicorn app.main:app --reload --port 8000
```

#### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Copy environment file
cp .env.example .env

# Edit .env with your configuration
# VITE_API_URL=http://localhost:8000

# Start development server
npm run dev
```

#### 4. Access the application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## 📁 Project Structure

```
resumade/
├── backend/
│   ├── app/
│   │   ├── core/           # Core configuration
│   │   ├── endpoints/      # API endpoints
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   └── main.py         # FastAPI app
│   ├── migrations/         # Alembic migrations
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── hooks/          # Custom hooks
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   ├── types/          # TypeScript types
│   │   ├── App.tsx         # Main app
│   │   └── main.tsx        # Entry point
│   ├── package.json
│   └── vite.config.ts
│
└── README.md
```

---

## 🔧 Configuration

### Backend Environment Variables

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/resumade

# Security
SECRET_KEY=your-secret-key-here
DEBUG=False

# JWT
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Supabase Storage
SUPABASE_URL=https://your-project.supabase.co
SERVICE_ROLE=your-service-role-key
BUCKET_NAME=resumes

# Google OAuth
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
GOOGLE_REDIRECT_URI=http://localhost:8000/api/auth/google/callback

# Frontend URL
FRONTEND_URL=http://localhost:3000

# Email (Resend)
RESEND_API_KEY=re_your_api_key
EMAIL_FROM=Resumade <noreply@yourdomain.com>
```

### Frontend Environment Variables

```env
VITE_API_URL=http://localhost:8000
```

---

---

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

---

## 🚀 Deployment

### Backend (Production)

```bash
# Install production dependencies
pip install -r requirements.txt

# Set production environment variables
export DEBUG=False
export DATABASE_URL=your-production-db-url

# Run migrations
alembic upgrade head

# Start backend server
uvicorn app.main:app --port 8000 --log-level info

### Frontend (Production)

```bash
# Build for production
npm run build

# Start frontend server
npm run dev
```

---

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [React](https://react.dev/) - UI library
- [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS
- [WeasyPrint](https://weasyprint.org/) - PDF generation
- [Lucide](https://lucide.dev/) - Beautiful icons

---

**Built with ❤️ by the Resumade Team**
