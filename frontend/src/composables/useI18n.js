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
    'stats.elementalMasteries': 'Dominios Elementales',
    'stats.elementalResistances': 'Resistencias Elementales',
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
    'elements.damageHelp': 'Prioridad para stats de dominio elemental. Se ordena automáticamente según los pesos de maestría; arrastra para desempatar.',
    'elements.resistancePrefs': 'Elementos de Resistencia',
    'elements.resistanceHelp': 'Prioridad para stats de resistencia elemental. Se ordena automáticamente según los pesos de resistencia; arrastra para desempatar.',
    
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
    'common.loading': 'Cargando...',
    
    // Monster Type Filter
    'monsterTypeFilter.title': 'Filtro por Tipo de Monstruo',
    'monsterTypeFilter.description': 'Selecciona qué tipos de monstruos considerar para los drops',
    'monsterTypeFilter.selectAll': 'Todos',
    'monsterTypeFilter.deselectAll': 'Ninguno',
    'monsterTypeFilter.error': 'Error al cargar tipos',
    
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
    
    // Alternatives Modal
    'alternatives.title': 'Alternativas de Items',
    'alternatives.itemPower': 'Item Power',
    'alternatives.betterAlternatives': 'Alternativas con Menor Power',
    'alternatives.noAlternatives': 'No hay alternativas disponibles para este item en el rango de nivel',
    'alternatives.viewAlternatives': 'Ver alternativas',

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
    'rarity.epic': 'Épico',
    'rarity.souvenir': 'Recuerdo',
    
    // Print
    'print.title': 'Items',
    'print.recommendedItems': 'Items Recomendados',
    'print.slot': 'Slot',
    'print.name': 'Nombre',
    'print.level': 'Nivel',
    'print.rarity': 'Rareza',
    'print.difficulty': 'Dificultad',
    'print.generated': 'Generado',
    'print.noItems': 'No hay items para imprimir',
    
    // Slots
    'slots.head': 'Cabeza',
    'slots.neck': 'Cuello',
    'slots.chest': 'Pecho',
    'slots.legs': 'Piernas',
    'slots.back': 'Espalda',
    'slots.shoulders': 'Hombros',
    'slots.belt': 'Cinturón',
    'slots.weapon': 'Arma',
    'slots.secondWeapon': 'Arma 2',
    'slots.accessory': 'Accesorio',
    'slots.ring': 'Anillo',
    'slots.pet': 'Mascota',
    'slots.mount': 'Montura',
    
    // Stats - Core
    'stat.HP': 'PdV',
    'stat.AP': 'PA',
    'stat.MP': 'PM',
    'stat.WP': 'PW',
    
    // Stats - Elemental Masteries
    'stat.Water_Mastery': 'Maestría Agua',
    'stat.Air_Mastery': 'Maestría Aire',
    'stat.Earth_Mastery': 'Maestría Tierra',
    'stat.Fire_Mastery': 'Maestría Fuego',
    'stat.Elemental_Mastery': 'Maestría Elemental',
    
    // Stats - Multi-Element Mastery
    'stat.Multi_Element_Mastery_1': 'Dominio (1 elemento)',
    'stat.Multi_Element_Mastery_2': 'Dominio (2 elementos)',
    'stat.Multi_Element_Mastery_3': 'Dominio (3 elementos)',
    'stat.Multi_Element_Mastery_4': 'Dominio (4 elementos)',
    'stat.Elemental_Mastery_1_elements': 'Maestría (1 elemento)',
    'stat.Elemental_Mastery_2_elements': 'Maestría (2 elementos)',
    'stat.Elemental_Mastery_3_elements': 'Maestría (3 elementos)',
    'stat.Elemental_Mastery_4_elements': 'Maestría (4 elementos)',
    'stat.Random_Elemental_Mastery': 'Maestría Elemental Aleatoria',
    
    // Stats - Position Masteries
    'stat.Critical_Mastery': 'Dominio Crítico',
    'stat.Rear_Mastery': 'Dominio Espalda',
    'stat.Melee_Mastery': 'Dominio de Melé',
    'stat.Distance_Mastery': 'Dominio Distancia',
    'stat.Healing_Mastery': 'Dominio Cura',
    'stat.Berserk_Mastery': 'Dominio Berserker',
    
    // Stats - Elemental Resistances
    'stat.Water_Resistance': 'Resistencia Agua',
    'stat.Air_Resistance': 'Resistencia Aire',
    'stat.Earth_Resistance': 'Resistencia Tierra',
    'stat.Fire_Resistance': 'Resistencia Fuego',
    'stat.Elemental_Resistance': 'Resistencia Elemental',
    
    // Stats - Random Elemental Resistance
    'stat.Random_Elemental_Resistance_1': 'Resistencia (1 elemento)',
    'stat.Random_Elemental_Resistance_2': 'Resistencia (2 elementos)',
    'stat.Random_Elemental_Resistance_3': 'Resistencia (3 elementos)',
    'stat.Random_Elemental_Resistance_4': 'Resistencia (4 elementos)',
    'stat.Elemental_Resistance_1_elements': 'Resistencia (1 elemento)',
    'stat.Elemental_Resistance_2_elements': 'Resistencia (2 elementos)',
    'stat.Elemental_Resistance_3_elements': 'Resistencia (3 elementos)',
    'stat.Elemental_Resistance_4_elements': 'Resistencia (4 elementos)',
    'stat.Random_Elemental_Resistance': 'Resistencia Elemental Aleatoria',
    
    // Stats - Other Resistances
    'stat.Critical_Resistance': 'Resistencia Crítica',
    'stat.Rear_Resistance': 'Resistencia Espalda',
    
    // Stats - Combat
    'stat.Critical_Hit': 'Golpe Crítico',
    'stat.Block': 'Anticipación',
    'stat.Initiative': 'Iniciativa',
    'stat.Dodge': 'Esquiva',
    'stat.Lock': 'Placaje',
    'stat.Wisdom': 'Sabiduría',
    'stat.Prospecting': 'Prospección',
    'stat.Range': 'Alcance',
    'stat.Control': 'Control',
    'stat.Force_Of_Will': 'Voluntad',
    
    // Stats - Percentages
    'stat.Damage_Inflicted': 'Daños Finales',
    'stat.Heals_Performed': 'Curas Finales',
    'stat.Heals_Received': 'Curas Recibidas',
    'stat.Armor_Given': 'Armadura Dada',
    'stat.Armor_Received': 'Armadura Recibida',
    'stat.Indirect_Damage': 'Daños Indirectos',
    
    // Stats - Other
    'stat.Kit_Skill': 'Nivel de Kit',
    'stat.Resistance': 'Resistencia',
    
    // General UI
    'ui.level': 'Nivel',
    'ui.damage': 'Daño',
    'ui.critical': 'Crítico',
    'ui.estimating': 'Estimando',
    'ui.calculating': 'Calculando',
    'ui.melee': 'Melé',
    'ui.distance': 'Distancia',
    'ui.damageType': 'Tipo de daño',
    'ui.showCritical': 'Mostrar daño crítico',
    'ui.noDamageStats': 'No hay estadísticas disponibles para calcular daño',
    'ui.bestElementDamage': 'ofrece el mejor daño promedio',
    'ui.perSpell': 'por hechizo',
    'ui.errorCalculating': 'Error al calcular daño',
    'ui.damageEstimation': 'Estimación de Daño por Elemento',
    'ui.damageEstimationDesc': 'Daño estimado vs resistencias enemigas (hechizo base 100 | {type} | Single Target)',
    'ui.resistanceFormula': 'Resistencias planas convertidas a % con fórmula oficial: 1 - 0.8^(res/100)',
    'ui.resistancesToShow': 'Resistencias a mostrar (valores planos)',
    'ui.normal': 'Normal',
    'ui.backstab': 'Espalda',
    'ui.backstabCritical': 'Espalda + Crít',
    'ui.recommendation': 'Recomendación',
    'ui.noData': 'No hay suficientes datos',
    'ui.mastery': 'dominio',
    'ui.resetToDefault': 'Restablecer a predeterminado',
    
    // Elements
    'element.Fire': 'Fuego',
    'element.Water': 'Agua',
    'element.Earth': 'Tierra',
    'element.Air': 'Aire',
    
    // Equipment Slots
    'equipment.title': 'Equipamiento',
    'equipment.head': 'Cabeza',
    'equipment.neck': 'Cuello',
    'equipment.chest': 'Pechera',
    'equipment.ring1': 'Anillo 1',
    'equipment.ring2': 'Anillo 2',
    'equipment.boots': 'Botas',
    'equipment.back': 'Capa',
    'equipment.shoulders': 'Hombros',
    'equipment.belt': 'Cinturón',
    'equipment.pet': 'Mascota',
    'equipment.weapon1': 'Arma Principal',
    'equipment.weapon2': 'Arma Secundaria',
    'equipment.accessory': 'Insignia',
    
    // Slot Names (for formatSlot function)
    'slot.HEAD': 'Cabeza',
    'slot.NECK': 'Cuello',
    'slot.CHEST': 'Pecho',
    'slot.LEGS': 'Piernas',
    'slot.BACK': 'Espalda',
    'slot.SHOULDERS': 'Hombros',
    'slot.BELT': 'Cinturón',
    'slot.FIRST_WEAPON': 'Arma',
    'slot.SECOND_WEAPON': 'Arma 2',
    'slot.ACCESSORY': 'Accesorio',
    'slot.LEFT_HAND': 'Anillo',
    'slot.RIGHT_HAND': 'Anillo',
    'slot.PET': 'Mascota',
    'slot.MOUNT': 'Montura',
    
    // Item
    'item.noStats': 'Sin stats'
  },
  en: {
    // Header
    'app.title': 'Wakfu Builder Assistant',
    'app.subtitle': 'Generate optimized equipment builds for your character',
    'language': 'Language',
    
    // Navigation
    'nav.myBuilds': 'My Builds',
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
    'stats.elementalMasteries': 'Elemental Masteries',
    'stats.elementalResistances': 'Elemental Resistances',
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
    'elements.damageHelp': 'Priority for elemental mastery stats. Auto-ordered by mastery weights; drag to break ties.',
    'elements.resistancePrefs': 'Resistance Elements',
    'elements.resistanceHelp': 'Priority for elemental resistance stats. Auto-ordered by resistance weights; drag to break ties.',
    
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
    'builds.loadBuild': 'Load Build',
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
    
    // My Builds View
    'myBuilds.title': 'My Saved Builds',
    'myBuilds.createNew': 'Create New',
    'myBuilds.loading': 'Loading builds...',
    'myBuilds.noBuildsSaved': 'You have no saved builds',
    'myBuilds.startByCreating': 'Start by creating your first build in the generator',
    'myBuilds.goToBuilder': 'Go to Generator',
    'myBuilds.unnamedBuild': 'Unnamed build',
    'myBuilds.selectBuild': 'Select a build',
    'myBuilds.selectBuildDescription': 'Choose a build from the sidebar to view its details',
    'myBuilds.loadInBuilder': 'Load in Generator',
    'myBuilds.rename': 'Rename',
    'myBuilds.renameBuild': 'Rename Build',
    'myBuilds.buildName': 'Build Name',
    'myBuilds.enterBuildName': 'Enter a name',
    'myBuilds.deleteBuild': 'Delete Build',
    'myBuilds.deleteConfirmation': 'Are you sure you want to delete this build?',
    'myBuilds.buildDeleted': 'Build deleted successfully',
    'myBuilds.buildRenamed': 'Build renamed successfully',
    'myBuilds.loadedInBuilder': 'Build loaded in generator',
    'myBuilds.errorLoading': 'Error loading builds',
    'myBuilds.errorDeleting': 'Error deleting build',
    'myBuilds.errorRenaming': 'Error renaming build',
    'myBuilds.justNow': 'Just now',
    'myBuilds.minutesAgo': '{count} minutes ago',
    'myBuilds.hoursAgo': '{count} hours ago',
    'myBuilds.daysAgo': '{count} days ago',
    
    // Common
    'common.cancel': 'Cancel',
    'common.save': 'Save',
    'common.delete': 'Delete',
    'common.edit': 'Edit',
    'common.close': 'Close',
    'common.confirm': 'Confirm',
    'common.yes': 'Yes',
    'common.no': 'No',
    'common.loading': 'Loading...',
    
    // Monster Type Filter
    'monsterTypeFilter.title': 'Monster Type Filter',
    'monsterTypeFilter.description': 'Select which monster types to consider for drops',
    'monsterTypeFilter.selectAll': 'All',
    'monsterTypeFilter.deselectAll': 'None',
    'monsterTypeFilter.error': 'Error loading types',
    
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
    
    // Ignored Items
    'ignoredItems.title': 'Ignored Items',
    'ignoredItems.description': 'Items that will not be included in future searches',
    'ignoredItems.empty': 'No ignored items',
    'ignoredItems.emptyHelp': 'Click the ban button (🚫) on any item to ignore it',
    'ignoredItems.ignore': 'Ignore item',
    'ignoredItems.unignore': 'Allow item',
    'ignoredItems.restore': 'Restore',
    'ignoredItems.ignoredAt': 'Ignored',
    'ignoredItems.clearAll': 'Clear All',
    'ignoredItems.confirmClearAll': 'Are you sure you want to remove all ignored items?',
    'ignoredItems.cleared': 'List Cleared',
    'ignoredItems.clearedDetail': 'All items have been restored',
    'ignoredItems.restored': 'Item Restored',
    'ignoredItems.restoredDetail': 'The item will now appear in searches',
    'ignoredItems.export': 'Export',
    'ignoredItems.import': 'Import',
    'ignoredItems.exported': 'Exported',
    'ignoredItems.exportedDetail': 'Ignored items list downloaded',
    'ignoredItems.imported': 'Imported',
    'ignoredItems.importedDetail': 'Ignored items list loaded',
    'ignoredItems.exportError': 'Export error',
    'ignoredItems.importError': 'Import error',
    
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
    
    // Alternatives Modal
    'alternatives.title': 'Item Alternatives',
    'alternatives.itemPower': 'Item Power',
    'alternatives.betterAlternatives': 'Alternatives with Lower Power',
    'alternatives.noAlternatives': 'No alternatives available for this item in the level range',
    'alternatives.viewAlternatives': 'View alternatives',

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
    'rarity.epic': 'Epic',
    'rarity.souvenir': 'Souvenir',
    
    // Print
    'print.title': 'Items',
    'print.recommendedItems': 'Recommended Items',
    'print.slot': 'Slot',
    'print.name': 'Name',
    'print.level': 'Level',
    'print.rarity': 'Rarity',
    'print.difficulty': 'Difficulty',
    'print.generated': 'Generated',
    'print.noItems': 'No items to print',
    
    // Slots
    'slots.head': 'Head',
    'slots.neck': 'Neck',
    'slots.chest': 'Chest',
    'slots.legs': 'Legs',
    'slots.back': 'Back',
    'slots.shoulders': 'Shoulders',
    'slots.belt': 'Belt',
    'slots.weapon': 'Weapon',
    'slots.secondWeapon': 'Second Weapon',
    'slots.accessory': 'Accessory',
    'slots.ring': 'Ring',
    'slots.pet': 'Pet',
    'slots.mount': 'Mount',
    
    // Stats - Core
    'stat.HP': 'HP',
    'stat.AP': 'AP',
    'stat.MP': 'MP',
    'stat.WP': 'WP',
    
    // Stats - Elemental Masteries
    'stat.Water_Mastery': 'Water Mastery',
    'stat.Air_Mastery': 'Air Mastery',
    'stat.Earth_Mastery': 'Earth Mastery',
    'stat.Fire_Mastery': 'Fire Mastery',
    'stat.Elemental_Mastery': 'Elemental Mastery',
    
    // Stats - Multi-Element Mastery
    'stat.Multi_Element_Mastery_1': 'Mastery (1 element)',
    'stat.Multi_Element_Mastery_2': 'Mastery (2 elements)',
    'stat.Multi_Element_Mastery_3': 'Mastery (3 elements)',
    'stat.Multi_Element_Mastery_4': 'Mastery (4 elements)',
    'stat.Elemental_Mastery_1_elements': 'Mastery (1 element)',
    'stat.Elemental_Mastery_2_elements': 'Mastery (2 elements)',
    'stat.Elemental_Mastery_3_elements': 'Mastery (3 elements)',
    'stat.Elemental_Mastery_4_elements': 'Mastery (4 elements)',
    'stat.Random_Elemental_Mastery': 'Random Elemental Mastery',
    
    // Stats - Position Masteries
    'stat.Critical_Mastery': 'Critical Mastery',
    'stat.Rear_Mastery': 'Rear Mastery',
    'stat.Melee_Mastery': 'Melee Mastery',
    'stat.Distance_Mastery': 'Distance Mastery',
    'stat.Healing_Mastery': 'Healing Mastery',
    'stat.Berserk_Mastery': 'Berserk Mastery',
    
    // Stats - Elemental Resistances
    'stat.Water_Resistance': 'Water Resistance',
    'stat.Air_Resistance': 'Air Resistance',
    'stat.Earth_Resistance': 'Earth Resistance',
    'stat.Fire_Resistance': 'Fire Resistance',
    'stat.Elemental_Resistance': 'Elemental Resistance',
    
    // Stats - Random Elemental Resistance
    'stat.Random_Elemental_Resistance_1': 'Resistance (1 element)',
    'stat.Random_Elemental_Resistance_2': 'Resistance (2 elements)',
    'stat.Random_Elemental_Resistance_3': 'Resistance (3 elements)',
    'stat.Random_Elemental_Resistance_4': 'Resistance (4 elements)',
    'stat.Elemental_Resistance_1_elements': 'Resistance (1 element)',
    'stat.Elemental_Resistance_2_elements': 'Resistance (2 elements)',
    'stat.Elemental_Resistance_3_elements': 'Resistance (3 elements)',
    'stat.Elemental_Resistance_4_elements': 'Resistance (4 elements)',
    'stat.Random_Elemental_Resistance': 'Random Elemental Resistance',
    
    // Stats - Other Resistances
    'stat.Critical_Resistance': 'Critical Resistance',
    'stat.Rear_Resistance': 'Rear Resistance',
    
    // Stats - Combat
    'stat.Critical_Hit': 'Critical Hit',
    'stat.Block': 'Block',
    'stat.Initiative': 'Initiative',
    'stat.Dodge': 'Dodge',
    'stat.Lock': 'Lock',
    'stat.Wisdom': 'Wisdom',
    'stat.Prospecting': 'Prospecting',
    'stat.Range': 'Range',
    'stat.Control': 'Control',
    'stat.Force_Of_Will': 'Force of Will',
    
    // Stats - Percentages
    'stat.Damage_Inflicted': 'Damage Inflicted',
    'stat.Heals_Performed': 'Heals Performed',
    'stat.Heals_Received': 'Heals Received',
    'stat.Armor_Given': 'Armor Given',
    'stat.Armor_Received': 'Armor Received',
    'stat.Indirect_Damage': 'Indirect Damage',
    
    // Stats - Other
    'stat.Kit_Skill': 'Kit Skill',
    'stat.Resistance': 'Resistance',
    
    // General UI
    'ui.level': 'Level',
    'ui.damage': 'Damage',
    'ui.critical': 'Critical',
    'ui.estimating': 'Estimating',
    'ui.calculating': 'Calculating',
    'ui.melee': 'Melee',
    'ui.distance': 'Distance',
    'ui.damageType': 'Damage type',
    'ui.showCritical': 'Show critical damage',
    'ui.noDamageStats': 'No stats available to calculate damage',
    'ui.bestElementDamage': 'offers the best average damage',
    'ui.perSpell': 'per spell',
    'ui.errorCalculating': 'Error calculating damage',
    'ui.damageEstimation': 'Damage Estimation by Element',
    'ui.damageEstimationDesc': 'Estimated damage vs enemy resistances (base spell 100 | {type} | Single Target)',
    'ui.resistanceFormula': 'Flat resistances converted to % with official formula: 1 - 0.8^(res/100)',
    'ui.resistancesToShow': 'Resistances to show (flat values)',
    'ui.normal': 'Normal',
    'ui.backstab': 'Backstab',
    'ui.backstabCritical': 'Backstab + Crit',
    'ui.recommendation': 'Recommendation',
    'ui.noData': 'Not enough data',
    'ui.mastery': 'mastery',
    'ui.resetToDefault': 'Reset to default',
    
    // Elements
    'element.Fire': 'Fire',
    'element.Water': 'Water',
    'element.Earth': 'Earth',
    'element.Air': 'Air',
    
    // Equipment Slots
    'equipment.title': 'Equipment',
    'equipment.head': 'Head',
    'equipment.neck': 'Neck',
    'equipment.chest': 'Chest',
    'equipment.ring1': 'Ring 1',
    'equipment.ring2': 'Ring 2',
    'equipment.boots': 'Boots',
    'equipment.back': 'Cape',
    'equipment.shoulders': 'Shoulders',
    'equipment.belt': 'Belt',
    'equipment.pet': 'Pet',
    'equipment.weapon1': 'Main Weapon',
    'equipment.weapon2': 'Secondary Weapon',
    'equipment.accessory': 'Emblem',
    
    // Slot Names (for formatSlot function)
    'slot.HEAD': 'Head',
    'slot.NECK': 'Neck',
    'slot.CHEST': 'Chest',
    'slot.LEGS': 'Legs',
    'slot.BACK': 'Back',
    'slot.SHOULDERS': 'Shoulders',
    'slot.BELT': 'Belt',
    'slot.FIRST_WEAPON': 'Weapon',
    'slot.SECOND_WEAPON': 'Weapon 2',
    'slot.ACCESSORY': 'Accessory',
    'slot.LEFT_HAND': 'Ring',
    'slot.RIGHT_HAND': 'Ring',
    'slot.PET': 'Pet',
    'slot.MOUNT': 'Mount',
    
    // Item
    'item.noStats': 'No stats'
  },
  fr: {
    // Header
    'app.title': 'Wakfu Builder Assistant',
    'app.subtitle': 'Générez des builds d\'équipement optimisés pour votre personnage',
    'language': 'Langue',
    
    // Navigation
    'nav.myBuilds': 'Mes Builds',
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
    'stats.elementalMasteries': 'Maîtrises Élémentaires',
    'stats.elementalResistances': 'Résistances Élémentaires',
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
    'elements.damageHelp': 'Priorité pour les stats de maîtrise élémentaire. Ordre automatique selon les poids de maîtrise ; glissez pour départager.',
    'elements.resistancePrefs': 'Éléments de Résistance',
    'elements.resistanceHelp': 'Priorité pour les stats de résistance élémentaire. Ordre automatique selon les poids de résistance ; glissez pour départager.',
    
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
    'builds.loadBuild': 'Charger Build',
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
    
    // Ignored Items
    'ignoredItems.title': 'Items Ignorés',
    'ignoredItems.description': 'Items qui ne seront pas inclus dans les recherches futures',
    'ignoredItems.empty': 'Aucun item ignoré',
    'ignoredItems.emptyHelp': 'Cliquez sur le bouton d\'interdiction (🚫) sur n\'importe quel item pour l\'ignorer',
    'ignoredItems.ignore': 'Ignorer l\'item',
    'ignoredItems.unignore': 'Autoriser l\'item',
    'ignoredItems.restore': 'Restaurer',
    'ignoredItems.ignoredAt': 'Ignoré',
    'ignoredItems.clearAll': 'Tout Effacer',
    'ignoredItems.confirmClearAll': 'Êtes-vous sûr de vouloir supprimer tous les items ignorés?',
    'ignoredItems.cleared': 'Liste Effacée',
    'ignoredItems.clearedDetail': 'Tous les items ont été restaurés',
    'ignoredItems.restored': 'Item Restauré',
    'ignoredItems.restoredDetail': 'L\'item apparaîtra maintenant dans les recherches',
    'ignoredItems.export': 'Exporter',
    'ignoredItems.import': 'Importer',
    'ignoredItems.exported': 'Exporté',
    'ignoredItems.exportedDetail': 'Liste d\'items ignorés téléchargée',
    'ignoredItems.imported': 'Importé',
    'ignoredItems.importedDetail': 'Liste d\'items ignorés chargée',
    'ignoredItems.exportError': 'Erreur d\'exportation',
    'ignoredItems.importError': 'Erreur d\'importation',
    
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
    
    // Alternatives Modal
    'alternatives.title': 'Alternatives d\'Items',
    'alternatives.itemPower': 'Puissance Item',
    'alternatives.betterAlternatives': 'Alternatives avec Puissance Inférieure',
    'alternatives.noAlternatives': 'Aucune alternative disponible pour cet item dans la plage de niveau',
    'alternatives.viewAlternatives': 'Voir alternatives',

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
    'rarity.epic': 'Épique',
    'rarity.souvenir': 'Souvenir',
    
    // Print
    'print.title': 'Objets',
    'print.recommendedItems': 'Objets Recommandés',
    'print.slot': 'Emplacement',
    'print.name': 'Nom',
    'print.level': 'Niveau',
    'print.rarity': 'Rareté',
    'print.difficulty': 'Difficulté',
    'print.generated': 'Généré',
    'print.noItems': 'Aucun objet à imprimer',
    
    // Slots
    'slots.head': 'Tête',
    'slots.neck': 'Cou',
    'slots.chest': 'Torse',
    'slots.legs': 'Jambes',
    'slots.back': 'Dos',
    'slots.shoulders': 'Épaules',
    'slots.belt': 'Ceinture',
    'slots.weapon': 'Arme',
    'slots.secondWeapon': 'Arme Secondaire',
    'slots.accessory': 'Accessoire',
    'slots.ring': 'Anneau',
    'slots.pet': 'Familier',
    'slots.mount': 'Monture',
    
    // Stats - Core
    'stat.HP': 'PdV',
    'stat.AP': 'PA',
    'stat.MP': 'PM',
    'stat.WP': 'PW',
    
    // Stats - Elemental Masteries
    'stat.Water_Mastery': 'Maîtrise Eau',
    'stat.Air_Mastery': 'Maîtrise Air',
    'stat.Earth_Mastery': 'Maîtrise Terre',
    'stat.Fire_Mastery': 'Maîtrise Feu',
    'stat.Elemental_Mastery': 'Maîtrise Élémentaire',
    
    // Stats - Multi-Element Mastery
    'stat.Multi_Element_Mastery_1': 'Maîtrise (1 élément)',
    'stat.Multi_Element_Mastery_2': 'Maîtrise (2 éléments)',
    'stat.Multi_Element_Mastery_3': 'Maîtrise (3 éléments)',
    'stat.Multi_Element_Mastery_4': 'Maîtrise (4 éléments)',
    'stat.Elemental_Mastery_1_elements': 'Maîtrise (1 élément)',
    'stat.Elemental_Mastery_2_elements': 'Maîtrise (2 éléments)',
    'stat.Elemental_Mastery_3_elements': 'Maîtrise (3 éléments)',
    'stat.Elemental_Mastery_4_elements': 'Maîtrise (4 éléments)',
    'stat.Random_Elemental_Mastery': 'Maîtrise Élémentaire Aléatoire',
    
    // Stats - Position Masteries
    'stat.Critical_Mastery': 'Maîtrise Critique',
    'stat.Rear_Mastery': 'Maîtrise Dos',
    'stat.Melee_Mastery': 'Maîtrise Mêlée',
    'stat.Distance_Mastery': 'Maîtrise Distance',
    'stat.Healing_Mastery': 'Maîtrise Soin',
    'stat.Berserk_Mastery': 'Maîtrise Berserk',
    
    // Stats - Elemental Resistances
    'stat.Water_Resistance': 'Résistance Eau',
    'stat.Air_Resistance': 'Résistance Air',
    'stat.Earth_Resistance': 'Résistance Terre',
    'stat.Fire_Resistance': 'Résistance Feu',
    'stat.Elemental_Resistance': 'Résistance Élémentaire',
    
    // Stats - Random Elemental Resistance
    'stat.Random_Elemental_Resistance_1': 'Résistance (1 élément)',
    'stat.Random_Elemental_Resistance_2': 'Résistance (2 éléments)',
    'stat.Random_Elemental_Resistance_3': 'Résistance (3 éléments)',
    'stat.Random_Elemental_Resistance_4': 'Résistance (4 éléments)',
    'stat.Elemental_Resistance_1_elements': 'Résistance (1 élément)',
    'stat.Elemental_Resistance_2_elements': 'Résistance (2 éléments)',
    'stat.Elemental_Resistance_3_elements': 'Résistance (3 éléments)',
    'stat.Elemental_Resistance_4_elements': 'Résistance (4 éléments)',
    'stat.Random_Elemental_Resistance': 'Résistance Élémentaire Aléatoire',
    
    // Stats - Other Resistances
    'stat.Critical_Resistance': 'Résistance Critique',
    'stat.Rear_Resistance': 'Résistance Dos',
    
    // Stats - Combat
    'stat.Critical_Hit': 'Coup Critique',
    'stat.Block': 'Parade',
    'stat.Initiative': 'Initiative',
    'stat.Dodge': 'Esquive',
    'stat.Lock': 'Tacle',
    'stat.Wisdom': 'Sagesse',
    'stat.Prospecting': 'Prospection',
    'stat.Range': 'Portée',
    'stat.Control': 'Contrôle',
    'stat.Force_Of_Will': 'Volonté',
    
    // Stats - Percentages
    'stat.Damage_Inflicted': 'Dégâts Infligés',
    'stat.Heals_Performed': 'Soins Réalisés',
    'stat.Heals_Received': 'Soins Reçus',
    'stat.Armor_Given': 'Armure Donnée',
    'stat.Armor_Received': 'Armure Reçue',
    'stat.Indirect_Damage': 'Dégâts Indirects',
    
    // Stats - Other
    'stat.Kit_Skill': 'Niveau de Kit',
    'stat.Resistance': 'Résistance',
    
    // General UI
    'ui.level': 'Niveau',
    'ui.damage': 'Dégâts',
    'ui.critical': 'Critique',
    'ui.estimating': 'Estimation',
    'ui.calculating': 'Calcul',
    'ui.melee': 'Mêlée',
    'ui.distance': 'Distance',
    'ui.damageType': 'Type de dégâts',
    'ui.showCritical': 'Afficher dégâts critiques',
    'ui.noDamageStats': 'Aucune statistique disponible pour calculer les dégâts',
    'ui.bestElementDamage': 'offre les meilleurs dégâts moyens',
    'ui.perSpell': 'par sort',
    'ui.errorCalculating': 'Erreur lors du calcul des dégâts',
    'ui.damageEstimation': 'Estimation des Dégâts par Élément',
    'ui.damageEstimationDesc': 'Dégâts estimés vs résistances ennemies (sort de base 100 | {type} | Cible unique)',
    'ui.resistanceFormula': 'Résistances plates converties en % avec formule officielle: 1 - 0.8^(res/100)',
    'ui.resistancesToShow': 'Résistances à afficher (valeurs plates)',
    'ui.normal': 'Normal',
    'ui.backstab': 'Dos',
    'ui.backstabCritical': 'Dos + Crit',
    'ui.recommendation': 'Recommandation',
    'ui.noData': 'Pas assez de données',
    'ui.mastery': 'maîtrise',
    'ui.resetToDefault': 'Réinitialiser par défaut',
    
    // Elements
    'element.Fire': 'Feu',
    'element.Water': 'Eau',
    'element.Earth': 'Terre',
    'element.Air': 'Air',
    
    // Equipment Slots
    'equipment.title': 'Équipement',
    'equipment.head': 'Tête',
    'equipment.neck': 'Cou',
    'equipment.chest': 'Plastron',
    'equipment.ring1': 'Anneau 1',
    'equipment.ring2': 'Anneau 2',
    'equipment.boots': 'Bottes',
    'equipment.back': 'Cape',
    'equipment.shoulders': 'Épaulettes',
    'equipment.belt': 'Ceinture',
    'equipment.pet': 'Familier',
    'equipment.weapon1': 'Arme Principale',
    'equipment.weapon2': 'Arme Secondaire',
    'equipment.accessory': 'Emblème',
    
    // Slot Names (for formatSlot function)
    'slot.HEAD': 'Tête',
    'slot.NECK': 'Cou',
    'slot.CHEST': 'Plastron',
    'slot.LEGS': 'Jambes',
    'slot.BACK': 'Dos',
    'slot.SHOULDERS': 'Épaulettes',
    'slot.BELT': 'Ceinture',
    'slot.FIRST_WEAPON': 'Arme',
    'slot.SECOND_WEAPON': 'Arme 2',
    'slot.ACCESSORY': 'Accessoire',
    'slot.LEFT_HAND': 'Anneau',
    'slot.RIGHT_HAND': 'Anneau',
    'slot.PET': 'Familier',
    'slot.MOUNT': 'Monture',
    
    // Item
    'item.noStats': 'Aucune stat'
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

