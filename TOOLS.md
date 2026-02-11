# TOOLS.md - Herramientas del Clasificador

## MCP Tarifar

Servidor MCP para consultar la nomenclatura y aranceles de Argentina/Mercosur.

**Estado:** ✅ Configurado y operativo

### Conexión
- **URL:** `https://tarifar.fastmcp.app/mcp`
- **Token:** `/home/clawd/.config/secrets/tarifar_mcp_token`
- **Protocolo:** FastMCP 2.0

### Herramientas Disponibles

#### Principales (USAR SIEMPRE)

| Tool | Descripción | Ejemplo |
|------|-------------|---------|
| `search_posiciones(query)` | Buscar posiciones arancelarias por código o texto | `search_posiciones("bolsos de cuero")` |
| `search_notas(query)` | Notas explicativas, RGI, exclusiones | `search_notas("Nota Capítulo 42")` |
| `search_leyes(query)` | Normativa, resoluciones, decretos | `search_leyes("ley 22415")` |

#### Complementarias

| Tool | Descripción | Cuándo usar |
|------|-------------|-------------|
| `search_jurisprudencia(query)` | Fallos, consultas vinculantes | Casos complejos |
| `search_doctrina(query)` | Interpretaciones doctrinarias | Ambigüedades en RGI |
| `search_acuerdos(query)` | Acuerdos comerciales | Preferencias arancelarias |
| `search_compendio(query)` | Guías, manuales | Clasificaciones especiales |
| `search_padron(query)` | Registros importadores | Verificar autorizaciones |

### Parámetros Comunes

- `query`: Texto de búsqueda (obligatorio)
- `page`: Página de resultados (default: 1)
- `per_page`: Resultados por página, máx 1500 (default: 50)
- `nomen_id`: ID de nomenclatura, "1" para NCM Argentina

### Detección Inteligente

El tool `search_posiciones()` detecta automáticamente:
- **Código de posición**: "4202.92.00.110" → búsqueda SQL exacta
- **Texto natural**: "bolsos de cuero" → búsqueda fulltext Lucene

### Respuesta de Posiciones

```json
{
  "id": 24613,
  "formatted": "4202.11.00.100Y",
  "descripcion": "Baúles, maletas...",
  "aranceles": [
    {"nombre": "AEC", "value": 20},
    {"nombre": "DIE", "value": 20},
    {"nombre": "IVA", "value": 21}
  ],
  "observaciones_impo": [...],
  "observaciones_expo": [...]
}
```

## Fuentes de Referencia

- [Tarifar](https://tarifar.com) - Nomenclador oficial
- [AFIP](https://www.afip.gob.ar) - Administración Federal
- [Aduana Argentina](https://www.argentina.gob.ar/aduana) - Normativa oficial
- Reglas Generales Interpretativas (RGI 1-6)
- Notas Legales y Explicativas del SA

## Códigos de Nomenclatura

- **NCM (8 dígitos)**: Nomenclatura Común del Mercosur
- **SIM (11 dígitos)**: Sistema Informático María (Argentina)
- **nomen_id = "1"**: NCM Argentina (default)

---

*Fuente: https://github.com/tarifar/tarifar-fast-mcp*
*Mantener actualizado con cambios en la nomenclatura.*
