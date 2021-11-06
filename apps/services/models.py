from django.conf import settings
from django.db import models

from apps.accounts.models import Client, Member
from apps.sifhub.models import Service

def request_attachment_path(instance, filename):
    return f'anexos/solicitacoes/{instance.pk}/{filename}'

def project_attachment_path(instance, filename):
    return f'anexos/projetos/{instance.pk}/{filename}'


class Request(models.Model):
    PREFER_EMAIL = 1
    PREFER_TELEPHONE = 2
    PREFERRED_METHOD_OF_CONTACT_CHOICES = (
        (PREFER_EMAIL, 'Email'),
        (PREFER_TELEPHONE, 'Telefone celular'),
    )

    REQUESTED = 1
    IN_ANALYSIS = 2
    APPROVED = 3
    IN_PROGRESS = 4
    FINISHED = 5
    CANCELED = 6
    STATUS_CHOICES = (
        (REQUESTED, 'Solicitado'),
        (IN_ANALYSIS, 'Em análise'),
        (APPROVED, 'Aprovado'),
        (IN_PROGRESS, 'Em andamento'),
        (FINISHED, 'Finalizado'),
        (CANCELED, 'Cancelado'),
    )

    client = models.ForeignKey(
        verbose_name='cliente',
        to=Client,
        on_delete=models.CASCADE,
    )
    service = models.ForeignKey(
        verbose_name='serviço',
        to=Service,
        on_delete=models.CASCADE,
    )
    description = models.TextField('descrição')
    attachment = models.FileField('anexo', upload_to=request_attachment_path, blank=True)
    preferred_method_of_contact = models.IntegerField(
        'forma de contato de preferência',
        choices=PREFERRED_METHOD_OF_CONTACT_CHOICES,
    )
    best_time_to_contact = models.TimeField('melhor horário para contato')
    status = models.IntegerField(
        'status',
        choices=STATUS_CHOICES,
        default=REQUESTED,
    )
    created_at = models.DateTimeField('data de registro', auto_now_add=True)
    updated_at = models.DateTimeField('data de modificação', auto_now=True)

    class Meta:
        verbose_name = 'solicitação'
        verbose_name_plural = 'solicitações'

    def __str__(self):
        return f'{self.service} para {self.client.business.name}'


class RequestDiscussion(models.Model):
    request = models.ForeignKey(
        verbose_name='solicitação',
        to=Request,
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        verbose_name='autor',
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    content = models.TextField('conteúdo')
    attachment = models.FileField('anexo', upload_to=request_attachment_path, blank=True)
    created_at = models.DateTimeField('data de publicação', auto_now_add=True)
    updated_at = models.DateTimeField('data de modificação', auto_now=True)

    class Meta:
        verbose_name = 'discussão da solicitação'
        verbose_name_plural = 'discussões das solicitações'

    def __str__(self):
        return f'{self.author.get_full_name}: {self.content}'


class Project(models.Model):
    request = models.OneToOneField(
        verbose_name='solicitação',
        to=Request,
        on_delete=models.CASCADE,
    )
    theme = models.CharField('tema', max_length=100, blank=True)
    general_objective = models.TextField('objetivo geral', blank=True)
    specific_objectives = models.TextField('objetivos específicos', blank=True)
    justification = models.TextField('justificativa', blank=True)
    created_at = models.DateTimeField('data de registro', auto_now_add=True)
    updated_at = models.DateTimeField('data de modificação', auto_now=True)

    class Meta:
        verbose_name = 'projeto'
        verbose_name_plural = 'projetos'

    def __str__(self):
        return 'Projeto de ' + str(self.request)


class Task(models.Model):
    project = models.ForeignKey(
        verbose_name='projeto',
        to=Project,
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        verbose_name='autor',
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='+',
    )
    assigned_to = models.ForeignKey(
        verbose_name='atribuída a',
        to=Member,
        on_delete=models.CASCADE,
        related_name='assigned_tasks',
    )
    task = models.TextField('tarefa')
    attachment = models.FileField('anexo', upload_to=project_attachment_path, blank=True)
    deadline = models.DateTimeField('prazo final', blank=True)
    concluded = models.BooleanField('concluída')
    created_at = models.DateTimeField('data de publicação', auto_now_add=True)
    updated_at = models.DateTimeField('data de modificação', auto_now=True)

    class Meta:
        verbose_name = 'tarefa'
        verbose_name_plural = 'tarefas'

    def __str__(self):
        return f'{self.author.get_full_name}: {self.task}'
