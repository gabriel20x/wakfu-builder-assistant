'use client'

import { useState } from 'react'
import FormStats from '@/components/FormStats'
import BuildResult from '@/components/BuildResult'
import ManualDropEditor from '@/components/ManualDropEditor'

export default function Home() {
  const [builds, setBuilds] = useState<any>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [activeTab, setActiveTab] = useState<'builder' | 'editor'>('builder')

  const handleSolve = async (params: any) => {
    setLoading(true)
    setError(null)
    
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      const response = await fetch(`${apiUrl}/build/solve`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(params),
      })
      
      if (!response.ok) {
        throw new Error('Failed to generate builds')
      }
      
      const data = await response.json()
      setBuilds(data)
    } catch (err: any) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
          <h1 className="text-3xl font-bold text-wakfu-primary">
            Wakfu Builder Crafter
          </h1>
          <p className="mt-2 text-gray-600">
            Generate optimal equipment builds based on stats and difficulty
          </p>
        </div>
      </header>

      {/* Tabs */}
      <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
        <div className="flex space-x-4 border-b border-gray-200">
          <button
            onClick={() => setActiveTab('builder')}
            className={`pb-4 px-4 font-semibold ${
              activeTab === 'builder'
                ? 'border-b-2 border-wakfu-primary text-wakfu-primary'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            Build Generator
          </button>
          <button
            onClick={() => setActiveTab('editor')}
            className={`pb-4 px-4 font-semibold ${
              activeTab === 'editor'
                ? 'border-b-2 border-wakfu-primary text-wakfu-primary'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            Drop Difficulty Editor
          </button>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        {activeTab === 'builder' ? (
          <div className="space-y-8">
            {/* Form */}
            <div className="card">
              <h2 className="text-2xl font-bold mb-6 text-gray-800">
                Build Parameters
              </h2>
              <FormStats onSubmit={handleSolve} loading={loading} />
            </div>

            {/* Error */}
            {error && (
              <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
                <strong className="font-bold">Error: </strong>
                <span>{error}</span>
              </div>
            )}

            {/* Results */}
            {builds && (
              <div className="space-y-6">
                <h2 className="text-2xl font-bold text-gray-800">
                  Generated Builds
                </h2>
                
                <BuildResult build={builds.easy} />
                <BuildResult build={builds.medium} />
                <BuildResult build={builds.hard} />
              </div>
            )}
          </div>
        ) : (
          <ManualDropEditor />
        )}
      </div>

      {/* Footer */}
      <footer className="mt-16 bg-white border-t border-gray-200">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
          <p className="text-center text-gray-500 text-sm">
            Wakfu Builder Crafter © 2024 - Game data version 1.90.1.43
          </p>
        </div>
      </footer>
    </main>
  )
}

