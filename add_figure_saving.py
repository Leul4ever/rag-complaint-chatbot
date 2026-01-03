import json
import os

nb_path = 'notebooks/Task_1_EDA_and_Preprocessing.ipynb'

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']

# Find the product distribution plot cell and add save code
for i, cell in enumerate(cells):
    if cell['cell_type'] == 'code':
        source = "".join(cell['source'])
        
        # Product distribution plot
        if 'Distribution of Complaints by Product' in source and 'plt.show()' in source:
            # Add save command before plt.show()
            new_source = source.replace(
                'plt.show()',
                "plt.savefig('../reports/figures/product_distribution.png', dpi=300, bbox_inches='tight')\nplt.show()"
            )
            cell['source'] = new_source.split('\n')
            print(f"Updated product distribution plot at cell {i}")
        
        # Narrative length plot
        elif 'Distribution of Complaint Narrative Word Counts' in source and 'plt.show()' in source:
            new_source = source.replace(
                'plt.show()',
                "plt.savefig('../reports/figures/narrative_length_distribution.png', dpi=300, bbox_inches='tight')\nplt.show()"
            )
            cell['source'] = new_source.split('\n')
            print(f"Updated narrative length plot at cell {i}")

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print("Notebook updated successfully!")
