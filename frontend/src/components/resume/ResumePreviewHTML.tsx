import type { Resume } from '../../types'
import type { JSX } from 'react'

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

  const renderLinkedInStyle = () => (
    <div className="bg-white p-8 shadow-lg" style={{ width: '210mm', minHeight: '297mm', margin: '0 auto' }}>
      {/* Header Card */}
      <div className="bg-gradient-to-r from-blue-600 to-blue-700 text-white p-6 rounded-lg mb-6 -mx-8 -mt-8">
        <div className="flex items-center gap-4">
          <div className="w-20 h-20 bg-white rounded-full flex items-center justify-center text-blue-600 text-2xl font-bold">
            {resume.personal_info?.full_name?.charAt(0) || 'U'}
          </div>
          <div>
            <h1 className="text-3xl font-bold mb-1">{resume.personal_info?.full_name || 'Your Name'}</h1>
            <div className="text-blue-100 text-sm space-y-1">
              <div>{resume.personal_info?.email} | {resume.personal_info?.phone}</div>
              <div>{resume.personal_info?.location}</div>
            </div>
          </div>
        </div>
      </div>

      {resume.personal_info?.summary && (
        <div className="mb-6 bg-gray-50 p-4 rounded-lg">
          <p className="text-gray-700 text-sm">{resume.personal_info.summary}</p>
        </div>
      )}

      {resume.experience && resume.experience.length > 0 && (
        <div className="mb-6">
          <h2 className="text-xl font-bold text-blue-600 mb-4 pb-2 border-b-2 border-blue-600">EXPERIENCE</h2>
          {resume.experience.map((exp, idx) => (
            <div key={idx} className="mb-4 bg-white border-l-4 border-blue-600 pl-4 py-2">
              <div className="flex justify-between mb-1">
                <h3 className="font-bold text-gray-900">{exp.position}</h3>
                <span className="text-sm text-gray-600">{exp.start_date} - {exp.current ? 'Present' : exp.end_date}</span>
              </div>
              <p className="text-gray-700 font-medium mb-1">{exp.company}</p>
              <p className="text-sm text-gray-600">{exp.description}</p>
            </div>
          ))}
        </div>
      )}

      {resume.education && resume.education.length > 0 && (
        <div className="mb-6">
          <h2 className="text-xl font-bold text-blue-600 mb-4 pb-2 border-b-2 border-blue-600">EDUCATION</h2>
          {resume.education.map((edu, idx) => (
            <div key={idx} className="mb-3">
              <div className="flex justify-between">
                <div>
                  <h3 className="font-bold text-gray-900">{edu.degree} in {edu.field_of_study}</h3>
                  <p className="text-gray-700">{edu.institution}</p>
                </div>
                <span className="text-sm text-gray-600">{edu.start_date} - {edu.end_date || 'Present'}</span>
              </div>
            </div>
          ))}
        </div>
      )}

      {resume.skills && resume.skills.length > 0 && (
        <div>
          <h2 className="text-xl font-bold text-blue-600 mb-4 pb-2 border-b-2 border-blue-600">SKILLS</h2>
          <div className="flex flex-wrap gap-2">
            {resume.skills.map((skill, idx) => (
              <span key={idx} className="px-4 py-2 bg-blue-100 text-blue-800 rounded-lg text-sm font-medium">
                {skill.name}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  )

  const renderGradientSidebar = () => (
    <div className="bg-white shadow-lg flex" style={{ width: '210mm', minHeight: '297mm', margin: '0 auto' }}>
      {/* Sidebar */}
      <div className="w-1/3 bg-gradient-to-b from-slate-800 via-slate-900 to-gray-900 text-white p-6">
        <div className="mb-6">
          <h1 className="text-2xl font-bold mb-2">{resume.personal_info?.full_name || 'Your Name'}</h1>
          <div className="text-slate-300 text-xs space-y-1">
            <div>{resume.personal_info?.email}</div>
            <div>{resume.personal_info?.phone}</div>
            <div>{resume.personal_info?.location}</div>
          </div>
        </div>

        {resume.skills && resume.skills.length > 0 && (
          <div className="mb-6">
            <h2 className="text-lg font-bold mb-3 border-b border-slate-600 pb-2">SKILLS</h2>
            <div className="space-y-2">
              {resume.skills.map((skill, idx) => (
                <div key={idx}>
                  <div className="text-sm mb-1">{skill.name}</div>
                  <div className="w-full bg-slate-950 rounded-full h-2">
                    <div 
                      className="bg-white rounded-full h-2"
                      style={{ width: skill.level === 'Expert' ? '95%' : skill.level === 'Advanced' ? '85%' : skill.level === 'Intermediate' ? '70%' : '60%' }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {resume.education && resume.education.length > 0 && (
          <div>
            <h2 className="text-lg font-bold mb-3 border-b border-slate-600 pb-2">EDUCATION</h2>
            {resume.education.map((edu, idx) => (
              <div key={idx} className="mb-3 text-sm">
                <div className="font-bold">{edu.degree}</div>
                <div className="text-slate-300">{edu.institution}</div>
                <div className="text-slate-400 text-xs">{edu.start_date} - {edu.end_date || 'Present'}</div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Main Content */}
      <div className="w-2/3 p-8">
        {resume.personal_info?.summary && (
          <div className="mb-6">
            <h2 className="text-xl font-bold text-slate-800 mb-3">PROFILE</h2>
            <p className="text-gray-700 text-sm">{resume.personal_info.summary}</p>
          </div>
        )}

        {resume.experience && resume.experience.length > 0 && (
          <div>
            <h2 className="text-xl font-bold text-slate-800 mb-4">EXPERIENCE</h2>
            {resume.experience.map((exp, idx) => (
              <div key={idx} className="mb-4">
                <div className="flex justify-between mb-1">
                  <h3 className="font-bold text-gray-900">{exp.position}</h3>
                  <span className="text-sm text-gray-600">{exp.start_date} - {exp.current ? 'Present' : exp.end_date}</span>
                </div>
                <p className="text-gray-700 font-medium mb-1">{exp.company}</p>
                <p className="text-sm text-gray-600">{exp.description}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )

  const renderMinimalistTwoColumn = () => (
    <div className="bg-white p-8 shadow-lg" style={{ width: '210mm', minHeight: '297mm', margin: '0 auto' }}>
      {/* Header */}
      <div className="text-center border-b-2 border-gray-800 pb-4 mb-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">{resume.personal_info?.full_name || 'Your Name'}</h1>
        <div className="text-sm text-gray-600 space-x-3">
          <span>{resume.personal_info?.email}</span>
          <span>|</span>
          <span>{resume.personal_info?.phone}</span>
          <span>|</span>
          <span>{resume.personal_info?.location}</span>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-8">
        {/* Left Column */}
        <div className="col-span-1 space-y-6">
          {resume.skills && resume.skills.length > 0 && (
            <div>
              <h2 className="text-sm font-bold text-gray-900 mb-3 uppercase tracking-wider border-b border-gray-300 pb-1">Skills</h2>
              <div className="space-y-1">
                {resume.skills.map((skill, idx) => (
                  <div key={idx} className="text-sm text-gray-700">{skill.name}</div>
                ))}
              </div>
            </div>
          )}

          {resume.education && resume.education.length > 0 && (
            <div>
              <h2 className="text-sm font-bold text-gray-900 mb-3 uppercase tracking-wider border-b border-gray-300 pb-1">Education</h2>
              {resume.education.map((edu, idx) => (
                <div key={idx} className="mb-3 text-sm">
                  <div className="font-semibold text-gray-900">{edu.degree}</div>
                  <div className="text-gray-700">{edu.institution}</div>
                  <div className="text-gray-500 text-xs">{edu.start_date?.substring(0, 4)} - {edu.end_date?.substring(0, 4) || 'Present'}</div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Right Column */}
        <div className="col-span-2 space-y-6">
          {resume.personal_info?.summary && (
            <div>
              <h2 className="text-sm font-bold text-gray-900 mb-3 uppercase tracking-wider border-b border-gray-300 pb-1">Summary</h2>
              <p className="text-sm text-gray-700">{resume.personal_info.summary}</p>
            </div>
          )}

          {resume.experience && resume.experience.length > 0 && (
            <div>
              <h2 className="text-sm font-bold text-gray-900 mb-3 uppercase tracking-wider border-b border-gray-300 pb-1">Experience</h2>
              {resume.experience.map((exp, idx) => (
                <div key={idx} className="mb-4">
                  <div className="flex justify-between mb-1">
                    <h3 className="font-semibold text-gray-900">{exp.position}</h3>
                    <span className="text-xs text-gray-500">{exp.start_date} - {exp.current ? 'Present' : exp.end_date}</span>
                  </div>
                  <p className="text-sm text-gray-700 mb-1">{exp.company}</p>
                  <p className="text-sm text-gray-600">{exp.description}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )

  const templates: Record<string, () => JSX.Element> = {
    'professional-blue': renderProfessionalBlue,
    'linkedin-style': renderLinkedInStyle,
    'gradient-sidebar': renderGradientSidebar,
    'minimalist-two-column': renderMinimalistTwoColumn
  }

  const renderTemplate = templates[template] || renderProfessionalBlue

  return (
    <div className="bg-gray-100 p-4 overflow-auto" style={{ height: 'calc(100vh - 180px)' }}>
      {renderTemplate()}
    </div>
  )
}
