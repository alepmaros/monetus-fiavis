from django.db import models

# Should be refactored later

class Day(models.Model):

    time    = models.DateTimeField(blank=False, null=False, unique=True)
    vcp     = models.FloatField(blank=True, null=True)
    updated = models.BooleanField(default=False, null=False)

    def __str__(self):
        return '%s' % (self.time)

    class Meta:
        ordering = ['-time']

class Stock(models.Model):
    """
    Modelo das ações
    """

    code   = models.CharField(max_length=10)
    day    = models.ForeignKey(Day, on_delete=models.CASCADE)

    # Value ...
    vcp     = models.FloatField(blank=False, null=False)
    vopen   = models.FloatField(blank=False, null=False)
    vhigh   = models.FloatField(blank=False, null=False)
    vlow    = models.FloatField(blank=False, null=False)
    vclose  = models.FloatField(blank=False, null=False)

    # Fund Share
    fshare  = models.FloatField(blank=False, null=False)

    class Meta:
        ordering = ['-fshare']