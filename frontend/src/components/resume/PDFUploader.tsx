import { useState, useRef } from 'react'
import { Upload, FileText, X, Loader } from 'lucide-react'
import { API_BASE_URL } from '../../services/api'
import type { Resume } from '../../types'

interface Props {
  onDataExtracted: (data: Partial<Resume>) => void
  onClose: () => void
}

export default function PDFUploader({ onDataExtracted, onClose }: Props) {
  const [uploading, setUploading] = useState(false)
  const [dragActive, setDragActive] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleFile = async (file: File) => {
    if (!file.type.includes('pdf')) {
      alert('Please upload a PDF file')
      return
    }

    if (file.size > 10 * 1024 * 1024) {
      alert('File size must be less than 10MB')
      return
    }

    setUploading(true)
    try {
      const formData = new FormData()
      formData.append('file', file)

      const response = await fetch(`${API_BASE_URL}/api/resumes/parse-pdf`, {
        method: 'POST',
        body: formData
      })

      if (!response.ok) {
        throw new Error('Failed to parse PDF')
      }

      const result = await response.json()
      if (result.success) {
        onDataExtracted(result.data)
        onClose()
      } else {
        throw new Error('Failed to extract data from PDF')
      }
    } catch (error) {
      console.error('PDF upload failed:', error)
      alert('Failed to parse PDF. Please try again or enter data manually.')
    } finally {
      setUploading(false)
    }
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    setDragActive(false)
    
    const files = Array.from(e.dataTransfer.files)
    if (files.length > 0) {
      handleFile(files[0])
    }
  }

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files
    if (files && files.length > 0) {
      handleFile(files[0])
    }
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-md mx-4">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-semibold text-gray-900">Import Resume</h3>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600"
          >
            <X size={20} />
          </button>
        </div>

        <div className="mb-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
          <h4 className="font-medium text-blue-900 mb-2">💡 LinkedIn Import</h4>
          <p className="text-sm text-blue-800 mb-2">
            To import from LinkedIn:
          </p>
          <ol className="text-sm text-blue-800 space-y-1 ml-4">
            <li>1. Go to your LinkedIn profile</li>
            <li>2. Click "More" → "Save to PDF"</li>
            <li>3. Upload the downloaded PDF here</li>
          </ol>
        </div>

        <div
          className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
            dragActive 
              ? 'border-emerald-500 bg-emerald-50' 
              : 'border-gray-300 hover:border-gray-400'
          }`}
          onDragOver={(e) => {
            e.preventDefault()
            setDragActive(true)
          }}
          onDragLeave={() => setDragActive(false)}
          onDrop={handleDrop}
        >
          {uploading ? (
            <div className="flex flex-col items-center">
              <Loader className="animate-spin text-emerald-600 mb-2" size={32} />
              <p className="text-gray-600">Parsing your resume...</p>
            </div>
          ) : (
            <div className="flex flex-col items-center">
              <div className="flex items-center justify-center w-12 h-12 bg-gray-100 rounded-lg mb-3">
                <FileText className="text-gray-600" size={24} />
              </div>
              <p className="text-gray-900 font-medium mb-1">
                Drop your PDF here or click to browse
              </p>
              <p className="text-sm text-gray-500 mb-4">
                We'll extract your information automatically
              </p>
              <button
                onClick={() => fileInputRef.current?.click()}
                className="flex items-center gap-2 px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700"
              >
                <Upload size={16} />
                Choose File
              </button>
            </div>
          )}
        </div>

        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf"
          onChange={handleFileSelect}
          className="hidden"
        />

        <div className="mt-4 text-xs text-gray-500">
          <p>• Only PDF files are supported</p>
          <p>• Maximum file size: 10MB</p>
          <p>• We'll extract personal info, experience, education, and skills</p>
        </div>
      </div>
    </div>
  )
}
