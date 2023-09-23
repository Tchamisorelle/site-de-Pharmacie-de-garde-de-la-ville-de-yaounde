from django.db import models
from django.contrib.auth import get_user_model  
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone

# Create your models here.
#from django.db import models

class formulaire_utilisateurr(AbstractUser):
    nom = models.CharField(max_length=20)
    prenom = models.CharField(max_length=20)
    sexe = models.CharField(max_length=6, choices=[('homme', 'Homme'), ('femme', 'Femme')])
    mail = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    qualification_chercheur = models.BooleanField(default=False)
    qualification_mentor = models.BooleanField(default=False)
    pays = models.CharField(max_length=50)
    
    #last_login = models.DateTimeField(blank=True, null=True)
    groups = models.ManyToManyField(Group, verbose_name="Groupes", blank=True, related_name="utilisateur")
    user_permissions = models.ManyToManyField(Permission, verbose_name="Permissions", blank=True, related_name="utilisateur")

    username = models.CharField(
        max_length=30,
        unique=False,
        # ... autres options ...
    )

    def __str__(self):
        return self.nom + " " + self.prenom
    
    class Meta:
        db_table = 'formulaire_utilisateurr' 

        
class ResetLink(models.Model):
    user = models.ForeignKey(formulaire_utilisateurr, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    expiration_time = models.DateTimeField()
    def __str__(self):
        return f"ResetLink for {self.user}"

    def is_valid(self):
        return timezone.now() <= self.expiration_time

class PharmacieDeGarde(models.Model):
    plage = models.CharField(max_length=100)
    pharmacie = models.CharField(max_length=200)
    telephone1= models.CharField(max_length=20)
    telephone2 = models.CharField(max_length=20)
    telephone3 = models.CharField(max_length=20)
    localisation = models.CharField(max_length=200)