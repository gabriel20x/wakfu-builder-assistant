# Wakforge community data

Archivos tomados de [Tmktahu/wakforge](https://github.com/Tmktahu/wakforge) (licencia MIT),
el builder open-source de wakforge.org.

- `state_data.json` — plantillas de descripción de estados (sublimaciones) con valores
  numéricos por nivel de estado (`num_N.level_M`). Origen: `src/models/state_data.json`.
- `{en,es,fr}_states.json` — textos localizados de las plantillas anteriores.
  Origen: `src/plugins/i18n/statesTranslations/`.

El gamedata oficial de Ankama solo trae el *nombre* de los estados que aplican las
sublimaciones (via actionId 304), no su efecto ni sus valores; estos archivos cubren ese hueco.
Los consume `scripts/build_static_data.py` para generar `frontend/public/data/sublimations.json`.
