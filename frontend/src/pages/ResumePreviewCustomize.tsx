import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { ArrowLeft, Download, Share2, ChevronDown, Save, Check } from 'lucide-react'
import { resumeService } from '../services'
import { API_BASE_URL } from '../services/api'
import TemplateCustomizer from '../components/resume/TemplateCustomizer'
import type { Resume } from '../types'

export default function ResumePreviewCustomize() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [resume, setResume] = useState<Resume | null>(null)
  const [loading, setLoading] = useState(true)
  const [previewKey, setPreviewKey] = useState(0)
  const [showExportDropdown, setShowExportDropdown] = useState(false)
  const [downloading, setDownloading] = useState(false)
  const [saving, setSaving] = useState(false)
  const [saveStatus, setSaveStatus] = useState<'saved' | 'saving' | 'unsaved'>('saved')
  const [isAuthenticated, setIsAuthenticated] = useState(false)

  useEffect(() => {
    const checkAuth = () => {
      const token = localStorage.getItem('token')
      setIsAuthenticated(!!token)
    }
    
    checkAuth()
    
    // Check auth periodically
    const interval = setInterval(checkAuth, 1000)
    
    loadResume()
    
    return () => clearInterval(interval)
  }, [id])

  const loadResume = async () => {
    try {
      const response = await resumeService.getResume(parseInt(id!))
      if (response.success && response.data) {
        setResume(response.data)
      }
    } catch (err) {
      console.error('Failed to load resume:', err)
    } finally {
      setLoading(false)
    }
  }

  const updateResumeData = (field: string, value: any) => {
    if (!resume) return
    setResume({ ...resume, [field]: value })
    setSaveStatus('unsaved')
  }

  const handleSave = async () => {
    if (!resume) return
    setSaving(true)
    setSaveStatus('saving')
    try {
      const response = await resumeService.updateResume(parseInt(id!), resume)
      if (response.success) {
        setSaveStatus('saved')
        setPreviewKey(prev => prev + 1)
      }
    } catch (err) {
      console.error('Failed to save:', err)
      setSaveStatus('unsaved')
    } finally {
      setSaving(false)
    }
  }

  const handleCustomizationUpdate = (field: string, value: any) => {
    updateResumeData(field, value)
  }

  const handleExport = async (format: string) => {
    setDownloading(true)
    try {
      const blob = await resumeService.exportResume(parseInt(id!), format)
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `${resume?.title || 'resume'}.${format}`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (err) {
      console.error('Export failed:', err)
    } finally {
      setDownloading(false)
      setShowExportDropdown(false)
    }
  }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="w-16 h-16 border-4 border-emerald-600 border-t-transparent rounded-full animate-spin"></div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header - Exact same as ResumeBuilder */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-full mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-4">
              <button
                onClick={() => navigate(-1)}
                className="p-2 hover:bg-gray-100 rounded-lg"
              >
                <ArrowLeft size={20} />
              </button>
              <input
                type="text"
                value={resume?.title || ''}
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
              <button
                onClick={() => navigate(`/resume/${id}/share`)}
                className="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
              >
                <Share2 size={20} />
                <span className="hidden sm:inline">Share</span>
              </button>
              
              <div className="relative">
                <button
                  onClick={() => setShowExportDropdown(!showExportDropdown)}
                  disabled={downloading}
                  className="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50"
                  title="Export Resume"
                >
                  <Download size={20} />
                  <span>Export</span>
                  <ChevronDown size={16} />
                </button>

                {showExportDropdown && (
                  <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-xl border border-gray-200 z-20">
                    <button
                      onClick={() => {
                        handleExport('pdf')
                        setShowExportDropdown(false)
                      }}
                      className="w-full text-left px-4 py-3 hover:bg-gray-50 border-b border-gray-100"
                    >
                      <div className="font-medium text-gray-900">PDF</div>
                      <div className="text-xs text-gray-500">Portable Document Format</div>
                    </button>
                    {isAuthenticated && (
                      <>
                        <button
                          onClick={() => {
                            handleExport('docx')
                            setShowExportDropdown(false)
                          }}
                          className="w-full text-left px-4 py-3 hover:bg-gray-50 border-b border-gray-100"
                        >
                          <div className="font-medium text-gray-900">DOCX</div>
                          <div className="text-xs text-gray-500">Microsoft Word Document</div>
                        </button>
                        <button
                          onClick={() => {
                            handleExport('txt')
                            setShowExportDropdown(false)
                          }}
                          className="w-full text-left px-4 py-3 hover:bg-gray-50"
                        >
                          <div className="font-medium text-gray-900">TXT</div>
                          <div className="text-xs text-gray-500">Plain Text Format</div>
                        </button>
                      </>
                    )}
                  </div>
                )}
              </div>
              <button
                onClick={handleSave}
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

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Customization Panel */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow-sm p-6 sticky top-24">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Customize Template</h2>
              {resume && (
                <TemplateCustomizer 
                  data={resume} 
                  onChange={handleCustomizationUpdate}
                />
              )}
            </div>
          </div>

          {/* Preview */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow-sm p-8">
              <iframe
                key={previewKey}
                src={`${API_BASE_URL}/api/resumes/${id}/preview`}
                className="w-full border-0"
                style={{ height: '1100px' }}
                title="Resume Preview"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
