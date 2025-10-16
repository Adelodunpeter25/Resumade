import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Search } from 'lucide-react'
import { resumeService } from '../services'
import { API_BASE_URL } from '../services/api'
import type { Template } from '../types'
import Header from '../components/common/Header'

export default function Templates() {
  const navigate = useNavigate()
  const [templates, setTemplates] = useState<Template[]>([])
  const [filteredTemplates, setFilteredTemplates] = useState<Template[]>([])
  const [loading, setLoading] = useState(true)
  const [previewUrls, setPreviewUrls] = useState<Record<string, string>>({})
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('all')
  const [categories, setCategories] = useState<string[]>([])

  useEffect(() => {
    loadTemplates()
  }, [])

  useEffect(() => {
    filterTemplates()
  }, [searchQuery, selectedCategory, templates])

  const loadTemplates = async () => {
    try {
      const response = await resumeService.getTemplates()
      if (response.success && response.data) {
        // Extract all_templates from the categorized response
        const allTemplates = response.data.all_templates || []
        setTemplates(allTemplates)
        setFilteredTemplates(allTemplates)
        
        // Extract unique categories
        const uniqueCategories = Array.from(new Set(allTemplates.map((t: Template) => t.category)))
        setCategories(uniqueCategories)
        
        // Generate preview URLs for each template
        const urls: Record<string, string> = {}
        allTemplates.forEach((template: Template) => {
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

  const filterTemplates = () => {
    let filtered = templates

    // Filter by category
    if (selectedCategory !== 'all') {
      filtered = filtered.filter(t => t.category === selectedCategory)
    }

    // Filter by search query
    if (searchQuery) {
      filtered = filtered.filter(t => 
        t.display_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        t.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
        t.category.toLowerCase().includes(searchQuery.toLowerCase())
      )
    }

    setFilteredTemplates(filtered)
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
      <Header />

      {/* Page Title */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <h1 className="text-3xl font-bold text-gray-900">Resume Templates</h1>
          <p className="text-gray-600 mt-2">Choose a template to start building your resume</p>
        </div>
      </div>

      {/* Search and Filter Bar */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex flex-col sm:flex-row gap-4">
            {/* Search */}
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
              <input
                type="text"
                placeholder="Search templates..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
              />
            </div>

            {/* Category Filter */}
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
            >
              <option value="all">All Categories</option>
              {categories.map(category => (
                <option key={category} value={category}>
                  {category.charAt(0).toUpperCase() + category.slice(1)}
                </option>
              ))}
            </select>
          </div>

          {/* Results count */}
          <div className="mt-3 text-sm text-gray-600">
            Showing {filteredTemplates.length} of {templates.length} templates
          </div>
        </div>
      </div>

      {/* Templates Grid */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {filteredTemplates.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-500 text-lg">No templates found matching your criteria</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {filteredTemplates.map((template) => (
              <div
                key={template.name}
                className="group cursor-pointer"
                onClick={() => navigate(`/resume/new?template=${template.name}`)}
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
        )}

        {/* CTA Section */}
        {filteredTemplates.length > 0 && (
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
        )}
      </main>
    </div>
  )
}
