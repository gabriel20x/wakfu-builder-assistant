'use client'

import { useState, useEffect } from 'react'

interface DropItem {
  item_id: number
  name: string
  level: number
  slot: string
  rarity: number
  difficulty: number
  manual_drop_difficulty: number | null
}

export default function ManualDropEditor() {
  const [items, setItems] = useState<DropItem[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [filter, setFilter] = useState('')
  const [editingItem, setEditingItem] = useState<number | null>(null)
  const [editValue, setEditValue] = useState<string>('')

  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

  useEffect(() => {
    fetchDropItems()
  }, [])

  const fetchDropItems = async () => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await fetch(
        `${apiUrl}/items?source_type=drop&limit=500`
      )
      
      if (!response.ok) {
        throw new Error('Failed to fetch items')
      }
      
      const data = await response.json()
      setItems(data)
    } catch (err: any) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleUpdate = async (itemId: number, difficulty: number) => {
    try {
      const response = await fetch(`${apiUrl}/items/${itemId}/difficulty`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ difficulty }),
      })
      
      if (!response.ok) {
        throw new Error('Failed to update difficulty')
      }
      
      // Update local state
      setItems(
        items.map((item) =>
          item.item_id === itemId
            ? { ...item, manual_drop_difficulty: difficulty, difficulty }
            : item
        )
      )
      
      setEditingItem(null)
      setEditValue('')
    } catch (err: any) {
      alert(`Error: ${err.message}`)
    }
  }

  const startEditing = (item: DropItem) => {
    setEditingItem(item.item_id)
    setEditValue(
      item.manual_drop_difficulty?.toString() || item.difficulty.toString()
    )
  }

  const cancelEditing = () => {
    setEditingItem(null)
    setEditValue('')
  }

  const submitEdit = (itemId: number) => {
    const value = parseFloat(editValue)
    if (isNaN(value) || value < 0 || value > 100) {
      alert('Please enter a valid difficulty between 0 and 100')
      return
    }
    handleUpdate(itemId, value)
  }

  const filteredItems = items.filter((item) =>
    item.name.toLowerCase().includes(filter.toLowerCase())
  )

  if (loading) {
    return (
      <div className="card text-center py-12">
        <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-wakfu-primary"></div>
        <p className="mt-4 text-gray-600">Loading drop items...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="card">
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
          <strong className="font-bold">Error: </strong>
          <span>{error}</span>
        </div>
      </div>
    )
  }

  return (
    <div className="card">
      <h2 className="text-2xl font-bold mb-6 text-gray-800">
        Manual Drop Difficulty Editor
      </h2>
      
      <p className="text-gray-600 mb-6">
        Update the difficulty rating for items obtained from mob drops. This
        will be used in future build calculations.
      </p>

      {/* Filter */}
      <div className="mb-6">
        <input
          type="text"
          placeholder="Search items by name..."
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className="input"
        />
      </div>

      {/* Items List */}
      <div className="space-y-2 max-h-[600px] overflow-y-auto">
        {filteredItems.length === 0 ? (
          <p className="text-center text-gray-500 py-8">
            No items found matching "{filter}"
          </p>
        ) : (
          filteredItems.map((item) => (
            <div
              key={item.item_id}
              className="bg-gray-50 p-4 rounded-lg flex items-center justify-between hover:bg-gray-100 transition-colors"
            >
              <div className="flex-1">
                <h3 className="font-semibold text-gray-800">{item.name}</h3>
                <p className="text-sm text-gray-600">
                  Level {item.level} • {item.slot.replace(/_/g, ' ')}
                </p>
              </div>

              <div className="flex items-center gap-4">
                {editingItem === item.item_id ? (
                  <>
                    <input
                      type="number"
                      min="0"
                      max="100"
                      step="0.1"
                      value={editValue}
                      onChange={(e) => setEditValue(e.target.value)}
                      className="w-24 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-wakfu-primary"
                      autoFocus
                      onKeyDown={(e) => {
                        if (e.key === 'Enter') {
                          submitEdit(item.item_id)
                        } else if (e.key === 'Escape') {
                          cancelEditing()
                        }
                      }}
                    />
                    <button
                      onClick={() => submitEdit(item.item_id)}
                      className="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors"
                    >
                      Save
                    </button>
                    <button
                      onClick={cancelEditing}
                      className="px-4 py-2 bg-gray-300 text-gray-700 rounded-lg hover:bg-gray-400 transition-colors"
                    >
                      Cancel
                    </button>
                  </>
                ) : (
                  <>
                    <div className="text-right">
                      <div className="text-xs text-gray-600">Difficulty</div>
                      <div className="text-lg font-semibold text-gray-800">
                        {item.difficulty.toFixed(1)}
                      </div>
                      {item.manual_drop_difficulty !== null && (
                        <div className="text-xs text-green-600">
                          (Manual)
                        </div>
                      )}
                    </div>
                    <button
                      onClick={() => startEditing(item)}
                      className="px-4 py-2 bg-wakfu-primary text-white rounded-lg hover:bg-blue-600 transition-colors"
                    >
                      Edit
                    </button>
                  </>
                )}
              </div>
            </div>
          ))
        )}
      </div>

      {/* Summary */}
      <div className="mt-6 pt-6 border-t border-gray-200">
        <p className="text-sm text-gray-600">
          Showing {filteredItems.length} of {items.length} drop items
        </p>
      </div>
    </div>
  )
}

