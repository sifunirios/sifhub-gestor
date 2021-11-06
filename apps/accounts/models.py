from django.contrib import admin
from django.contrib.auth.models import AbstractBaseUser, Group, PermissionsMixin
from django.core.mail import send_mail
from django.db import models

from localflavor.br.models import BRCNPJField, BRStateField

from .managers import ClientManager, MemberManager, UserManager
from .validators import AcademicYearValidator, RegistryValidator


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('endereço de email', unique=True)
    name = models.CharField('nome', max_length=50)
    surname = models.CharField('sobrenome', max_length=50)
    photo = models.ImageField(
        'foto',
        upload_to='imagens/usuarios',
        blank=True,
        help_text='É preferível que a proporção da foto seja de 1:1 (quadrada).'
    )
    is_active = models.BooleanField(
        'ativo',
        default=True,
        help_text=
            'Indica que o usuário será tratado como ativo. '
            'Ao invés de excluir o usuário, desmarque isso.',
    )
    is_staff = models.BooleanField(
        'membro da equipe',
        default=False,
        help_text='Indica que usuário consegue acessar este site de administração.',
    )
    created_at = models.DateTimeField('data de registro', auto_now_add=True)
    updated_at = models.DateTimeField('data de modificação', auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']

    class Meta:
        verbose_name = 'usuário'
        verbose_name_plural = 'usuários'
        ordering = ['name', 'surname']

    def __str__(self):
        return self.get_full_name or self.email

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    @property
    @admin.display(description='nome')
    def get_short_name(self):
        return self.name

    @property
    @admin.display(description='nome completo')
    def get_full_name(self):
        return f'{self.name} {self.surname}'.strip()

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Client(User):
    objects = ClientManager()

    class Meta:
        proxy = True
        verbose_name = 'cliente'
        verbose_name_plural = 'clientes'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.is_staff = False
        super().save(*args, **kwargs)


class ClientBusiness(models.Model):
    BRANCH_OF_ACTIVITY_CHOICES = (
        (1, 'Alimentação e Bebidas'),
        (2, 'Aluguel'),
        (3, 'Construção'),
        (4, 'Educação'),
        (5, 'Entretenimento'),
        (6, 'Estética e Cosméticos'),
        (7, 'Informática'),
        (8, 'Saúde'),
        (9, 'Serviços Especializados'),
        (10, 'Vendas e Marketing'),
        (11, 'Vestuário e Calçados'),
        (12, 'Outro'),
    )

    client = models.OneToOneField(
        verbose_name='cliente',
        to=Client,
        on_delete=models.CASCADE,
        related_name='business',
    )
    name = models.CharField('nome', max_length=50)
    cnpj = BRCNPJField('CNPJ', blank=True)
    address = models.CharField('endereço', max_length=100)
    city = models.CharField('cidade', max_length=30)
    state = BRStateField('estado')
    telephone = models.CharField('telefone celular', max_length=15)
    branch_of_activity = models.SmallIntegerField(
        'ramo de atividade',
        choices=BRANCH_OF_ACTIVITY_CHOICES,
        null=True,
    )
    created_at = models.DateTimeField('data de registro', auto_now_add=True)
    updated_at = models.DateTimeField('data de modificação', auto_now=True)

    class Meta:
        verbose_name = 'negócio'
        verbose_name_plural = 'negócios'

    def __str__(self):
        return self.name


class Member(User):
    objects = MemberManager()

    class Meta:
        proxy = True
        verbose_name = 'membro'
        verbose_name_plural = 'membros'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.is_staff = True
        super().save(*args, **kwargs)


class MemberProfile(models.Model):
    SEMESTER_CHOICES = [
        (1, '1º semestre'),
        (2, '2º semestre'),
        (3, '3º semestre'),
        (4, '4º semestre'),
        (5, '5º semestre'),
        (6, '6º semestre'),
        (7, '7º semestre'),
        (8, '8º semestre'),
    ]

    member = models.OneToOneField(
        verbose_name='membro',
        to=Member,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    member_type = models.ForeignKey(
        verbose_name='tipo do membro',
        to=Group,
        on_delete=models.CASCADE,
        null=True,
    )
    registry = models.CharField(
        'matrícula',
        max_length=10,
        validators=[RegistryValidator()],
        unique=True,
        blank=True,
        null=True,
    )
    initial_academic_year = models.CharField(
        'período letivo inicial',
        max_length=6,
        help_text='Ex: 2017.1',
        validators=[AcademicYearValidator()],
        blank=True,
    )
    current_semester = models.SmallIntegerField(
        'semestre atual',
        choices=SEMESTER_CHOICES,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'perfil'
        verbose_name_plural = 'perfis'

    def __str__(self):
        return self.member.get_full_name or self.member.email
