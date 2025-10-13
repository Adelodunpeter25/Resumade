import { useState } from 'react'
import { Plus, Edit2, Trash2, GripVertical, Check, X } from 'lucide-react'
import type { Resume } from '../../types'

interface Section {
  id: string
  name: string
  type: 'default' | 'custom'
  component?: string
  data?: any[]
}

interface Props {
  resume: Partial<Resume>
  onChange: (field: string, value: any) => void
}

const defaultSections: Section[] = [
  { id: 'personal', name: 'Personal Details', type: 'default', component: 'PersonalInfoForm' },
  { id: 'summary', name: 'Professional Summary', type: 'default' },
  { id: 'experience', name: 'Work Experience', type: 'default', component: 'ExperienceForm', data: [] },
  { id: 'education', name: 'Education', type: 'default', component: 'EducationForm', data: [] },
  { id: 'skills', name: 'Skills', type: 'default', component: 'SkillsForm', data: [] },
  { id: 'languages', name: 'Languages', type: 'default', data: [] },
  { id: 'certifications', name: 'Certifications', type: 'default', component: 'CertificationsForm', data: [] },
  { id: 'links', name: 'Links / Websites', type: 'default', data: [] },
  { id: 'interests', name: 'Interests', type: 'default', data: [] }
]

export default function SectionManager({ resume, onChange }: Props) {
  const [sections, setSections] = useState<Section[]>(() => {
    if (!resume) return defaultSections
    
    const customSections = resume.custom_sections || []
    const sectionNames = resume.section_names || {}
    
    return defaultSections.map(section => ({
      ...section,
      name: sectionNames[section.id] || section.name
    })).concat(customSections.map((custom: any) => ({
      id: custom.id,
      name: custom.name,
      type: 'custom' as const,
      data: custom.data || []
    })))
  })
  
  const [editingSection, setEditingSection] = useState<string | null>(null)
  const [editName, setEditName] = useState('')
  const [newSectionName, setNewSectionName] = useState('')

  const updateSections = (newSections: Section[]) => {
    setSections(newSections)
    
    // Update resume data
    const sectionNames: Record<string, string> = {}
    const customSections: any[] = []
    
    newSections.forEach(section => {
      if (section.type === 'default') {
        const defaultSection = defaultSections.find(d => d.id === section.id)
        if (defaultSection && section.name !== defaultSection.name) {
          sectionNames[section.id] = section.name
        }
      } else {
        customSections.push({
          id: section.id,
          name: section.name,
          data: section.data || []
        })
      }
    })
    
    onChange('section_names', sectionNames)
    onChange('custom_sections', customSections)
  }

  const startEditing = (sectionId: string, currentName: string) => {
    setEditingSection(sectionId)
    setEditName(currentName)
  }

  const saveEdit = () => {
    if (!editingSection || !editName.trim()) return
    
    const newSections = sections.map(section =>
      section.id === editingSection
        ? { ...section, name: editName.trim() }
        : section
    )
    
    updateSections(newSections)
    setEditingSection(null)
    setEditName('')
  }

  const cancelEdit = () => {
    setEditingSection(null)
    setEditName('')
  }

  const addCustomSection = () => {
    if (!newSectionName.trim()) return
    
    const newSection: Section = {
      id: `custom_${Date.now()}`,
      name: newSectionName.trim(),
      type: 'custom',
      data: []
    }
    
    updateSections([...sections, newSection])
    setNewSectionName('')
  }

  const deleteSection = (sectionId: string) => {
    const newSections = sections.filter(section => section.id !== sectionId)
    updateSections(newSections)
  }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Manage Sections</h3>
      
      {/* Section List */}
      <div className="space-y-2 mb-6">
        {sections.map((section) => (
          <div
            key={section.id}
            className="flex items-center gap-3 p-3 border border-gray-200 rounded-lg hover:bg-gray-50"
          >
            <GripVertical 
              size={16} 
              className="text-gray-400 cursor-move"
            />
            
            {editingSection === section.id ? (
              <div className="flex-1 flex items-center gap-2">
                <input
                  type="text"
                  value={editName}
                  onChange={(e) => setEditName(e.target.value)}
                  className="flex-1 px-2 py-1 border border-gray-300 rounded text-sm"
                  autoFocus
                  onKeyDown={(e) => {
                    if (e.key === 'Enter') saveEdit()
                    if (e.key === 'Escape') cancelEdit()
                  }}
                />
                <button
                  onClick={saveEdit}
                  className="p-1 text-emerald-600 hover:bg-emerald-50 rounded"
                >
                  <Check size={16} />
                </button>
                <button
                  onClick={cancelEdit}
                  className="p-1 text-red-600 hover:bg-red-50 rounded"
                >
                  <X size={16} />
                </button>
              </div>
            ) : (
              <>
                <div className="flex-1">
                  <span className="font-medium text-gray-900">{section.name}</span>
                  <span className="ml-2 text-xs text-gray-500">
                    ({section.type === 'default' ? 'Default' : 'Custom'})
                  </span>
                </div>
                
                <button
                  onClick={() => startEditing(section.id, section.name)}
                  className="p-1 text-gray-600 hover:bg-gray-100 rounded"
                  title="Rename section"
                >
                  <Edit2 size={16} />
                </button>
                
                {section.type === 'custom' && (
                  <button
                    onClick={() => deleteSection(section.id)}
                    className="p-1 text-red-600 hover:bg-red-50 rounded"
                    title="Delete section"
                  >
                    <Trash2 size={16} />
                  </button>
                )}
              </>
            )}
          </div>
        ))}
      </div>
      
      {/* Add Custom Section */}
      <div className="border-t border-gray-200 pt-4">
        <h4 className="font-medium text-gray-900 mb-3">Add Custom Section</h4>
        <div className="flex gap-2">
          <input
            type="text"
            value={newSectionName}
            onChange={(e) => setNewSectionName(e.target.value)}
            placeholder="Section name (e.g., Awards, Publications)"
            className="flex-1 px-3 py-2 border border-gray-300 rounded-lg text-sm"
            onKeyDown={(e) => {
              if (e.key === 'Enter') addCustomSection()
            }}
          />
          <button
            onClick={addCustomSection}
            disabled={!newSectionName.trim()}
            className="flex items-center gap-2 px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Plus size={16} />
            Add
          </button>
        </div>
      </div>
    </div>
  )
}
