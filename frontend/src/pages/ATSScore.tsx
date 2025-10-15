import { useState, useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { ArrowLeft, RefreshCw, CheckCircle, AlertCircle, XCircle } from 'lucide-react'
import { atsService } from '../services'
import type { ATSScore as ATSScoreType } from '../services/atsService'

export default function ATSScore() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [score, setScore] = useState<ATSScoreType | null>(null)
  const [loading, setLoading] = useState(true)
  const [calculating, setCalculating] = useState(false)

  useEffect(() => {
    if (id) {
      calculateScore()
    }
  }, [id])

  const calculateScore = async () => {
    if (!id || isNaN(Number(id))) {
      alert('Invalid resume ID')
      navigate('/dashboard')
      return
    }
    setCalculating(true)
    try {
      const response = await atsService.calculateScore(Number(id))
      setScore(response)
    } catch (err) {
      console.error('ATS Error:', err)
      alert('Failed to calculate ATS score')
    } finally {
      setLoading(false)
      setCalculating(false)
    }
  }

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600'
    if (score >= 60) return 'text-yellow-600'
    return 'text-red-600'
  }

  const getScoreBgColor = (score: number) => {
    if (score >= 80) return 'bg-green-100'
    if (score >= 60) return 'bg-yellow-100'
    return 'bg-red-100'
  }

  const getScoreIcon = (score: number) => {
    if (score >= 80) return <CheckCircle className="text-green-600" size={48} />
    if (score >= 60) return <AlertCircle className="text-yellow-600" size={48} />
    return <XCircle className="text-red-600" size={48} />
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
              <h1 className="text-xl font-bold text-gray-900">ATS Score Analysis</h1>
            </div>
            <button
              onClick={calculateScore}
              disabled={calculating}
              className="flex items-center gap-2 bg-gradient-to-r from-emerald-600 to-teal-600 text-white px-4 py-2 rounded-lg hover:from-emerald-700 hover:to-teal-700 disabled:opacity-50"
            >
              <RefreshCw size={20} className={calculating ? 'animate-spin' : ''} />
              <span>{calculating ? 'Calculating...' : 'Recalculate'}</span>
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {score && (
          <div className="space-y-6">
            {/* Overall Score & Interpretation */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="bg-white rounded-lg shadow p-6">
                <h2 className="text-xl font-bold text-gray-900 mb-2 text-center">Overall ATS Score</h2>
                <p className="text-gray-600 text-center text-sm mb-6">
                  Your resume's compatibility with ATS
                </p>
                <div className="flex justify-center">
                  <div className="relative w-40 h-40">
                    <svg className="w-40 h-40 transform -rotate-90">
                      <circle
                        cx="80"
                        cy="80"
                        r="72"
                        stroke="#e5e7eb"
                        strokeWidth="14"
                        fill="none"
                      />
                      <circle
                        cx="80"
                        cy="80"
                        r="72"
                        stroke={score.ats_score >= 80 ? '#10b981' : score.ats_score >= 60 ? '#f59e0b' : '#ef4444'}
                        strokeWidth="14"
                        fill="none"
                        strokeDasharray={`${2 * Math.PI * 72}`}
                        strokeDashoffset={`${2 * Math.PI * 72 * (1 - score.ats_score / 100)}`}
                        strokeLinecap="round"
                        className="transition-all duration-1000"
                      />
                    </svg>
                    <div className="absolute inset-0 flex flex-col items-center justify-center">
                      <div className={`text-4xl font-bold ${getScoreColor(score.ats_score)}`}>
                        {score.ats_score}
                      </div>
                      <div className="text-gray-600 text-xs mt-1">out of 100</div>
                    </div>
                  </div>
                </div>
              </div>
              
              {/* Score Interpretation */}
              <div className={`${getScoreBgColor(score.ats_score)} border ${
                score.ats_score >= 80 ? 'border-green-200' :
                score.ats_score >= 60 ? 'border-yellow-200' :
                'border-red-200'
              } rounded-lg p-6 flex flex-col items-center justify-center text-center`}>
                <h3 className={`text-8xl font-bold mb-4 ${getScoreColor(score.ats_score)}`}>
                  {score.grade}
                </h3>
                <p className="text-gray-700 text-base">
                  {score.ats_score >= 80
                    ? 'Your resume is well-optimized for ATS systems and should pass most automated screenings.'
                    : score.ats_score >= 60
                    ? 'Your resume has a decent chance of passing ATS systems, but there\'s room for improvement.'
                    : 'Your resume may struggle with ATS systems. Consider implementing the suggestions below.'}
                </p>
              </div>
            </div>

            {/* Section Scores */}
            <div className="bg-white rounded-lg shadow p-8">
              <h3 className="text-xl font-bold text-gray-900 mb-6">Section Breakdown</h3>
              <div className="space-y-4">
                {Object.entries(score.section_breakdown).map(([section, sectionData]) => {
                  const percentage = typeof sectionData === 'number' ? sectionData : sectionData.percentage
                  return (
                    <div key={section}>
                      <div className="flex justify-between items-center mb-2">
                        <span className="text-gray-700 font-medium capitalize">
                          {section.replace('_', ' ')}
                        </span>
                        <span className={`font-semibold ${getScoreColor(percentage)}`}>
                          {percentage}%
                        </span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-3">
                        <div
                          className={`h-3 rounded-full transition-all ${
                            percentage >= 80 ? 'bg-green-600' :
                            percentage >= 60 ? 'bg-yellow-600' :
                            'bg-red-600'
                          }`}
                          style={{ width: `${percentage}%` }}
                        />
                      </div>
                    </div>
                  )
                })}
              </div>
            </div>

            {/* AI Feedback */}
            {score.ai_feedback && (
              <div className="bg-gradient-to-br from-purple-50 to-indigo-50 border-2 border-purple-300 rounded-xl p-8 shadow-lg">
                <h3 className="text-2xl font-bold text-purple-900 mb-6 flex items-center gap-3">
                  <span className="text-3xl">✨</span>
                  AI-Powered Insights
                </h3>
                <div className="text-gray-800 leading-relaxed space-y-4">
                  {score.ai_feedback.split('\n').map((line, index) => {
                    const trimmed = line.trim()
                    if (!trimmed) return null
                    
                    // Main numbered items
                    if (/^\d+\./.test(trimmed)) {
                      return (
                        <div key={index} className="font-semibold text-lg text-purple-900 mt-6 first:mt-0">
                          {trimmed.replace(/\*\*/g, '')}
                        </div>
                      )
                    }
                    
                    // Bullet points
                    if (trimmed.startsWith('•')) {
                      return (
                        <div key={index} className="ml-6 flex gap-3">
                          <span className="text-purple-600 mt-1">•</span>
                          <span className="flex-1">{trimmed.substring(1).trim().replace(/\*\*/g, '')}</span>
                        </div>
                      )
                    }
                    
                    // Regular paragraphs
                    return (
                      <p key={index} className="text-gray-700">
                        {trimmed.replace(/\*\*/g, '')}
                      </p>
                    )
                  })}
                </div>
              </div>
            )}


          </div>
        )}
      </main>
    </div>
  )
}
