import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { ArrowLeft } from 'lucide-react'
import { resumeService } from '../services'
import type { Template } from '../types'
import ResumePreviewHTML from '../components/resume/ResumePreviewHTML'

// Sample resume data for preview
const sampleResume = {
  title: 'Sample Resume',
  template_name: 'professional-blue',
  personal_info: {
    full_name: 'John Doe',
    email: 'john.doe@email.com',
    phone: '(555) 123-4567',
    location: 'New York, NY',
    linkedin: 'linkedin.com/in/johndoe',
    website: 'johndoe.com',
    summary: 'Results-driven software engineer with 5+ years of experience in full-stack development. Proven track record of delivering scalable solutions and leading cross-functional teams to success.'
  },
  experience: [
    {
      company: 'Tech Solutions Inc.',
      position: 'Senior Software Engineer',
      location: 'New York, NY',
      start_date: '2021-03',
      end_date: '',
      current: true,
      description: 'Led development of microservices architecture serving 1M+ users. Mentored team of 5 junior developers and improved deployment efficiency by 40%.'
    },
    {
      company: 'Digital Innovations',
      position: 'Software Engineer',
      location: 'Boston, MA',
      start_date: '2019-06',
      end_date: '2021-02',
      current: false,
      description: 'Developed and maintained RESTful APIs and React applications. Collaborated with product team to deliver features on time.'
    }
  ],
  education: [
    {
      institution: 'Massachusetts Institute of Technology',
      degree: "Bachelor's of Science",
      field_of_study: 'Computer Science',
      location: 'Cambridge, MA',
      start_date: '2015-09',
      end_date: '2019-05',
      gpa: '3.8/4.0'
    }
  ],
  skills: [
    { name: 'JavaScript', level: 'Expert' },
    { name: 'React', level: 'Expert' },
    { name: 'Node.js', level: 'Advanced' },
    { name: 'Python', level: 'Advanced' },
    { name: 'TypeScript', level: 'Advanced' },
    { name: 'AWS', level: 'Intermediate' },
    { name: 'Docker', level: 'Intermediate' },
    { name: 'PostgreSQL', level: 'Advanced' }
  ],
  certifications: [
    {
      name: 'AWS Certified Solutions Architect',
      issuer: 'Amazon Web Services',
      date: '2022-08',
      credential_id: 'AWS-12345'
    }
  ],
  projects: [
    {
      name: 'E-Commerce Platform',
      description: 'Built scalable e-commerce platform handling 10K+ daily transactions',
      technologies: ['React', 'Node.js', 'MongoDB', 'Stripe'],
      url: 'github.com/johndoe/ecommerce'
    }
  ]
}

export default function Templates() {
  const navigate = useNavigate()
  const [templates, setTemplates] = useState<Template[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadTemplates()
  }, [])

  const loadTemplates = async () => {
    try {
      const response = await resumeService.getTemplates()
      if (response.success && response.data) {
        setTemplates(response.data)
      }
    } catch (err) {
      // Fallback templates
      setTemplates([
        { name: 'professional-blue', display_name: 'Professional Blue', description: 'Clean and professional with blue accents', preview_url: '' },
        { name: 'minimalist-two-column', display_name: 'Minimalist Two Column', description: 'Simple and elegant two-column layout', preview_url: '' },
        { name: 'linkedin-style', display_name: 'LinkedIn Style', description: 'Modern card-based design', preview_url: '' },
        { name: 'gradient-sidebar', display_name: 'Gradient Sidebar', description: 'Eye-catching gradient sidebar', preview_url: '' }
      ])
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
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
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
                  <div className="scale-[0.35] origin-top-left w-[285%] h-[285%]">
                    <ResumePreviewHTML 
                      resume={{ ...sampleResume, template_name: template.name }} 
                      template={template.name}
                    />
                  </div>
                  {/* Hover Overlay */}
                  <div className="absolute inset-0 bg-black/0 group-hover:bg-black/40 transition-all duration-300 flex items-center justify-center">
                    <button className="opacity-0 group-hover:opacity-100 transform scale-90 group-hover:scale-100 transition-all duration-300 bg-white text-gray-900 px-8 py-3 rounded-lg font-semibold shadow-xl hover:bg-gray-50">
                      Use Template
                    </button>
                  </div>
                </div>
                
                {/* Template Name */}
                <div className="p-3 text-center">
                  <h3 className="font-semibold text-gray-900 text-sm">
                    {template.display_name}
                  </h3>
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
