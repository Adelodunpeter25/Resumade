import { useState, useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { ArrowLeft, Plus, Copy, Trash2, ExternalLink, Check } from 'lucide-react'
import { resumeService } from '../services'
import type { ShareLink } from '../types'

export default function ResumeShare() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [shareLinks, setShareLinks] = useState<ShareLink[]>([])
  const [loading, setLoading] = useState(true)
  const [creating, setCreating] = useState(false)
  const [expiresIn, setExpiresIn] = useState(30)
  const [copiedToken, setCopiedToken] = useState<string | null>(null)

  useEffect(() => {
    if (id) {
      loadShareLinks()
    }
  }, [id])

  const loadShareLinks = async () => {
    try {
      const response = await resumeService.getShareLinks(Number(id))
      if (response.success && response.data) {
        setShareLinks(response.data)
      }
    } catch (err) {
      alert('Failed to load share links')
    } finally {
      setLoading(false)
    }
  }

  const createShareLink = async () => {
    setCreating(true)
    try {
      const response = await resumeService.createShareLink(Number(id), expiresIn)
      if (response.success && response.data) {
        setShareLinks([...shareLinks, response.data])
      }
    } catch (err) {
      alert('Failed to create share link')
    } finally {
      setCreating(false)
    }
  }

  const deleteShareLink = async (token: string) => {
    if (!confirm('Delete this share link?')) return

    try {
      await resumeService.deleteShareLink(Number(id), token)
      setShareLinks(shareLinks.filter(link => link.token !== token))
    } catch (err) {
      alert('Failed to delete share link')
    }
  }

  const copyToClipboard = (token: string) => {
    const url = `${window.location.origin}/shared/${token}`
    navigator.clipboard.writeText(url)
    setCopiedToken(token)
    setTimeout(() => setCopiedToken(null), 2000)
  }

  const openLink = (token: string) => {
    window.open(`${window.location.origin}/shared/${token}`, '_blank')
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
          <div className="flex items-center gap-4">
            <button
              onClick={() => navigate(`/resume/${id}`)}
              className="p-2 hover:bg-gray-100 rounded-lg"
            >
              <ArrowLeft size={20} />
            </button>
            <h1 className="text-xl font-bold text-gray-900">Share Resume</h1>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Create New Link */}
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h2 className="text-lg font-bold text-gray-900 mb-4">Create Share Link</h2>
          <div className="flex gap-4">
            <div className="flex-1">
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
            <div className="flex items-end">
              <button
                onClick={createShareLink}
                disabled={creating}
                className="flex items-center gap-2 bg-gradient-to-r from-emerald-600 to-teal-600 text-white px-6 py-2 rounded-lg hover:from-emerald-700 hover:to-teal-700 disabled:opacity-50"
              >
                <Plus size={20} />
                <span>{creating ? 'Creating...' : 'Create Link'}</span>
              </button>
            </div>
          </div>
        </div>

        {/* Active Links */}
        <div className="bg-white rounded-lg shadow">
          <div className="p-6 border-b border-gray-200">
            <h2 className="text-lg font-bold text-gray-900">Active Share Links</h2>
          </div>

          {shareLinks.length === 0 ? (
            <div className="p-12 text-center">
              <div className="text-gray-400 mb-4">🔗</div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">No share links yet</h3>
              <p className="text-gray-600">Create a share link to share your resume publicly</p>
            </div>
          ) : (
            <div className="divide-y divide-gray-200">
              {shareLinks.map((link) => {
                const isExpired = new Date(link.expires_at) < new Date()
                const isActive = link.is_active && !isExpired

                return (
                  <div key={link.token} className="p-6">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-2">
                          <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                            isActive
                              ? 'bg-green-100 text-green-700'
                              : 'bg-gray-100 text-gray-700'
                          }`}>
                            {isActive ? 'Active' : 'Inactive'}
                          </span>
                          {isExpired && (
                            <span className="px-2 py-1 rounded-full text-xs font-medium bg-red-100 text-red-700">
                              Expired
                            </span>
                          )}
                        </div>
                        <div className="text-sm text-gray-600 mb-2">
                          Created: {new Date(link.created_at).toLocaleDateString()}
                        </div>
                        <div className="text-sm text-gray-600 mb-3">
                          Expires: {new Date(link.expires_at).toLocaleDateString()}
                        </div>
                        <div className="flex items-center gap-2 bg-gray-50 px-3 py-2 rounded-lg">
                          <code className="text-sm text-gray-700 flex-1 truncate">
                            {window.location.origin}/shared/{link.token}
                          </code>
                        </div>
                      </div>
                      <div className="flex items-center gap-2 ml-4">
                        <button
                          onClick={() => copyToClipboard(link.token)}
                          className="p-2 text-gray-600 hover:text-emerald-600 hover:bg-emerald-50 rounded-lg"
                          title="Copy link"
                        >
                          {copiedToken === link.token ? (
                            <Check size={20} className="text-emerald-600" />
                          ) : (
                            <Copy size={20} />
                          )}
                        </button>
                        <button
                          onClick={() => openLink(link.token)}
                          className="p-2 text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded-lg"
                          title="Open link"
                        >
                          <ExternalLink size={20} />
                        </button>
                        <button
                          onClick={() => deleteShareLink(link.token)}
                          className="p-2 text-gray-600 hover:text-red-600 hover:bg-red-50 rounded-lg"
                          title="Delete"
                        >
                          <Trash2 size={20} />
                        </button>
                      </div>
                    </div>
                  </div>
                )
              })}
            </div>
          )}
        </div>
      </main>
    </div>
  )
}
