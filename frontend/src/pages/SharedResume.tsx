import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { Download } from 'lucide-react'
import { resumeService } from '../services'
import type { Resume } from '../types'

export default function SharedResume() {
  const { token } = useParams()
  const [resume, setResume] = useState<Resume | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    if (token) {
      loadResume()
    }
  }, [token])

  const loadResume = async () => {
    try {
      const response = await resumeService.getSharedResume(token!)
      if (response.success && response.data) {
        setResume(response.data)
      } else {
        setError('Resume not found or link has expired')
      }
    } catch (err) {
      setError('Failed to load resume')
    } finally {
      setLoading(false)
    }
  }

  const handleDownload = async () => {
    if (!resume) return

    try {
      const blob = await resumeService.downloadPDF(resume.id)
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `${resume.title}.pdf`
      a.click()
      window.URL.revokeObjectURL(url)
    } catch (err) {
      alert('Failed to download resume')
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="w-16 h-16 border-4 border-emerald-600 border-t-transparent rounded-full animate-spin"></div>
      </div>
    )
  }

  if (error || !resume) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-6xl mb-4">🔒</div>
          <h1 className="text-2xl font-bold text-gray-900 mb-2">Resume Not Available</h1>
          <p className="text-gray-600">{error || 'This link may have expired or been removed'}</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-emerald-600 to-teal-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold">R</span>
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">{resume.title}</h1>
                <p className="text-sm text-gray-500">Shared Resume</p>
              </div>
            </div>
            <button
              onClick={handleDownload}
              className="flex items-center gap-2 bg-gradient-to-r from-emerald-600 to-teal-600 text-white px-4 py-2 rounded-lg hover:from-emerald-700 hover:to-teal-700"
            >
              <Download size={20} />
              <span>Download PDF</span>
            </button>
          </div>
        </div>
      </header>

      {/* Resume Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <iframe
            src={`http://localhost:8001/api/resumes/templates/preview?template=${resume.template}&resume_id=${resume.id}`}
            className="w-full border-0"
            style={{ height: '1100px' }}
            title="Resume Preview"
          />
        </div>
      </main>
    </div>
  )
}

