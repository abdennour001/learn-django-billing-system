from django.db import models
from django import utils
import datetime

# Create your models here.

class Client(models.Model):
    SEXE = (
        ('M', 'Masculin'),
        ('F', 'Feminin')
    )
    nom = models.CharField(max_length=50, null=True, blank=True)
    prenom = models.CharField(max_length=50, null=True, blank=True)
    adresse = models.TextField(null=True, blank=True)
    tel = models.CharField(max_length = 10, null=True, blank=True)
    sexe = models.CharField(max_length=1, choices = SEXE)
    
    def __str__(self):
        return self.nom + ' ' + self.prenom

    def get_chiffre(self):
        return sum(l.get_total() for l in self.facture_set.all())


class Fournisseur(models.Model):
    """
    Model Fournisseur
    """
    nom = models.CharField(max_length=50, null=True, blank=True)
    prenom = models.CharField(max_length=50, null=True, blank=True)
    adresse = models.TextField(null=True, blank=True)
    tel = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.nom + ' ' + self.prenom

class Produit(models.Model):
    designation = models.CharField(max_length=50)
    prix = models.FloatField(default=0)

    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE, related_name='produits', blank=True)

    def __str__(self):
        return f"{self.designation}, {self.fournisseur}"
    
    
class Facture(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateField(default=utils.timezone.now)

    # add __str__ magic method to facture.
    def __str__(self):
        return f"Client: {self.client}, {self.date}"

    """
    get total price of this facture.
    we used the aggregate function with the F class of models package so we can produce one query that
    basically sum the product of the price of a product and it quantity.
    """
    def get_total(self):
        total = self.lignes.all().aggregate(
            total=models.Sum(models.F("produit__prix") * models.F("qte"), output_field=models.FloatField()))['total']
        return total if total is not None else 0.0

class LigneFacture(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    qte = models.IntegerField(default=1)
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE, related_name='lignes')
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['produit', 'facture'], name="produit-facture")
        ]

    def __str__(self):
        return f"{self.produit}, {self.qte}, {self.facture}"