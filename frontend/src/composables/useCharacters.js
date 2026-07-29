import { ref } from 'vue'

// Personajes del usuario ("Mis PJ"), persistidos en localStorage.
// Cada personaje: { id, name, classId, level, allocation: { [aptitudeId]: puntos }, createdAt, updatedAt }

const STORAGE_KEY = 'wakfu_characters_v1'
const MAX_CHARACTERS = 20

const characters = ref([])

function initializeCharacters() {
  try {
    const stored = localStorage.getItem(STORAGE_KEY)
    if (stored) {
      characters.value = JSON.parse(stored)
    }
  } catch (error) {
    console.error('Error loading characters:', error)
  }
}

function persist() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(characters.value))
  } catch (error) {
    console.error('Error saving characters:', error)
  }
}

export function createCharacter({ name, classId = null, level = 245, allocation = {} } = {}) {
  const now = new Date().toISOString()
  const character = {
    id: Date.now().toString(),
    name: name || `PJ ${characters.value.length + 1}`,
    classId,
    level,
    allocation,
    createdAt: now,
    updatedAt: now
  }
  characters.value.unshift(character)
  if (characters.value.length > MAX_CHARACTERS) {
    characters.value = characters.value.slice(0, MAX_CHARACTERS)
  }
  persist()
  return character
}

export function updateCharacter(id, changes) {
  const character = characters.value.find(c => c.id === id)
  if (!character) return null
  Object.assign(character, changes, { updatedAt: new Date().toISOString() })
  persist()
  return character
}

export function deleteCharacter(id) {
  characters.value = characters.value.filter(c => c.id !== id)
  persist()
}

export function getCharacter(id) {
  return characters.value.find(c => c.id === id) || null
}

initializeCharacters()

export function useCharacters() {
  return {
    characters,
    createCharacter,
    updateCharacter,
    deleteCharacter,
    getCharacter
  }
}
