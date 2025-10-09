import type { Resume } from '../../types'

interface Props {
  resume: Partial<Resume>
  template: string
}

export default function ResumePreviewHTML({ resume, template }: Props) {
  const renderProfessionalBlue = () => (
    <div className="bg-white p-8 shadow-lg" style={{ width: '210mm', minHeight: '297mm', margin: '0 auto' }}>
      {/* Header */}
      <div className="border-b-4 border-blue-600 pb-4 mb-6">
        <h1 className="text-4xl font-bold text-gray-900 mb-2">
          {resume.personal_info?.full_name || 'Your Name'}
        </h1>
        <div className="flex flex-wrap gap-3 text-sm text-gray-600">
          <span>{resume.personal_info?.email}</span>
          <span>•</span>
          <span>{resume.personal_info?.phone}</span>
          <span>•</span>
          <span>{resume.personal_info?.location}</span>
        </div>
        {resume.personal_info?.linkedin && (
          <div className="text-sm text-blue-600 mt-1">{resume.personal_info.linkedin}</div>
        )}
      </div>

      {/* Summary */}
      {resume.personal_info?.summary && (
        <div className="mb-6">
          <h2 className="text-xl font-bold text-blue-600 mb-2">PROFESSIONAL SUMMARY</h2>
          <p className="text-gray-700 text-sm leading-relaxed">{resume.personal_info.summary}</p>
        </div>
      )}

      {/* Experience */}
      {resume.experience && resume.experience.length > 0 && (
        <div className="mb-6">
          <h2 className="text-xl font-bold text-blue-600 mb-3">EXPERIENCE</h2>
          {resume.experience.map((exp, idx) => (
            <div key={idx} className="mb-4">
              <div className="flex justify-between items-start mb-1">
                <div>
                  <h3 className="font-bold text-gray-900">{exp.position}</h3>
                  <p className="text-gray-700">{exp.company}</p>
                </div>
                <span className="text-sm text-gray-600">
                  {exp.start_date} - {exp.current ? 'Present' : exp.end_date}
                </span>
              </div>
              <p className="text-sm text-gray-600">{exp.description}</p>
            </div>
          ))}
        </div>
      )}

      {/* Education */}
      {resume.education && resume.education.length > 0 && (
        <div className="mb-6">
          <h2 className="text-xl font-bold text-blue-600 mb-3">EDUCATION</h2>
          {resume.education.map((edu, idx) => (
            <div key={idx} className="mb-3">
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="font-bold text-gray-900">{edu.degree} in {edu.field_of_study}</h3>
                  <p className="text-gray-700">{edu.institution}</p>
                </div>
                <span className="text-sm text-gray-600">
                  {edu.start_date} - {edu.end_date || 'Present'}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Skills */}
      {resume.skills && resume.skills.length > 0 && (
        <div className="mb-6">
          <h2 className="text-xl font-bold text-blue-600 mb-3">SKILLS</h2>
          <div className="flex flex-wrap gap-2">
            {resume.skills.map((skill, idx) => (
              <span key={idx} className="px-3 py-1 bg-blue-100 text-blue-800 rounded text-sm">
                {skill.name}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  )

  const renderMinimalist = () => (
    <div className="bg-white p-8 shadow-lg" style={{ width: '210mm', minHeight: '297mm', margin: '0 auto' }}>
      {/* Header */}
      <div className="text-center border-b border-gray-300 pb-6 mb-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          {resume.personal_info?.full_name || 'Your Name'}
        </h1>
        <div className="text-sm text-gray-600 space-x-2">
          <span>{resume.personal_info?.email}</span>
          <span>|</span>
          <span>{resume.personal_info?.phone}</span>
          <span>|</span>
          <span>{resume.personal_info?.location}</span>
        </div>
      </div>

      {/* Summary */}
      {resume.personal_info?.summary && (
        <div className="mb-6">
          <p className="text-gray-700 text-sm text-center italic">{resume.personal_info.summary}</p>
        </div>
      )}

      {/* Experience */}
      {resume.experience && resume.experience.length > 0 && (
        <div className="mb-6">
          <h2 className="text-lg font-bold text-gray-900 mb-3 uppercase tracking-wide">Experience</h2>
          {resume.experience.map((exp, idx) => (
            <div key={idx} className="mb-4">
              <div className="flex justify-between mb-1">
                <h3 className="font-semibold text-gray-900">{exp.position}</h3>
                <span className="text-sm text-gray-600">{exp.start_date} - {exp.current ? 'Present' : exp.end_date}</span>
              </div>
              <p className="text-gray-700 text-sm mb-1">{exp.company}</p>
              <p className="text-sm text-gray-600">{exp.description}</p>
            </div>
          ))}
        </div>
      )}

      {/* Education */}
      {resume.education && resume.education.length > 0 && (
        <div className="mb-6">
          <h2 className="text-lg font-bold text-gray-900 mb-3 uppercase tracking-wide">Education</h2>
          {resume.education.map((edu, idx) => (
            <div key={idx} className="mb-3">
              <div className="flex justify-between">
                <div>
                  <h3 className="font-semibold text-gray-900">{edu.degree}</h3>
                  <p className="text-sm text-gray-700">{edu.institution}</p>
                </div>
                <span className="text-sm text-gray-600">{edu.start_date} - {edu.end_date || 'Present'}</span>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Skills */}
      {resume.skills && resume.skills.length > 0 && (
        <div>
          <h2 className="text-lg font-bold text-gray-900 mb-3 uppercase tracking-wide">Skills</h2>
          <div className="flex flex-wrap gap-2">
            {resume.skills.map((skill, idx) => (
              <span key={idx} className="text-sm text-gray-700">
                {skill.name}{idx < resume.skills!.length - 1 ? ' •' : ''}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  )

  const templates: Record<string, () => JSX.Element> = {
    'professional-blue': renderProfessionalBlue,
    'minimalist-two-column': renderMinimalist,
    'linkedin-style': renderProfessionalBlue,
    'gradient-sidebar': renderMinimalist
  }

  const renderTemplate = templates[template] || renderProfessionalBlue

  return (
    <div className="bg-gray-100 p-4 overflow-auto" style={{ height: 'calc(100vh - 180px)' }}>
      {renderTemplate()}
    </div>
  )
}
