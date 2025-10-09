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
      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white rounded-lg shadow p-8">
          {/* Personal Info */}
          <div className="mb-8 text-center border-b border-gray-200 pb-6">
            <h2 className="text-3xl font-bold text-gray-900 mb-2">
              {resume.personal_info.full_name}
            </h2>
            <div className="flex flex-wrap justify-center gap-4 text-gray-600">
              <span>{resume.personal_info.email}</span>
              <span>•</span>
              <span>{resume.personal_info.phone}</span>
              <span>•</span>
              <span>{resume.personal_info.location}</span>
            </div>
            {resume.personal_info.summary && (
              <p className="mt-4 text-gray-700">{resume.personal_info.summary}</p>
            )}
          </div>

          {/* Experience */}
          {resume.experience.length > 0 && (
            <div className="mb-8">
              <h3 className="text-xl font-bold text-gray-900 mb-4">Experience</h3>
              <div className="space-y-4">
                {resume.experience.map((exp, index) => (
                  <div key={index}>
                    <div className="flex justify-between items-start mb-1">
                      <div>
                        <h4 className="font-semibold text-gray-900">{exp.position}</h4>
                        <p className="text-gray-700">{exp.company}</p>
                      </div>
                      <span className="text-sm text-gray-600">
                        {exp.start_date} - {exp.current ? 'Present' : exp.end_date}
                      </span>
                    </div>
                    <p className="text-gray-600 text-sm">{exp.description}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Education */}
          {resume.education.length > 0 && (
            <div className="mb-8">
              <h3 className="text-xl font-bold text-gray-900 mb-4">Education</h3>
              <div className="space-y-4">
                {resume.education.map((edu, index) => (
                  <div key={index}>
                    <div className="flex justify-between items-start">
                      <div>
                        <h4 className="font-semibold text-gray-900">{edu.degree} in {edu.field_of_study}</h4>
                        <p className="text-gray-700">{edu.institution}</p>
                      </div>
                      <span className="text-sm text-gray-600">
                        {edu.start_date} - {edu.end_date || 'Present'}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Skills */}
          {resume.skills.length > 0 && (
            <div className="mb-8">
              <h3 className="text-xl font-bold text-gray-900 mb-4">Skills</h3>
              <div className="flex flex-wrap gap-2">
                {resume.skills.map((skill, index) => (
                  <span
                    key={index}
                    className="px-3 py-1 bg-emerald-100 text-emerald-700 rounded-full text-sm"
                  >
                    {skill.name} - {skill.level}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  )
}
