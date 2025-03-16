"""
Tree taxonomy data and helper functions
"""

TREES = [
    ("Albizia", "Albizia", "julibrissim", "images/albizia.jpg"),
    ("Ailante", "Ailanthus", "altissima", "images/ailante.jpg"),
    ("Aulne glutineux", "Alnus", "glutinosa", "images/aulne.jpg"),
    ("Arbre de Judée", "Cercis", "siliquastrum", "images/arbre_judee.jpg"),
    ("Chêne pédonculé", "Quercus", "robur", "images/chene.jpg"),
    ("Érable sycomore", "Acer", "pseudoplatanus", "images/erable.jpg"),
    ("Hêtre", "Fagus", "sylvatica", "images/hetre.jpg"),
    ("Pin sylvestre", "Pinus", "sylvestris", "images/pin.jpg"),
    ("Saule pleureur", "Salix", "alba 'Tristis'", "images/saule.jpg"),
    ("Bouleau verruqueux", "Betula", "pendula", "images/bouleau.jpg"),
    ("Charme commun", "Carpinus", "betulus", "images/charme.jpg"),
    ("Marronnier d'Inde", "Aesculus", "hippocastanum", "images/marronnier.jpg"),
    ("Tilleul à grandes feuilles", "Tilia", "platyphyllos", "images/tilleul.jpg"),
    ("Robinier faux-acacia", "Robinia", "pseudoacacia", "images/robinier.jpg"),
    ("Platane commun", "Platanus", "x hispanica", "images/platane.jpg"),
    ("Orme champêtre", "Ulmus", "minor", "images/orme.jpg"),
    ("Peuplier noir", "Populus", "nigra", "images/peuplier.jpg"),
    ("If commun", "Taxus", "baccata", "images/if.jpg")
]

HELP_TEXT = """
Guide d'utilisation:

1. Choisissez un niveau de difficulté :
   - Facile : Un élément à deviner, tous les autres indices visibles
   - Moyen : Deux éléments à deviner, un indice visible

2. Pour chaque question :
   - Le nom commun (en français)
   - Le genre (en latin)
   - L'espèce (en latin)
3. Entrez votre réponse dans le champ texte
4. Cliquez sur 'Valider' ou appuyez sur Entrée
5. Pour passer à une nouvelle question, cliquez sur 'Nouvelle question'

Conseils:
- Les accents sont importants pour les noms français
- Vous avez trois essais avant que la réponse ne soit révélée
"""

DIFFICULTY_LEVELS = {
    'facile': 1,    # Number of elements to guess
    'moyen': 2
}