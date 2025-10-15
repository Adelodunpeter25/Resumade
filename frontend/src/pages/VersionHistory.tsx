import { useState, useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { ArrowLeft, Plus, RotateCcw, Clock } from 'lucide-react'
import { resumeService } from '../services'
import type { ResumeVersion } from '../types'

export default function VersionHistory() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [versions, setVersions] = useState<ResumeVersion[]>([])
  const [loading, setLoading] = useState(true)
  const [creating, setCreating] = useState(false)
  const [selectedVersion, setSelectedVersion] = useState<ResumeVersion | null>(null)

  useEffect(() => {
    if (id && !isNaN(Number(id))) {
      loadVersions()
    } else {
      navigate('/dashboard')
    }
  }, [id])

  const loadVersions = async () => {
    if (!id || isNaN(Number(id))) return
    try {
      const response = await resumeService.getVersions(Number(id))
      if (response.success && response.data) {
        setVersions(response.data)
      }
    } catch (err) {
      alert('Failed to load versions')
    } finally {
      setLoading(false)
    }
  }

  const createVersion = async () => {
    if (!id || isNaN(Number(id))) return
    setCreating(true)
    try {
      const response = await resumeService.createVersion(Number(id))
      if (response.success && response.data) {
        setVersions([response.data, ...versions])
      }
    } catch (err) {
      alert('Failed to create version')
    } finally {
      setCreating(false)
    }
  }

  const restoreVersion = async (version: ResumeVersion) => {
    if (!id || isNaN(Number(id))) return
    if (!confirm(`Restore to version ${version.version_number}? This will overwrite your current resume.`)) return

    try {
      const content = {
        personal_info: version.personal_info,
        experience: version.experience,
        education: version.education,
        skills: version.skills,
        certifications: version.certifications,
        projects: version.projects
      }
      await resumeService.updateResume(Number(id), content)
      navigate(`/resume/${id}`)
    } catch (err) {
      alert('Failed to restore version')
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
            <div className="flex items-center gap-4">
              <button
                onClick={() => navigate(`/resume/${id}`)}
                className="p-2 hover:bg-gray-100 rounded-lg"
              >
                <ArrowLeft size={20} />
              </button>
              <h1 className="text-xl font-bold text-gray-900">Version History</h1>
            </div>
            <button
              onClick={createVersion}
              disabled={creating}
              className="flex items-center gap-2 bg-gradient-to-r from-emerald-600 to-teal-600 text-white px-4 py-2 rounded-lg hover:from-emerald-700 hover:to-teal-700 disabled:opacity-50"
            >
              <Plus size={20} />
              <span>{creating ? 'Creating...' : 'Create Snapshot'}</span>
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-12 gap-6">
          {/* Version List */}
          <div className="col-span-5">
            <div className="bg-white rounded-lg shadow">
              <div className="p-6 border-b border-gray-200">
                <h2 className="text-lg font-bold text-gray-900">Saved Versions</h2>
              </div>

              {versions.length === 0 ? (
                <div className="p-12 text-center">
                  <Clock className="mx-auto text-gray-400 mb-4" size={48} />
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">No versions yet</h3>
                  <p className="text-gray-600">Create a snapshot to save the current state</p>
                </div>
              ) : (
                <div className="divide-y divide-gray-200 max-h-[calc(100vh-250px)] overflow-y-auto">
                  {versions.map((version) => (
                    <div
                      key={version.id}
                      onClick={() => setSelectedVersion(version)}
                      className={`p-4 cursor-pointer transition-colors ${
                        selectedVersion?.id === version.id
                          ? 'bg-emerald-50 border-l-4 border-emerald-600'
                          : 'hover:bg-gray-50'
                      }`}
                    >
                      <div className="flex justify-between items-start mb-2">
                        <div>
                          <h3 className="font-semibold text-gray-900">
                            Version {version.version_number}
                          </h3>
                          <p className="text-sm text-gray-600">
                            {new Date(version.created_at).toLocaleString()}
                          </p>
                        </div>
                        <button
                          onClick={(e) => {
                            e.stopPropagation()
                            restoreVersion(version)
                          }}
                          className="p-2 text-emerald-600 hover:bg-emerald-100 rounded-lg"
                          title="Restore this version"
                        >
                          <RotateCcw size={18} />
                        </button>
                      </div>
                      <div className="text-xs text-gray-500">
                        {version.title}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Version Preview */}
          <div className="col-span-7">
            <div className="bg-white rounded-lg shadow">
              <div className="p-6 border-b border-gray-200">
                <h2 className="text-lg font-bold text-gray-900">
                  {selectedVersion ? `Version ${selectedVersion.version_number} Preview` : 'Select a version'}
                </h2>
              </div>

              {selectedVersion ? (
                <div className="p-6 max-h-[calc(100vh-250px)] overflow-y-auto">
                  {/* Personal Info */}
                  <div className="mb-6">
                    <h3 className="text-lg font-bold text-gray-900 mb-3">Personal Information</h3>
                    <div className="space-y-2 text-sm">
                      <p><span className="font-medium">Name:</span> {selectedVersion.personal_info.full_name}</p>
                      <p><span className="font-medium">Email:</span> {selectedVersion.personal_info.email}</p>
                      <p><span className="font-medium">Phone:</span> {selectedVersion.personal_info.phone}</p>
                      <p><span className="font-medium">Location:</span> {selectedVersion.personal_info.location}</p>
                    </div>
                  </div>

                  {/* Experience */}
                  {selectedVersion.experience.length > 0 && (
                    <div className="mb-6">
                      <h3 className="text-lg font-bold text-gray-900 mb-3">Experience</h3>
                      <div className="space-y-3">
                        {selectedVersion.experience.map((exp, index) => (
                          <div key={index} className="border-l-2 border-emerald-600 pl-3">
                            <p className="font-medium text-gray-900">{exp.position}</p>
                            <p className="text-sm text-gray-600">{exp.company}</p>
                            <p className="text-xs text-gray-500">
                              {exp.start_date} - {exp.current ? 'Present' : exp.end_date}
                            </p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Education */}
                  {selectedVersion.education.length > 0 && (
                    <div className="mb-6">
                      <h3 className="text-lg font-bold text-gray-900 mb-3">Education</h3>
                      <div className="space-y-3">
                        {selectedVersion.education.map((edu, index) => (
                          <div key={index} className="border-l-2 border-emerald-600 pl-3">
                            <p className="font-medium text-gray-900">{edu.degree}</p>
                            <p className="text-sm text-gray-600">{edu.institution}</p>
                            <p className="text-xs text-gray-500">
                              {edu.start_date} - {edu.end_date || 'Present'}
                            </p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Skills */}
                  {selectedVersion.skills.length > 0 && (
                    <div className="mb-6">
                      <h3 className="text-lg font-bold text-gray-900 mb-3">Skills</h3>
                      <div className="flex flex-wrap gap-2">
                        {selectedVersion.skills.map((skill, index) => (
                          <span
                            key={index}
                            className="px-3 py-1 bg-emerald-100 text-emerald-700 rounded-full text-sm"
                          >
                            {skill.name}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Metadata */}
                  <div className="mt-6 pt-6 border-t border-gray-200">
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <span className="font-medium text-gray-700">Template:</span>
                        <span className="ml-2 text-gray-600">{selectedVersion.template}</span>
                      </div>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="p-12 text-center text-gray-500">
                  Select a version from the list to preview its contents
                </div>
              )}
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
