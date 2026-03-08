#!/usr/bin/env python3
"""Generate classification workflow diagram as PDF — v2 improved readability."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

def draw_workflow():
    fig, ax = plt.subplots(1, 1, figsize=(16, 28))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 28)
    ax.axis('off')
    fig.patch.set_facecolor('white')

    # Colors
    C_HEADER = '#1a1a2e'
    C_STEP = '#16213e'
    C_SUBSTEP = '#0f3460'
    C_SEARCH = '#e94560'
    C_DECISION = '#f5a623'
    C_OUTPUT = '#27ae60'
    C_PENALTY = '#c0392b'
    C_LIGHT = '#f0f2f5'
    C_TEXT = 'white'
    C_DARK = '#1a1a2e'

    def box(x, y, w, h, text, color, tc='white', fs=10, bold=False):
        b = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15",
                           facecolor=color, edgecolor='#444', linewidth=1.3)
        ax.add_patch(b)
        ax.text(x + w/2, y + h/2, text, ha='center', va='center',
                fontsize=fs, color=tc, fontweight='bold' if bold else 'normal',
                linespacing=1.4)

    def arrow(x1, y1, x2, y2, label='', color='#555', lw=2):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color=color, lw=lw))
        if label:
            mx, my = (x1+x2)/2 + 0.2, (y1+y2)/2
            ax.text(mx, my, label, fontsize=9, color=color, fontweight='bold')

    def mcp_badge(x, y):
        box(x, y, 1.6, 0.4, 'MCP', C_SEARCH, fs=9, bold=True)

    # ========== TITLE ==========
    ax.text(8, 27.4, 'CLASIFICADOR ADUANERO NCM-SIM', ha='center',
            fontsize=18, fontweight='bold', color=C_HEADER)
    ax.text(8, 27.0, 'Workflow de Clasificacion Arancelaria  --  Tarifar MCP', ha='center',
            fontsize=11, color='#666')

    # ========== PASO 1 ==========
    y = 26.0
    box(1.5, y, 13, 0.8,
        'PASO 1  --  Analisis Tecnico del Producto\n'
        'Sintetizar producto  |  Identificar keywords  |  Determinar info faltante',
        C_STEP, fs=10, bold=True)
    arrow(8, y, 8, y - 0.3)

    # ========== PASO 2 HEADER ==========
    y = 25.0
    box(1, y, 14, 0.6, 'PASO 2  --  Busqueda Estrategica en Tarifar MCP',
        C_HEADER, fs=12, bold=True)
    arrow(8, y, 8, y - 0.3)

    # --- 2a: Posiciones ---
    y = 23.8
    box(1.5, y, 6.5, 0.8,
        '2a) search_posiciones()\n'
        'Busqueda por codigo o descripcion natural',
        C_SUBSTEP, fs=9)
    mcp_badge(8.5, y + 0.2)
    box(10.5, y, 4, 0.8,
        'Ej: "bolsos de cuero"\n'
        'Ej: "4202.92.00.110"',
        C_LIGHT, C_DARK, fs=9)
    arrow(8, y, 8, y - 0.4)

    # --- 2b: Notas (expanded) ---
    y = 21.5
    box(0.5, y, 15, 1.9,
        'PASO 2b  --  CONSULTA OBLIGATORIA DE NOTAS  (Cascada descendente)\n\n'
        'b.1  Identificar Seccion  (tabla secciones-capitulos)\n'
        'b.2  search_notas("Seccion XX")  --  minimo 2 queries con variantes\n'
        'b.3  search_notas("Capitulo YY")  --  TODOS los capitulos candidatos\n'
        'b.4  search_notas("42.02")  --  notas explicativas de partida\n'
        'b.5  search_notas("subpartida 4202.92")  --  si existen',
        C_SUBSTEP, fs=9)
    box(12, y + 1.5, 3.2, 0.35, '[!] NO NEGOCIABLE', C_PENALTY, fs=8, bold=True)
    arrow(8, y, 8, y - 0.35)

    # --- Resumen notas ---
    y = 20.6
    box(2, y, 12, 0.6,
        'DOCUMENTAR: inclusiones, exclusiones, definiciones, alcance\n'
        '[!] Si hay exclusion  -->  DETENERSE y reclasificar antes de continuar',
        C_DECISION, C_DARK, fs=9, bold=True)
    arrow(8, y, 8, y - 0.4)

    # --- 2c: Resoluciones de Clasificacion ---
    y = 19.0
    box(1.5, y, 6.5, 1.1,
        '2c) search_resoluciones_clasificacion()\n\n'
        'Por posicion:  "8471"  -->  "84.71"\n'
        'Por texto:  "cafe tostado"\n'
        'Mixto:  "8471 computadoras"',
        C_SUBSTEP, fs=9)
    mcp_badge(8.5, y + 0.35)
    box(10.5, y, 4, 1.1,
        'Precedentes oficiales:\n\n'
        'Identico = evidencia fuerte\n'
        'Similar = evidencia de apoyo\n'
        'Contradictorio = senalar',
        C_LIGHT, C_DARK, fs=9)
    arrow(8, y, 8, y - 0.4)

    # --- 2d: Normativa ---
    y = 17.9
    box(1.5, y, 6.5, 0.7,
        '2d) search_leyes()\n'
        'Antidumping, licencias, regulaciones especiales',
        C_SUBSTEP, fs=9)
    mcp_badge(8.5, y + 0.15)
    arrow(8, y, 8, y - 0.4)

    # --- 2e: Jurisprudencia ---
    y = 16.9
    box(1.5, y, 6.5, 0.7,
        '2e) search_jurisprudencia() + search_doctrina()\n'
        'Consultas vinculantes, interpretaciones doctrinarias',
        C_SUBSTEP, fs=9)
    mcp_badge(8.5, y + 0.15)
    arrow(8, y, 8, y - 0.5)

    # ========== PASO 3: RGI ==========
    y = 15.2
    box(1, y, 14, 1.2,
        'PASO 3  --  Aplicar Reglas Generales Interpretativas (RGI)\n\n'
        'RGI 1: Texto de partida + Notas legales (fuerza legal)\n'
        'RGI 2: Incompletos / mezclas    |    RGI 3: a) Mas especifica  b) Caracter esencial  c) Ultima\n'
        'RGI 4: Analogia    |    RGI 5: Envases    |    RGI 6: Subpartidas',
        C_STEP, fs=9, bold=True)
    arrow(8, y, 8, y - 0.4)

    # ========== PASO 4: Exclusiones ==========
    y = 13.8
    box(1, y, 14, 0.9,
        'PASO 4  --  Documentar Exclusiones  (min. 2-3 posiciones descartadas)\n\n'
        'Citar texto exacto de la nota que excluye.\n'
        'Ej: "Excluido por Nota 1.e) del Capitulo 42: los articulos de la partida 64.01"',
        C_STEP, fs=9, bold=True)
    arrow(8, y, 8, y - 0.4)

    # ========== PASO 5: Confianza ==========
    y = 11.8
    box(0.5, y, 15, 1.5,
        'PASO 5  --  Evaluacion de Confianza (0-100%)\n\n'
        '[+] Coincidencia literal: +25%          [+] Notas de seccion OK: +10%\n'
        '[+] Notas de capitulo OK: +15%          [+] Notas explicativas partida: +10%\n'
        '[+] RGI sin ambiguedad: +15%            [+] Info tecnica completa: +10%\n'
        '[+] Exclusiones citadas: +10%\n'
        '[!] Notas NO consultadas: -30%          [!] Cap. alternativos no verificados: -15%',
        C_STEP, fs=9, bold=True)
    arrow(8, y, 8, y - 0.5)

    # ========== DECISION DIAMOND ==========
    y = 9.8
    dw, dh = 5, 1.4
    dx = 8 - dw/2
    diamond_x = [dx, dx + dw/2, dx + dw, dx + dw/2]
    diamond_y = [y + dh/2, y + dh, y + dh/2, y]
    ax.fill(diamond_x, diamond_y, color=C_DECISION, edgecolor='#333', linewidth=1.5)
    ax.text(8, y + dh/2, 'Confianza >= 70% ?', ha='center', va='center',
            fontsize=12, color=C_DARK, fontweight='bold')

    # NO branch (left)
    arrow(dx, y + dh/2, 3.5, y + dh/2, '< 70%', C_PENALTY, lw=2.5)

    y_no = 8.0
    box(0.5, y_no, 5.5, 1.8,
        'PROCESO ITERATIVO\n\n'
        'Identificar info faltante\n'
        '2-3 preguntas tecnicas especificas\n'
        'Explicar POR QUE importa cada una\n'
        'Esperar respuesta\n'
        '--> Volver a PASO 1',
        C_PENALTY, fs=9, bold=True)

    # Feedback arrow back up
    ax.annotate('', xy=(0.5, 26.4), xytext=(0.5, y_no + 0.9),
                arrowprops=dict(arrowstyle='->', color=C_PENALTY, lw=2.5,
                               connectionstyle='arc3,rad=0.15'))
    ax.text(0.1, 17, 'VOLVER A PASO 1', fontsize=9, color=C_PENALTY,
            fontweight='bold', rotation=90)

    # YES branch (right)
    arrow(dx + dw, y + dh/2, 11.5, y + dh/2, '>= 70%', C_OUTPUT, lw=2.5)

    # ========== PASO 6: Resultado ==========
    y_yes = 7.2
    box(9.5, y_yes, 6, 3.3,
        'PASO 6  --  Resultado Final\n\n'
        '> Codigo NCM-SIM\n'
        '> Descripcion oficial\n'
        '> RGI aplicadas\n'
        '> Exclusiones descartadas\n\n'
        'Info arancelaria:\n'
        '  AEC, DIE, IVA, Tasa Est.\n\n'
        'Requisitos especiales:\n'
        '  LNA/LA, ANMAT, SENASA\n\n'
        'Nivel de confianza: XX%',
        C_OUTPUT, fs=9, bold=True)

    # ========== FOOTER: Tools ==========
    y = 2.5
    ax.plot([0.5, 15.5], [y + 1.0, y + 1.0], color='#ccc', linewidth=1.5)
    ax.text(8, y + 0.7, 'Herramientas MCP Tarifar', ha='center', fontsize=12,
            fontweight='bold', color=C_HEADER)

    tools = [
        ('search_posiciones', 'Posiciones NCM/SIM'),
        ('search_notas', 'Notas Seccion/Capitulo/Partida'),
        ('search_resoluciones_clasificacion', 'Precedentes oficiales'),
        ('search_leyes', 'Normativa vigente'),
        ('search_jurisprudencia', 'Fallos y consultas vinculantes'),
        ('search_doctrina', 'Interpretaciones doctrinarias'),
    ]
    for i, (tool, desc) in enumerate(tools):
        col = i % 3
        row = i // 3
        tx = 1.5 + col * 4.5
        ty = y + 0.1 - row * 0.6
        ax.text(tx, ty, tool, fontsize=8, fontweight='bold', color=C_SEARCH)
        ax.text(tx, ty - 0.25, desc, fontsize=8, color='#666')

    # Watermark
    ax.text(8, 0.5, 'Tarifar x Clasificador Aduanero  --  Generado automaticamente',
            ha='center', fontsize=8, color='#aaa', style='italic')

    plt.tight_layout()
    out = '/home/clawd/dev/agents/clasificador/workflow-clasificacion.pdf'
    fig.savefig(out, format='pdf', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out}")

if __name__ == '__main__':
    draw_workflow()
