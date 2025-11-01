'use client'

import { useState } from 'react'

interface FormStatsProps {
  onSubmit: (params: any) => void
  loading: boolean
}

const AVAILABLE_STATS = [
  { key: 'HP', label: 'Health Points (HP)', defaultWeight: 1.0 },
  { key: 'AP', label: 'Action Points (AP)', defaultWeight: 2.5 },
  { key: 'MP', label: 'Movement Points (MP)', defaultWeight: 2.0 },
  { key: 'Critical_Hit', label: 'Critical Hit', defaultWeight: 1.5 },
  { key: 'Damage_Inflicted', label: 'Damage Inflicted', defaultWeight: 1.2 },
  { key: 'Resistance', label: 'Resistance', defaultWeight: 1.0 },
  { key: 'Mastery', label: 'Mastery', defaultWeight: 1.3 },
  { key: 'Lock', label: 'Lock', defaultWeight: 0.8 },
  { key: 'Dodge', label: 'Dodge', defaultWeight: 0.8 },
  { key: 'Initiative', label: 'Initiative', defaultWeight: 0.7 },
  { key: 'Wisdom', label: 'Wisdom', defaultWeight: 1.0 },
  { key: 'Prospecting', label: 'Prospecting', defaultWeight: 0.5 },
]

export default function FormStats({ onSubmit, loading }: FormStatsProps) {
  const [levelMax, setLevelMax] = useState(230)
  const [statWeights, setStatWeights] = useState<{ [key: string]: number }>(
    AVAILABLE_STATS.reduce((acc, stat) => {
      acc[stat.key] = stat.defaultWeight
      return acc
    }, {} as { [key: string]: number })
  )

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSubmit({
      level_max: levelMax,
      stat_weights: statWeights,
    })
  }

  const handleStatChange = (statKey: string, value: number) => {
    setStatWeights({
      ...statWeights,
      [statKey]: value,
    })
  }

  const handleReset = () => {
    setLevelMax(230)
    setStatWeights(
      AVAILABLE_STATS.reduce((acc, stat) => {
        acc[stat.key] = stat.defaultWeight
        return acc
      }, {} as { [key: string]: number })
    )
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Level Max */}
      <div>
        <label className="block text-sm font-semibold text-gray-700 mb-2">
          Maximum Level: {levelMax}
        </label>
        <input
          type="range"
          min="1"
          max="230"
          value={levelMax}
          onChange={(e) => setLevelMax(Number(e.target.value))}
          className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-wakfu-primary"
        />
        <div className="flex justify-between text-xs text-gray-500 mt-1">
          <span>1</span>
          <span>230</span>
        </div>
      </div>

      {/* Stat Weights */}
      <div>
        <h3 className="text-lg font-semibold text-gray-800 mb-4">
          Stat Priorities
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {AVAILABLE_STATS.map((stat) => (
            <div key={stat.key} className="space-y-2">
              <label className="flex justify-between text-sm font-medium text-gray-700">
                <span>{stat.label}</span>
                <span className="text-wakfu-primary font-semibold">
                  {statWeights[stat.key].toFixed(1)}
                </span>
              </label>
              <input
                type="range"
                min="0"
                max="5"
                step="0.1"
                value={statWeights[stat.key]}
                onChange={(e) =>
                  handleStatChange(stat.key, Number(e.target.value))
                }
                className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-wakfu-primary"
              />
              <div className="flex justify-between text-xs text-gray-500">
                <span>0</span>
                <span>5</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Buttons */}
      <div className="flex space-x-4 pt-4">
        <button
          type="submit"
          disabled={loading}
          className="btn-primary flex-1 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? (
            <span className="flex items-center justify-center">
              <svg
                className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                ></circle>
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                ></path>
              </svg>
              Generating Builds...
            </span>
          ) : (
            'Generate Builds'
          )}
        </button>
        <button
          type="button"
          onClick={handleReset}
          className="btn-secondary"
          disabled={loading}
        >
          Reset
        </button>
      </div>
    </form>
  )
}

