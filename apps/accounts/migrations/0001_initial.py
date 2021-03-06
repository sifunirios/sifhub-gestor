# Generated by Django 3.2.9 on 2021-11-06 19:00

import apps.accounts.managers
import apps.accounts.validators
from django.db import migrations, models
import django.db.models.deletion
import localflavor.br.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='endereço de email')),
                ('name', models.CharField(max_length=50, verbose_name='nome')),
                ('surname', models.CharField(max_length=50, verbose_name='sobrenome')),
                ('is_active', models.BooleanField(default=True, help_text='Indica que o usuário será tratado como ativo. Ao invés de excluir o usuário, desmarque isso.', verbose_name='ativo')),
                ('is_staff', models.BooleanField(default=False, help_text='Indica que usuário consegue acessar este site de administração.', verbose_name='membro da equipe')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='data de registro')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='data de modificação')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'usuário',
                'verbose_name_plural': 'usuários',
                'ordering': ['name', 'surname'],
            },
            managers=[
                ('objects', apps.accounts.managers.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
            ],
            options={
                'verbose_name': 'cliente',
                'verbose_name_plural': 'clientes',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('accounts.user',),
            managers=[
                ('objects', apps.accounts.managers.ClientManager()),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
            ],
            options={
                'verbose_name': 'membro',
                'verbose_name_plural': 'membros',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('accounts.user',),
            managers=[
                ('objects', apps.accounts.managers.MemberManager()),
            ],
        ),
        migrations.CreateModel(
            name='MemberProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registry', models.CharField(blank=True, max_length=10, null=True, unique=True, validators=[apps.accounts.validators.RegistryValidator()], verbose_name='matrícula')),
                ('initial_academic_year', models.CharField(blank=True, help_text='Ex: 2017.1', max_length=6, validators=[apps.accounts.validators.AcademicYearValidator()], verbose_name='período letivo inicial')),
                ('current_semester', models.SmallIntegerField(blank=True, choices=[(1, '1º semestre'), (2, '2º semestre'), (3, '3º semestre'), (4, '4º semestre'), (5, '5º semestre'), (6, '6º semestre'), (7, '7º semestre'), (8, '8º semestre')], null=True, verbose_name='semestre atual')),
                ('member_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.group', verbose_name='tipo do membro')),
                ('member', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='accounts.member', verbose_name='membro')),
            ],
            options={
                'verbose_name': 'perfil',
                'verbose_name_plural': 'perfis',
            },
        ),
        migrations.CreateModel(
            name='ClientBusiness',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='nome')),
                ('cnpj', localflavor.br.models.BRCNPJField(blank=True, max_length=18, verbose_name='CNPJ')),
                ('address', models.CharField(max_length=100, verbose_name='endereço')),
                ('city', models.CharField(max_length=30, verbose_name='cidade')),
                ('state', localflavor.br.models.BRStateField(max_length=2, verbose_name='estado')),
                ('telephone', models.CharField(max_length=15, verbose_name='telefone celular')),
                ('branch_of_activity', models.SmallIntegerField(choices=[(1, 'Alimentação e Bebidas'), (2, 'Aluguel'), (3, 'Construção'), (4, 'Educação'), (5, 'Entretenimento'), (6, 'Estética e Cosméticos'), (7, 'Informática'), (8, 'Saúde'), (9, 'Serviços Especializados'), (10, 'Vendas e Marketing'), (11, 'Vestuário e Calçados'), (12, 'Outro')], null=True, verbose_name='ramo de atividade')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='data de registro')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='data de modificação')),
                ('client', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='business', to='accounts.client', verbose_name='cliente')),
            ],
            options={
                'verbose_name': 'negócio',
                'verbose_name_plural': 'negócios',
            },
        ),
    ]
