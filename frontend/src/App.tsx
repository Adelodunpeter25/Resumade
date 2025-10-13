import { lazy, Suspense } from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'

// Eager load critical pages
import LandingPage from './pages/LandingPage'
import Login from './pages/Login'
import Register from './pages/Register'

// Lazy load non-critical pages
const ForgotPassword = lazy(() => import('./pages/ForgotPassword'))
const ResetPassword = lazy(() => import('./pages/ResetPassword'))
const AuthCallback = lazy(() => import('./pages/AuthCallback'))
const Dashboard = lazy(() => import('./pages/Dashboard'))
const ResumeBuilder = lazy(() => import('./pages/ResumeBuilder'))
const TemplateSelector = lazy(() => import('./pages/TemplateSelector'))
const ATSScore = lazy(() => import('./pages/ATSScore'))
const ResumeShare = lazy(() => import('./pages/ResumeShare'))
const SharedResume = lazy(() => import('./pages/SharedResume'))
const VersionHistory = lazy(() => import('./pages/VersionHistory'))
const ResumePreview = lazy(() => import('./pages/ResumePreview'))
const Templates = lazy(() => import('./pages/Templates'))
const PrivacyPolicy = lazy(() => import('./pages/PrivacyPolicy'))
const TermsOfService = lazy(() => import('./pages/TermsOfService'))

// Loading fallback
const LoadingFallback = () => (
  <div className="min-h-screen flex items-center justify-center">
    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-emerald-600"></div>
  </div>
)

function App() {
  return (
    <BrowserRouter>
      <Suspense fallback={<LoadingFallback />}>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/templates" element={<Templates />} />
          <Route path="/privacy" element={<PrivacyPolicy />} />
          <Route path="/terms" element={<TermsOfService />} />
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
      </Suspense>
    </BrowserRouter>
  )
}

export default App
