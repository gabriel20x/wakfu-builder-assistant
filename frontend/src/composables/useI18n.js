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
    
    // Navigation
    'nav.myBuilds': 'Mis Builds',
    'nav.builder': 'Build Generator',
    'nav.metadata': 'Metadatos de Items',
    
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
    'config.onlyDroppable': 'Solo Items Dropeables',
    'config.onlyDroppableHint': '(solo items que se obtienen de monstruos)',
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
    
    // Build Management
    'builds.saveBuild': 'Guardar Build',
    'builds.loadBuild': 'Cargar Build',
    'builds.manageBuilds': 'Gestionar Builds',
    'builds.savedBuilds': 'Builds Guardadas',
    'builds.history': 'Historial',
    'builds.saved': 'Guardadas',
    'builds.load': 'Cargar',
    'builds.delete': 'Eliminar',
    'builds.enterBuildName': 'Nombre para esta build',
    'builds.buildSaved': 'Build Guardada',
    'builds.buildLoaded': 'Build Cargada',
    'builds.historyBuild': 'Build del historial',
    'builds.noSavedBuilds': 'No hay builds guardadas',
    'builds.noHistory': 'No hay historial de builds',
    'builds.deleteConfirm': '¿Eliminar esta build?',
    
    // My Builds View
    'myBuilds.title': 'Mis Builds Guardadas',
    'myBuilds.createNew': 'Crear Nueva',
    'myBuilds.loading': 'Cargando builds...',
    'myBuilds.noBuildsSaved': 'No tienes builds guardadas',
    'myBuilds.startByCreating': 'Comienza creando tu primera build en el generador',
    'myBuilds.goToBuilder': 'Ir al Generador',
    'myBuilds.unnamedBuild': 'Build sin nombre',
    'myBuilds.selectBuild': 'Selecciona una build',
    'myBuilds.selectBuildDescription': 'Elige una build del sidebar para ver sus detalles',
    'myBuilds.loadInBuilder': 'Cargar en Generador',
    'myBuilds.rename': 'Renombrar',
    'myBuilds.renameBuild': 'Renombrar Build',
    'myBuilds.buildName': 'Nombre de la Build',
    'myBuilds.enterBuildName': 'Ingresa un nombre',
    'myBuilds.deleteBuild': 'Eliminar Build',
    'myBuilds.deleteConfirmation': '¿Estás seguro de que quieres eliminar esta build?',
    'myBuilds.buildDeleted': 'Build eliminada correctamente',
    'myBuilds.buildRenamed': 'Build renombrada correctamente',
    'myBuilds.loadedInBuilder': 'Build cargada en el generador',
    'myBuilds.errorLoading': 'Error al cargar las builds',
    'myBuilds.errorDeleting': 'Error al eliminar la build',
    'myBuilds.errorRenaming': 'Error al renombrar la build',
    'myBuilds.justNow': 'Ahora mismo',
    'myBuilds.minutesAgo': 'hace {count} minutos',
    'myBuilds.hoursAgo': 'hace {count} horas',
    'myBuilds.daysAgo': 'hace {count} días',
    
    // Common
    'common.cancel': 'Cancelar',
    'common.save': 'Guardar',
    'common.delete': 'Eliminar',
    'common.edit': 'Editar',
    'common.close': 'Cerrar',
    'common.confirm': 'Confirmar',
    'common.yes': 'Sí',
    'common.no': 'No',
    
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
    'toast.presetError': 'No se pudo aplicar el preset',
    
    // Item Metadata Admin
    'metadata.title': 'Administrador de Metadatos de Items',
    'metadata.description': 'Agrega información extra a los items (drop rates, recetas, etc.) que no está disponible en los datos del juego',
    
    // Ignored Items
    'ignoredItems.title': 'Items Ignorados',
    'ignoredItems.description': 'Items que no se incluirán en futuras búsquedas',
    'ignoredItems.empty': 'No hay items ignorados',
    'ignoredItems.emptyHelp': 'Haz clic en el botón de prohibir (🚫) en cualquier item para ignorarlo',
    'ignoredItems.ignore': 'Ignorar item',
    'ignoredItems.unignore': 'Permitir item',
    'ignoredItems.restore': 'Restaurar',
    'ignoredItems.ignoredAt': 'Ignorado',
    'ignoredItems.clearAll': 'Limpiar Todo',
    'ignoredItems.confirmClearAll': '¿Estás seguro de que quieres eliminar todos los items ignorados?',
    'ignoredItems.cleared': 'Lista Limpiada',
    'ignoredItems.clearedDetail': 'Todos los items han sido restaurados',
    'ignoredItems.restored': 'Item Restaurado',
    'ignoredItems.restoredDetail': 'El item ahora aparecerá en las búsquedas',
    'ignoredItems.export': 'Exportar',
    'ignoredItems.import': 'Importar',
    'ignoredItems.exported': 'Exportado',
    'ignoredItems.exportedDetail': 'Lista de items ignorados descargada',
    'ignoredItems.imported': 'Importado',
    'ignoredItems.importedDetail': 'Lista de items ignorados cargada',
    'ignoredItems.exportError': 'Error al exportar',
    'ignoredItems.importError': 'Error al importar',
    'metadata.totalItems': 'Items con Metadatos',
    'metadata.coverage': 'Cobertura de Metadatos',
    'metadata.editMetadata': 'Editar Metadatos',
    'metadata.hasMetadata': 'Info',
    'metadata.withDropRate': 'Con Drop Rate',
    'metadata.withCraftable': 'Con Flag Crafteable',
    'metadata.withCorrection': 'Con Corrección de Origen',
    'metadata.withRelicFragments': 'Con Info de Fragmentos',
    'metadata.search': 'Buscar',
    'metadata.searching': 'Buscando...',
    'metadata.searchPlaceholder': 'Buscar items por nombre...',
    'metadata.searchMinLength': 'Por favor ingresa al menos 2 caracteres',
    'metadata.searchError': 'Error al buscar items',
    'metadata.results': 'Resultados',
    'metadata.hasMetadata': 'Tiene metadatos',
    'metadata.editTitle': 'Editar Metadatos',
    'metadata.itemId': 'ID del Item',
    'metadata.itemName': 'Nombre',
    'metadata.currentSource': 'Origen Actual',
    'metadata.correctedSource': 'Corrección de Origen',
    'metadata.noCorrection': 'Sin corrección',
    'metadata.dropRate': 'Drop Rate',
    'metadata.dropRatePlaceholder': 'ej: 2.5',
    'metadata.isCraftable': '¿Es Crafteable?',
    'metadata.unknown': 'Desconocido',
    'metadata.yes': 'Sí',
    'metadata.no': 'No',
    'metadata.isObtainable': '¿Es Obtenible?',
    'metadata.difficultyOverride': 'Override de Dificultad',
    'metadata.difficultyPlaceholder': 'ej: 15.5',
    'metadata.sourceNotes': 'Notas sobre el Origen',
    'metadata.notesPlaceholder': 'ej: Se obtiene del boss Nox con 2% drop rate...',
    'metadata.addedBy': 'Agregado por',
    'metadata.addedByPlaceholder': 'Tu nombre o username',
    'metadata.save': 'Guardar',
    'metadata.saving': 'Guardando...',
    'metadata.delete': 'Eliminar',
    'metadata.cancel': 'Cancelar',
    'metadata.source': 'Origen',
    'metadata.saveSuccess': 'Metadatos guardados exitosamente',
    'metadata.saveError': 'Error al guardar metadatos',
    'metadata.deleteConfirm': '¿Estás seguro de eliminar estos metadatos?',
    'metadata.deleteSuccess': 'Metadatos eliminados exitosamente',
    'metadata.deleteError': 'Error al eliminar metadatos',
    
    // Acquisition Methods
    'metadata.acquisitionMethodsTitle': '📦 Métodos de Obtención',
    'metadata.acquisitionMethodsSubtitle': 'Marca todos los métodos por los que se puede obtener este item',
    'metadata.generalSettings': 'Configuración General',
    'metadata.methodDrop': 'Drop de Mobs/Bosses',
    'metadata.methodRecipe': 'Receta / Crafteo',
    'metadata.methodFragments': 'Fragmentos de Reliquia',
    'metadata.methodCrupier': 'Crupier (Monedas)',
    'metadata.methodChallengeReward': 'Recompensa de Reto',
    'metadata.methodQuest': 'Misión / Quest',
    'metadata.methodOther': 'Otro Método',
    
    // Drop Method
    'metadata.dropSourcesList': 'Fuentes de Drop',
    'metadata.dropSourcesDetected': 'Drops detectados automáticamente',
    'metadata.monsterIdLabel': 'Monstruo',
    'metadata.monsterIdFallback': 'Monstruo #{id}',
    'metadata.addRate': 'Agregar %',
    'metadata.fragmentRatePlaceholder': 'ej: 8.12',
    'metadata.notes': 'Notas Generales',
    
    // Recipe Method
    'metadata.recipeInfo': 'Este item se obtiene mediante crafteo/receta',
    'metadata.ingredients': 'ingredientes',
    
    // Fragments Method
    'metadata.fragmentItemId': 'ID del Fragmento',
    'metadata.fragmentItemIdPlaceholder': 'ej: 12345',
    'metadata.fragmentName': 'Nombre del Fragmento',
    'metadata.fragmentNamePlaceholder': 'ej: Fragmento de Ortiz',
    'metadata.fragmentsRequired': 'Fragmentos Requeridos',
    'metadata.fragmentDropSources': 'Fuentes de Drop de Fragmentos',
    'metadata.sourceName': 'Nombre de la fuente',
    'metadata.addSource': 'Agregar Fuente',
    
    // Crupier Method
    'metadata.currencyItemId': 'ID de la Moneda',
    'metadata.currencyItemIdPlaceholder': 'ej: 54321',
    'metadata.currencyName': 'Nombre de la Moneda',
    'metadata.currencyNamePlaceholder': 'ej: Ficha preciosa',
    'metadata.currencyAmount': 'Cantidad de Monedas',
    'metadata.currencyAmountPlaceholder': 'ej: 50',
    'metadata.crupierNotes': 'Notas sobre Crupier',
    'metadata.crupierNotesPlaceholder': 'ej: Se canjea en cualquier crupier de mazmorras...',
    
    // Challenge/Reward Method
    'metadata.challengeType': 'Tipo de Reto',
    'metadata.challengeTypePlaceholder': 'ej: Reto de mazmorra, Reto diario...',
    'metadata.challengeNotes': 'Notas sobre el Reto',
    'metadata.challengeNotesPlaceholder': 'ej: Recompensa por completar todos los retos de...',
    
    // Quest Method
    'metadata.questName': 'Nombre de la Misión',
    'metadata.questNamePlaceholder': 'ej: La búsqueda del tesoro perdido',
    'metadata.questNotes': 'Notas sobre la Misión',
    'metadata.questNotesPlaceholder': 'ej: Recompensa final de la cadena de misiones...',
    
    // Other Method
    'metadata.otherMethodName': 'Nombre del Método',
    'metadata.otherMethodNamePlaceholder': 'ej: Evento especial, Compra directa...',
    'metadata.otherNotes': 'Notas',
    'metadata.otherNotesPlaceholder': 'ej: Solo disponible durante eventos de temporada...',
    
    // Rarity names
    'rarity.common': 'Común',
    'rarity.unusual': 'Inusual',
    'rarity.rare': 'Raro',
    'rarity.mythic': 'Mítico',
    'rarity.legendary': 'Legendario',
    'rarity.relic': 'Reliquia',
    'rarity.epic': 'Épico'
  },
  en: {
    // Header
    'app.title': 'Wakfu Builder Assistant',
    'app.subtitle': 'Generate optimized equipment builds for your character',
    'language': 'Language',
    
    // Navigation
    'nav.builder': 'Build Generator',
    'nav.metadata': 'Item Metadata',
    
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
    'config.onlyDroppable': 'Only Droppable Items',
    'config.onlyDroppableHint': '(only items dropped by monsters)',
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
    
    // Build Management
    'builds.saveBuild': 'Save Build',
    'builds.manageBuilds': 'Manage Builds',
    'builds.savedBuilds': 'Saved Builds',
    'builds.history': 'History',
    'builds.saved': 'Saved',
    'builds.load': 'Load',
    'builds.delete': 'Delete',
    'builds.enterBuildName': 'Name for this build',
    'builds.buildSaved': 'Build Saved',
    'builds.buildLoaded': 'Build Loaded',
    'builds.historyBuild': 'Build from history',
    'builds.noSavedBuilds': 'No saved builds',
    'builds.noHistory': 'No build history',
    'builds.deleteConfirm': 'Delete this build?',
    
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
    'toast.presetError': 'Could not apply preset',
    
    // Item Metadata Admin
    'metadata.title': 'Item Metadata Administrator',
    'metadata.description': 'Add extra information to items (drop rates, recipes, etc.) not available in game data',
    'metadata.totalItems': 'Items with Metadata',
    'metadata.coverage': 'Metadata Coverage',
    'metadata.editMetadata': 'Edit Metadata',
    'metadata.hasMetadata': 'Info',
    'metadata.withDropRate': 'With Drop Rate',
    'metadata.withCraftable': 'With Craftable Flag',
    'metadata.withCorrection': 'With Source Correction',
    'metadata.withRelicFragments': 'With Fragment Info',
    'metadata.search': 'Search',
    'metadata.searching': 'Searching...',
    'metadata.searchPlaceholder': 'Search items by name...',
    'metadata.searchMinLength': 'Please enter at least 2 characters',
    'metadata.searchError': 'Error searching items',
    'metadata.results': 'Results',
    'metadata.hasMetadata': 'Has metadata',
    'metadata.editTitle': 'Edit Metadata',
    'metadata.itemId': 'Item ID',
    'metadata.itemName': 'Name',
    'metadata.currentSource': 'Current Source',
    'metadata.correctedSource': 'Source Correction',
    'metadata.noCorrection': 'No correction',
    'metadata.dropRate': 'Drop Rate',
    'metadata.dropRatePlaceholder': 'e.g: 2.5',
    'metadata.isCraftable': 'Is Craftable?',
    'metadata.unknown': 'Unknown',
    'metadata.yes': 'Yes',
    'metadata.no': 'No',
    'metadata.isObtainable': 'Is Obtainable?',
    'metadata.difficultyOverride': 'Difficulty Override',
    'metadata.difficultyPlaceholder': 'e.g: 15.5',
    'metadata.sourceNotes': 'Source Notes',
    'metadata.notesPlaceholder': 'e.g: Obtained from Nox boss with 2% drop rate...',
    'metadata.addedBy': 'Added by',
    'metadata.addedByPlaceholder': 'Your name or username',
    'metadata.save': 'Save',
    'metadata.saving': 'Saving...',
    'metadata.delete': 'Delete',
    'metadata.cancel': 'Cancel',
    'metadata.source': 'Source',
    'metadata.saveSuccess': 'Metadata saved successfully',
    'metadata.saveError': 'Error saving metadata',
    'metadata.deleteConfirm': 'Are you sure you want to delete this metadata?',
    'metadata.deleteSuccess': 'Metadata deleted successfully',
    'metadata.deleteError': 'Error deleting metadata',
    
    // Acquisition Methods
    'metadata.acquisitionMethodsTitle': '📦 Acquisition Methods',
    'metadata.acquisitionMethodsSubtitle': 'Check all methods by which this item can be obtained',
    'metadata.generalSettings': 'General Settings',
    'metadata.methodDrop': 'Drop from Mobs/Bosses',
    'metadata.methodRecipe': 'Recipe / Crafting',
    'metadata.methodFragments': 'Relic Fragments',
    'metadata.methodCrupier': 'Crupier (Currency)',
    'metadata.methodChallengeReward': 'Challenge Reward',
    'metadata.methodQuest': 'Quest / Mission',
    'metadata.methodOther': 'Other Method',
    
    // Drop Method
    'metadata.dropSourcesList': 'Drop Sources',
    'metadata.dropSourcesDetected': 'Auto-detected Drops',
    'metadata.monsterIdLabel': 'Monster',
    'metadata.monsterIdFallback': 'Monster #{id}',
    'metadata.addRate': 'Add %',
    'metadata.fragmentRatePlaceholder': 'e.g: 8.12',
    'metadata.notes': 'General Notes',
    
    // Recipe Method
    'metadata.recipeInfo': 'This item is obtained through crafting/recipe',
    'metadata.ingredients': 'ingredients',
    
    // Fragments Method
    'metadata.fragmentItemId': 'Fragment ID',
    'metadata.fragmentItemIdPlaceholder': 'e.g: 12345',
    'metadata.fragmentName': 'Fragment Name',
    'metadata.fragmentNamePlaceholder': 'e.g: Ortiz Fragment',
    'metadata.fragmentsRequired': 'Fragments Required',
    'metadata.fragmentDropSources': 'Fragment Drop Sources',
    'metadata.sourceName': 'Source name',
    'metadata.addSource': 'Add Source',
    
    // Crupier Method
    'metadata.currencyItemId': 'Currency ID',
    'metadata.currencyItemIdPlaceholder': 'e.g: 54321',
    'metadata.currencyName': 'Currency Name',
    'metadata.currencyNamePlaceholder': 'e.g: Precious Token',
    'metadata.currencyAmount': 'Currency Amount',
    'metadata.currencyAmountPlaceholder': 'e.g: 50',
    'metadata.crupierNotes': 'Crupier Notes',
    'metadata.crupierNotesPlaceholder': 'e.g: Exchange at any dungeon crupier...',
    
    // Challenge/Reward Method
    'metadata.challengeType': 'Challenge Type',
    'metadata.challengeTypePlaceholder': 'e.g: Dungeon challenge, Daily challenge...',
    'metadata.challengeNotes': 'Challenge Notes',
    'metadata.challengeNotesPlaceholder': 'e.g: Reward for completing all challenges of...',
    
    // Quest Method
    'metadata.questName': 'Quest Name',
    'metadata.questNamePlaceholder': 'e.g: The Lost Treasure Hunt',
    'metadata.questNotes': 'Quest Notes',
    'metadata.questNotesPlaceholder': 'e.g: Final reward of the quest chain...',
    
    // Other Method
    'metadata.otherMethodName': 'Method Name',
    'metadata.otherMethodNamePlaceholder': 'e.g: Special event, Direct purchase...',
    'metadata.otherNotes': 'Notes',
    'metadata.otherNotesPlaceholder': 'e.g: Only available during seasonal events...',
    
    // Rarity names
    'rarity.common': 'Common',
    'rarity.unusual': 'Unusual',
    'rarity.rare': 'Rare',
    'rarity.mythic': 'Mythic',
    'rarity.legendary': 'Legendary',
    'rarity.relic': 'Relic',
    'rarity.epic': 'Epic'
  },
  fr: {
    // Header
    'app.title': 'Wakfu Builder Assistant',
    'app.subtitle': 'Générez des builds d\'équipement optimisés pour votre personnage',
    'language': 'Langue',
    
    // Navigation
    'nav.builder': 'Générateur de Build',
    'nav.metadata': 'Métadonnées d\'Items',
    
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
    'config.onlyDroppable': 'Seulement Items Dropables',
    'config.onlyDroppableHint': '(seulement les items obtenus de monstres)',
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
    
    // Build Management
    'builds.saveBuild': 'Sauvegarder Build',
    'builds.manageBuilds': 'Gérer les Builds',
    'builds.savedBuilds': 'Builds Sauvegardées',
    'builds.history': 'Historique',
    'builds.saved': 'Sauvegardées',
    'builds.load': 'Charger',
    'builds.delete': 'Supprimer',
    'builds.enterBuildName': 'Nom pour ce build',
    'builds.buildSaved': 'Build Sauvegardé',
    'builds.buildLoaded': 'Build Chargé',
    'builds.historyBuild': 'Build de l\'historique',
    'builds.noSavedBuilds': 'Aucun build sauvegardé',
    'builds.noHistory': 'Aucun historique de builds',
    'builds.deleteConfirm': 'Supprimer ce build?',
    
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
    'toast.presetError': 'Impossible d\'appliquer le preset',
    
    // Item Metadata Admin
    'metadata.title': 'Administrateur de Métadonnées d\'Items',
    'metadata.description': 'Ajoutez des informations supplémentaires aux items (taux de drop, recettes, etc.) non disponibles dans les données du jeu',
    'metadata.totalItems': 'Items avec Métadonnées',
    'metadata.coverage': 'Couverture de Métadonnées',
    'metadata.editMetadata': 'Modifier les Métadonnées',
    'metadata.hasMetadata': 'Info',
    'metadata.withDropRate': 'Avec Taux de Drop',
    'metadata.withCraftable': 'Avec Flag Craftable',
    'metadata.withCorrection': 'Avec Correction de Source',
    'metadata.withRelicFragments': 'Avec Info de Fragments',
    'metadata.search': 'Rechercher',
    'metadata.searching': 'Recherche...',
    'metadata.searchPlaceholder': 'Rechercher des items par nom...',
    'metadata.searchMinLength': 'Veuillez entrer au moins 2 caractères',
    'metadata.searchError': 'Erreur lors de la recherche d\'items',
    'metadata.results': 'Résultats',
    'metadata.hasMetadata': 'A des métadonnées',
    'metadata.editTitle': 'Modifier les Métadonnées',
    'metadata.itemId': 'ID de l\'Item',
    'metadata.itemName': 'Nom',
    'metadata.currentSource': 'Source Actuelle',
    'metadata.correctedSource': 'Correction de Source',
    'metadata.noCorrection': 'Sans correction',
    'metadata.dropRate': 'Taux de Drop',
    'metadata.dropRatePlaceholder': 'ex: 2.5',
    'metadata.isCraftable': 'Est Craftable?',
    'metadata.unknown': 'Inconnu',
    'metadata.yes': 'Oui',
    'metadata.no': 'Non',
    'metadata.isObtainable': 'Est Obtenable?',
    'metadata.difficultyOverride': 'Override de Difficulté',
    'metadata.difficultyPlaceholder': 'ex: 15.5',
    'metadata.sourceNotes': 'Notes sur la Source',
    'metadata.notesPlaceholder': 'ex: Obtenu du boss Nox avec 2% de taux de drop...',
    'metadata.addedBy': 'Ajouté par',
    'metadata.addedByPlaceholder': 'Votre nom ou username',
    'metadata.save': 'Sauvegarder',
    'metadata.saving': 'Sauvegarde...',
    'metadata.delete': 'Supprimer',
    'metadata.cancel': 'Annuler',
    'metadata.source': 'Source',
    'metadata.saveSuccess': 'Métadonnées sauvegardées avec succès',
    'metadata.saveError': 'Erreur lors de la sauvegarde des métadonnées',
    'metadata.deleteConfirm': 'Êtes-vous sûr de vouloir supprimer ces métadonnées?',
    'metadata.deleteSuccess': 'Métadonnées supprimées avec succès',
    'metadata.deleteError': 'Erreur lors de la suppression des métadonnées',
    
    // Acquisition Methods
    'metadata.acquisitionMethodsTitle': '📦 Méthodes d\'Acquisition',
    'metadata.acquisitionMethodsSubtitle': 'Cochez toutes les méthodes par lesquelles cet item peut être obtenu',
    'metadata.generalSettings': 'Paramètres Généraux',
    'metadata.methodDrop': 'Drop de Mobs/Boss',
    'metadata.methodRecipe': 'Recette / Craft',
    'metadata.methodFragments': 'Fragments de Relique',
    'metadata.methodCrupier': 'Crupier (Monnaie)',
    'metadata.methodChallengeReward': 'Récompense de Défi',
    'metadata.methodQuest': 'Quête / Mission',
    'metadata.methodOther': 'Autre Méthode',
    
    // Drop Method
    'metadata.dropSourcesList': 'Sources de Drop',
    'metadata.dropSourcesDetected': 'Drops détectés automatiquement',
    'metadata.monsterIdLabel': 'Monstre',
    'metadata.monsterIdFallback': 'Monstre #{id}',
    'metadata.addRate': 'Ajouter %',
    'metadata.fragmentRatePlaceholder': 'ex: 8.12',
    'metadata.notes': 'Notes Générales',
    
    // Recipe Method
    'metadata.recipeInfo': 'Cet item est obtenu par craft/recette',
    'metadata.ingredients': 'ingrédients',
    
    // Fragments Method
    'metadata.fragmentItemId': 'ID du Fragment',
    'metadata.fragmentItemIdPlaceholder': 'ex: 12345',
    'metadata.fragmentName': 'Nom du Fragment',
    'metadata.fragmentNamePlaceholder': 'ex: Fragment d\'Ortiz',
    'metadata.fragmentsRequired': 'Fragments Requis',
    'metadata.fragmentDropSources': 'Sources de Drop de Fragments',
    'metadata.sourceName': 'Nom de la source',
    'metadata.addSource': 'Ajouter une Source',
    
    // Crupier Method
    'metadata.currencyItemId': 'ID de la Monnaie',
    'metadata.currencyItemIdPlaceholder': 'ex: 54321',
    'metadata.currencyName': 'Nom de la Monnaie',
    'metadata.currencyNamePlaceholder': 'ex: Jeton précieux',
    'metadata.currencyAmount': 'Quantité de Monnaie',
    'metadata.currencyAmountPlaceholder': 'ex: 50',
    'metadata.crupierNotes': 'Notes sur Crupier',
    'metadata.crupierNotesPlaceholder': 'ex: Échangeable chez n\'importe quel crupier de donjon...',
    
    // Challenge/Reward Method
    'metadata.challengeType': 'Type de Défi',
    'metadata.challengeTypePlaceholder': 'ex: Défi de donjon, Défi quotidien...',
    'metadata.challengeNotes': 'Notes sur le Défi',
    'metadata.challengeNotesPlaceholder': 'ex: Récompense pour avoir complété tous les défis de...',
    
    // Quest Method
    'metadata.questName': 'Nom de la Quête',
    'metadata.questNamePlaceholder': 'ex: La quête du trésor perdu',
    'metadata.questNotes': 'Notes sur la Quête',
    'metadata.questNotesPlaceholder': 'ex: Récompense finale de la chaîne de quêtes...',
    
    // Other Method
    'metadata.otherMethodName': 'Nom de la Méthode',
    'metadata.otherMethodNamePlaceholder': 'ex: Événement spécial, Achat direct...',
    'metadata.otherNotes': 'Notes',
    'metadata.otherNotesPlaceholder': 'ex: Disponible uniquement pendant les événements saisonniers...',
    
    // Rarity names
    'rarity.common': 'Commun',
    'rarity.unusual': 'Inhabituel',
    'rarity.rare': 'Rare',
    'rarity.mythic': 'Mythique',
    'rarity.legendary': 'Légendaire',
    'rarity.relic': 'Relique',
    'rarity.epic': 'Épique'
  }
}

export function useI18n() {
  const t = (key, params = {}) => {
    const lang = currentLanguage.value
    let text = translations[lang]?.[key] || translations['en']?.[key] || key
    
    // Replace parameters like {count}, {name}, etc.
    if (params && typeof text === 'string') {
      Object.keys(params).forEach(param => {
        text = text.replace(new RegExp(`\\{${param}\\}`, 'g'), params[param])
      })
    }
    
    return text
  }
  
  return { t }
}

