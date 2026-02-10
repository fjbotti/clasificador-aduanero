# Configuración MCP Server para NCM-SIM

Para usar esta skill con datos reales, necesitas configurar un MCP Server que exponga la nomenclatura arancelaria.

## Opción 1: MCP Server con Base de Datos

Crea un MCP server que lea de PostgreSQL/SQLite con los datos del CSV importados:

```typescript
// ncm-sim-server/index.ts
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new Server({
  name: "ncm-sim-server",
  version: "1.0.0"
}, {
  capabilities: { tools: {} }
});

// Tool: Buscar por descripción
server.setRequestHandler("tools/call", async (request) => {
  if (request.params.name === "ncm_search") {
    const { query, limit = 10 } = request.params.arguments;
    // Query a tu base de datos
    const results = await db.query(`
      SELECT codigo, descripcion, line_number 
      FROM sim_encadenada 
      WHERE descripcion ILIKE $1 
      LIMIT $2
    `, [`%${query}%`, limit]);
    return { content: [{ type: "text", text: JSON.stringify(results) }] };
  }
  // ... otros tools
});

const transport = new StdioServerTransport();
await server.connect(transport);
```

## Opción 2: MCP Server con CSV en Memoria

```typescript
import * as fs from 'fs';
import * as csv from 'csv-parse/sync';

const data = csv.parse(fs.readFileSync('sim_encadenada_aranceles.csv'), {
  columns: true,
  skip_empty_lines: true
});

// Indexar para búsqueda rápida
const index = new Map();
data.forEach((row, i) => {
  index.set(row.codigo, { ...row, line_number: i + 2 });
});
```

## Configuración en Claude Code

Agregar a `~/.claude/mcp_servers.json`:

```json
{
  "mcpServers": {
    "ncm-sim-server": {
      "command": "node",
      "args": ["/path/to/ncm-sim-server/dist/index.js"],
      "env": {
        "DATABASE_URL": "postgresql://..."
      }
    }
  }
}
```

## Configuración en Clawdbot

Agregar a `~/.clawdbot/clawdbot.json`:

```json
{
  "mcp": {
    "servers": {
      "ncm-sim-server": {
        "command": "node",
        "args": ["/path/to/ncm-sim-server/dist/index.js"]
      }
    }
  }
}
```

## Tools Requeridos

El MCP server debe implementar:

| Tool | Parámetros | Retorno |
|------|------------|---------|
| `ncm_search` | `query: string, limit?: number` | Array de candidatas |
| `ncm_get` | `codigo: string` | Detalle completo |
| `ncm_validate` | `codigo: string` | `{ exists: boolean }` |
| `ncm_aranceles` | `codigo: string` | Info arancelaria |

## Ejemplo de Respuesta ncm_search

```json
{
  "results": [
    {
      "codigo": "8471.30.19.000U",
      "descripcion": "Las demás máquinas automáticas para tratamiento de datos, portátiles",
      "line_number": 12456,
      "capitulo": "84",
      "seccion": "XVI"
    }
  ]
}
```
