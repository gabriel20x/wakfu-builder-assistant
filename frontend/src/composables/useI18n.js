import { ref } from 'vue'
import { useLanguage } from './useLanguage'

const { currentLanguage } = useLanguage()

// UI Translations
const translations = {
  es: {
    // Header
    'app.title': 'Wakfu Builder Assistant',
    'app.subtitle': 'Genera builds optimizados de equipo para tu personaje',
    'language': 'Idioma',
    
    // Config Panel
    'config.title': 'Configuración del Build',
    'config.characterLevel': 'Nivel Máximo del Personaje',
    'config.statPriority': 'Prioridad de Stats',
    'config.statPriorityHelp': 'Marca los stats que quieres priorizar',
    'config.selectAll': 'Todos',
    'config.selectNone': 'Ninguno',
    'config.advancedOptions': 'Opciones Avanzadas',
    'config.advancedHelp': 'Items difíciles de conseguir',
    'config.includePet': 'Incluir Mascotas',
    'config.includePetHint': '(pueden ser difíciles de conseguir)',
    'config.includeEmblem': 'Incluir Emblemas',
    'config.includeEmblemHint': '(pueden ser difíciles de conseguir)',
    'config.generateButton': 'Generar Builds',
    'config.generating': 'Generando...',
    
    // Stat Categories
    'stats.main': 'Características',
    'stats.masteries': 'Dominios y Resistencias',
    'stats.combat': 'Combate',
    'stats.secondary': 'Secundarias',
    
    // Quick Start
    'quickStart.title': 'Quick Start - Presets por Clase',
    'quickStart.help': 'Selecciona tu clase y rol para autoconfigurar',
    'quickStart.class': 'Clase',
    'quickStart.role': 'Rol / Build',
    'quickStart.selectClass': 'Selecciona tu clase',
    'quickStart.selectRole': 'Selecciona rol',
    'quickStart.applyPreset': 'Aplicar Preset',
    'quickStart.applying': 'Aplicando...',
    'quickStart.previewTitle': 'Stats Principales (Top 6)',
    'quickStart.primary': 'Principal',
    
    // Element Preferences
    'elements.title': 'Preferencias de Elementos',
    'elements.damagePrefs': 'Elementos de Daño',
    'elements.damageHelp': 'Prioridad para stats de dominio elemental',
    'elements.resistancePrefs': 'Elementos de Resistencia',
    'elements.resistanceHelp': 'Prioridad para stats de resistencia elemental',
    
    // Results Panel
    'results.title': 'Items de la Build',
    'results.loading': 'Generando builds optimizados...',
    'results.emptyTitle': '¿Listo para comenzar?',
    'results.emptyText': 'Configura las prioridades de stats y haz clic en "Generar Builds"',
    'results.emptyHelp': 'El sistema generará 5 builds optimizados con diferentes niveles de dificultad de obtención',
    
    // Build Types
    'builds.easy': 'Fácil',
    'builds.medium': 'Medio',
    'builds.hardEpic': 'Difícil (Épico)',
    'builds.hardRelic': 'Difícil (Reliquia)',
    'builds.full': 'Completo',
    'builds.difficulty': 'Dificultad',
    
    // Stats Panel
    'statsPanel.title': 'Stats Totales',
    'statsPanel.equipmentOnly': 'Solo Equipo',
    'statsPanel.withBase': 'Con Stats Base',
    
    // Toast Messages
    'toast.buildsGenerated': 'Builds Generados',
    'toast.buildsGeneratedDetail': 'builds optimizados creados',
    'toast.statsSelected': 'stats priorizados',
    'toast.noStatsSelected': 'No hay stats seleccionados',
    'toast.noStatsSelectedDetail': 'Por favor marca al menos un stat para priorizar',
    'toast.error': 'Error',
    'toast.errorGenerating': 'Error al generar builds. Por favor intenta de nuevo.',
    'toast.presetApplied': 'Preset Aplicado',
    'toast.presetError': 'No se pudo aplicar el preset'
  },
  en: {
    // Header
    'app.title': 'Wakfu Builder Assistant',
    'app.subtitle': 'Generate optimized equipment builds for your character',
    'language': 'Language',
    
    // Config Panel
    'config.title': 'Build Configuration',
    'config.characterLevel': 'Max Character Level',
    'config.statPriority': 'Stat Priority',
    'config.statPriorityHelp': 'Check the stats you want to prioritize',
    'config.selectAll': 'All',
    'config.selectNone': 'None',
    'config.advancedOptions': 'Advanced Options',
    'config.advancedHelp': 'Hard-to-get items',
    'config.includePet': 'Include Pets',
    'config.includePetHint': '(may be hard to obtain)',
    'config.includeEmblem': 'Include Emblems',
    'config.includeEmblemHint': '(may be hard to obtain)',
    'config.generateButton': 'Generate Builds',
    'config.generating': 'Generating...',
    
    // Stat Categories
    'stats.main': 'Main Stats',
    'stats.masteries': 'Masteries & Resistances',
    'stats.combat': 'Combat',
    'stats.secondary': 'Secondary',
    
    // Quick Start
    'quickStart.title': 'Quick Start - Class Presets',
    'quickStart.help': 'Select your class and role to auto-configure',
    'quickStart.class': 'Class',
    'quickStart.role': 'Role / Build',
    'quickStart.selectClass': 'Select your class',
    'quickStart.selectRole': 'Select role',
    'quickStart.applyPreset': 'Apply Preset',
    'quickStart.applying': 'Applying...',
    'quickStart.previewTitle': 'Main Stats (Top 6)',
    'quickStart.primary': 'Primary',
    
    // Element Preferences
    'elements.title': 'Element Preferences',
    'elements.damagePrefs': 'Damage Elements',
    'elements.damageHelp': 'Priority for elemental mastery stats',
    'elements.resistancePrefs': 'Resistance Elements',
    'elements.resistanceHelp': 'Priority for elemental resistance stats',
    
    // Results Panel
    'results.title': 'Build Items',
    'results.loading': 'Generating optimized builds...',
    'results.emptyTitle': 'Ready to begin?',
    'results.emptyText': 'Configure stat priorities and click "Generate Builds"',
    'results.emptyHelp': 'The system will generate 5 optimized builds with different difficulty levels',
    
    // Build Types
    'builds.easy': 'Easy',
    'builds.medium': 'Medium',
    'builds.hardEpic': 'Hard (Epic)',
    'builds.hardRelic': 'Hard (Relic)',
    'builds.full': 'Complete',
    'builds.difficulty': 'Difficulty',
    
    // Stats Panel
    'statsPanel.title': 'Total Stats',
    'statsPanel.equipmentOnly': 'Equipment Only',
    'statsPanel.withBase': 'With Base Stats',
    
    // Toast Messages
    'toast.buildsGenerated': 'Builds Generated',
    'toast.buildsGeneratedDetail': 'optimized builds created',
    'toast.statsSelected': 'stats prioritized',
    'toast.noStatsSelected': 'No stats selected',
    'toast.noStatsSelectedDetail': 'Please check at least one stat to prioritize',
    'toast.error': 'Error',
    'toast.errorGenerating': 'Error generating builds. Please try again.',
    'toast.presetApplied': 'Preset Applied',
    'toast.presetError': 'Could not apply preset'
  },
  fr: {
    // Header
    'app.title': 'Wakfu Builder Assistant',
    'app.subtitle': 'Générez des builds d\'équipement optimisés pour votre personnage',
    'language': 'Langue',
    
    // Config Panel
    'config.title': 'Configuration du Build',
    'config.characterLevel': 'Niveau Max du Personnage',
    'config.statPriority': 'Priorité des Stats',
    'config.statPriorityHelp': 'Cochez les stats que vous voulez prioriser',
    'config.selectAll': 'Tous',
    'config.selectNone': 'Aucun',
    'config.advancedOptions': 'Options Avancées',
    'config.advancedHelp': 'Items difficiles à obtenir',
    'config.includePet': 'Inclure les Familiers',
    'config.includePetHint': '(peuvent être difficiles à obtenir)',
    'config.includeEmblem': 'Inclure les Emblèmes',
    'config.includeEmblemHint': '(peuvent être difficiles à obtenir)',
    'config.generateButton': 'Générer Builds',
    'config.generating': 'Génération...',
    
    // Stat Categories
    'stats.main': 'Caractéristiques',
    'stats.masteries': 'Maîtrises & Résistances',
    'stats.combat': 'Combat',
    'stats.secondary': 'Secondaires',
    
    // Quick Start
    'quickStart.title': 'Quick Start - Presets par Classe',
    'quickStart.help': 'Sélectionnez votre classe et rôle pour auto-configurer',
    'quickStart.class': 'Classe',
    'quickStart.role': 'Rôle / Build',
    'quickStart.selectClass': 'Sélectionnez votre classe',
    'quickStart.selectRole': 'Sélectionnez le rôle',
    'quickStart.applyPreset': 'Appliquer le Preset',
    'quickStart.applying': 'Application...',
    'quickStart.previewTitle': 'Stats Principales (Top 6)',
    'quickStart.primary': 'Principal',
    
    // Element Preferences
    'elements.title': 'Préférences d\'Éléments',
    'elements.damagePrefs': 'Éléments de Dégâts',
    'elements.damageHelp': 'Priorité pour les stats de maîtrise élémentaire',
    'elements.resistancePrefs': 'Éléments de Résistance',
    'elements.resistanceHelp': 'Priorité pour les stats de résistance élémentaire',
    
    // Results Panel
    'results.title': 'Items du Build',
    'results.loading': 'Génération de builds optimisés...',
    'results.emptyTitle': 'Prêt à commencer?',
    'results.emptyText': 'Configurez les priorités de stats et cliquez sur "Générer Builds"',
    'results.emptyHelp': 'Le système générera 5 builds optimisés avec différents niveaux de difficulté',
    
    // Build Types
    'builds.easy': 'Facile',
    'builds.medium': 'Moyen',
    'builds.hardEpic': 'Difficile (Épique)',
    'builds.hardRelic': 'Difficile (Relique)',
    'builds.full': 'Complet',
    'builds.difficulty': 'Difficulté',
    
    // Stats Panel
    'statsPanel.title': 'Stats Totales',
    'statsPanel.equipmentOnly': 'Équipement Seul',
    'statsPanel.withBase': 'Avec Stats de Base',
    
    // Toast Messages
    'toast.buildsGenerated': 'Builds Générés',
    'toast.buildsGeneratedDetail': 'builds optimisés créés',
    'toast.statsSelected': 'stats priorisés',
    'toast.noStatsSelected': 'Aucun stat sélectionné',
    'toast.noStatsSelectedDetail': 'Veuillez cocher au moins un stat à prioriser',
    'toast.error': 'Erreur',
    'toast.errorGenerating': 'Erreur lors de la génération des builds. Veuillez réessayer.',
    'toast.presetApplied': 'Preset Appliqué',
    'toast.presetError': 'Impossible d\'appliquer le preset'
  }
}

export function useI18n() {
  const t = (key) => {
    const lang = currentLanguage.value
    return translations[lang]?.[key] || translations['en']?.[key] || key
  }
  
  return { t }
}

