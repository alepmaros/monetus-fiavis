from django.db import models

class Acoes(models.Model):
    """
    Modelo das ações
    """

    codigo = models.CharField(max_length=10)
    hora   = models.DateTimeField(blank=False, null=False)

    vopen   = models.DecimalField(max_digits = 7, decimal_places = 4)
    vhigh   = models.DecimalField(max_digits = 7, decimal_places = 4)
    vlow    = models.DecimalField(max_digits = 7, decimal_places = 4)
    vclose  = models.DecimalField(max_digits = 7, decimal_places = 4)