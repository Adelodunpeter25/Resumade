import { BrowserRouter, Routes, Route } from 'react-router-dom'
import LandingPage from './pages/LandingPage'
import Login from './pages/Login'
import Register from './pages/Register'
import ForgotPassword from './pages/ForgotPassword'
import ResetPassword from './pages/ResetPassword'
import AuthCallback from './pages/AuthCallback'
import Dashboard from './pages/Dashboard'
import ResumeBuilder from './pages/ResumeBuilder'
import TemplateSelector from './pages/TemplateSelector'
import ATSScore from './pages/ATSScore'
import ResumeShare from './pages/ResumeShare'
import SharedResume from './pages/SharedResume'
import VersionHistory from './pages/VersionHistory'
import ResumePreview from './pages/ResumePreview'
import Templates from './pages/Templates'
import PrivacyPolicy from './pages/PrivacyPolicy'
import TermsOfService from './pages/TermsOfService'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/templates" element={<Templates />} />
        <Route path="/privacy" element={<PrivacyPolicy />} />
        <Route path="/terms" element={<TermsOfService />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/reset-password" element={<ResetPassword />} />
        <Route path="/auth/callback" element={<AuthCallback />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/resume/:id" element={<ResumeBuilder />} />
        <Route path="/resume/:id/templates" element={<TemplateSelector />} />
        <Route path="/resume/:id/ats-score" element={<ATSScore />} />
        <Route path="/resume/:id/share" element={<ResumeShare />} />
        <Route path="/resume/:id/versions" element={<VersionHistory />} />
        <Route path="/resume/:id/preview" element={<ResumePreview />} />
        <Route path="/shared/:token" element={<SharedResume />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
