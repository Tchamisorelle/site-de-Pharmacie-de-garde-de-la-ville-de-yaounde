from django.contrib import admin
from .models import formulaire_utilisateurr

# Register your models here.
class FormulaireUtilisateurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'sexe', 'mail', 'qualification_chercheur', 'qualification_mentor', 'pays')
    list_filter = ('sexe', 'qualification_chercheur', 'qualification_mentor', 'pays')
    search_fields = ('nom', 'prenom', 'mail')

admin.site.register(formulaire_utilisateurr, FormulaireUtilisateurAdmin)
