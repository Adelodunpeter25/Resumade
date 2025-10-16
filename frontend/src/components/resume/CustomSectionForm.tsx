import { useState } from 'react'
import { Plus, Trash2, Edit2, Check, X } from 'lucide-react'
import type { CustomSectionItem } from '../../types'

interface Props {
  sectionName: string
  items: CustomSectionItem[]
  onChange: (items: CustomSectionItem[]) => void
}

export default function CustomSectionForm({ sectionName, items, onChange }: Props) {
  const [editingItem, setEditingItem] = useState<string | null>(null)
  const [newItem, setNewItem] = useState<Partial<CustomSectionItem>>({})

  const addItem = () => {
    if (!newItem.title?.trim()) return
    
    const item: CustomSectionItem = {
      id: `item_${Date.now()}`,
      title: newItem.title.trim(),
      description: newItem.description?.trim() || '',
      date: newItem.date?.trim() || '',
      location: newItem.location?.trim() || ''
    }
    
    onChange([...items, item])
    setNewItem({})
  }

  const updateItem = (id: string, updates: Partial<CustomSectionItem>) => {
    const updatedItems = items.map(item =>
      item.id === id ? { ...item, ...updates } : item
    )
    onChange(updatedItems)
  }

  const deleteItem = (id: string) => {
    onChange(items.filter(item => item.id !== id))
  }

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold text-gray-900">{sectionName}</h3>
      
      {/* Existing Items */}
      <div className="space-y-3">
        {items.map((item) => (
          <div key={item.id} className="border border-gray-200 rounded-lg p-4">
            {editingItem === item.id ? (
              <div className="space-y-3">
                <input
                  type="text"
                  value={item.title}
                  onChange={(e) => updateItem(item.id, { title: e.target.value })}
                  placeholder="Title"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                />
                <div className="grid grid-cols-2 gap-3">
                  <input
                    type="text"
                    value={item.date || ''}
                    onChange={(e) => updateItem(item.id, { date: e.target.value })}
                    placeholder="Date (e.g., 2023)"
                    className="px-3 py-2 border border-gray-300 rounded-lg"
                  />
                  <input
                    type="text"
                    value={item.location || ''}
                    onChange={(e) => updateItem(item.id, { location: e.target.value })}
                    placeholder="Location (optional)"
                    className="px-3 py-2 border border-gray-300 rounded-lg"
                  />
                </div>
                <textarea
                  value={item.description || ''}
                  onChange={(e) => updateItem(item.id, { description: e.target.value })}
                  placeholder="Description (optional)"
                  rows={3}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                />
                <div className="flex gap-2">
                  <button
                    onClick={() => setEditingItem(null)}
                    className="flex items-center gap-2 px-3 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700"
                  >
                    <Check size={16} />
                    Save
                  </button>
                  <button
                    onClick={() => setEditingItem(null)}
                    className="flex items-center gap-2 px-3 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
                  >
                    <X size={16} />
                    Cancel
                  </button>
                </div>
              </div>
            ) : (
              <div>
                <div className="flex justify-between items-start mb-2">
                  <h4 className="font-medium text-gray-900">{item.title}</h4>
                  <div className="flex gap-1">
                    <button
                      onClick={() => setEditingItem(item.id)}
                      className="p-1 text-gray-600 hover:bg-gray-100 rounded"
                    >
                      <Edit2 size={16} />
                    </button>
                    <button
                      onClick={() => deleteItem(item.id)}
                      className="p-1 text-red-600 hover:bg-red-50 rounded"
                    >
                      <Trash2 size={16} />
                    </button>
                  </div>
                </div>
                {(item.date || item.location) && (
                  <div className="text-sm text-gray-600 mb-2">
                    {item.date} {item.date && item.location && '•'} {item.location}
                  </div>
                )}
                {item.description && (
                  <p className="text-gray-700 text-sm">{item.description}</p>
                )}
              </div>
            )}
          </div>
        ))}
      </div>
      
      {/* Add New Item */}
      <div className="border-2 border-dashed border-gray-300 rounded-lg p-4">
        <div className="space-y-3">
          <input
            type="text"
            value={newItem.title || ''}
            onChange={(e) => setNewItem({ ...newItem, title: e.target.value })}
            placeholder="Title"
            className="w-full px-3 py-2 border border-gray-300 rounded-lg"
          />
          <div className="grid grid-cols-2 gap-3">
            <input
              type="text"
              value={newItem.date || ''}
              onChange={(e) => setNewItem({ ...newItem, date: e.target.value })}
              placeholder="Date (e.g., 2023)"
              className="px-3 py-2 border border-gray-300 rounded-lg"
            />
            <input
              type="text"
              value={newItem.location || ''}
              onChange={(e) => setNewItem({ ...newItem, location: e.target.value })}
              placeholder="Location (optional)"
              className="px-3 py-2 border border-gray-300 rounded-lg"
            />
          </div>
          <textarea
            value={newItem.description || ''}
            onChange={(e) => setNewItem({ ...newItem, description: e.target.value })}
            placeholder="Description (optional)"
            rows={3}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg"
          />
          <button
            onClick={addItem}
            disabled={!newItem.title?.trim()}
            className="flex items-center gap-2 px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Plus size={16} />
            Add {sectionName} Item
          </button>
        </div>
      </div>
    </div>
  )
}
