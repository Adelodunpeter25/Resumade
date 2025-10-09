import { Plus, Trash2 } from 'lucide-react'
import type { Resume, Certification } from '../../types'

interface Props {
  data: Partial<Resume>
  onChange: (field: string, value: any) => void
}

export default function CertificationsForm({ data, onChange }: Props) {
  const certifications = data.certifications || []

  const addCertification = () => {
    onChange('certifications', [...certifications, {
      name: '',
      issuer: '',
      date: '',
      credential_id: ''
    }])
  }

  const updateCertification = (index: number, field: keyof Certification, value: any) => {
    const updated = [...certifications]
    updated[index] = { ...updated[index], [field]: value }
    onChange('certifications', updated)
  }

  const removeCertification = (index: number) => {
    onChange('certifications', certifications.filter((_, i) => i !== index))
  }

  return (
    <div className="space-y-6">
      {certifications.map((cert, index) => (
        <div key={index} className="border border-gray-200 rounded-lg p-6 relative">
          <button
            onClick={() => removeCertification(index)}
            className="absolute top-4 right-4 p-2 text-red-600 hover:bg-red-50 rounded-lg"
          >
            <Trash2 size={20} />
          </button>

          <div className="grid grid-cols-2 gap-4 mb-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Certification Name *
              </label>
              <input
                type="text"
                value={cert.name}
                onChange={(e) => updateCertification(index, 'name', e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Issuing Organization *
              </label>
              <input
                type="text"
                value={cert.issuer}
                onChange={(e) => updateCertification(index, 'issuer', e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
                required
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Issue Date *
              </label>
              <input
                type="month"
                value={cert.date}
                onChange={(e) => updateCertification(index, 'date', e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Credential ID
              </label>
              <input
                type="text"
                value={cert.credential_id || ''}
                onChange={(e) => updateCertification(index, 'credential_id', e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
              />
            </div>
          </div>
        </div>
      ))}

      <button
        onClick={addCertification}
        className="w-full flex items-center justify-center gap-2 px-4 py-3 border-2 border-dashed border-gray-300 rounded-lg hover:border-emerald-500 hover:bg-emerald-50 text-gray-600 hover:text-emerald-600"
      >
        <Plus size={20} />
        <span>Add Certification</span>
      </button>
    </div>
  )
}
