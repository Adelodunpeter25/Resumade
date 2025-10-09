import { useState, useEffect, useCallback } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { ArrowLeft, Save, Eye, Palette, BarChart3, History, Check, LogIn, Download } from 'lucide-react'
import { resumeService } from '../services'
import type { Resume, Template } from '../types'

import PersonalInfoForm from '../components/resume/PersonalInfoForm'
import ExperienceForm from '../components/resume/ExperienceForm'
import EducationForm from '../components/resume/EducationForm'
import SkillsForm from '../components/resume/SkillsForm'
import CertificationsForm from '../components/resume/CertificationsForm'
import ProjectsForm from '../components/resume/ProjectsForm'
import ResumePreviewHTML from '../components/resume/ResumePreviewHTML'

const steps = [
  { id: 'personal', label: 'Personal Info', component: PersonalInfoForm },
  { id: 'experience', label: 'Experience', component: ExperienceForm },
  { id: 'education', label: 'Education', component: EducationForm },
  { id: 'skills', label: 'Skills', component: SkillsForm },
  { id: 'certifications', label: 'Certifications', component: CertificationsForm },
  { id: 'projects', label: 'Projects', component: ProjectsForm }
]

const GUEST_RESUME_KEY = 'guest_resume'

export default function ResumeBuilder() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [currentStep, setCurrentStep] = useState(0)
  const [resume, setResume] = useState<Partial<Resume>>({
    title: 'Untitled Resume',
    template_name: 'professional-blue',
    personal_info: {
      full_name: '',
      email: '',
      phone: '',
      location: '',
      linkedin: '',
      website: '',
      summary: ''
    },
    experience: [],
    education: [],
    skills: [],
    certifications: [],
    projects: []
  })
  const [templates, setTemplates] = useState<Template[]>([])
  const [saving, setSaving] = useState(false)
  const [saveStatus, setSaveStatus] = useState<'saved' | 'saving' | 'unsaved'>('saved')
  const [loading, setLoading] = useState(!!id)
  const [showTemplateDropdown, setShowTemplateDropdown] = useState(false)
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [downloading, setDownloading] = useState(false)

  useEffect(() => {
    const token = localStorage.getItem('token')
    setIsAuthenticated(!!token)
    
    loadTemplates()
    
    if (id && id !== 'new') {
      if (token) {
        loadResume()
      } else {
        navigate('/login')
      }
    } else if (id === 'new' && !token) {
      // Guest mode - load from localStorage
      const savedResume = localStorage.getItem(GUEST_RESUME_KEY)
      if (savedResume) {
        setResume(JSON.parse(savedResume))
      }
      setLoading(false)
    } else {
      setLoading(false)
    }
  }, [id])

  // Autosave effect
  useEffect(() => {
    if (saveStatus === 'saved') return

    const timer = setTimeout(() => {
      handleSave(true)
    }, 2000)

    return () => clearTimeout(timer)
  }, [resume, saveStatus])

  const loadTemplates = async () => {
    try {
      const response = await resumeService.getTemplates()
      if (response.success && response.data) {
        setTemplates(response.data)
      }
    } catch (err) {
      // Fallback templates for guests
      setTemplates([
        { name: 'professional-blue', display_name: 'Professional Blue', description: 'Clean and professional', preview_url: '' },
        { name: 'minimalist-two-column', display_name: 'Minimalist', description: 'Simple and elegant', preview_url: '' }
      ])
    }
  }

  const loadResume = async () => {
    try {
      const response = await resumeService.getResume(Number(id))
      if (response.success && response.data) {
        setResume(response.data)
      }
    } catch (err) {
      alert('Failed to load resume')
      navigate('/dashboard')
    } finally {
      setLoading(false)
    }
  }

  const handleSave = async (isAutosave = false) => {
    if (!isAutosave) setSaving(true)
    setSaveStatus('saving')
    
    try {
      if (!isAuthenticated) {
        // Guest mode - save to localStorage
        localStorage.setItem(GUEST_RESUME_KEY, JSON.stringify(resume))
        setSaveStatus('saved')
      } else if (id && id !== 'new') {
        await resumeService.updateResume(Number(id), resume)
        setSaveStatus('saved')
      } else {
        const response = await resumeService.createResume(resume)
        if (response.success && response.data) {
          navigate(`/resume/${response.data.id}`, { replace: true })
        }
        setSaveStatus('saved')
      }
    } catch (err) {
      alert('Failed to save resume')
      setSaveStatus('unsaved')
    } finally {
      if (!isAutosave) setSaving(false)
    }
  }

  const updateResumeData = useCallback((field: string, value: any) => {
    setResume(prev => ({ ...prev, [field]: value }))
    setSaveStatus('unsaved')
  }, [])

  const changeTemplate = (templateName: string) => {
    updateResumeData('template_name', templateName)
    setShowTemplateDropdown(false)
  }

  const handleFeatureClick = (feature: string) => {
    if (!isAuthenticated) {
      if (confirm(`${feature} requires an account. Would you like to login or sign up?`)) {
        handleLoginPrompt()
      }
      return
    }
    
    // Navigate to feature
    switch(feature) {
      case 'versions':
        navigate(`/resume/${id}/versions`)
        break
      case 'ats':
        navigate(`/resume/${id}/ats-score`)
        break
      case 'preview':
        navigate(`/resume/${id}/preview`)
        break
    }
  }

  const handleLoginPrompt = () => {
    navigate('/login')
  }

  const handleDownload = async () => {
    setDownloading(true)
    try {
      let blob: Blob
      
      if (isAuthenticated && id && id !== 'new') {
        blob = await resumeService.downloadPDF(Number(id), resume.template_name)
      } else {
        // Guest download
        blob = await resumeService.generateGuestPDF(resume, resume.template_name || 'professional-blue')
      }
      
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `${resume.title || 'resume'}.pdf`
      a.click()
      window.URL.revokeObjectURL(url)
    } catch (err) {
      alert('Failed to download PDF')
    } finally {
      setDownloading(false)
    }
  }

  const CurrentStepComponent = steps[currentStep].component

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="w-16 h-16 border-4 border-emerald-600 border-t-transparent rounded-full animate-spin"></div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-full mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-4">
              <button
                onClick={() => navigate(isAuthenticated ? '/dashboard' : '/')}
                className="p-2 hover:bg-gray-100 rounded-lg"
              >
                <ArrowLeft size={20} />
              </button>
              <input
                type="text"
                value={resume.title}
                onChange={(e) => updateResumeData('title', e.target.value)}
                className="text-xl font-bold border-none focus:outline-none focus:ring-2 focus:ring-emerald-500 rounded px-2"
              />
              <span className="text-sm text-gray-500">
                {saveStatus === 'saving' && '💾 Saving...'}
                {saveStatus === 'saved' && <span className="flex items-center gap-1 text-green-600"><Check size={16} /> Saved</span>}
                {saveStatus === 'unsaved' && '⚠️ Unsaved changes'}
              </span>
              {!isAuthenticated && (
                <span className="text-xs bg-yellow-100 text-yellow-800 px-2 py-1 rounded">
                  Guest Mode
                </span>
              )}
            </div>
            <div className="flex items-center gap-2">
              {!isAuthenticated && (
                <button
                  onClick={handleLoginPrompt}
                  className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                  <LogIn size={20} />
                  <span>Login to Save</span>
                </button>
              )}
              <div className="relative">
                <button
                  onClick={() => setShowTemplateDropdown(!showTemplateDropdown)}
                  className="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
                >
                  <Palette size={20} />
                  <span>Template</span>
                </button>
                {showTemplateDropdown && (
                  <div className="absolute right-0 mt-2 w-64 bg-white rounded-lg shadow-xl border border-gray-200 z-20">
                    {templates.map((template) => (
                      <button
                        key={template.name}
                        onClick={() => changeTemplate(template.name)}
                        className={`w-full text-left px-4 py-3 hover:bg-gray-50 border-b border-gray-100 last:border-0 ${
                          resume.template_name === template.name ? 'bg-emerald-50' : ''
                        }`}
                      >
                        <div className="font-medium text-gray-900">{template.display_name}</div>
                        <div className="text-xs text-gray-500">{template.description}</div>
                      </button>
                    ))}
                  </div>
                )}
              </div>
              <button
                onClick={() => handleFeatureClick('versions')}
                className="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
                title={!isAuthenticated ? 'Login required' : 'Version History'}
              >
                <History size={20} />
              </button>
              <button
                onClick={() => handleFeatureClick('ats')}
                className="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
                title={!isAuthenticated ? 'Login required' : 'ATS Score'}
              >
                <BarChart3 size={20} />
              </button>
              <button
                onClick={!isAuthenticated ? handleDownload : () => handleFeatureClick('preview')}
                disabled={!isAuthenticated && downloading}
                className="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50"
                title={!isAuthenticated ? 'Download PDF' : 'Preview & Download'}
              >
                {!isAuthenticated ? <Download size={20} /> : <Eye size={20} />}
                {!isAuthenticated && downloading && <span className="text-xs">...</span>}
              </button>
              <button
                onClick={() => handleSave(false)}
                disabled={saving}
                className="flex items-center gap-2 bg-gradient-to-r from-emerald-600 to-teal-600 text-white px-4 py-2 rounded-lg hover:from-emerald-700 hover:to-teal-700 disabled:opacity-50"
              >
                <Save size={20} />
                <span>{saving ? 'Saving...' : 'Save'}</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-12 gap-6">
          {/* Steps Sidebar */}
          <div className="col-span-2">
            <div className="bg-white rounded-lg shadow p-4 sticky top-24">
              <h3 className="font-semibold text-gray-900 mb-4">Sections</h3>
              <nav className="space-y-2">
                {steps.map((step, index) => (
                  <button
                    key={step.id}
                    onClick={() => setCurrentStep(index)}
                    className={`w-full text-left px-4 py-2 rounded-lg transition-colors text-sm ${
                      currentStep === index
                        ? 'bg-emerald-50 text-emerald-600 font-medium'
                        : 'text-gray-600 hover:bg-gray-50'
                    }`}
                  >
                    {step.label}
                  </button>
                ))}
              </nav>
            </div>
          </div>

          {/* Form Content */}
          <div className="col-span-5">
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">
                {steps[currentStep].label}
              </h2>
              <CurrentStepComponent
                data={resume}
                onChange={updateResumeData}
              />
              
              {/* Navigation Buttons */}
              <div className="flex justify-between mt-8 pt-6 border-t border-gray-200">
                <button
                  onClick={() => setCurrentStep(prev => Math.max(0, prev - 1))}
                  disabled={currentStep === 0}
                  className="px-6 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50"
                >
                  Previous
                </button>
                <button
                  onClick={() => setCurrentStep(prev => Math.min(steps.length - 1, prev + 1))}
                  disabled={currentStep === steps.length - 1}
                  className="px-6 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 disabled:opacity-50"
                >
                  Next
                </button>
              </div>
            </div>
          </div>

          {/* Live Preview */}
          <div className="col-span-5">
            <div className="bg-white rounded-lg shadow sticky top-24">
              <div className="p-4 border-b border-gray-200">
                <h3 className="font-semibold text-gray-900">Live Preview</h3>
              </div>
              <ResumePreviewHTML 
                resume={resume} 
                template={resume.template_name || 'professional-blue'} 
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
