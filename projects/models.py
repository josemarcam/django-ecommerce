from django.contrib.auth.models import Permission
from django.db.models import Q
from djmoney.models.fields import MoneyField
from users.models import User
from decimal import Decimal
from django.db import models
from model_utils.models import TimeStampedModel
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse

class Project(TimeStampedModel):
    
    name = models.CharField(_("Project Name"), max_length=250)
    description = models.TextField(_("Project Description"), max_length=1000)
    users = models.ManyToManyField(
        User, 
        help_text=_('Users that are related with this project'),
        related_name="projects",
        through='ProjectUser'
    )
    initial_budget = MoneyField(
        _("Initial Budget"),
        help_text=_('The value that had planed to start the project'),
        decimal_places=2,
        default=0,
        default_currency='BRL',
        max_digits=11,
    )
    start_date = models.DateField(
        _("Start Date"),
        help_text=_('Date that the project will start or already started'),
        blank=True,
    )
    end_date = models.DateField(
        _("End Date"), 
        help_text=_('Date that the project will end or already ended'),
        blank=True,
    )
    is_ended = models.BooleanField(_('finished'), default=False,
        help_text=_('To determinate if this project had already ended.')
    )
    is_started = models.BooleanField(_('started'), default=True,
        help_text=_('To determinate if this project had already started.')
    )

    class Meta:
        verbose_name = _('projeto')
        verbose_name_plural = _('projetos')
    
    def __str__(self):
        return f"Projeto {self.name}"

    def get_phases(self):
        return ProjectPhase.objects.filter(project = self.id).all()
    
    def get_current_phase(self):
        criterion1 = Q(project = self.id)
        criterion2 = Q(is_current = True)
        return ProjectPhase.objects.filter(criterion1 & criterion2).first()

    def get_absolute_url(self):
        return reverse("projects:details", kwargs={"id": self.id})
    
    def get_create_phase_url(self):
        return reverse("projects:new_phase", kwargs={"id": self.id})

class ProjectPhase(models.Model):
    name = models.CharField(_("Phase Name"), max_length=250)
    project = models.ForeignKey(Project, related_name="phases", on_delete=models.CASCADE)
    description = models.TextField(_("Phase Description"), max_length=1000)
    initial_budget = MoneyField(
        _("Initial Budget"),
        help_text=_('The value that had planed to this phase'),
        decimal_places=2,
        default=0,
        default_currency='BRL',
        max_digits=11,
    )
    spent_budget = MoneyField(
        _("spent Budget"),
        help_text=_('Budget that has already been spent'),
        decimal_places=2,
        default=0,
        default_currency='BRL',
        max_digits=11,
    )
    start_date = models.DateField(
        _("Start Date"),
        help_text=_('Date that the project will start or already started'),
        blank=True,
    )
    end_date = models.DateField(
        _("End Date"), 
        help_text=_('Date that the project will end or already ended'),
        blank=True,
    )
    is_current = models.BooleanField(_('current'), default=False,
        help_text=_('To if the project is in this current phase.')
    )

    class Meta:
        verbose_name = _('Fase')
        verbose_name_plural = _('Fases')

    def get_current_budget(self):
        activities = self.get_activities()
        budget = 0
        for activity in activities:
            budget += activity.cust

        return self.initial_budget - budget
    
    def get_activities(self):
        return self.activities.filter(phase = self.id).all()

    def get_create_activity_url(self):
        return reverse("activities:new_activity", kwargs={"project_id": self.project.id, "phase_id":self.id})

    def __str__(self):
        return f"{self.project.name} > {self.name}"


class ProjectUser(models.Model):
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permissions = models.ManyToManyField(Permission)
    
    class Meta:
        permissions = (
            ('can_update_project', 'Pode atualizar o Projeto'),
        )
