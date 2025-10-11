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
    setCalculating(true)
    try {
      const response = await atsService.calculateScore(Number(id))
      console.log('ATS Response:', response)
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
            {/* Overall Score */}
            <div className="bg-white rounded-lg shadow p-8">
              <div className="flex items-center justify-between">
                <div className="flex-1">
                  <h2 className="text-2xl font-bold text-gray-900 mb-2">Overall ATS Score</h2>
                  <p className="text-gray-600">
                    Your resume's compatibility with Applicant Tracking Systems
                  </p>
                </div>
                <div className="flex items-center gap-6">
                  {getScoreIcon(score.ats_score)}
                  <div className="text-center">
                    <div className={`text-6xl font-bold ${getScoreColor(score.ats_score)}`}>
                      {score.ats_score}
                    </div>
                    <div className="text-gray-600 text-sm">out of 100</div>
                  </div>
                </div>
              </div>
            </div>

            {/* Section Scores */}
            <div className="bg-white rounded-lg shadow p-8">
              <h3 className="text-xl font-bold text-gray-900 mb-6">Section Breakdown</h3>
              <div className="space-y-4">
                {Object.entries(score.section_breakdown).map(([section, sectionScore]) => (
                  <div key={section}>
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-gray-700 font-medium capitalize">
                        {section.replace('_', ' ')}
                      </span>
                      <span className={`font-semibold ${getScoreColor(sectionScore)}`}>
                        {sectionScore}%
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-3">
                      <div
                        className={`h-3 rounded-full transition-all ${
                          sectionScore >= 80 ? 'bg-green-600' :
                          sectionScore >= 60 ? 'bg-yellow-600' :
                          'bg-red-600'
                        }`}
                        style={{ width: `${sectionScore}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Feedback */}
            {score.feedback && (
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
                <h3 className="text-lg font-bold text-blue-900 mb-4 flex items-center gap-2">
                  <AlertCircle size={24} />
                  Feedback
                </h3>
                <p className="text-blue-700">{score.feedback}</p>
              </div>
            )}

            {/* Suggestions */}
            {score.suggestions.length > 0 && (
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
                <h3 className="text-lg font-bold text-blue-900 mb-4 flex items-center gap-2">
                  <AlertCircle size={24} />
                  Improvement Suggestions
                </h3>
                <ul className="space-y-3">
                  {score.suggestions.map((suggestion, index) => (
                    <li key={index} className="text-blue-700 flex items-start gap-3">
                      <span className="text-blue-600 font-bold mt-1">{index + 1}.</span>
                      <span>{suggestion}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Score Interpretation */}
            <div className={`${getScoreBgColor(score.ats_score)} border ${
              score.ats_score >= 80 ? 'border-green-200' :
              score.ats_score >= 60 ? 'border-yellow-200' :
              'border-red-200'
            } rounded-lg p-6`}>
              <h3 className={`text-lg font-bold mb-2 ${getScoreColor(score.ats_score)}`}>
                {score.grade}
              </h3>
              <p className="text-gray-700">
                {score.ats_score >= 80
                  ? 'Your resume is well-optimized for ATS systems and should pass most automated screenings.'
                  : score.ats_score >= 60
                  ? 'Your resume has a decent chance of passing ATS systems, but there\'s room for improvement.'
                  : 'Your resume may struggle with ATS systems. Consider implementing the suggestions above.'}
              </p>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}
