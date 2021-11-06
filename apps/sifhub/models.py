from django.core.validators import FileExtensionValidator
from django.db import models

from apps.accounts.models import Member


class Service(models.Model):
    name = models.CharField('nome do servico', max_length=80)
    icon = models.FileField(
        'ícone',
        upload_to='imagens/servicos/icones',
        blank=True,
        validators=[FileExtensionValidator(['svg', 'png'])],
        help_text='O ícone deve ter formato SVG ou PNG.',
    )
    description = models.TextField(
        'descrição',
        max_length=200,
        help_text='Breve descrição do serviço em até 200 caracteres.',
    )
    is_active = models.BooleanField(
        'ativo',
        default=True,
        help_text=
            'Indica que o serviço será tratado como ativo. '
            'Ao invés de excluir o serviço, desmarque isso.',
    )

    class Meta:
        verbose_name = 'serviço'
        verbose_name_plural = 'serviços'
        ordering = ['name']

    def __str__(self):
        return self.name


class Team(models.Model):
    service = models.OneToOneField(
        verbose_name='serviço',
        to=Service,
        on_delete=models.CASCADE,
    )
    leader = models.ForeignKey(
        verbose_name='líder',
        to=Member,
        on_delete=models.SET_NULL,
        related_name='teams_led',
        null=True,
    )
    members = models.ManyToManyField(
        verbose_name='membros',
        to=Member,
        related_name='teams',
        related_query_name='team',
        blank=True,
    )

    class Meta:
        verbose_name = 'equipe'
        verbose_name_plural = 'equipes'
        ordering = ['service__name']

    def __str__(self):
        return self.service.name
