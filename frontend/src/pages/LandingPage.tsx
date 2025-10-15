import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { API_BASE_URL } from '../services/api'

export default function LandingPage() {
  const navigate = useNavigate()
  const [openFaq, setOpenFaq] = useState<number | null>(null)
  const [currentFeatureIndex, setCurrentFeatureIndex] = useState(5) // Start from middle set
  const [isTransitioning, setIsTransitioning] = useState(true)
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [typedText, setTypedText] = useState('Professional') // Show first word immediately
  const [isDeleting, setIsDeleting] = useState(false)
  const [loopNum, setLoopNum] = useState(0)
  const [typingSpeed, setTypingSpeed] = useState(150)

  const features = [
    {
      icon: '📝',
      title: 'Easy to Use',
      description: 'Simple form-based interface with live preview. No design skills required. Build your resume in minutes.'
    },
    {
      icon: '🎨',
      title: 'Professional Templates',
      description: 'Choose from 15+ expertly designed templates that are ATS-friendly and recruiter-approved.'
    },
    {
      icon: '⚡',
      title: 'Instant Download',
      description: 'Download your resume as PDF instantly. Multiple formats available for different needs.'
    },
    {
      icon: '🚀',
      title: 'Want Quick Edit?',
      description: 'Import your existing resume and edit. No signup required.'
    },
    {
      icon: '🔓',
      title: 'Flexible Access',
      description: 'Quick edit with no signup, or unlock more features like version history by signing up easily with Google.'
    }
  ]

  const getCardsPerView = () => {
    if (typeof window === 'undefined') return 1
    if (window.innerWidth >= 1536) return 4 // 2xl
    if (window.innerWidth >= 1024) return 3 // lg
    return 1 // mobile
  }

  const nextFeature = () => {
    setIsTransitioning(true)
    setCurrentFeatureIndex((prev) => prev + 1)
  }

  const prevFeature = () => {
    setIsTransitioning(true)
    setCurrentFeatureIndex((prev) => prev - 1)
  }

  // Infinite loop: reset position without animation when reaching end of clones
  useEffect(() => {
    if (currentFeatureIndex === features.length * 2) {
      setTimeout(() => {
        setIsTransitioning(false)
        setCurrentFeatureIndex(features.length)
      }, 500)
    } else if (currentFeatureIndex === features.length - 1) {
      setTimeout(() => {
        setIsTransitioning(false)
        setCurrentFeatureIndex(features.length * 2 - 1)
      }, 500)
    }
  }, [currentFeatureIndex, features.length])

  const words = ['Professional', 'ATS-Friendly', 'Modern', 'Job-Winning']
  const subtitles = {
    'Professional': 'Designed by HR experts to make the best first impression',
    'ATS-Friendly': 'Pass automated screenings and reach human recruiters',
    'Modern': 'Stand out from the crowd with contemporary designs',
    'Job-Winning': 'Get more interviews with optimized resume templates'
  }
  const fullText = words[loopNum % words.length]
  const currentSubtitle = subtitles[fullText as keyof typeof subtitles]

  useEffect(() => {
    const handleTyping = () => {
      const currentText = fullText

      if (!isDeleting) {
        setTypedText(currentText.substring(0, typedText.length + 1))
        setTypingSpeed(150)

        if (typedText === currentText) {
          setTimeout(() => setIsDeleting(true), 2000)
        }
      } else {
        setTypedText(currentText.substring(0, typedText.length - 1))
        setTypingSpeed(75)

        if (typedText === '') {
          setIsDeleting(false)
          setLoopNum(loopNum + 1)
        }
      }
    }

    const timer = setTimeout(handleTyping, typingSpeed)
    return () => clearTimeout(timer)
  }, [typedText, isDeleting, loopNum, typingSpeed, fullText])

  const toggleFaq = (index: number) => {
    setOpenFaq(openFaq === index ? null : index)
  }

  const faqs = [
    {
      question: "Is Resumade really free?",
      answer: "Yes! You can create and download your first resume completely free. Premium features include additional templates and advanced customization options."
    },
    {
      question: "Are the templates ATS-friendly?",
      answer: "Absolutely! All our templates are designed to pass Applicant Tracking Systems (ATS) used by most companies, ensuring your resume gets seen by human recruiters."
    },
    {
      question: "How long does it take to build a resume?",
      answer: "Most users complete their resume in 10-15 minutes. Our intuitive interface and pre-written content suggestions make the process quick and easy."
    },
    {
      question: "Can I edit my resume after downloading?",
      answer: "Yes! Your resume is saved to your account and you can edit it anytime. Download updated versions whenever you need them."
    },
    {
      question: "What file formats are available?",
      answer: "You can download your resume as PDF (recommended), Word document, or plain text format to meet different application requirements."
    },
    {
      question: "Do you offer customer support?",
      answer: "Yes! Our support team is available 24/7 via chat and email to help you create the perfect resume and answer any questions."
    }
  ]
  return (
    <div className="min-h-screen bg-white">
      {/* Header */}
      <header className="absolute top-0 w-full z-50 bg-white/80 backdrop-blur-md border-b border-gray-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-gradient-to-br from-emerald-600 to-teal-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-sm">R</span>
              </div>
              <h1 className="text-xl font-bold bg-gradient-to-r from-emerald-600 to-teal-600 bg-clip-text text-transparent">
                Resumade
              </h1>
            </div>
            <div className="flex items-center space-x-4">
              {/* Desktop Menu */}
              <div className="hidden md:flex items-center space-x-4">
                <a href="/login" className="text-gray-600 hover:text-gray-900 font-medium transition-colors">
                  Login
                </a>
                <a href="/register" className="bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 text-white px-6 py-2 rounded-full font-medium transition-all transform hover:scale-105 shadow-lg">
                  Sign Up
                </a>
              </div>

              {/* Mobile Hamburger */}
              <button
                onClick={() => setMobileMenuOpen(true)}
                className="md:hidden p-2 text-gray-600 hover:text-gray-900"
                aria-label="Open menu"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Mobile Sidebar - Outside header */}
      <>
        {/* Overlay */}
        <div 
          className={`fixed inset-0 bg-black/50 z-[100] md:hidden transition-opacity duration-300 ${mobileMenuOpen ? 'opacity-100' : 'opacity-0 pointer-events-none'}`}
          onClick={() => setMobileMenuOpen(false)}
        />
        
        {/* Sidebar */}
        <div className={`fixed top-0 right-0 h-full w-64 bg-white shadow-2xl z-[101] md:hidden transform transition-transform duration-300 ease-in-out ${mobileMenuOpen ? 'translate-x-0' : 'translate-x-full'}`}>
          <div className="p-6">
            <button
              onClick={() => setMobileMenuOpen(false)}
              className="absolute top-4 right-4 p-2 text-gray-600 hover:text-gray-900"
              aria-label="Close menu"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>

            {/* Logo */}
            <div className="flex items-center space-x-2 mb-8">
              <div className="w-8 h-8 bg-gradient-to-br from-emerald-600 to-teal-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-sm">R</span>
              </div>
              <h1 className="text-xl font-bold bg-gradient-to-r from-emerald-600 to-teal-600 bg-clip-text text-transparent">
                Resumade
              </h1>
            </div>

            <div className="space-y-4">
              <a 
                href="/login" 
                className="block w-full text-center py-3 text-gray-700 hover:bg-gray-100 rounded-lg font-medium transition-colors"
              >
                Login
              </a>
              <a 
                href="/register" 
                className="block w-full text-center py-3 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 text-white rounded-lg font-medium shadow-lg transition-all"
              >
                Sign Up
              </a>
            </div>
          </div>
        </div>
      </>

      {/* Hero Section */}
      <section className="relative pt-20 pb-32 overflow-hidden">
        {/* Background Elements */}
        <div className="absolute inset-0 bg-gradient-to-br from-emerald-50 via-white to-teal-50"></div>
        <div className="absolute top-0 left-0 w-full h-full">
          <div className="absolute top-20 left-10 w-72 h-72 bg-gradient-to-br from-emerald-400/20 to-teal-400/20 rounded-full blur-3xl"></div>
          <div className="absolute top-40 right-10 w-96 h-96 bg-gradient-to-br from-teal-400/20 to-cyan-400/20 rounded-full blur-3xl"></div>
          <div className="absolute bottom-20 left-1/2 w-80 h-80 bg-gradient-to-br from-green-400/20 to-emerald-400/20 rounded-full blur-3xl"></div>
        </div>

        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20">
          <div className="text-center">
            {/* Badge */}
            <div className="inline-flex items-center px-4 py-2 bg-gradient-to-r from-emerald-100 to-teal-100 rounded-full text-sm font-medium text-emerald-700 mb-8">
              <span className="w-2 h-2 bg-green-500 rounded-full mr-2 animate-pulse"></span>
              Professional templates designed by experts
            </div>

            {/* Main Headline */}
            <h1 className="text-5xl md:text-7xl font-bold text-gray-900 mb-6 leading-tight">
              Build Your <span className="bg-gradient-to-r from-emerald-600 to-teal-600 bg-clip-text text-transparent">{typedText}</span>
              <span className="animate-pulse text-emerald-600">|</span>
              <br />
              Resume in Minutes
            </h1>

            {/* Subtitle */}
            <p className="text-xl md:text-2xl text-gray-600 mb-12 max-w-3xl mx-auto leading-relaxed transition-all duration-500">
              {currentSubtitle}
            </p>

            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-16">
              <a href="/resume/new" className="bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 text-white px-8 py-4 rounded-full font-semibold text-lg transition-all transform hover:scale-105 shadow-xl">
                Start Building Free
              </a>
              <a href="/templates" className="border-2 border-emerald-600 text-emerald-600 hover:bg-emerald-600 hover:text-white px-8 py-4 rounded-full font-semibold text-lg transition-all">
                View Templates
              </a>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto">
              <div className="text-center">
                <div className="text-3xl md:text-4xl font-bold text-emerald-600 mb-2">50K+</div>
                <div className="text-gray-600">Resumes Created</div>
              </div>
              <div className="text-center">
                <div className="text-3xl md:text-4xl font-bold text-emerald-600 mb-2">15+</div>
                <div className="text-gray-600">Professional Templates</div>
              </div>
              <div className="text-center">
                <div className="text-3xl md:text-4xl font-bold text-emerald-600 mb-2">95%</div>
                <div className="text-gray-600">Success Rate</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Template Showcase Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
              Choose Your Perfect Template
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Professional, ATS-friendly templates designed to get you hired
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
            {[
              { name: 'professional-blue', display: 'Professional Blue' },
              { name: 'linkedin-style', display: 'LinkedIn Style' },
              { name: 'gradient-sidebar', display: 'Gradient Sidebar' },
              { name: 'minimalist-two-column', display: 'Minimalist Two Column' }
            ].map((template) => (
              <div
                key={template.name}
                className="group cursor-pointer"
                onClick={() => navigate(`/resume/new?template=${template.name}`)}
              >
                <div className="bg-white rounded-lg overflow-hidden shadow-sm hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1">
                  <div className="aspect-[8.5/11] bg-gray-50 relative overflow-hidden border-b border-gray-100">
                    <iframe
                      src={`${API_BASE_URL}/api/resumes/templates/preview?template=${template.name}`}
                      className="w-full h-full border-0 pointer-events-none scale-[0.4] origin-top-left"
                      style={{ width: '250%', height: '250%' }}
                      title={`${template.display} Preview`}
                    />
                    <div className="absolute inset-0 bg-black/0 group-hover:bg-black/40 transition-all duration-300 flex items-center justify-center">
                      <button className="opacity-0 group-hover:opacity-100 transform scale-90 group-hover:scale-100 transition-all duration-300 bg-white text-gray-900 px-6 py-2 rounded-lg font-semibold shadow-xl">
                        Use Template
                      </button>
                    </div>
                  </div>
                  <div className="p-3 text-center">
                    <h3 className="font-semibold text-gray-900 text-sm">
                      {template.display}
                    </h3>
                  </div>
                </div>
              </div>
            ))}
          </div>

          <div className="text-center">
            <button
              onClick={() => navigate('/templates')}
              className="inline-flex items-center gap-2 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 text-white px-8 py-4 rounded-full font-semibold text-lg transition-all transform hover:scale-105 shadow-xl"
            >
              View All Templates
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </button>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-20 bg-gradient-to-br from-emerald-50 to-teal-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
              How It Works
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Create your professional resume in just 3 simple steps
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 lg:gap-12">
            {/* Step 1 */}
            <div className="relative">
              <div className="bg-white rounded-2xl p-8 shadow-lg hover:shadow-xl transition-shadow">
                <div className="absolute -top-6 left-1/2 transform -translate-x-1/2">
                  <div className="w-12 h-12 bg-gradient-to-r from-emerald-600 to-teal-600 rounded-full flex items-center justify-center text-white font-bold text-xl shadow-lg">
                    1
                  </div>
                </div>
                <div className="mt-6 text-center">
                  <div className="w-20 h-20 bg-emerald-100 rounded-full flex items-center justify-center mx-auto mb-6">
                    <svg className="w-10 h-10 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM4 13a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H5a1 1 0 01-1-1v-6zM16 13a1 1 0 011-1h2a1 1 0 011 1v6a1 1 0 01-1 1h-2a1 1 0 01-1-1v-6z" />
                    </svg>
                  </div>
                  <h3 className="text-2xl font-bold text-gray-900 mb-3">Choose Template</h3>
                  <p className="text-gray-600">
                    Select from our collection of professional, ATS-friendly templates designed by experts
                  </p>
                </div>
              </div>
              {/* Arrow */}
              <div className="hidden md:block absolute top-1/2 -right-6 transform -translate-y-1/2">
                <svg className="w-12 h-12 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                </svg>
              </div>
            </div>

            {/* Step 2 */}
            <div className="relative">
              <div className="bg-white rounded-2xl p-8 shadow-lg hover:shadow-xl transition-shadow">
                <div className="absolute -top-6 left-1/2 transform -translate-x-1/2">
                  <div className="w-12 h-12 bg-gradient-to-r from-emerald-600 to-teal-600 rounded-full flex items-center justify-center text-white font-bold text-xl shadow-lg">
                    2
                  </div>
                </div>
                <div className="mt-6 text-center">
                  <div className="w-20 h-20 bg-teal-100 rounded-full flex items-center justify-center mx-auto mb-6">
                    <svg className="w-10 h-10 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                    </svg>
                  </div>
                  <h3 className="text-2xl font-bold text-gray-900 mb-3">Fill in Details</h3>
                  <p className="text-gray-600">
                    Add your information with our easy-to-use editor and see live preview as you type
                  </p>
                </div>
              </div>
              {/* Arrow */}
              <div className="hidden md:block absolute top-1/2 -right-6 transform -translate-y-1/2">
                <svg className="w-12 h-12 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                </svg>
              </div>
            </div>

            {/* Step 3 */}
            <div className="relative">
              <div className="bg-white rounded-2xl p-8 shadow-lg hover:shadow-xl transition-shadow">
                <div className="absolute -top-6 left-1/2 transform -translate-x-1/2">
                  <div className="w-12 h-12 bg-gradient-to-r from-emerald-600 to-teal-600 rounded-full flex items-center justify-center text-white font-bold text-xl shadow-lg">
                    3
                  </div>
                </div>
                <div className="mt-6 text-center">
                  <div className="w-20 h-20 bg-cyan-100 rounded-full flex items-center justify-center mx-auto mb-6">
                    <svg className="w-10 h-10 text-cyan-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                    </svg>
                  </div>
                  <h3 className="text-2xl font-bold text-gray-900 mb-3">Download PDF</h3>
                  <p className="text-gray-600">
                    Download your professional resume as a PDF and start applying to your dream jobs
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* CTA */}
          <div className="text-center mt-12">
            <a
              href="/resume/new"
              className="inline-flex items-center gap-2 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 text-white px-8 py-4 rounded-full font-semibold text-lg transition-all transform hover:scale-105 shadow-xl"
            >
              Get Started Now - It's Free
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </a>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
              Why Choose Resumade?
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Everything you need to create a standout resume that gets you noticed by employers.
            </p>
          </div>

          {/* Carousel */}
          <div className="relative">
            <div className="overflow-hidden">
              <div 
                className={`flex ${isTransitioning ? 'transition-transform duration-500 ease-in-out' : ''}`}
                style={{ 
                  transform: `translateX(calc(-${currentFeatureIndex} * (100% / ${getCardsPerView()})))` 
                }}
              >
                {[...features, ...features, ...features].map((feature, index) => (
                  <div
                    key={index}
                    className="w-full lg:w-1/3 2xl:w-1/4 flex-shrink-0 px-4"
                  >
                    <div className="bg-white rounded-lg overflow-hidden shadow-sm hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1 h-full">
                      <div className="p-8 flex flex-col items-center text-center h-full">
                        <div className="w-16 h-16 bg-gradient-to-br from-emerald-600 to-teal-600 rounded-lg flex items-center justify-center mb-6">
                          <span className="text-white text-3xl">{feature.icon}</span>
                        </div>
                        <h3 className="text-xl font-bold text-gray-900 mb-4">
                          {feature.title}
                        </h3>
                        <p className="text-gray-600 text-sm leading-relaxed">
                          {feature.description}
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Navigation */}
            <div className="flex justify-center items-center gap-4 mt-8">
              <button
                onClick={prevFeature}
                className="p-2 rounded-full bg-gray-200 hover:bg-emerald-600 hover:text-white transition-colors"
                aria-label="Previous"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                </svg>
              </button>

              <div className="flex gap-2">
                {features.map((_, index) => (
                  <button
                    key={index}
                    onClick={() => setCurrentFeatureIndex(features.length + index)}
                    className={`w-3 h-3 rounded-full transition-all ${
                      (currentFeatureIndex % features.length) === index
                        ? 'bg-emerald-600 w-8'
                        : 'bg-gray-300 hover:bg-gray-400'
                    }`}
                    aria-label={`Go to feature ${index + 1}`}
                  />
                ))}
              </div>

              <button
                onClick={nextFeature}
                className="p-2 rounded-full bg-gray-200 hover:bg-emerald-600 hover:text-white transition-colors"
                aria-label="Next"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="py-20 bg-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
              Frequently Asked Questions
            </h2>
            <p className="text-xl text-gray-600">
              Everything you need to know about Resumade
            </p>
          </div>

          <div className="space-y-4">
            {faqs.map((faq, index) => (
              <div key={index} className="border border-gray-200 rounded-2xl overflow-hidden">
                <button
                  onClick={() => toggleFaq(index)}
                  className="w-full px-6 py-4 text-left bg-white hover:bg-gray-50 transition-colors flex justify-between items-center"
                >
                  <h3 className="text-lg font-semibold text-gray-900">{faq.question}</h3>
                  <span className={`text-emerald-600 text-xl transition-transform ${openFaq === index ? 'rotate-180' : ''}`}>
                    ▼
                  </span>
                </button>
                {openFaq === index && (
                  <div className="px-6 py-4 bg-gray-50 border-t border-gray-200">
                    <p className="text-gray-600">{faq.answer}</p>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-emerald-600 to-teal-600">
        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
            Want Resume.io Without the Paywall?
          </h2>
          <p className="text-xl text-emerald-100 mb-8">
            Get all the features you need, completely free. No hidden costs, no premium tiers.
          </p>
          <a href="/register" className="bg-white text-emerald-600 hover:bg-gray-100 px-8 py-4 rounded-full font-semibold text-lg transition-all transform hover:scale-105 shadow-xl">
            Join Resumade - Free Forever
          </a>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="flex items-center justify-center space-x-2 mb-4">
            <div className="w-8 h-8 bg-gradient-to-br from-emerald-600 to-teal-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">R</span>
            </div>
            <h3 className="text-xl font-bold">Resumade</h3>
          </div>
          <p className="text-gray-400">
            © 2025 Resumade. All rights reserved.
          </p>
        </div>
      </footer>
    </div>
  )
}
