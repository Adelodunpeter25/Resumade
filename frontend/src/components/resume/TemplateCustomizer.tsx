import { useState } from 'react'
import { Palette, Type, Layout } from 'lucide-react'
import type { Resume } from '../../types'

interface Props {
  data: Partial<Resume>
  onChange: (field: string, value: any) => void
}

const colorPresets = [
  { name: 'Emerald', primary: '#059669', secondary: '#0d9488' },
  { name: 'Blue', primary: '#2563eb', secondary: '#1d4ed8' },
  { name: 'Purple', primary: '#7c3aed', secondary: '#6d28d9' },
  { name: 'Red', primary: '#dc2626', secondary: '#b91c1c' },
  { name: 'Orange', primary: '#ea580c', secondary: '#c2410c' },
  { name: 'Gray', primary: '#374151', secondary: '#4b5563' }
]

const fontOptions = [
  'Inter',
  'Arial',
  'Helvetica',
  'Georgia',
  'Times New Roman',
  'Roboto',
  'Open Sans'
]

export default function TemplateCustomizer({ data, onChange }: Props) {
  const [activeTab, setActiveTab] = useState<'colors' | 'fonts' | 'spacing'>('colors')
  
  const customization = data.customization || {
    primary_color: '#059669',
    secondary_color: '#0d9488',
    font_family: 'Inter',
    font_size: '14',
    line_height: '1.5',
    margin: '0.5'
  }

  const updateCustomization = (field: string, value: string) => {
    onChange('customization', { ...customization, [field]: value })
  }

  const applyColorPreset = (preset: typeof colorPresets[0]) => {
    onChange('customization', {
      ...customization,
      primary_color: preset.primary,
      secondary_color: preset.secondary
    })
  }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Customize Template</h3>
      
      {/* Tabs */}
      <div className="flex space-x-1 mb-6 bg-gray-100 rounded-lg p-1">
        <button
          onClick={() => setActiveTab('colors')}
          className={`flex items-center gap-2 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
            activeTab === 'colors' 
              ? 'bg-white text-gray-900 shadow-sm' 
              : 'text-gray-600 hover:text-gray-900'
          }`}
        >
          <Palette size={16} />
          Colors
        </button>
        <button
          onClick={() => setActiveTab('fonts')}
          className={`flex items-center gap-2 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
            activeTab === 'fonts' 
              ? 'bg-white text-gray-900 shadow-sm' 
              : 'text-gray-600 hover:text-gray-900'
          }`}
        >
          <Type size={16} />
          Typography
        </button>
        <button
          onClick={() => setActiveTab('spacing')}
          className={`flex items-center gap-2 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
            activeTab === 'spacing' 
              ? 'bg-white text-gray-900 shadow-sm' 
              : 'text-gray-600 hover:text-gray-900'
          }`}
        >
          <Layout size={16} />
          Layout
        </button>
      </div>

      {/* Colors Tab */}
      {activeTab === 'colors' && (
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Color Presets
            </label>
            <div className="grid grid-cols-3 gap-2">
              {colorPresets.map((preset) => (
                <button
                  key={preset.name}
                  onClick={() => applyColorPreset(preset)}
                  className="flex items-center gap-2 p-2 border rounded-lg hover:bg-gray-50"
                >
                  <div className="flex">
                    <div 
                      className="w-4 h-4 rounded-l"
                      style={{ backgroundColor: preset.primary }}
                    />
                    <div 
                      className="w-4 h-4 rounded-r"
                      style={{ backgroundColor: preset.secondary }}
                    />
                  </div>
                  <span className="text-sm">{preset.name}</span>
                </button>
              ))}
            </div>
          </div>
          
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Primary Color
              </label>
              <div className="flex items-center gap-2">
                <input
                  type="color"
                  value={customization.primary_color}
                  onChange={(e) => updateCustomization('primary_color', e.target.value)}
                  className="w-10 h-10 rounded border"
                />
                <input
                  type="text"
                  value={customization.primary_color}
                  onChange={(e) => updateCustomization('primary_color', e.target.value)}
                  className="flex-1 px-3 py-2 border rounded-lg text-sm"
                />
              </div>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Secondary Color
              </label>
              <div className="flex items-center gap-2">
                <input
                  type="color"
                  value={customization.secondary_color}
                  onChange={(e) => updateCustomization('secondary_color', e.target.value)}
                  className="w-10 h-10 rounded border"
                />
                <input
                  type="text"
                  value={customization.secondary_color}
                  onChange={(e) => updateCustomization('secondary_color', e.target.value)}
                  className="flex-1 px-3 py-2 border rounded-lg text-sm"
                />
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Typography Tab */}
      {activeTab === 'fonts' && (
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Font Family
            </label>
            <select
              value={customization.font_family}
              onChange={(e) => updateCustomization('font_family', e.target.value)}
              className="w-full px-3 py-2 border rounded-lg"
            >
              {fontOptions.map((font) => (
                <option key={font} value={font} style={{ fontFamily: font }}>
                  {font}
                </option>
              ))}
            </select>
          </div>
          
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Font Size (px)
              </label>
              <input
                type="range"
                min="12"
                max="18"
                value={customization.font_size}
                onChange={(e) => updateCustomization('font_size', e.target.value)}
                className="w-full"
              />
              <div className="text-center text-sm text-gray-600 mt-1">
                {customization.font_size}px
              </div>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Line Height
              </label>
              <input
                type="range"
                min="1.2"
                max="2.0"
                step="0.1"
                value={customization.line_height}
                onChange={(e) => updateCustomization('line_height', e.target.value)}
                className="w-full"
              />
              <div className="text-center text-sm text-gray-600 mt-1">
                {customization.line_height}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Layout Tab */}
      {activeTab === 'spacing' && (
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Page Margins (inches)
            </label>
            <input
              type="range"
              min="0.3"
              max="1.0"
              step="0.1"
              value={customization.margin}
              onChange={(e) => updateCustomization('margin', e.target.value)}
              className="w-full"
            />
            <div className="text-center text-sm text-gray-600 mt-1">
              {customization.margin}"
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
