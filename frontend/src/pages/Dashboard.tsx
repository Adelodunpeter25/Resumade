import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Plus, FileText, Download, Share2, Trash2, Edit, LogOut } from 'lucide-react'
import { resumeService, authService } from '../services'
import type { Resume, User } from '../types'

export default function Dashboard() {
  const navigate = useNavigate()
  const [user, setUser] = useState<User | null>(null)
  const [resumes, setResumes] = useState<Resume[]>([])
  const [loading, setLoading] = useState(true)
  const [page, setPage] = useState(1)
  const [total, setTotal] = useState(0)

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) {
      navigate('/login')
      return
    }
    loadData()
  }, [page])

  const loadData = async () => {
    try {
      const [userRes, resumesRes] = await Promise.all([
        authService.getCurrentUser(),
        resumeService.getResumes(page, 10)
      ])

      if (userRes.success && userRes.data) {
        setUser(userRes.data)
      }

      if (resumesRes.success && resumesRes.data) {
        setResumes(resumesRes.data.data || [])
        setTotal(resumesRes.data.total || 0)
      }
    } catch (err) {
      console.error('Failed to load data:', err)
      navigate('/login')
    } finally {
      setLoading(false)
    }
  }

  const handleLogout = async () => {
    await authService.logout()
    localStorage.removeItem('token')
    navigate('/login')
  }

  const handleDelete = async (id: number) => {
    if (!confirm('Delete this resume?')) return
    
    try {
      await resumeService.deleteResume(id)
      loadData()
    } catch (err) {
      alert('Failed to delete resume')
    }
  }

  const handleDownload = async (id: number, title: string) => {
    try {
      const blob = await resumeService.downloadPDF(id)
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `${title}.pdf`
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

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-br from-emerald-600 to-teal-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold">R</span>
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">Resumade</h1>
                <p className="text-sm text-gray-500">Welcome, {user?.full_name}</p>
              </div>
            </div>
            <button
              onClick={handleLogout}
              className="flex items-center gap-2 text-gray-600 hover:text-gray-900"
            >
              <LogOut size={20} />
              <span>Logout</span>
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Total Resumes</p>
                <p className="text-3xl font-bold text-gray-900">{total}</p>
              </div>
              <FileText className="text-emerald-600" size={40} />
            </div>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Avg ATS Score</p>
                <p className="text-3xl font-bold text-gray-900">
                  {resumes && resumes.length > 0
                    ? Math.round(resumes.reduce((acc, r) => acc + (r.ats_score || 0), 0) / resumes.length)
                    : 0}
                </p>
              </div>
              <div className="text-4xl">📊</div>
            </div>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Templates Used</p>
                <p className="text-3xl font-bold text-gray-900">
                  {resumes && resumes.length > 0 ? new Set(resumes.map(r => r.template_name)).size : 0}
                </p>
              </div>
              <div className="text-4xl">🎨</div>
            </div>
          </div>
        </div>

        {/* Resumes Section */}
        <div className="bg-white rounded-lg shadow">
          <div className="p-6 border-b border-gray-200">
            <div className="flex justify-between items-center">
              <h2 className="text-2xl font-bold text-gray-900">My Resumes</h2>
              <button
                onClick={() => navigate('/resume/new')}
                className="flex items-center gap-2 bg-gradient-to-r from-emerald-600 to-teal-600 text-white px-4 py-2 rounded-lg hover:from-emerald-700 hover:to-teal-700"
              >
                <Plus size={20} />
                <span>Create Resume</span>
              </button>
            </div>
          </div>

          {!resumes || resumes.length === 0 ? (
            <div className="p-12 text-center">
              <FileText className="mx-auto text-gray-400 mb-4" size={64} />
              <h3 className="text-xl font-semibold text-gray-900 mb-2">No resumes yet</h3>
              <p className="text-gray-600 mb-6">Create your first resume to get started</p>
              <button
                onClick={() => navigate('/resume/new')}
                className="bg-gradient-to-r from-emerald-600 to-teal-600 text-white px-6 py-3 rounded-lg hover:from-emerald-700 hover:to-teal-700"
              >
                Create Your First Resume
              </button>
            </div>
          ) : (
            <div className="divide-y divide-gray-200">
              {resumes.map((resume) => (
                <div key={resume.id} className="p-6 hover:bg-gray-50 transition-colors">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <h3 className="text-lg font-semibold text-gray-900 mb-1">{resume.title}</h3>
                      <div className="flex items-center gap-4 text-sm text-gray-600">
                        <span>Template: {resume.template_name}</span>
                        <span>•</span>
                        <span>Updated: {new Date(resume.updated_at).toLocaleDateString()}</span>
                        {resume.ats_score && (
                          <>
                            <span>•</span>
                            <span className="flex items-center gap-1">
                              ATS Score: 
                              <span className={`font-semibold ${
                                resume.ats_score >= 80 ? 'text-green-600' :
                                resume.ats_score >= 60 ? 'text-yellow-600' :
                                'text-red-600'
                              }`}>
                                {resume.ats_score}%
                              </span>
                            </span>
                          </>
                        )}
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => navigate(`/resume/${resume.id}`)}
                        className="p-2 text-gray-600 hover:text-emerald-600 hover:bg-emerald-50 rounded-lg"
                        title="Edit"
                      >
                        <Edit size={20} />
                      </button>
                      <button
                        onClick={() => handleDownload(resume.id, resume.title)}
                        className="p-2 text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded-lg"
                        title="Download"
                      >
                        <Download size={20} />
                      </button>
                      <button
                        onClick={() => navigate(`/resume/${resume.id}/share`)}
                        className="p-2 text-gray-600 hover:text-purple-600 hover:bg-purple-50 rounded-lg"
                        title="Share"
                      >
                        <Share2 size={20} />
                      </button>
                      <button
                        onClick={() => handleDelete(resume.id)}
                        className="p-2 text-gray-600 hover:text-red-600 hover:bg-red-50 rounded-lg"
                        title="Delete"
                      >
                        <Trash2 size={20} />
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Pagination */}
          {total > 10 && (
            <div className="p-6 border-t border-gray-200 flex justify-between items-center">
              <button
                onClick={() => setPage(p => Math.max(1, p - 1))}
                disabled={page === 1}
                className="px-4 py-2 border border-gray-300 rounded-lg disabled:opacity-50"
              >
                Previous
              </button>
              <span className="text-gray-600">
                Page {page} of {Math.ceil(total / 10)}
              </span>
              <button
                onClick={() => setPage(p => p + 1)}
                disabled={page >= Math.ceil(total / 10)}
                className="px-4 py-2 border border-gray-300 rounded-lg disabled:opacity-50"
              >
                Next
              </button>
            </div>
          )}
        </div>
      </main>
    </div>
  )
}
