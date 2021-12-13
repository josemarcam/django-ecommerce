from django.db import models
from djmoney.models.fields import MoneyField
from model_utils.models import TimeStampedModel
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse

from users.models import User
from projects.models import ProjectPhase

# Create your models here.

class Activity(TimeStampedModel):
    
    class ActivityType(models.TextChoices):
        INFORMATIVO = 'IN', _('Informative')
        TRIBUTARIO = 'TR', _('Tributary')

    name = models.CharField(_("Activity Name"), max_length=250)
    short_description = models.TextField(_("Shprt Activity Description"), max_length=100,default="Descrição breve")
    description = models.TextField(_("Activity Description"), max_length=1000)
    creator = models.ForeignKey(User, related_name="activities", on_delete=models.CASCADE)
    phase = models.ForeignKey(ProjectPhase, related_name="activities", on_delete=models.CASCADE)
    type = models.CharField(
        max_length=2,
        choices=ActivityType.choices,
        default=ActivityType.INFORMATIVO,
    )
    cust = MoneyField(
        _("Cust"),
        help_text=_('a cust that affects the budget of the phase.'),
        decimal_places=2,
        default=0,
        default_currency='BRL',
        max_digits=11,
    )
    
    class Meta:
        ordering=("-created",)

    def __str__(self):
        return f"{self.name}"

    def get_activity_detail_url(self):
        return reverse("activities:details", kwargs={"activity_id":self.id})
    
    def get_type_name(self):
        return self.ActivityType(self.type).name
