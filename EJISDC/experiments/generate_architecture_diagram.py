"""
Generate architecture diagram for EJISDC paper.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import os

# Setup
fig, ax = plt.subplots(figsize=(14, 8))
ax.set_xlim(0, 14)
ax.set_ylim(0, 8)
ax.axis('off')

# Colors
erp_color = '#3498db'       # Blue
config_color = '#2ecc71'    # Green
process_color = '#9b59b6'   # Purple
output_color = '#e74c3c'    # Red
arrow_color = '#34495e'     # Dark gray

def draw_box(ax, x, y, width, height, text, color, fontsize=10):
    """Draw a rounded rectangle with text."""
    box = FancyBboxPatch((x, y), width, height, 
                          boxstyle="round,pad=0.02,rounding_size=0.2",
                          facecolor=color, edgecolor='black', linewidth=2, alpha=0.8)
    ax.add_patch(box)
    ax.text(x + width/2, y + height/2, text, ha='center', va='center', 
            fontsize=fontsize, fontweight='bold', color='white', wrap=True)

def draw_arrow(ax, start, end):
    """Draw an arrow between points."""
    ax.annotate('', xy=end, xytext=start,
                arrowprops=dict(arrowstyle='->', color=arrow_color, lw=2))

# Title
ax.text(7, 7.5, 'ERP-ProcessMiner Architecture', ha='center', fontsize=16, fontweight='bold')

# Layer 1: ERP Data Sources
draw_box(ax, 0.5, 5.5, 2.5, 1.2, 'PO Header\n(CSV)', erp_color)
draw_box(ax, 3.2, 5.5, 2.5, 1.2, 'Goods Receipt\n(CSV)', erp_color)
draw_box(ax, 5.9, 5.5, 2.5, 1.2, 'Invoice\n(CSV)', erp_color)

# ERP Layer label
ax.text(4.5, 7, 'ERP Data Exports', ha='center', fontsize=12, fontstyle='italic')

# Layer 2: Declarative Configuration
draw_box(ax, 9.5, 5.5, 4, 1.2, 'Declarative JSON\nConfiguration', config_color)

# Arrows to configuration validation
draw_arrow(ax, (2.75, 5.5), (10.5, 5.5))
draw_arrow(ax, (4.45, 5.5), (10.5, 5.5))
draw_arrow(ax, (7.15, 5.5), (10.5, 5.5))

# Layer 3: Core Processing
draw_box(ax, 0.5, 3, 3, 1.2, 'Data Loaders\n& Validation', process_color)
draw_box(ax, 4, 3, 3, 1.2, 'Event Log\nConstruction', process_color)
draw_box(ax, 7.5, 3, 3, 1.2, 'Process\nDiscovery', process_color)
draw_box(ax, 11, 3, 2.5, 1.2, 'Conformance\nChecking', process_color)

# Arrows for processing flow
draw_arrow(ax, (11.5, 5.5), (2, 4.2))
draw_arrow(ax, (3.5, 3.6), (4, 3.6))
draw_arrow(ax, (7, 3.6), (7.5, 3.6))
draw_arrow(ax, (10.5, 3.6), (11, 3.6))

# Layer 4: Outputs
draw_box(ax, 1, 0.5, 2.5, 1.2, 'Event Log\n(XES/CSV)', output_color)
draw_box(ax, 4, 0.5, 2.5, 1.2, 'DFG\nVisualization', output_color)
draw_box(ax, 7, 0.5, 2.5, 1.2, 'Petri Net\nModel', output_color)
draw_box(ax, 10, 0.5, 3, 1.2, 'Conformance\nReport', output_color)

# Arrows to outputs
draw_arrow(ax, (5.5, 3), (2.25, 1.7))
draw_arrow(ax, (9, 3), (5.25, 1.7))
draw_arrow(ax, (9, 3), (8.25, 1.7))
draw_arrow(ax, (12.25, 3), (11.5, 1.7))

# Legend
legend_elements = [
    mpatches.Patch(facecolor=erp_color, edgecolor='black', label='ERP Data'),
    mpatches.Patch(facecolor=config_color, edgecolor='black', label='Configuration'),
    mpatches.Patch(facecolor=process_color, edgecolor='black', label='Processing'),
    mpatches.Patch(facecolor=output_color, edgecolor='black', label='Outputs')
]
ax.legend(handles=legend_elements, loc='lower right', fontsize=10)

plt.tight_layout()

# Save
output_dir = r"C:\Users\aleke\Documents\My_Devs_IDE\17. My OpenSource Projects\1. erp-process-mining-tkit_ACMs_\paper"
plt.savefig(os.path.join(output_dir, 'architecture_diagram.png'), dpi=300, bbox_inches='tight', 
            facecolor='white', edgecolor='none')
plt.savefig(os.path.join(output_dir, 'architecture_diagram.pdf'), bbox_inches='tight',
            facecolor='white', edgecolor='none')
print("Architecture diagram saved!")
