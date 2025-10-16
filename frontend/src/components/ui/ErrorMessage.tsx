import { AlertCircle, X } from 'lucide-react'

interface Props {
  message: string
  onClose?: () => void
}

export default function ErrorMessage({ message, onClose }: Props) {
  if (!message) return null

  return (
    <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-start gap-3">
      <AlertCircle className="text-red-600 flex-shrink-0 mt-0.5" size={20} />
      <p className="text-red-800 text-sm flex-1">{message}</p>
      {onClose && (
        <button onClick={onClose} className="text-red-600 hover:text-red-800">
          <X size={18} />
        </button>
      )}
    </div>
  )
}
