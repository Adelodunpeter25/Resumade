import { memo } from 'react'
import { Plus, Trash2, X } from 'lucide-react'
import { useState } from 'react'
import type { Resume, Project } from '../../types'
import RichTextEditor from '../common/RichTextEditor'

interface Props {
  data: Partial<Resume>
  onChange: (field: string, value: any) => void
}

function ProjectsForm({ data, onChange }: Props) {
  const projects = data.projects || []
  const [techInput, setTechInput] = useState<{ [key: number]: string }>({})

  const addProject = () => {
    onChange('projects', [...projects, {
      name: '',
      description: '',
      technologies: [],
      url: ''
    }])
  }

  const updateProject = (index: number, field: keyof Project, value: any) => {
    const updated = [...projects]
    updated[index] = { ...updated[index], [field]: value }
    onChange('projects', updated)
  }

  const removeProject = (index: number) => {
    onChange('projects', projects.filter((_, i) => i !== index))
  }

  const addTechnology = (index: number) => {
    const tech = techInput[index]?.trim()
    if (tech) {
      const updated = [...projects]
      updated[index] = {
        ...updated[index],
        technologies: [...updated[index].technologies, tech]
      }
      onChange('projects', updated)
      setTechInput({ ...techInput, [index]: '' })
    }
  }

  const removeTechnology = (projectIndex: number, techIndex: number) => {
    const updated = [...projects]
    updated[projectIndex] = {
      ...updated[projectIndex],
      technologies: updated[projectIndex].technologies.filter((_, i) => i !== techIndex)
    }
    onChange('projects', updated)
  }

  return (
    <div className="space-y-6">
      {projects.map((project, index) => (
        <div key={index} className="border border-gray-200 rounded-lg p-6 relative">
          <button
            onClick={() => removeProject(index)}
            className="absolute top-4 right-4 p-2 text-red-600 hover:bg-red-50 rounded-lg"
          >
            <Trash2 size={20} />
          </button>

          <div className="grid grid-cols-2 gap-4 mb-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Project Name *
              </label>
              <input
                type="text"
                value={project.name}
                onChange={(e) => updateProject(index, 'name', e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Project URL
              </label>
              <input
                type="url"
                value={project.url || ''}
                onChange={(e) => updateProject(index, 'url', e.target.value)}
                placeholder="https://github.com/username/project"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
              />
            </div>
          </div>

          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Description *
            </label>
            <RichTextEditor
              value={project.description}
              onChange={(value) => updateProject(index, 'description', value)}
              placeholder="Describe the project and your role..."
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Technologies
            </label>
            <div className="flex gap-2 mb-2">
              <input
                type="text"
                value={techInput[index] || ''}
                onChange={(e) => setTechInput({ ...techInput, [index]: e.target.value })}
                onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addTechnology(index))}
                placeholder="e.g., React, Node.js"
                className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
              />
              <button
                type="button"
                onClick={() => addTechnology(index)}
                className="px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700"
              >
                Add
              </button>
            </div>
            <div className="flex flex-wrap gap-2">
              {project.technologies.map((tech, techIndex) => (
                <span
                  key={techIndex}
                  className="inline-flex items-center gap-1 px-3 py-1 bg-emerald-100 text-emerald-700 rounded-full text-sm"
                >
                  {tech}
                  <button
                    type="button"
                    onClick={() => removeTechnology(index, techIndex)}
                    className="hover:text-emerald-900"
                  >
                    <X size={14} />
                  </button>
                </span>
              ))}
            </div>
          </div>
        </div>
      ))}

      <button
        onClick={addProject}
        className="w-full flex items-center justify-center gap-2 px-4 py-3 border-2 border-dashed border-gray-300 rounded-lg hover:border-emerald-500 hover:bg-emerald-50 text-gray-600 hover:text-emerald-600"
      >
        <Plus size={20} />
        <span>Add Project</span>
      </button>
    </div>
  )
}

export default memo(ProjectsForm)
