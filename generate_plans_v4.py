#!/usr/bin/env python3
"""
Bhagamandala House — Professional Architectural Plans v4
MAJOR REDESIGN: Wider footprint (42x30), back-to-back baths,
rectangular bedrooms, FF work room, west sitout, safety features.
Bhagamandala, Kodagu — v4 (April 2026)
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import numpy as np
import os

OUT = os.path.dirname(os.path.abspath(__file__))

# Professional color scheme
C = {
    'bg': '#FFFFFF', 'wall': '#2C2C2C', 'wall_fill': '#E8E8E8',
    'dim': '#CC0000', 'door': '#8B4513', 'window': '#4A90D9',
    'room_label': '#1A1A1A', 'sub_label': '#666666',
    'furniture': '#D2B48C', 'furn_edge': '#A0A0A0',
    'vastu': '#E65100', 'grid': '#F0F0F0', 'title_bg': '#F5F5F5',
    'green': '#4CAF50', 'blue': '#1976D2',
    'hall': '#FAFAF0', 'br1': '#E8C4A8', 'br2': '#DEB894',
    'master': '#D4A574', 'kitchen': '#FFFCF0',
    'bath': '#E0F2F1', 'bath_border': '#00897B',
    'storage': '#F5F5F5', 'veranda': '#FFF8F0', 'passage': '#FAFAFA',
    'stair': '#F0F0F0', 'sitout': '#F5FAF0', 'family': '#FAFAF5',
    'gwc': '#F3E5F5', 'work': '#FFF3E0',
}

WALL_EXT = 1.0
WALL_INT = 0.75


def dim_line(ax, x1, y1, x2, y2, text, offset=1.5, fontsize=7, side='outside'):
    horizontal = abs(y2 - y1) < 0.1
    if horizontal:
        yo = y1 + offset if side == 'outside' else y1 - offset
        ax.plot([x1, x1], [y1, yo], color=C['dim'], linewidth=0.4, linestyle='-')
        ax.plot([x2, x2], [y2, yo], color=C['dim'], linewidth=0.4, linestyle='-')
        ax.annotate('', xy=(x2, yo), xytext=(x1, yo),
                    arrowprops=dict(arrowstyle='<->', color=C['dim'], lw=0.8))
        ax.text((x1+x2)/2, yo + 0.3, text, ha='center', va='bottom',
                fontsize=fontsize, color=C['dim'], fontweight='bold',
                bbox=dict(facecolor='white', edgecolor='none', pad=1, alpha=0.9))
    else:
        xo = x1 + offset if side == 'outside' else x1 - offset
        ax.plot([x1, xo], [y1, y1], color=C['dim'], linewidth=0.4)
        ax.plot([x2, xo], [y2, y2], color=C['dim'], linewidth=0.4)
        ax.annotate('', xy=(xo, y2), xytext=(xo, y1),
                    arrowprops=dict(arrowstyle='<->', color=C['dim'], lw=0.8))
        ax.text(xo + 0.3, (y1+y2)/2, text, ha='left', va='center',
                fontsize=fontsize, color=C['dim'], fontweight='bold', rotation=90,
                bbox=dict(facecolor='white', edgecolor='none', pad=1, alpha=0.9))


def draw_wall(ax, x1, y1, x2, y2, thickness=WALL_EXT):
    horizontal = abs(y2 - y1) < 0.1
    if horizontal:
        rect = patches.Rectangle((min(x1,x2), y1 - thickness/2),
                                 abs(x2-x1), thickness,
                                 facecolor=C['wall'], edgecolor=C['wall'], linewidth=0.5)
    else:
        rect = patches.Rectangle((x1 - thickness/2, min(y1,y2)),
                                 thickness, abs(y2-y1),
                                 facecolor=C['wall'], edgecolor=C['wall'], linewidth=0.5)
    ax.add_patch(rect)


def draw_room_fill(ax, x, y, w, h, color, alpha=0.5):
    rect = patches.Rectangle((x, y), w, h, facecolor=color, edgecolor='none', alpha=alpha)
    ax.add_patch(rect)


def draw_door_arc(ax, x, y, width=3, direction='right', orient='h'):
    if orient == 'h':
        ax.plot([x, x+width], [y, y], color='white', linewidth=3, zorder=5)
        if direction == 'right':
            ax.plot([x, x+width*0.7], [y, y+width*0.7], color=C['door'], linewidth=1, zorder=6)
            arc = matplotlib.patches.Arc((x, y), width*1.4, width*1.4, angle=0,
                                        theta1=0, theta2=90, color=C['door'], linewidth=0.5, linestyle='--', zorder=6)
        else:
            ax.plot([x+width, x+width-width*0.7], [y, y+width*0.7], color=C['door'], linewidth=1, zorder=6)
            arc = matplotlib.patches.Arc((x+width, y), width*1.4, width*1.4, angle=0,
                                        theta1=90, theta2=180, color=C['door'], linewidth=0.5, linestyle='--', zorder=6)
        ax.add_patch(arc)
    else:
        ax.plot([x, x], [y, y+width], color='white', linewidth=3, zorder=5)
        ax.plot([x, x+width*0.7], [y, y+width*0.7], color=C['door'], linewidth=1, zorder=6)


def draw_window_h(ax, x, y, width=4):
    ax.plot([x, x+width], [y, y], color='white', linewidth=3, zorder=5)
    ax.plot([x, x+width], [y-0.15, y-0.15], color=C['window'], linewidth=2, zorder=6)
    ax.plot([x, x+width], [y+0.15, y+0.15], color=C['window'], linewidth=2, zorder=6)
    for gx in np.linspace(x+0.3, x+width-0.3, 4):
        ax.plot([gx, gx], [y-0.15, y+0.15], color=C['window'], linewidth=0.5, zorder=6)


def draw_window_v(ax, x, y, width=4):
    ax.plot([x, x], [y, y+width], color='white', linewidth=3, zorder=5)
    ax.plot([x-0.15, x-0.15], [y, y+width], color=C['window'], linewidth=2, zorder=6)
    ax.plot([x+0.15, x+0.15], [y, y+width], color=C['window'], linewidth=2, zorder=6)
    for gy in np.linspace(y+0.3, y+width-0.3, 4):
        ax.plot([x-0.15, x+0.15], [gy, gy], color=C['window'], linewidth=0.5, zorder=6)


def room_label(ax, x, y, name, size_text='', fontsize=9):
    ax.text(x, y + (0.6 if size_text else 0), name,
            ha='center', va='center', fontsize=fontsize, fontweight='bold',
            color=C['room_label'], family='sans-serif')
    if size_text:
        ax.text(x, y - 0.5, size_text, ha='center', va='center',
                fontsize=fontsize-2, color=C['sub_label'], family='sans-serif')


def furniture(ax, x, y, w, h, label='', color=None):
    c = color or C['furniture']
    rect = patches.Rectangle((x, y), w, h, facecolor=c, edgecolor=C['furn_edge'],
                              linewidth=0.5, alpha=0.6, zorder=3)
    ax.add_patch(rect)
    if label:
        ax.text(x+w/2, y+h/2, label, ha='center', va='center',
                fontsize=5, color='#555555', zorder=4)


def draw_bath(ax, x, y, w, h, label='BATH', fontsize=7, actual_w=None, actual_h=None):
    rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15",
                          facecolor=C['bath'], edgecolor=C['bath_border'],
                          linewidth=2, alpha=0.7, zorder=3)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h/2 + 0.5, label, ha='center', va='center',
            fontsize=fontsize, color=C['bath_border'], fontweight='bold', zorder=4)
    dw, dh = actual_w or w, actual_h or h
    ax.text(x + w/2, y + h/2 - 0.8, f"{dw:.0f}' x {dh:.0f}' = {dw*dh:.0f} sqft",
            ha='center', va='center', fontsize=5, color='#555', zorder=4)


def compass(ax, x, y, size=1.5):
    ax.annotate('', xy=(x, y+size), xytext=(x, y),
                arrowprops=dict(arrowstyle='->', color='#CC0000', lw=2))
    ax.text(x, y+size+0.3, 'N', fontsize=10, ha='center', va='center',
            fontweight='bold', color='#CC0000')
    circle = plt.Circle((x, y), size*0.5, fill=False, color='#CC0000',
                         linewidth=0.5, linestyle='--')
    ax.add_patch(circle)
    for d, dx, dy in [('E', size*0.7, 0), ('W', -size*0.7, 0), ('S', 0, -size*0.7)]:
        ax.text(x+dx, y+dy, d, fontsize=6, ha='center', va='center', color='#888')


def title_block(ax, title, subtitle, x, y):
    ax.text(x, y, title, fontsize=16, fontweight='bold', ha='center', va='center',
            color='#1A1A1A', family='sans-serif',
            bbox=dict(boxstyle='square,pad=0.4', facecolor=C['title_bg'],
                      edgecolor='#333333', linewidth=1.5))
    ax.text(x, y-1.2, subtitle, fontsize=8, ha='center', va='center',
            color='#666666', family='sans-serif')


def setup_ax(ax, xlim, ylim):
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_aspect('equal')
    ax.set_facecolor(C['bg'])
    ax.set_axis_off()


# ============================================================
# V4 GROUND FLOOR PLAN
# ============================================================
# Building: 42 ft (N-S) x 30 ft (E-W) interior
# + 8 ft veranda on East = 42 x 38 total
#
# Coordinate system:
#   x axis: 0=South, 42=North (N-S = 42 ft)
#   y axis: 0=East (road), 38=West (estate)
#   Veranda: y=0..8, Interior: y=8..38
#
# LAYOUT:
#   NORTH ROW (x=26..42, 16ft N-S):
#     Hall 16x16 (NE):     x=26..42, y=8..24
#     BR2 14x16 (NW):      x=26..40, y=24..38
#
#   SERVICE STRIP (x=16..26, 10ft N-S):
#     Store 8x10:           x=16..26, y=30..38
#     Bath2 7x10:           x=16..26, y=23..30
#     Passage 3x10:         x=16..26, y=20..23
#     Bath1 7x10:           x=16..26, y=13..20
#     Staircase 5x10:       x=16..26, y=8..13
#
#   SOUTH ROW (x=0..16, 16ft N-S):
#     Kitchen 14x16 (SE):   x=0..16, y=8..22
#     Master BR 16x16 (SW): x=0..16, y=22..38

def gen_gf():
    fig, ax = plt.subplots(1, 1, figsize=(22, 18))
    setup_ax(ax, (-6, 50), (-6, 46))

    title_block(ax, 'GROUND FLOOR PLAN (v4 — Optimized)',
                'Back-to-Back Baths | Rectangular BRs | Kitchen adj. Store | 42\'x38\' footprint', 22, 44)

    # ── ROOM FILLS ──
    # Veranda
    draw_room_fill(ax, 0, 0, 42, 8, C['veranda'])
    # Guest WC in veranda NE corner
    draw_room_fill(ax, 38, 2, 4, 4, C['gwc'])
    # Hall (NE)
    draw_room_fill(ax, 26, 8, 16, 16, C['hall'])
    # BR2 (NW)
    draw_room_fill(ax, 26, 24, 14, 14, C['br2'])
    # Store (W, adj kitchen)
    draw_room_fill(ax, 16, 30, 10, 8, C['storage'])
    # Bath 2
    draw_room_fill(ax, 16, 23, 10, 7, C['bath'], 0.3)
    # Passage
    draw_room_fill(ax, 16, 20, 10, 3, C['passage'])
    # Bath 1
    draw_room_fill(ax, 16, 13, 10, 7, C['bath'], 0.3)
    # Staircase
    draw_room_fill(ax, 16, 8, 10, 5, C['stair'])
    # Kitchen (SE)
    draw_room_fill(ax, 0, 8, 16, 14, C['kitchen'])
    # Master BR (SW)
    draw_room_fill(ax, 0, 22, 16, 16, C['br1'])

    # ── EXTERNAL WALLS ──
    draw_wall(ax, 0, 0, 42, 0, WALL_EXT)        # East (road)
    draw_wall(ax, 0, 38, 42, 38, WALL_EXT)      # West (estate)
    draw_wall(ax, 0, 0, 0, 38, WALL_EXT)        # South
    draw_wall(ax, 42, 0, 42, 38, WALL_EXT)      # North
    draw_wall(ax, 0, 8, 42, 8, WALL_EXT)        # Veranda back wall

    # ── INTERNAL WALLS ──
    # North row / South row divider at x=16 (partial, through service strip)
    draw_wall(ax, 16, 8, 16, 38, WALL_INT)      # Service strip west wall (continuous)

    # Hall / BR2 divider at y=24
    draw_wall(ax, 26, 24, 42, 24, WALL_INT)

    # Service strip east wall at x=26
    draw_wall(ax, 26, 8, 26, 38, WALL_INT)

    # Kitchen / Master divider at y=22
    draw_wall(ax, 0, 22, 16, 22, WALL_INT)

    # Bath2 / Store divider at y=30
    draw_wall(ax, 16, 30, 26, 30, WALL_INT)

    # Bath2 / Passage divider at y=23
    draw_wall(ax, 16, 23, 26, 23, WALL_INT)

    # Passage / Bath1 divider at y=20
    draw_wall(ax, 16, 20, 26, 20, WALL_INT)

    # Bath1 / Stair divider at y=13
    draw_wall(ax, 16, 13, 26, 13, WALL_INT)

    # Stair bottom wall (part of veranda back wall already at y=8)

    # Guest WC walls
    draw_wall(ax, 38, 2, 38, 6, WALL_INT)
    draw_wall(ax, 38, 6, 42, 6, WALL_INT)

    # ── BATHROOMS (distinctive) ──
    draw_bath(ax, 16.5, 13.5, 9, 6, 'BATH 1\n(Master)', 7, actual_w=7, actual_h=10)
    furniture(ax, 17, 14, 4, 3, 'Shower\nEncl. 4\'x3\'', '#B2DFDB')
    furniture(ax, 22, 14, 3, 2.5, 'WC\n(Commode)', '#B2DFDB')
    furniture(ax, 17, 17.5, 5, 1.5, 'Basin Counter\n5\' Granite', '#B2DFDB')
    ax.text(24.5, 17.5, 'Geyser', fontsize=4, ha='center', color='#666')

    draw_bath(ax, 16.5, 23.5, 9, 6, 'BATH 2\n(BR2)', 7, actual_w=7, actual_h=10)
    furniture(ax, 17, 24, 4, 3, 'Shower\nEncl. 4\'x3\'', '#B2DFDB')
    furniture(ax, 22, 24, 3, 2.5, 'WC\n(Commode)', '#B2DFDB')
    furniture(ax, 17, 27.5, 5, 1.5, 'Basin Counter\n5\' Granite', '#B2DFDB')
    ax.text(24.5, 27.5, 'Geyser', fontsize=4, ha='center', color='#666')

    # ── DOORS ──
    # D1: Main door (East wall, Hall)
    draw_door_arc(ax, 30, 8, 4, 'right', 'h')
    ax.text(32, 6.5, 'D1: MAIN DOOR\n4\' x 7\' Burma Teak', fontsize=5.5,
            ha='center', color=C['door'], fontweight='bold')

    # D3: Master BR (from passage through bath zone)
    draw_door_arc(ax, 8, 22, 3, 'left', 'h')

    # D4: BR2 (from passage)
    draw_door_arc(ax, 30, 24, 3, 'right', 'h')

    # D5: Kitchen (from east / veranda area)
    draw_door_arc(ax, 8, 8, 3, 'right', 'h')

    # Bath1 door (from Master BR side)
    draw_door_arc(ax, 12, 20, 2.5, 'left', 'h')
    ax.text(12, 19, 'Bath from\nMaster only', fontsize=4, ha='center', color=C['bath_border'])

    # Bath2 door (from BR2 side)
    draw_door_arc(ax, 30, 23, 2.5, 'left', 'h')
    ax.text(30, 22, 'Bath from\nBR2 only', fontsize=4, ha='center', color=C['bath_border'])

    # Store door (from kitchen side / passage)
    draw_door_arc(ax, 18, 30, 2.5, 'left', 'h')
    ax.text(19, 29.2, 'Store\n(Kitchen access)', fontsize=4, ha='center', color='#555')

    # Kitchen rear door
    draw_door_arc(ax, 6, 8, 2.5, 'left', 'h')

    # Guest WC door
    draw_door_arc(ax, 39, 6, 2, 'left', 'h')

    # ── WINDOWS ──
    # East wall (road) — Hall
    draw_window_h(ax, 28, 0, 5)
    draw_window_h(ax, 35, 0, 5)
    # East wall — Kitchen
    draw_window_h(ax, 4, 0, 4)
    # West wall (estate) — Master BR
    draw_window_h(ax, 4, 38, 5)
    # West wall — BR2
    draw_window_h(ax, 30, 38, 5)
    # South wall
    draw_window_v(ax, 0, 28, 5)      # Master BR south window
    # North wall
    draw_window_v(ax, 42, 28, 5)     # BR2 north window
    draw_window_v(ax, 42, 12, 4)     # Hall north window
    # Kitchen south
    draw_window_v(ax, 0, 12, 4)      # Kitchen south window
    # Store west
    draw_window_h(ax, 20, 38, 3)

    # ── ROOM LABELS ──
    # Veranda
    room_label(ax, 18, 4, 'PORCH / SITOUT / JAGALI', "42' x 8' = 336 sqft | Kota Stone | 5 Wood Pillars", 10)
    # Pillars
    for px in [5, 13, 21, 29, 37]:
        pillar = plt.Circle((px, 3), 0.4, facecolor='#5D3A1A', edgecolor='#3E2723',
                             linewidth=1.5, zorder=5)
        ax.add_patch(pillar)

    # Guest WC
    room_label(ax, 40, 4, 'GWC', '4\'x4\'', 6)

    # Hall
    room_label(ax, 34, 16, 'HALL / LIVING', "16' x 16' = 256 sqft", 11)
    ax.text(34, 13.5, 'NE — Pooja, TV, L-Sofa, 6-seat Dining', fontsize=5.5, ha='center', color=C['vastu'])
    # Pooja
    pooja = FancyBboxPatch((39, 10), 2.5, 1.5, boxstyle="round,pad=0.1",
                           facecolor='#FFF3E0', edgecolor='#E65100', linewidth=1.5, linestyle='--', zorder=5)
    ax.add_patch(pooja)
    ax.text(40.25, 10.75, 'POOJA', fontsize=5, ha='center', color='#E65100', fontweight='bold', zorder=6)
    # Hall furniture
    furniture(ax, 27, 15, 7, 3.5, '5-Seater\nL-Sofa', '#D7CCC8')
    furniture(ax, 35, 15, 3, 2, 'TV\nUnit', '#A1887F')
    furniture(ax, 27, 19, 5, 3, '6-Seat\nDining', '#FFCA28')

    # BR2
    room_label(ax, 33, 32, 'BEDROOM 2 (Guest)', "14' x 16' = 224 sqft NET RECTANGLE", 9)
    ax.text(33, 37, 'NW — Guest Room', fontsize=5, ha='center', color=C['vastu'])
    furniture(ax, 27, 33, 6, 4, 'Queen Bed\n5\'x6\'6"', '#D1C4E9')
    furniture(ax, 27, 28, 3, 3, 'Ward-\nrobe', '#B39DDB')
    furniture(ax, 35, 28, 4, 3, 'Study\nDesk', '#D1C4E9')

    # Store
    room_label(ax, 21, 34, 'STORE', "8' x 10' = 80 sqft\nAdj. Kitchen!", 7)

    # Staircase
    room_label(ax, 21, 10, 'STAIR', "5' x 10'", 7)
    for sy in np.arange(8.5, 12.5, 0.6):
        ax.plot([16.5, 25.5], [sy, sy], color='#999', linewidth=0.4)
    ax.annotate('UP →', xy=(23, 12.5), fontsize=7, ha='center', color='#666', fontweight='bold')
    ax.text(21, 8.5, 'Under-stair\nstorage', fontsize=4.5, ha='center', color='#888')

    # Passage
    ax.text(21, 21.5, 'PASSAGE\n3\' wide', fontsize=6, ha='center', color='#999')

    # Kitchen
    room_label(ax, 8, 16, 'KITCHEN', "14' x 16' = 224 sqft", 10)
    ax.text(8, 13, 'SE — Agni / Fire Element', fontsize=5, ha='center', color=C['vastu'])
    furniture(ax, 1, 9, 14, 1.5, 'L-Shaped Kitchen Slab + Sink', '#FFE082')
    furniture(ax, 1, 11, 3, 3, 'Fridge', '#E0E0E0')
    furniture(ax, 1, 16, 5, 4, '6-Seat\nDining', '#FFCA28')
    furniture(ax, 10, 17, 4, 2, 'Pantry\nShelf', '#FFE082')
    ax.text(12, 21, 'Washing\narea', fontsize=4, ha='center', color='#888')

    # Master BR
    room_label(ax, 8, 32, 'MASTER BEDROOM', "16' x 16' = 256 sqft NET RECTANGLE", 10)
    ax.text(8, 37, 'SW — Owner\'s Room', fontsize=5, ha='center', color=C['vastu'])
    furniture(ax, 2, 30, 7, 5, 'King Bed\n6\'x6\'6"', '#C8E6C9')
    furniture(ax, 10, 30, 4, 5, 'Double\nWardrobe', '#A5D6A7')
    furniture(ax, 2, 27, 3, 2.5, 'Dressing\nUnit', '#C8E6C9')
    furniture(ax, 6, 23, 2.5, 2, 'Chair', '#E8F5E9')

    # Veranda furniture
    furniture(ax, 2, 5, 4, 2, 'Wooden\nSwing', '#D7CCC8')
    furniture(ax, 14, 5, 5, 2, 'Sitting\nChairs', '#D7CCC8')
    furniture(ax, 33, 5, 4, 2, 'Shoe\nRack', '#BCAAA4')

    # ── CALLOUT BOX ──
    callout = ('v4 KEY IMPROVEMENTS\n'
               '━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'
               '• Building widened: 42x30 interior\n'
               '• Bedrooms: FULL RECTANGLES\n'
               '  Master 16x16=256, BR2 14x16=224\n'
               '• Baths BACK-TO-BACK: single stack\n'
               '  Both 7x10=70 sqft (spacious!)\n'
               '• Kitchen ADJACENT to Storage\n'
               '• Zero dead/wasted space')
    ax.text(38, -5, callout, fontsize=5.5, va='top', color='#00695C',
            family='monospace', bbox=dict(boxstyle='round,pad=0.5', facecolor='#E0F2F1',
                                          edgecolor='#00897B', linewidth=1.5))

    # ── DIMENSIONS ──
    dim_line(ax, 0, 0, 42, 0, "42'-0\"", -2.5, 8, 'outside')
    dim_line(ax, 0, 0, 0, 38, "38'-0\" (incl. 8' veranda)", -4, 7, 'outside')
    dim_line(ax, 0, 8, 0, 38, "30'-0\" interior", -2, 6, 'outside')

    # Top (West wall)
    dim_line(ax, 0, 38, 16, 38, "16'-0\"", 2, 6.5)
    dim_line(ax, 16, 38, 26, 38, "10'-0\"", 2, 5.5)
    dim_line(ax, 26, 38, 42, 38, "16'-0\"", 2, 6.5)

    # Right (North wall)
    dim_line(ax, 42, 0, 42, 8, "8' Ver.", 2.5, 5.5)
    dim_line(ax, 42, 8, 42, 24, "16' Hall", 2.5, 6)
    dim_line(ax, 42, 24, 42, 38, "14' BR2", 2.5, 6)

    # ── VASTU + DIRECTION ──
    ax.text(21, -3, 'EAST (ROAD SIDE — Bhagamandala-Talakaveri Hwy)',
            fontsize=9, ha='center', color=C['blue'], fontweight='bold')
    ax.text(21, 41, 'WEST (COFFEE ESTATE / HILLS — Private, Views)',
            fontsize=9, ha='center', color=C['green'], fontweight='bold')
    ax.text(-5, 19, 'SOUTH', fontsize=7, ha='center', va='center', rotation=90, color='#888')
    ax.text(47, 19, 'NORTH', fontsize=7, ha='center', va='center', rotation=90, color='#888')

    compass(ax, 46, -3.5)

    vastu_text = ('VASTU OK\n'
                  '━━━━━━━━━━━\n'
                  'Door: EAST\n'
                  'Pooja: NE\n'
                  'Kitchen: SE\n'
                  'Master: SW\n'
                  'BR2: NW\n'
                  'Baths: Center\n'
                  'Stair: SW')
    ax.text(-5, 38, vastu_text, fontsize=5.5, va='top', color=C['vastu'],
            family='monospace', bbox=dict(boxstyle='round,pad=0.5', facecolor='#FFF3E0',
                                          edgecolor='#FFB74D', linewidth=1))

    plt.tight_layout()
    fig.savefig(os.path.join(OUT, 'GF_Plan_v4.png'), dpi=250, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print('Ground Floor Plan v4 saved')


# ============================================================
# V4 FIRST FLOOR PLAN
# ============================================================
# FF sits above: South row (16ft) + Service strip (10ft) = 26ft N-S
# FF width: 30 ft E-W (same as GF interior)
# + 8ft Sitout on WEST extending beyond footprint
#
# Coordinate system (same orientation as GF):
#   x: 0=South, 26=North (N-S = 26)
#   y: 8=East wall (no veranda on FF), 38=West wall
#   Sitout: y=38..46 (extending west)
#
# LAYOUT:
#   NORTH STRIP (x=16..26, 10ft, above GF service strip):
#     Work Room 14x10:    x=16..26, y=8..22
#     Passage 4x10:       x=16..26, y=22..26
#     Bath 3 (7x10):      x=16..26, y=26..33
#     Staircase 5x10:     x=16..26, y=33..38
#
#   SOUTH ROW (x=0..16, 16ft N-S):
#     Family Hall 14x16:  x=0..16, y=8..22
#     Master BR 16x16:    x=0..16, y=22..38
#
#   SITOUT: 26 x 8, y=38..46 (West, supported by pillars below)

def gen_ff():
    fig, ax = plt.subplots(1, 1, figsize=(22, 16))
    setup_ax(ax, (-6, 34), (-4, 52))

    title_block(ax, 'FIRST FLOOR PLAN (v4 — Master Suite + Work Room)',
                'FF Master BR 256sqft | Dedicated Work Room | Full-Width West Sitout | All dims in feet', 14, 50)

    # Room fills
    draw_room_fill(ax, 0, 8, 16, 14, C['family'])       # Family Hall
    draw_room_fill(ax, 0, 22, 16, 16, C['master'])       # Master BR
    draw_room_fill(ax, 16, 8, 10, 14, C['work'])         # Work Room
    draw_room_fill(ax, 16, 22, 10, 4, C['passage'])      # Passage/Landing
    draw_room_fill(ax, 16, 26, 10, 7, C['bath'], 0.3)    # Bath 3
    draw_room_fill(ax, 16, 33, 10, 5, C['stair'])        # Staircase

    # Sitout (extending west)
    draw_room_fill(ax, 0, 38, 26, 8, C['sitout'], 0.6)

    # ── EXTERNAL WALLS ──
    draw_wall(ax, 0, 8, 26, 8, WALL_EXT)       # East wall (road, solid)
    draw_wall(ax, 0, 38, 26, 38, WALL_EXT)     # West wall (before sitout)
    draw_wall(ax, 0, 8, 0, 38, WALL_EXT)       # South wall
    draw_wall(ax, 26, 8, 26, 38, WALL_EXT)     # North wall

    # Sitout walls (lightweight / railing)
    ax.plot([0, 0], [38, 46], color='#333', linewidth=1.5, linestyle='--')
    ax.plot([26, 26], [38, 46], color='#333', linewidth=1.5, linestyle='--')
    ax.plot([0, 26], [46, 46], color='#333', linewidth=2)  # Outer railing line

    # ── INTERNAL WALLS ──
    draw_wall(ax, 16, 8, 16, 38, WALL_INT)      # Work/Bath zone divider
    draw_wall(ax, 0, 22, 26, 22, WALL_INT)      # Family Hall / Master+Work divider
    draw_wall(ax, 16, 26, 26, 26, WALL_INT)     # Passage / Bath3 divider
    draw_wall(ax, 16, 33, 26, 33, WALL_INT)     # Bath3 / Staircase divider

    # ── BATH 3 ──
    draw_bath(ax, 16.5, 26.5, 9, 6, 'BATH 3\n(Master)', 7, actual_w=7, actual_h=10)
    furniture(ax, 17, 27, 4, 4, 'Shower\nEnclosure\n4\'x4\' Glass', '#B2DFDB')
    furniture(ax, 22, 27, 3, 3, 'WC\n(Commode)', '#B2DFDB')
    furniture(ax, 17, 31, 5, 1.3, 'Basin Counter 5\' Granite', '#B2DFDB')
    ax.text(24, 31, 'Geyser', fontsize=4, ha='center', color='#666')

    # ── ROOMS ──
    # Family Hall
    room_label(ax, 8, 15, 'FAMILY HALL / TV', "14' x 16' = 224 sqft", 10)
    furniture(ax, 1, 12, 7, 4, 'L-Shaped\nSofa', '#D7CCC8')
    furniture(ax, 10, 12, 4, 3, 'TV\nUnit', '#A1887F')
    furniture(ax, 1, 17, 5, 3, 'Book-\nshelf', '#D7CCC8')
    ax.text(8, 9.5, 'SOLID WALL EAST (Road privacy)', fontsize=5.5, ha='center',
            color='#C62828', fontweight='bold')

    # Master Bedroom (SW — YOUR main room)
    room_label(ax, 8, 32, 'MASTER BEDROOM', "16' x 16' = 256 sqft", 11)
    ax.text(8, 37, 'SW — Your Private Suite', fontsize=5.5, ha='center', color=C['vastu'])
    furniture(ax, 2, 30, 7, 5, 'King Bed\n6\'x6\'6"', '#C8E6C9')
    furniture(ax, 10, 30, 4, 6, 'Walk-in\nCloset\nArea', '#A5D6A7')
    furniture(ax, 2, 27, 3, 2.5, 'Dressing\nTable', '#C8E6C9')
    furniture(ax, 6, 23, 3, 2, 'Reading\nChair', '#E8F5E9')

    # Work Room
    room_label(ax, 21, 15, 'WORK / STUDY', "14' x 10' = 140 sqft", 9)
    ax.text(21, 12.5, 'Dedicated Home Office', fontsize=5.5, ha='center', color='#E65100')
    furniture(ax, 17, 16, 6, 3, 'L-Desk +\nMonitor', '#FFE082')
    furniture(ax, 24, 16, 1.5, 3, 'Book\nShelf', '#FFE082')
    furniture(ax, 17, 10, 4, 2.5, 'Filing +\nPrinter', '#FFF3E0')
    # Work room windows
    ax.text(21, 9, 'W: East (daylight) + North', fontsize=4.5, ha='center', color=C['window'])

    # Staircase
    room_label(ax, 21, 35, 'STAIR', "5'x10'", 7)
    for sy in np.arange(33.5, 37.5, 0.6):
        ax.plot([16.5, 25.5], [sy, sy], color='#999', linewidth=0.4)
    ax.text(21, 37.5, 'UP to\nTerrace', fontsize=5, ha='center', color='#666')
    ax.text(21, 33.5, 'DOWN to GF', fontsize=5, ha='center', color='#666')

    # Passage
    ax.text(21, 24, 'LANDING\n+ PASSAGE', fontsize=6, ha='center', color='#999')

    # ── SITOUT ──
    sitout_border = patches.Rectangle((0, 38), 26, 8, facecolor='none',
                                       edgecolor='#2E7D32', linewidth=2, linestyle='--')
    ax.add_patch(sitout_border)
    room_label(ax, 13, 42, 'COVERED SITOUT / JAGALI', "26' x 8' = 208 sqft\nPanoramic Coffee Estate + Hill Views", 11)
    ax.text(13, 39.5, 'WEST → Coffee Plantation + Western Ghats', fontsize=6,
            ha='center', color=C['green'], fontweight='bold')

    # Sitout safety railing
    for rx in np.arange(1, 26, 1):
        ax.plot([rx, rx], [46, 45.5], color='#444', linewidth=0.4)
    ax.text(13, 46.8, 'MS Grill Screen 6\' + 3.5\' Solid Parapet = 9.5\' Total Barrier (SAFETY)',
            fontsize=5.5, ha='center', color='#C62828', fontweight='bold')

    # Sitout furniture
    furniture(ax, 2, 40, 4, 3, 'Wooden\nSwing', '#AED581')
    furniture(ax, 8, 40, 5, 3, 'Daybed /\nDivan', '#AED581')
    furniture(ax, 15, 40, 3, 2, 'Coffee\nTable', '#AED581')
    furniture(ax, 20, 40, 4, 3, 'Chairs\n+ Plants', '#AED581')

    # Support pillars for sitout (below, shown as reference)
    for px in [4, 13, 22]:
        pillar = plt.Circle((px, 38.5), 0.3, facecolor='#5D3A1A', edgecolor='#3E2723',
                             linewidth=1, zorder=5)
        ax.add_patch(pillar)

    # ── WINDOWS ──
    draw_window_v(ax, 26, 12, 4)     # Work room north
    draw_window_h(ax, 20, 8, 4)      # Work room east
    draw_window_h(ax, 4, 8, 5)       # Family Hall east
    draw_window_v(ax, 26, 28, 4)     # Near Bath 3
    draw_window_h(ax, 4, 22, 4)      # Master BR south facing... actually this is internal divider
    draw_window_v(ax, 0, 28, 5)      # Master BR south wall
    draw_window_v(ax, 0, 12, 4)      # Family Hall south
    # Master west window (opens to sitout)
    draw_window_h(ax, 6, 38, 5)

    # ── DOORS ──
    draw_door_arc(ax, 8, 22, 3.5, 'right', 'h')    # Master BR door
    draw_door_arc(ax, 4, 22, 3, 'left', 'h')        # Family Hall / Master door
    draw_door_arc(ax, 18, 22, 3, 'right', 'h')      # Work room door from landing
    # Bath 3 door from Master
    draw_door_arc(ax, 14, 28, 2.5, 'left', 'h')
    ax.text(14, 27, 'Bath from\nMaster only', fontsize=4, ha='center', color=C['bath_border'])
    # Sitout access (French doors from Master)
    draw_door_arc(ax, 10, 38, 4, 'right', 'h')
    ax.text(12, 39, 'French Door\nto Sitout', fontsize=4, ha='left', color=C['green'])

    # ── DIMENSIONS ──
    dim_line(ax, 0, 8, 26, 8, "26'-0\" (N-S)", -2.5, 7, 'outside')
    dim_line(ax, 0, 8, 0, 38, "30'-0\" (E-W interior)", -3.5, 7, 'outside')
    dim_line(ax, 0, 38, 0, 46, "8'-0\" Sitout", -2, 6, 'outside')

    # Top dims
    dim_line(ax, 0, 46, 16, 46, "16'-0\"", 1.5, 6)
    dim_line(ax, 16, 46, 26, 46, "10'-0\"", 1.5, 5.5)

    # Right side
    dim_line(ax, 26, 8, 26, 22, "14' FamHall", 2.5, 5.5)
    dim_line(ax, 26, 22, 26, 38, "16' MasterBR", 2.5, 5.5)

    compass(ax, 30, -2)

    ax.text(13, -3, 'EAST (Road) — Solid Wall, NO balcony (Privacy + Safety)',
            fontsize=8, ha='center', color=C['blue'], fontweight='bold')

    # Area summary box
    area_text = ('FF AREA SUMMARY\n'
                 '━━━━━━━━━━━━━━━━━━━━━━\n'
                 'Master BR:   16x16 = 256 sqft\n'
                 'Bath 3:      7x10  =  70 sqft\n'
                 'Family Hall: 14x16 = 224 sqft\n'
                 'Work Room:   14x10 = 140 sqft\n'
                 'Staircase:   5x10  =  50 sqft\n'
                 'Passage:     4x10  =  40 sqft\n'
                 'Sitout:      26x8  = 208 sqft\n'
                 '━━━━━━━━━━━━━━━━━━━━━━\n'
                 'FF Interior:        780 sqft\n'
                 'FF + Sitout:        988 sqft')
    ax.text(30, 40, area_text, fontsize=5.5, va='top', color='#1A1A1A',
            family='monospace', bbox=dict(boxstyle='round,pad=0.5', facecolor='#F5F5F5',
                                          edgecolor='#999', linewidth=1))

    plt.tight_layout()
    fig.savefig(os.path.join(OUT, 'FF_Plan_v4.png'), dpi=250, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print('First Floor Plan v4 saved')


# ============================================================
# SITE LAYOUT (v4 — wider building)
# ============================================================
def gen_site():
    fig, ax = plt.subplots(1, 1, figsize=(16, 14))
    setup_ax(ax, (-6, 68), (-8, 58))

    title_block(ax, 'SITE LAYOUT PLAN (v4)',
                'Plot: 60\' x 50\' | Building: 42\' x 38\' | East-Facing | On Talakaveri Road Curve', 31, 56)

    # Plot
    plot = patches.Rectangle((0, 0), 60, 50, facecolor='#F5FFF5',
                             edgecolor='#333', linewidth=3)
    ax.add_patch(plot)

    # Compound wall (7ft solid on road side for curve safety)
    cw = patches.Rectangle((2, 2), 56, 46, facecolor='none',
                           edgecolor='#8D6E63', linewidth=1.5, linestyle='--')
    ax.add_patch(cw)
    ax.text(30, 49, 'COMPOUND WALL: 7\' SOLID laterite (road side) | 6\' solid (other sides)', fontsize=5.5,
            ha='center', color='#C62828', fontweight='bold')

    # House (42 x 38 including veranda)
    house = patches.Rectangle((12, 5), 42, 38, facecolor='#FFF5E1',
                              edgecolor='#333', linewidth=2.5)
    ax.add_patch(house)

    # Veranda highlight
    ver = patches.Rectangle((12, 5), 42, 8, facecolor=C['veranda'],
                            edgecolor='#8D6E63', linewidth=1, alpha=0.6)
    ax.add_patch(ver)
    ax.text(33, 9, 'PORCH / SITOUT (Jagali) 42\'x8\'', fontsize=6, ha='center', color='#BF360C')

    # FF Sitout on west side (extends beyond GF footprint)
    sitout = patches.Rectangle((12, 43), 26, 5, facecolor=C['sitout'],
                               edgecolor='#2E7D32', linewidth=1.5, linestyle='--', alpha=0.4)
    ax.add_patch(sitout)
    ax.text(25, 45.5, 'FF SITOUT (above)\n26\'x8\' — West Views', fontsize=5, ha='center', color='#2E7D32')

    room_label(ax, 33, 26, 'MAIN HOUSE G+1', "42' x 38' | ~2,576 sq.ft\nMangalore Tile Roof | v4 Layout", 12)

    # Steps
    for i in range(5):
        step = patches.Rectangle((26, 3 - i*0.4), 10, 0.4,
                                 facecolor='#BDBDBD', edgecolor='#9E9E9E', linewidth=0.3)
        ax.add_patch(step)
    ax.text(31, 1, 'Granite Steps (5 nos)', fontsize=5, ha='center', color='#666')

    # Garage
    garage = patches.Rectangle((4, 36), 7, 12, facecolor='#EEEEEE',
                               edgecolor='#666', linewidth=1.5)
    ax.add_patch(garage)
    room_label(ax, 7.5, 42, 'OPEN\nGARAGE', "15'x25'\n2 Cars", 7)

    # Tool shed
    shed = patches.Rectangle((4, 32), 7, 4, facecolor='#EFEBE9',
                             edgecolor='#795548', linewidth=1)
    ax.add_patch(shed)
    room_label(ax, 7.5, 34, 'SHED', "10'x8'", 6)

    # Coffee drying yard
    yard = patches.Rectangle((35, 38), 22, 10, facecolor='#FFF3E0',
                             edgecolor='#E65100', linewidth=1.5, linestyle='--')
    ax.add_patch(yard)
    room_label(ax, 46, 43, 'COFFEE DRYING\nYARD', "30'x20' PCC\n+ Retractable Roof", 8)

    # Septic
    septic = plt.Circle((5, 25), 1.5, facecolor='#FFCDD2', edgecolor='#C62828', linewidth=1)
    ax.add_patch(septic)
    ax.text(5, 25, 'SEPTIC', fontsize=5, ha='center', fontweight='bold', color='#B71C1C')

    # Well
    well = plt.Circle((5, 18), 1.5, facecolor='#BBDEFB', edgecolor='#1565C0', linewidth=1)
    ax.add_patch(well)
    ax.text(5, 18, 'WELL', fontsize=5, ha='center', fontweight='bold', color='#0D47A1')

    # Tulsi
    tulsi = plt.Circle((53, 44), 1.5, facecolor='#C8E6C9', edgecolor='#2E7D32', linewidth=1.5)
    ax.add_patch(tulsi)
    ax.text(53, 44, 'Tulsi', fontsize=5, ha='center', fontweight='bold', color='#1B5E20')

    # Solar
    ax.text(33, 35, 'SOLAR 3kW on South Roof Slope', fontsize=5.5, ha='center',
            color='#E65100', bbox=dict(boxstyle='round', facecolor='#FFF3E0', edgecolor='#FF9800', pad=0.3))

    # Garden
    ax.text(8, 12, 'GARDEN\nLAWN', fontsize=7, ha='center', color='#2E7D32', style='italic')

    # CCTV markers
    for cx, cy, label in [(14, 5, 'CAM1\nGate'), (54, 5, 'CAM2\nRoad'), (33, 43, 'CAM3\nBack'), (8, 42, 'CAM4\nPark')]:
        ax.plot(cx, cy, 'rv', markersize=6, zorder=5)
        ax.text(cx, cy-1.5, label, fontsize=3.5, ha='center', color='#C62828')

    # Gate
    gate = patches.Rectangle((24, -0.5), 12, 2, facecolor='#424242', edgecolor='#212121', linewidth=2)
    ax.add_patch(gate)
    ax.text(30, 0.5, 'MAIN GATE\n12\' Vehicle + 4\' Ped.\nSET BACK from curve!', fontsize=5.5,
            ha='center', color='white', fontweight='bold')

    # Road (curved representation)
    road = patches.Rectangle((-4, -6), 72, 4, facecolor='#757575')
    ax.add_patch(road)
    ax.plot([-4, 68], [-4, -4], color='#FFD600', linewidth=1, linestyle='--')
    ax.text(31, -4, 'BHAGAMANDALA—TALAKAVERI ROAD (CURVE — CAUTION!)', fontsize=8,
            ha='center', color='white', fontweight='bold')

    # Safety callout
    safety = ('SAFETY (Isolated + Highway Curve)\n'
              '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'
              '• 7\' solid wall on road side (crash protection)\n'
              '• CCTV: 4 cameras (gate, road, back, parking)\n'
              '• Motion sensor LED floods (front + back)\n'
              '• MS grills on ALL windows (12mm bars)\n'
              '• Reflectors on compound wall (night visibility)\n'
              '• Gate set back from curve apex')
    ax.text(62, 30, safety, fontsize=5, va='top', color='#B71C1C',
            family='monospace', bbox=dict(boxstyle='round,pad=0.5', facecolor='#FFEBEE',
                                          edgecolor='#E53935', linewidth=1))

    dim_line(ax, 0, 0, 60, 0, "60'-0\"", -7, 8, 'outside')
    dim_line(ax, 0, 0, 0, 50, "50'-0\"", -4.5, 8, 'outside')

    compass(ax, 62, -5)

    plt.tight_layout()
    fig.savefig(os.path.join(OUT, 'Site_Layout_v4.png'), dpi=250, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print('Site Layout v4 saved')


# ============================================================
# FRONT ELEVATION (v4 — wider building)
# ============================================================
def gen_front_elev():
    fig, ax = plt.subplots(1, 1, figsize=(20, 12))
    setup_ax(ax, (-3, 49), (-4, 30))

    title_block(ax, 'FRONT ELEVATION (EAST — ROAD SIDE) v4',
                'Bhagamandala House | 42\' Wide | Solid FF Wall | Safety Design', 23, 28.5)

    # Ground
    ax.plot([-2, 48], [0, 0], color='#333', linewidth=2)
    ax.fill_between([-2, 48], [-1], [0], color='#8D6E63', alpha=0.3)

    # Plinth
    plinth = patches.Rectangle((1, 0), 42, 4, facecolor='#909090', edgecolor='#555', linewidth=1.5)
    ax.add_patch(plinth)
    ax.text(22, 2, 'KADAPPA STONE CLADDING — 4\' PLINTH', fontsize=7, ha='center', color='white', fontweight='bold')

    # Steps
    for i in range(5):
        w = 8 + i * 1.6
        x = 22 - w/2
        step = patches.Rectangle((x, i * 0.8), w, 0.8,
                                 facecolor='#BDBDBD', edgecolor='#999', linewidth=0.5)
        ax.add_patch(step)

    # GF wall
    gf_wall = patches.Rectangle((1, 4), 42, 10, facecolor='#FFF5E1', edgecolor='#999', linewidth=1)
    ax.add_patch(gf_wall)

    # Wooden pillars (5 nos for wider veranda)
    for px in [5, 13.5, 22, 30.5, 39]:
        pts = np.array([[px-0.7, 4.5], [px+0.7, 4.5], [px+0.5, 13.8], [px-0.5, 13.8]])
        pillar = patches.Polygon(pts, facecolor='#5D3A1A', edgecolor='#3E2723', linewidth=1.5)
        ax.add_patch(pillar)
        cap = patches.Rectangle((px-0.9, 13.5), 1.8, 0.5, facecolor='#5D3A1A', edgecolor='#3E2723', linewidth=1)
        ax.add_patch(cap)

    # Main door
    door = patches.Rectangle((20, 4.5), 4, 7, facecolor='#5D3A1A', edgecolor='#3E2723', linewidth=2)
    ax.add_patch(door)
    ax.plot([22, 22], [4.5, 11.5], color='#3E2723', linewidth=1)
    ax.text(22, 4, 'MAIN DOOR 4\'x7\' TEAK', fontsize=5.5, ha='center', color=C['door'], fontweight='bold')

    # GF windows
    for wx in [8, 34]:
        win = patches.Rectangle((wx, 7), 5, 4, facecolor='#BBDEFB', edgecolor='#666', linewidth=1)
        ax.add_patch(win)
        ax.plot([wx+2.5, wx+2.5], [7, 11], color='#666', linewidth=0.5)

    ax.text(22, 13, 'PORCH / SITOUT (Jagali) — 42\'x8\' | 5 Chadara Kamba Pillars', fontsize=6,
            ha='center', color='#795548', style='italic')

    # FF slab line
    ax.plot([1, 43], [14, 14], color='#333', linewidth=2.5)

    # FF wall (solid — no balcony on road side)
    ff_wall = patches.Rectangle((5, 14), 34, 8, facecolor='#FFF5E1', edgecolor='#999', linewidth=1)
    ax.add_patch(ff_wall)
    ax.text(22, 21.5, 'SOLID WALL — NO BALCONY (Privacy + Safety from Highway)', fontsize=6.5,
            ha='center', color='#C62828', fontweight='bold')

    # FF windows (smaller, higher for privacy)
    for wx in [8, 16, 24, 32]:
        win = patches.Rectangle((wx, 17), 4, 3, facecolor='#BBDEFB', edgecolor='#666', linewidth=1)
        ax.add_patch(win)
        # MS grill overlay
        for gx in np.arange(wx+0.5, wx+4, 0.5):
            ax.plot([gx, gx], [17, 20], color='#555', linewidth=0.3)
    ax.text(22, 16, 'MS GRILLS on ALL windows (Safety — isolated house)', fontsize=5,
            ha='center', color='#555')

    # Roof
    roof_pts = np.array([[-1, 22], [45, 22], [37, 26.5], [7, 26.5]])
    roof = patches.Polygon(roof_pts, facecolor='#CC5500', edgecolor='#8B2500', linewidth=2.5)
    ax.add_patch(roof)
    ax.plot([7, 37], [26.5, 26.5], color='#5D1F00', linewidth=3)
    ax.text(22, 24, 'MANGALORE CLAY TILES | 30° Hip Roof | 5\' Overhang', fontsize=7,
            ha='center', color='white', fontweight='bold')

    # Solar panels on south slope
    for i in range(3):
        solar = patches.Rectangle((8 + i*3.5, 22.8 + i*0.4), 3, 0.8,
                                  facecolor='#1E3A5F', edgecolor='#0D47A1', linewidth=0.5, alpha=0.85)
        ax.add_patch(solar)

    # Dimensions
    dim_line(ax, 43, 0, 43, 4, "4' Plinth", 3, 6)
    dim_line(ax, 43, 4, 43, 14, "10' GF", 3, 6)
    dim_line(ax, 43, 14, 43, 22, "8' FF", 3, 6)
    dim_line(ax, 1, 0, 43, 0, "42'-0\"", -3, 8, 'outside')

    plt.tight_layout()
    fig.savefig(os.path.join(OUT, 'Front_Elevation_v4.png'), dpi=250, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print('Front Elevation v4 saved')


# ============================================================
# BACK ELEVATION (v4 — sitout instead of 2 balconies)
# ============================================================
def gen_back_elev():
    fig, ax = plt.subplots(1, 1, figsize=(20, 12))
    setup_ax(ax, (-3, 49), (-3, 30))

    title_block(ax, 'BACK ELEVATION (WEST — COFFEE ESTATE) v4',
                'Full-Width Sitout | Plantation + Hill Views | Safety Grill Screen', 23, 28.5)

    ax.plot([-2, 48], [0, 0], color='#333', linewidth=2)
    ax.fill_between([-2, 48], [-1], [0], color='#8D6E63', alpha=0.3)

    # Plinth
    plinth = patches.Rectangle((1, 0), 42, 4, facecolor='#909090', edgecolor='#555', linewidth=1.5)
    ax.add_patch(plinth)
    ax.text(22, 2, 'KADAPPA STONE PLINTH 4\'', fontsize=7, ha='center', color='white', fontweight='bold')

    # GF wall
    gf = patches.Rectangle((1, 4), 42, 10, facecolor='#FFF5E1', edgecolor='#999', linewidth=1)
    ax.add_patch(gf)

    # GF windows
    for wx in [4, 12, 20, 28, 36]:
        win = patches.Rectangle((wx, 7), 4, 3.5, facecolor='#BBDEFB', edgecolor='#666', linewidth=1)
        ax.add_patch(win)

    # FF slab
    ax.plot([1, 43], [14, 14], color='#333', linewidth=2.5)

    # FF wall
    ff = patches.Rectangle((5, 14), 34, 8, facecolor='#FFF5E1', edgecolor='#999', linewidth=1)
    ax.add_patch(ff)

    # SITOUT (full width, replacing 2 small balconies)
    sitout = patches.Rectangle((5, 14.5), 28, 3, facecolor='#DCEDC8', edgecolor='#333', linewidth=1.5)
    ax.add_patch(sitout)
    ax.text(19, 16, 'COVERED SITOUT 26\'x8\' — Full-Width West-Facing', fontsize=7,
            ha='center', fontweight='bold', color='#33691E')

    # Parapet wall (3.5ft solid)
    ax.fill_between([5, 33], [14.5], [15.5], color='#BDBDBD', alpha=0.5)
    ax.text(19, 14.8, '3.5\' Solid Parapet', fontsize=4.5, ha='center', color='#555')

    # MS grill screen above parapet (6ft)
    for rx in np.arange(5.5, 33, 0.8):
        ax.plot([rx, rx], [15.5, 17.5], color='#444', linewidth=0.3)
    ax.text(19, 18, '6\' MS Grill Screen (Safety)', fontsize=5.5, ha='center', color='#C62828')

    # Swing visible in sitout
    furniture(ax, 8, 15.5, 4, 1.5, 'Swing', '#AED581')
    furniture(ax, 15, 15.5, 5, 1.5, 'Daybed', '#AED581')
    furniture(ax, 23, 15.5, 4, 1.5, 'Chairs', '#AED581')

    # FF windows above sitout
    for wx in [10, 22, 30]:
        win = patches.Rectangle((wx, 19), 4, 2.5, facecolor='#BBDEFB', edgecolor='#666', linewidth=1)
        ax.add_patch(win)

    # Roof
    roof_pts = np.array([[-1, 22], [45, 22], [37, 26.5], [7, 26.5]])
    roof = patches.Polygon(roof_pts, facecolor='#CC5500', edgecolor='#8B2500', linewidth=2.5)
    ax.add_patch(roof)
    ax.plot([7, 37], [26.5, 26.5], color='#5D1F00', linewidth=3)
    ax.text(22, 24, 'MANGALORE CLAY TILES | Hip Roof | 5\' Overhang covers Sitout', fontsize=6.5,
            ha='center', color='white', fontweight='bold')

    # Terrace indicator
    terrace = FancyBboxPatch((32, 22.5), 5, 2, boxstyle="round,pad=0.2",
                             facecolor='#B0BEC5', edgecolor='#37474F', linewidth=1.5, alpha=0.9)
    ax.add_patch(terrace)
    ax.text(34.5, 23.5, 'TERRACE\n12x10', fontsize=5, ha='center', color='#1A1A1A', fontweight='bold')

    # Support pillars for sitout
    for px in [8, 19, 30]:
        pts = np.array([[px-0.5, 4], [px+0.5, 4], [px+0.4, 14.5], [px-0.4, 14.5]])
        pillar = patches.Polygon(pts, facecolor='#5D3A1A', edgecolor='#3E2723', linewidth=1)
        ax.add_patch(pillar)
    ax.text(19, 13.5, 'Support pillars for sitout', fontsize=4.5, ha='center', color='#795548')

    ax.text(22, -2, 'VIEW: Coffee Estate & Western Ghats Hills — All-Season Outdoor Living',
            fontsize=9, ha='center', color=C['green'], fontweight='bold')

    dim_line(ax, 1, 0, 43, 0, "42'-0\"", -2, 8, 'outside')
    dim_line(ax, 5, 14.5, 33, 14.5, "26'-0\" Sitout", -1, 6, 'outside')

    plt.tight_layout()
    fig.savefig(os.path.join(OUT, 'Back_Elevation_v4.png'), dpi=250, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print('Back Elevation v4 saved')


# ============================================================
# ROOF PLAN (v4 — with terrace)
# ============================================================
def gen_roof():
    fig, ax = plt.subplots(1, 1, figsize=(14, 12))
    setup_ax(ax, (-4, 50), (-6, 42))

    title_block(ax, 'ROOF PLAN + SOLAR + TERRACE (v4)',
                'Hip Roof 30° | Mangalore Tiles | 5\' Overhang | Partial Terrace over Stair', 23, 40)

    # Roof outline (larger than building due to overhang)
    outer = patches.Polygon([(0, 0), (46, 0), (46, 36), (0, 36)],
                           facecolor='#CC5500', edgecolor='#8B2500', linewidth=3, alpha=0.8)
    ax.add_patch(outer)

    # Ridge
    ax.plot([14, 32], [18, 18], color='#5D1F00', linewidth=4)
    ax.text(23, 18, 'RIDGE LINE', fontsize=7, ha='center', color='white',
            fontweight='bold', bbox=dict(facecolor='#5D1F00', edgecolor='none', pad=2))

    # Hip lines
    for corner, ridge in [((0,0),(14,18)), ((46,0),(32,18)), ((0,36),(14,18)), ((46,36),(32,18))]:
        ax.plot([corner[0], ridge[0]], [corner[1], ridge[1]], color='#8B4513', linewidth=1.5, linestyle='--')

    # Slope labels
    ax.text(23, 7, 'SOUTH SLOPE (Solar panels here)', fontsize=10, ha='center', color='white', fontweight='bold')
    ax.text(23, 29, 'NORTH SLOPE', fontsize=10, ha='center', color='white', fontweight='bold')

    # Solar panels
    for i in range(6):
        col, row = i % 3, i // 3
        sx, sy = 14 + col * 6, 3 + row * 5
        panel = FancyBboxPatch((sx, sy), 5, 3.5, boxstyle="round,pad=0.1",
                               facecolor='#1E3A5F', edgecolor='#0D47A1', linewidth=1.5, alpha=0.9)
        ax.add_patch(panel)
        ax.text(sx+2.5, sy+1.75, f'Panel {i+1}\n500W', fontsize=6, ha='center', color='white', fontweight='bold')

    # Partial Terrace
    terrace = FancyBboxPatch((1, 1), 10, 8, boxstyle="round,pad=0.2",
                             facecolor='#B0BEC5', edgecolor='#37474F', linewidth=2, alpha=0.9)
    ax.add_patch(terrace)
    ax.text(6, 5, 'PARTIAL\nTERRACE\n12×10 ft', fontsize=7, ha='center', color='#1A1A1A', fontweight='bold')
    ax.text(6, 2, 'RCC slab\n+ Pergola\nStair access', fontsize=5, ha='center', color='#455A64')

    # Gutters
    for side in [(0,0,0,36), (46,0,46,36), (0,0,46,0), (0,36,46,36)]:
        ax.plot([side[0],side[2]], [side[1],side[3]], color='#5D4037', linewidth=5, alpha=0.2)
    ax.text(23, -1, 'PVC Rain Gutters → RWH Sump (5,000L)', fontsize=5.5, ha='center', color='#5D4037')

    # Info box
    specs = ('SOLAR: 3 kW Grid-Tied | 6 x 500W Mono\n'
             'South slope for max sun | Hybrid Inverter\n'
             'Subsidy: 40% (Karnataka) | Net metering CESCOM')
    ax.text(23, -3.5, specs, fontsize=7, ha='center',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#FFF8E1', edgecolor='#FFA000', linewidth=1.5))

    compass(ax, 44, -3)

    plt.tight_layout()
    fig.savefig(os.path.join(OUT, 'Roof_Solar_v4.png'), dpi=250, bbox_inches='tight', facecolor='white')
    plt.close()
    print('Roof + Solar v4 saved')


# ============================================================
# MAIN
# ============================================================
if __name__ == '__main__':
    print('Generating v4 architectural plans...\n')
    print('V4: Wider footprint, back-to-back baths, rectangular BRs,')
    print('    FF work room, west sitout, safety features\n')
    gen_gf()
    gen_ff()
    gen_site()
    gen_front_elev()
    gen_back_elev()
    gen_roof()
    print(f'\nAll v4 plans saved to: {OUT}')
