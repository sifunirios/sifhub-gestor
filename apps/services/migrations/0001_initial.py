# Generated by Django 3.2.9 on 2021-11-06 19:00

import apps.services.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
        ('sifhub', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('theme', models.CharField(blank=True, max_length=100, verbose_name='tema')),
                ('general_objective', models.TextField(blank=True, verbose_name='objetivo geral')),
                ('specific_objectives', models.TextField(blank=True, verbose_name='objetivos específicos')),
                ('justification', models.TextField(blank=True, verbose_name='justificativa')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='data de registro')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='data de modificação')),
            ],
            options={
                'verbose_name': 'projeto',
                'verbose_name_plural': 'projetos',
            },
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(verbose_name='descrição')),
                ('attachment', models.FileField(blank=True, upload_to=apps.services.models.request_attachment_path, verbose_name='anexo')),
                ('preferred_method_of_contact', models.IntegerField(choices=[(1, 'Email'), (2, 'Telefone celular')], verbose_name='forma de contato de preferência')),
                ('best_time_to_contact', models.TimeField(verbose_name='melhor horário para contato')),
                ('status', models.IntegerField(choices=[(1, 'Solicitado'), (2, 'Em análise'), (3, 'Aprovado'), (4, 'Em andamento'), (5, 'Finalizado'), (6, 'Cancelado')], default=1, verbose_name='status')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='data de registro')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='data de modificação')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.client', verbose_name='cliente')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sifhub.service', verbose_name='serviço')),
            ],
            options={
                'verbose_name': 'solicitação',
                'verbose_name_plural': 'solicitações',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.TextField(verbose_name='tarefa')),
                ('attachment', models.FileField(blank=True, upload_to=apps.services.models.project_attachment_path, verbose_name='anexo')),
                ('deadline', models.DateTimeField(blank=True, verbose_name='prazo final')),
                ('concluded', models.BooleanField(verbose_name='concluída')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='data de publicação')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='data de modificação')),
                ('assigned_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigned_tasks', to='accounts.member', verbose_name='atribuída a')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='autor')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.project', verbose_name='projeto')),
            ],
            options={
                'verbose_name': 'tarefa',
                'verbose_name_plural': 'tarefas',
            },
        ),
        migrations.CreateModel(
            name='RequestDiscussion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='conteúdo')),
                ('attachment', models.FileField(blank=True, upload_to=apps.services.models.request_attachment_path, verbose_name='anexo')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='data de publicação')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='data de modificação')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='autor')),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.request', verbose_name='solicitação')),
            ],
            options={
                'verbose_name': 'discussão da solicitação',
                'verbose_name_plural': 'discussões das solicitações',
            },
        ),
        migrations.AddField(
            model_name='project',
            name='request',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='services.request', verbose_name='solicitação'),
        ),
    ]
