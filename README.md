# Resumade 

A full-stack resume builder with ATS optimization, real-time editing, and multiple export formats.
Build and customize professional resumes with beautiful, responsive templates, real-time preview, and support for PDF, DOCX, and TXT exports.


![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.13-blue.svg)
![React](https://img.shields.io/badge/react-18.3-blue.svg)

## ✨ Features

### Core Features
- 🎨 **Multiple Professional Templates** - Choose from modern, professional designs
- 📝 **Real-time Preview** - See changes instantly as you type
- 🤖 **AI-Powered ATS Optimization** - Google Gemini AI provides intelligent scoring and personalized recommendations
- 📊 **Skill Validation** - 127+ validated technical and soft skills
- 📄 **Multiple Export Formats** - PDF, DOCX, and TXT
- 📤 **PDF Upload & Parse** - Extract data from existing resumes
- 📜 **Version History** - Track and restore previous versions (Authenticated user)
- 🔗 **Smart Resume Sharing** - Generate shareable links with custom expiration
- 🎨 **Template Customization** - Customize colors, fonts, and layout

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
- **Google Gemini AI** - AI-powered resume feedback
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
- npm

### Installation

#### 1. Clone the repository
```bash
git clone https://github.com/Adelodunpeter25/Resumade.git
cd Resumade
```

#### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip3 install -r requirements.txt

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
