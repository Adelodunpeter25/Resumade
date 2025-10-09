import { useState, useEffect } from 'react'

export default function LandingPage() {
  const [openFaq, setOpenFaq] = useState<number | null>(null)
  const [typedText, setTypedText] = useState('Professional') // Show first word immediately
  const [isDeleting, setIsDeleting] = useState(false)
  const [loopNum, setLoopNum] = useState(0)
  const [typingSpeed, setTypingSpeed] = useState(150)

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
              <a href="/login" className="text-gray-600 hover:text-gray-900 font-medium transition-colors">
                Login
              </a>
              <a href="/resume/new" className="bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 text-white px-6 py-2 rounded-full font-medium transition-all transform hover:scale-105 shadow-lg">
                Build Resume
              </a>
            </div>
          </div>
        </div>
      </header>

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

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="bg-white p-8 rounded-2xl shadow-lg hover:shadow-xl transition-shadow">
              <div className="w-12 h-12 bg-gradient-to-br from-emerald-600 to-teal-600 rounded-lg flex items-center justify-center mb-6">
                <span className="text-white text-xl">📝</span>
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-4">Easy to Use</h3>
              <p className="text-gray-600">
                Simple drag-and-drop interface. No design skills required. Build your resume in minutes.
              </p>
            </div>

            <div className="bg-white p-8 rounded-2xl shadow-lg hover:shadow-xl transition-shadow">
              <div className="w-12 h-12 bg-gradient-to-br from-emerald-600 to-teal-600 rounded-lg flex items-center justify-center mb-6">
                <span className="text-white text-xl">🎨</span>
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-4">Professional Templates</h3>
              <p className="text-gray-600">
                Choose from 15+ expertly designed templates that are ATS-friendly and recruiter-approved.
              </p>
            </div>

            <div className="bg-white p-8 rounded-2xl shadow-lg hover:shadow-xl transition-shadow">
              <div className="w-12 h-12 bg-gradient-to-br from-emerald-600 to-teal-600 rounded-lg flex items-center justify-center mb-6">
                <span className="text-white text-xl">⚡</span>
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-4">Instant Download</h3>
              <p className="text-gray-600">
                Download your resume as PDF instantly. Multiple formats available for different needs.
              </p>
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
            Ready to Land Your Dream Job?
          </h2>
          <p className="text-xl text-emerald-100 mb-8">
            Join thousands of job seekers who've successfully built their careers with Resumade.
          </p>
          <a href="/resume/new" className="bg-white text-emerald-600 hover:bg-gray-100 px-8 py-4 rounded-full font-semibold text-lg transition-all transform hover:scale-105 shadow-xl">
            Start Building Your Resume
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
            © 2024 Resumade. All rights reserved. Build your future today.
          </p>
        </div>
      </footer>
    </div>
  )
}
