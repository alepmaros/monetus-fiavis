from django.db import models

class Stock(models.Model):
    """
    Modelo das ações
    """

    code   = models.CharField(max_length=10)
    time   = models.DateTimeField(blank=False, null=False)

    vcp     = models.FloatField(blank=False, null=False)
    vopen   = models.FloatField(blank=False, null=False)
    vhigh   = models.FloatField(blank=False, null=False)
    vlow    = models.FloatField(blank=False, null=False)
    vclose  = models.FloatField(blank=False, null=False)

    fshare  = models.FloatField(blank=False, null=False)

    class Meta:
        ordering = ['-time', '-fshare']