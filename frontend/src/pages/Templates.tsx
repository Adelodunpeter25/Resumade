import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { ArrowLeft } from 'lucide-react'
import { resumeService } from '../services'
import { API_BASE_URL } from '../services/api'
import type { Template } from '../types'

export default function Templates() {
  const navigate = useNavigate()
  const [templates, setTemplates] = useState<Template[]>([])
  const [loading, setLoading] = useState(true)
  const [previewUrls, setPreviewUrls] = useState<Record<string, string>>({})

  useEffect(() => {
    loadTemplates()
  }, [])

  const loadTemplates = async () => {
    try {
      const response = await resumeService.getTemplates()
      if (response.success && response.data) {
        setTemplates(response.data)
        
        // Generate preview URLs for each template
        const urls: Record<string, string> = {}
        response.data.forEach((template: Template) => {
          urls[template.name] = `${API_BASE_URL}/api/resumes/templates/preview?template=${template.name}`
        })
        setPreviewUrls(urls)
      }
    } catch (err) {
      console.error('Failed to load templates:', err)
    } finally {
      setLoading(false)
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
          <div className="flex items-center gap-4">
            <button
              onClick={() => navigate('/')}
              className="p-2 hover:bg-gray-100 rounded-lg"
            >
              <ArrowLeft size={20} />
            </button>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Resume Templates</h1>
              <p className="text-sm text-gray-600">Choose a template to start building your resume</p>
            </div>
          </div>
        </div>
      </header>

      {/* Templates Grid */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {templates.map((template) => (
            <div
              key={template.name}
              className="group cursor-pointer"
              onClick={() => navigate('/resume/new')}
            >
              {/* Card */}
              <div className="bg-white rounded-lg overflow-hidden shadow-sm hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1">
                {/* Template Preview */}
                <div className="aspect-[8.5/11] bg-gray-50 relative overflow-hidden border-b border-gray-100">
                  <iframe
                    src={previewUrls[template.name]}
                    className="w-full h-full border-0 pointer-events-none scale-[0.4] origin-top-left"
                    style={{ width: '250%', height: '250%' }}
                    title={`${template.display_name} Preview`}
                  />
                  {/* Hover Overlay */}
                  <div className="absolute inset-0 bg-black/0 group-hover:bg-black/40 transition-all duration-300 flex items-center justify-center">
                    <button className="opacity-0 group-hover:opacity-100 transform scale-90 group-hover:scale-100 transition-all duration-300 bg-white text-gray-900 px-8 py-3 rounded-lg font-semibold shadow-xl hover:bg-gray-50">
                      Use Template
                    </button>
                  </div>
                </div>
                
                {/* Template Info */}
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

        {/* CTA Section */}
        <div className="mt-16 text-center">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            Ready to Build Your Resume?
          </h2>
          <p className="text-gray-600 mb-8 max-w-2xl mx-auto">
            All templates are free to use and optimized for Applicant Tracking Systems (ATS).
            Start building your professional resume in minutes.
          </p>
          <button
            onClick={() => navigate('/resume/new')}
            className="bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 text-white px-8 py-4 rounded-full font-semibold text-lg transition-all transform hover:scale-105 shadow-xl"
          >
            Start Building Free
          </button>
        </div>
      </main>
    </div>
  )
}
