import { AlertCircle, AlertTriangle, Info, X } from 'lucide-react';

interface Props {
  message: string;
  type: 'error' | 'warning' | 'info';
  visible: boolean;
  onClose: () => void;
}

export default function ErrorNotification({ message, type, visible, onClose }: Props) {
  if (!visible) return null;

  const icons = {
    error: AlertCircle,
    warning: AlertTriangle,
    info: Info
  };

  const colors = {
    error: 'bg-red-50 border-red-200 text-red-800',
    warning: 'bg-yellow-50 border-yellow-200 text-yellow-800',
    info: 'bg-blue-50 border-blue-200 text-blue-800'
  };

  const Icon = icons[type];

  return (
    <div className={`fixed top-4 right-4 z-50 max-w-md p-4 border rounded-lg shadow-lg ${colors[type]} animate-in slide-in-from-right`}>
      <div className="flex items-start gap-3">
        <Icon size={20} className="flex-shrink-0 mt-0.5" />
        <p className="text-sm font-medium flex-1">{message}</p>
        <button
          onClick={onClose}
          className="flex-shrink-0 hover:opacity-70"
        >
          <X size={16} />
        </button>
      </div>
    </div>
  );
}
