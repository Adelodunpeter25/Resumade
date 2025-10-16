import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

export default function Header() {
  const navigate = useNavigate()
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  return (
    <>
      <header className="bg-white/80 backdrop-blur-md border-b border-gray-100 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-2 cursor-pointer" onClick={() => navigate('/')}>
              <div className="w-8 h-8 bg-gradient-to-br from-emerald-600 to-teal-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-sm">R</span>
              </div>
              <h1 className="text-xl font-bold bg-gradient-to-r from-emerald-600 to-teal-600 bg-clip-text text-transparent">
                Resumade
              </h1>
            </div>

            {/* Center Navigation */}
            <div className="hidden md:flex items-center space-x-8">
              <a href="/" className="text-gray-600 hover:text-gray-900 font-medium transition-colors">
                Home
              </a>
              <a href="/templates" className="text-gray-600 hover:text-gray-900 font-medium transition-colors">
                Templates
              </a>
              <a href="/contact" className="text-gray-600 hover:text-gray-900 font-medium transition-colors">
                Contact
              </a>
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

      {/* Mobile Sidebar */}
      <>
        {/* Overlay */}
        <div 
          className={`fixed inset-0 bg-black/50 z-[100] md:hidden transition-opacity duration-300 ${mobileMenuOpen ? 'opacity-100' : 'opacity-0 pointer-events-none'}`}
          onClick={() => setMobileMenuOpen(false)}
        />
        
        {/* Sidebar */}
        <div className={`fixed top-0 right-0 h-full w-64 bg-white shadow-2xl z-[101] md:hidden transform transition-transform duration-300 ${mobileMenuOpen ? 'translate-x-0' : 'translate-x-full'}`}>
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
            
            <div className="mt-8 space-y-4">
              <a href="/" className="block text-gray-600 hover:text-gray-900 font-medium py-2">
                Home
              </a>
              <a href="/templates" className="block text-gray-600 hover:text-gray-900 font-medium py-2">
                Templates
              </a>
              <a href="/contact" className="block text-gray-600 hover:text-gray-900 font-medium py-2">
                Contact
              </a>
              <a href="/login" className="block bg-white border-2 border-emerald-600 text-emerald-600 px-6 py-2 rounded-full font-medium text-center hover:bg-emerald-50 transition-colors">
                Login
              </a>
              <a href="/register" className="block bg-gradient-to-r from-emerald-600 to-teal-600 text-white px-6 py-2 rounded-full font-medium text-center">
                Sign Up
              </a>
            </div>
          </div>
        </div>
      </>
    </>
  )
}
