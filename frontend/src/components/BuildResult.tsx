'use client'

interface BuildResultProps {
  build: {
    build_type: string
    items: Array<{
      item_id: number
      name: string
      level: number
      slot: string
      rarity: number
      is_epic: boolean
      is_relic: boolean
      difficulty: number
      stats: { [key: string]: number }
    }>
    total_stats: { [key: string]: number }
    total_difficulty: number
    num_items: number
  }
}

const RARITY_COLORS: { [key: number]: string } = {
  0: 'text-gray-600',      // Common
  1: 'text-blue-600',      // Unusual
  2: 'text-purple-600',    // Rare
  3: 'text-pink-600',      // Mythical
  4: 'text-yellow-600',    // Legendary
  5: 'text-orange-600',    // Relic
  6: 'text-teal-600',      // Souvenir
  7: 'text-red-600',       // Epic
}

const RARITY_NAMES: { [key: number]: string } = {
  0: 'Common',
  1: 'Unusual',
  2: 'Rare',
  3: 'Mythical',
  4: 'Legendary',
  5: 'Relic',
  6: 'Souvenir',
  7: 'Epic',
}

const BUILD_TYPE_COLORS: { [key: string]: string } = {
  easy: 'bg-green-100 border-green-300 text-green-800',
  medium: 'bg-yellow-100 border-yellow-300 text-yellow-800',
  hard: 'bg-red-100 border-red-300 text-red-800',
}

const BUILD_TYPE_ICONS: { [key: string]: string } = {
  easy: '🌱',
  medium: '⚡',
  hard: '🔥',
}

export default function BuildResult({ build }: BuildResultProps) {
  const buildTypeClass =
    BUILD_TYPE_COLORS[build.build_type] || BUILD_TYPE_COLORS.medium

  return (
    <div className={`card border-2 ${buildTypeClass}`}>
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-2xl font-bold capitalize flex items-center gap-2">
          {BUILD_TYPE_ICONS[build.build_type]} {build.build_type} Build
        </h3>
        <div className="text-right">
          <div className="text-sm text-gray-600">Average Difficulty</div>
          <div className="text-2xl font-bold">
            {build.total_difficulty.toFixed(1)}/100
          </div>
        </div>
      </div>

      {/* Total Stats */}
      <div className="mb-6 p-4 bg-gray-50 rounded-lg">
        <h4 className="font-semibold text-gray-700 mb-3">Total Stats</h4>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {Object.entries(build.total_stats).map(([statName, statValue]) => (
            <div
              key={statName}
              className="bg-white p-2 rounded shadow-sm text-center"
            >
              <div className="text-xs text-gray-600">
                {statName.replace(/_/g, ' ')}
              </div>
              <div className="text-lg font-bold text-wakfu-primary">
                {statValue}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Items */}
      <div>
        <h4 className="font-semibold text-gray-700 mb-3">
          Equipment ({build.num_items} items)
        </h4>
        <div className="space-y-2">
          {build.items.map((item) => (
            <div
              key={item.item_id}
              className="bg-gray-50 p-4 rounded-lg hover:bg-gray-100 transition-colors"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    <h5
                      className={`font-semibold ${
                        RARITY_COLORS[item.rarity] || 'text-gray-800'
                      }`}
                    >
                      {item.name}
                    </h5>
                    {item.is_epic && (
                      <span className="px-2 py-0.5 bg-red-100 text-red-700 text-xs font-semibold rounded">
                        EPIC
                      </span>
                    )}
                    {item.is_relic && (
                      <span className="px-2 py-0.5 bg-orange-100 text-orange-700 text-xs font-semibold rounded">
                        RELIC
                      </span>
                    )}
                  </div>
                  <div className="text-sm text-gray-600 mt-1">
                    Level {item.level} • {item.slot.replace(/_/g, ' ')} •{' '}
                    {RARITY_NAMES[item.rarity] || 'Unknown'}
                  </div>
                  {Object.keys(item.stats).length > 0 && (
                    <div className="mt-2 flex flex-wrap gap-2">
                      {Object.entries(item.stats).map(([stat, value]) => (
                        <span
                          key={stat}
                          className="text-xs bg-white px-2 py-1 rounded shadow-sm"
                        >
                          {stat.replace(/_/g, ' ')}: +{value}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
                <div className="text-right ml-4">
                  <div className="text-xs text-gray-600">Difficulty</div>
                  <div className="text-lg font-semibold text-gray-800">
                    {item.difficulty.toFixed(1)}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

