import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Plus, FileText, Download, Trash2, Edit, LogOut, Search, Copy, Check } from 'lucide-react'
import { resumeService, authService } from '../services'
import { API_BASE_URL } from '../services/api'
import type { Resume, User, Template } from '../types'

export default function Dashboard() {
  const navigate = useNavigate()
  const [user, setUser] = useState<User | null>(null)
  const [resumes, setResumes] = useState<Resume[]>([])
  const [loading, setLoading] = useState(true)
  const [page, setPage] = useState(1)
  const [total, setTotal] = useState(0)
  const [searchQuery, setSearchQuery] = useState('')
  const [templateFilter, setTemplateFilter] = useState('all')
  const [atsFilter, setAtsFilter] = useState('all')
  const [templates, setTemplates] = useState<string[]>([])
  const [activeTab, setActiveTab] = useState<'resumes' | 'templates' | 'share'>('resumes')
  const [allTemplates, setAllTemplates] = useState<Template[]>([])
  const [previewUrls, setPreviewUrls] = useState<Record<string, string>>({})
  const [templateSearchQuery, setTemplateSearchQuery] = useState('')
  const [shareSubTab, setShareSubTab] = useState<'create' | 'view'>('create')
  const [selectedResumeId, setSelectedResumeId] = useState<number | null>(null)
  const [shareLinks, setShareLinks] = useState<any[]>([])
  const [expiresIn, setExpiresIn] = useState(30)
  const [creating, setCreating] = useState(false)
  const [copiedToken, setCopiedToken] = useState<string | null>(null)

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) {
      navigate('/login')
      return
    }
    loadData()
    loadAllTemplates()
  }, [page])

  useEffect(() => {
    if (activeTab === 'share' && shareSubTab === 'view') {
      loadShareLinks()
    }
  }, [activeTab, shareSubTab])

  const loadShareLinks = async () => {
    try {
      const allLinks: any[] = []
      for (const resume of resumes) {
        const linksRes = await resumeService.getShareLinks(resume.id)
        if (linksRes.success && linksRes.data) {
          allLinks.push(...linksRes.data)
        }
      }
      setShareLinks(allLinks)
    } catch (err) {
      console.error('Failed to load share links:', err)
    }
  }

  const loadData = async () => {
    try {
      const [userRes, resumesRes] = await Promise.all([
        authService.getCurrentUser(),
        resumeService.getResumes(page, 10)
      ])

      if (userRes.success && userRes.data) {
        setUser(userRes.data)
      }

      if (resumesRes.success) {
        const allResumes = Array.isArray(resumesRes.data) ? resumesRes.data : ((resumesRes.data as any)?.data || [])
        setResumes(allResumes)
        setTotal((resumesRes as any).total || allResumes.length || 0)
        // Extract unique templates
        const uniqueTemplates = [...new Set(allResumes.map((r: Resume) => r.template_name).filter(Boolean))] as string[]
        setTemplates(uniqueTemplates)
      }
    } catch (err) {
      console.error('Failed to load data:', err)
      navigate('/login')
    } finally {
      setLoading(false)
    }
  }

  const loadAllTemplates = async () => {
    try {
      const response = await resumeService.getTemplates()
      if (response.success && response.data) {
        const templates = response.data.all_templates || []
        setAllTemplates(templates)
        const urls: Record<string, string> = {}
        templates.forEach((template: Template) => {
          urls[template.name] = `${API_BASE_URL}/api/resumes/templates/preview?template=${template.name}`
        })
        setPreviewUrls(urls)
      }
    } catch (err) {
      console.error('Failed to load templates:', err)
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

  // Filter resumes based on search and filters
  const filteredResumes = resumes.filter(resume => {
    const matchesSearch = resume.title.toLowerCase().includes(searchQuery.toLowerCase())
    const matchesTemplate = templateFilter === 'all' || resume.template_name === templateFilter
    const matchesATS = atsFilter === 'all' || 
      (atsFilter === 'excellent' && (resume.ats_score || 0) >= 80) ||
      (atsFilter === 'good' && (resume.ats_score || 0) >= 60 && (resume.ats_score || 0) < 80) ||
      (atsFilter === 'needs-work' && (resume.ats_score || 0) < 60)
    return matchesSearch && matchesTemplate && matchesATS
  })

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

        {/* Tabs & Content Section */}
        <div className="bg-white rounded-lg shadow">
          {/* Tabs */}
          <div className="border-b border-gray-200">
            <div className="flex">
              <button
                onClick={() => setActiveTab('resumes')}
                className={`px-6 py-4 font-semibold border-b-2 transition-colors ${
                  activeTab === 'resumes'
                    ? 'border-emerald-600 text-emerald-600'
                    : 'border-transparent text-gray-600 hover:text-gray-900'
                }`}
              >
                My Resumes
              </button>
              <button
                onClick={() => setActiveTab('templates')}
                className={`px-6 py-4 font-semibold border-b-2 transition-colors ${
                  activeTab === 'templates'
                    ? 'border-emerald-600 text-emerald-600'
                    : 'border-transparent text-gray-600 hover:text-gray-900'
                }`}
              >
                Templates
              </button>
              <button
                onClick={() => setActiveTab('share')}
                className={`px-6 py-4 font-semibold border-b-2 transition-colors ${
                  activeTab === 'share'
                    ? 'border-emerald-600 text-emerald-600'
                    : 'border-transparent text-gray-600 hover:text-gray-900'
                }`}
              >
                Share
              </button>
            </div>
          </div>

          {activeTab === 'resumes' && (
            <>
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

              {/* Search & Filters */}
              <div className="p-6 border-b border-gray-200 space-y-4">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
              <input
                type="text"
                placeholder="Search resumes by title..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
              />
            </div>
            <div className="flex gap-4">
              <select
                value={templateFilter}
                onChange={(e) => setTemplateFilter(e.target.value)}
                className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
              >
                <option value="all">All Templates</option>
                {templates.map(template => (
                  <option key={template} value={template}>
                    {template.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')}
                  </option>
                ))}
              </select>
              <select
                value={atsFilter}
                onChange={(e) => setAtsFilter(e.target.value)}
                className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
              >
                <option value="all">All ATS Scores</option>
                <option value="excellent">Excellent (80-100)</option>
                <option value="good">Good (60-79)</option>
                <option value="needs-work">Needs Work (&lt;60)</option>
              </select>
              </div>
              </div>

              {!filteredResumes || filteredResumes.length === 0 ? (
            <div className="p-12 text-center">
              <FileText className="mx-auto text-gray-400 mb-4" size={64} />
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                {resumes.length === 0 ? 'No resumes yet' : 'No resumes found'}
              </h3>
              <p className="text-gray-600 mb-6">
                {resumes.length === 0 ? 'Create your first resume to get started' : 'Try adjusting your search or filters'}
              </p>
              {resumes.length === 0 && (
                <button
                  onClick={() => navigate('/resume/new')}
                  className="bg-gradient-to-r from-emerald-600 to-teal-600 text-white px-6 py-3 rounded-lg hover:from-emerald-700 hover:to-teal-700"
                >
                  Create Your First Resume
                </button>
              )}
              </div>
            ) : (
              <div className="divide-y divide-gray-200">
              {filteredResumes.map((resume) => (
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
            </>
          )}

          {activeTab === 'share' && (
            <>
              <div className="border-b border-gray-200">
                <div className="flex px-6">
                  <button
                    onClick={() => setShareSubTab('create')}
                    className={`px-4 py-3 font-medium border-b-2 transition-colors ${
                      shareSubTab === 'create'
                        ? 'border-emerald-600 text-emerald-600'
                        : 'border-transparent text-gray-600 hover:text-gray-900'
                    }`}
                  >
                    Share a Resume
                  </button>
                  <button
                    onClick={() => setShareSubTab('view')}
                    className={`px-4 py-3 font-medium border-b-2 transition-colors ${
                      shareSubTab === 'view'
                        ? 'border-emerald-600 text-emerald-600'
                        : 'border-transparent text-gray-600 hover:text-gray-900'
                    }`}
                  >
                    Shared Resumes
                  </button>
                </div>
              </div>

              {shareSubTab === 'create' && (
                <div className="p-8">
                  <h3 className="text-xl font-bold text-gray-900 mb-6">Share a Resume</h3>
                  
                  <div className="max-w-2xl">
                    <div className="mb-6">
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Select Resume
                      </label>
                      <select
                        value={selectedResumeId || ''}
                        onChange={(e) => setSelectedResumeId(Number(e.target.value))}
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
                      >
                        <option value="">Choose a resume...</option>
                        {resumes.map((resume) => (
                          <option key={resume.id} value={resume.id}>
                            {resume.title}
                          </option>
                        ))}
                      </select>
                    </div>

                    <div className="mb-6">
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Expires in (days)
                      </label>
                      <input
                        type="number"
                        min="1"
                        max="365"
                        value={expiresIn}
                        onChange={(e) => setExpiresIn(Number(e.target.value))}
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
                      />
                    </div>

                    <button
                      onClick={async () => {
                        if (!selectedResumeId) {
                          alert('Please select a resume')
                          return
                        }
                        setCreating(true)
                        try {
                          const response = await resumeService.createShareLink(selectedResumeId, expiresIn)
                          if (response.success) {
                            alert('Share link created successfully!')
                            setShareSubTab('view')
                          }
                        } catch (err: any) {
                          const errorMsg = err.response?.data?.detail || err.message || 'Failed to create share link'
                          alert(errorMsg)
                        } finally {
                          setCreating(false)
                        }
                      }}
                      disabled={creating || !selectedResumeId}
                      className="bg-gradient-to-r from-emerald-600 to-teal-600 text-white px-6 py-3 rounded-lg hover:from-emerald-700 hover:to-teal-700 disabled:opacity-50"
                    >
                      {creating ? 'Creating...' : 'Create Share Link'}
                    </button>
                  </div>
                </div>
              )}

              {shareSubTab === 'view' && (
                <div className="p-8">
                  <h3 className="text-xl font-bold text-gray-900 mb-6">Shared Resumes</h3>
                  {shareLinks.length === 0 ? (
                    <div className="text-center py-12">
                      <div className="text-gray-400 mb-4">🔗</div>
                      <h3 className="text-lg font-semibold text-gray-900 mb-2">No shared resumes yet</h3>
                      <p className="text-gray-600">Create a share link from the "Share a Resume" tab</p>
                    </div>
                  ) : (
                    <div className="space-y-4">
                      {shareLinks.map((link) => {
                        const resume = resumes.find(r => r.id === link.resume_id)
                        const isExpired = new Date(link.expires_at) < new Date()
                        const isActive = !isExpired

                        return (
                          <div key={link.token} className="bg-white border border-gray-200 rounded-lg p-6">
                            <div className="flex items-start justify-between mb-4">
                              <div>
                                <h4 className="font-semibold text-gray-900 mb-1">{resume?.title || 'Resume'}</h4>
                                <div className="flex items-center gap-2">
                                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                                    isActive ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-700'
                                  }`}>
                                    {isActive ? 'Active' : 'Inactive'}
                                  </span>
                                  {isExpired && (
                                    <span className="px-2 py-1 rounded-full text-xs font-medium bg-red-100 text-red-700">
                                      Expired
                                    </span>
                                  )}
                                </div>
                              </div>
                              <button
                                onClick={async () => {
                                  if (!confirm('Delete this share link?')) return
                                  try {
                                    await resumeService.deleteShareLink(link.resume_id, link.token)
                                    setShareLinks(shareLinks.filter(l => l.token !== link.token))
                                  } catch (err) {
                                    alert('Failed to delete share link')
                                  }
                                }}
                                className="p-2 text-gray-600 hover:text-red-600 hover:bg-red-50 rounded-lg"
                                title="Delete"
                              >
                                <Trash2 size={20} />
                              </button>
                            </div>
                            <div className="text-sm text-gray-600 mb-3">
                              <div>Created: {new Date(link.created_at).toLocaleDateString()}</div>
                              <div>Expires: {new Date(link.expires_at).toLocaleDateString()}</div>
                            </div>
                            <div className="flex items-center gap-2 bg-gray-50 px-3 py-2 rounded-lg">
                              <code className="text-sm text-gray-700 flex-1 truncate">
                                {window.location.origin}/shared/{link.slug || link.token}
                              </code>
                              <button
                                onClick={() => {
                                  const url = `${window.location.origin}/shared/${link.slug || link.token}`
                                  navigator.clipboard.writeText(url)
                                  setCopiedToken(link.token)
                                  setTimeout(() => setCopiedToken(null), 2000)
                                }}
                                className="p-2 text-gray-600 hover:text-emerald-600 hover:bg-emerald-50 rounded-lg"
                                title="Copy link"
                              >
                                {copiedToken === link.token ? (
                                  <Check size={20} className="text-emerald-600" />
                                ) : (
                                  <Copy size={20} />
                                )}
                              </button>
                            </div>
                          </div>
                        )
                      })}
                    </div>
                  )}
                </div>
              )}
            </>
          )}

          {activeTab === 'templates' && (
            <>
              <div className="p-6 border-b border-gray-200">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                  <input
                    type="text"
                    placeholder="Search templates by name, description, or category..."
                    value={templateSearchQuery}
                    onChange={(e) => setTemplateSearchQuery(e.target.value)}
                    className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
                  />
                </div>
              </div>
              <div className="p-8">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                  {allTemplates.filter(template => {
                    const query = templateSearchQuery.toLowerCase()
                    return template.display_name.toLowerCase().includes(query) ||
                           template.description.toLowerCase().includes(query) ||
                           template.name.toLowerCase().includes(query) ||
                           (template.category && template.category.toLowerCase().includes(query))
                  }).map((template) => (
                  <div
                    key={template.name}
                    className="group cursor-pointer"
                    onClick={() => navigate(`/resume/new?template=${template.name}`)}
                  >
                    <div className="bg-white rounded-lg overflow-hidden shadow-sm hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1 border border-gray-200">
                      <div className="aspect-[8.5/11] bg-gray-50 relative overflow-hidden border-b border-gray-100">
                        <iframe
                          src={previewUrls[template.name]}
                          className="w-full h-full border-0 pointer-events-none scale-[0.4] origin-top-left"
                          style={{ width: '250%', height: '250%' }}
                          title={`${template.display_name} Preview`}
                        />
                        <div className="absolute inset-0 bg-black/0 group-hover:bg-black/40 transition-all duration-300 flex items-center justify-center">
                          <button className="opacity-0 group-hover:opacity-100 transform scale-90 group-hover:scale-100 transition-all duration-300 bg-white text-gray-900 px-8 py-3 rounded-lg font-semibold shadow-xl hover:bg-gray-50">
                            Use Template
                          </button>
                        </div>
                      </div>
                      <div className="p-4">
                        <h3 className="font-semibold text-gray-900 text-base mb-1">
                          {template.display_name}
                        </h3>
                        <p className="text-sm text-gray-600">
                          {template.description}
                        </p>
                      </div>
                    </div>
                  </div>
                  ))}
                </div>
              </div>
            </>
          )}
        </div>
      </main>
    </div>
  )
}
