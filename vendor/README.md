# vendor/ — CodeMirror 6 vendorizado

`codemirror.bundle.js` es un bundle ESM autocontenido de CodeMirror 6 para este
SPA. No hay build step en la app: `app.js` hace `import('./vendor/codemirror.bundle.js')`
directamente en el navegador. `entry.js` es la fuente del bundle (re-exporta los
paquetes usados); el artefacto commiteado es `codemirror.bundle.js`.

El tema del editor y el autocompletado NO viven acá: están en `app.js` y usan
exclusivamente `var(--token)` de `styles.css`, así que regenerar el bundle jamás
toca el tema (cero hex en el JS del editor).

## Versiones usadas

- @codemirror/state 6.7.6
- @codemirror/view 6.43.15
- @codemirror/language 6.13.1
- @codemirror/commands 6.11.1
- @codemirror/autocomplete 6.20.4
- @codemirror/lang-python 6.2.1
- @lezer/highlight 1.2.5 (dependencia; `entry.js` re-exporta `tags`)
- esbuild 0.28.2 (solo para generar el bundle)

Tamaño actual del artefacto: 909084 bytes (~888 KB).

## Regeneración exacta

Ejecutar desde cualquier carpeta temporal **fuera del repositorio** (nunca
dejar `node_modules` en el worktree; no se commitea):

```bash
REPO=/ruta/a/python-ejercicios/curso_pokemon_web
SCRATCH=$(mktemp -d) && cd "$SCRATCH"
npm init -y
npm install --no-audit --no-fund \
  @codemirror/state@6.7.6 @codemirror/view@6.43.15 @codemirror/language@6.13.1 \
  @codemirror/commands@6.11.1 @codemirror/autocomplete@6.20.4 \
  @codemirror/lang-python@6.2.1 @lezer/highlight@1.2.5 esbuild@0.28.2
cp "$REPO/vendor/entry.js" .
npx esbuild entry.js --bundle --format=esm \
  --outfile="$REPO/vendor/codemirror.bundle.js"
```

## Minificación (aplicada al artefacto commiteado)

El bundle commiteado está minificado: 909,084 → 458,548 bytes (-49.5%).
Después del comando de generación, minificar en el lugar:

    npx --yes esbuild@0.28.2 codemirror.bundle.js --minify --format=esm \
      --outfile=codemirror.bundle.js

Verificación obligatoria después de regenerar (los 284 exports deben sobrevivir) y luego
correr la suite de navegador, que monta el editor real:

    node -e "import('./codemirror.bundle.js').then(m=>console.log(Object.keys(m).length))"
    ../../.venv/Scripts/python -m pytest -q -m browser
