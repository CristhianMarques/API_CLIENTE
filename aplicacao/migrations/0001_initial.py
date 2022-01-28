# Generated by Django 3.2.7 on 2021-10-09 02:38

import aplicacao.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contato_Empresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nome', models.CharField(max_length=250, verbose_name='Nome Contato')),
                ('Funcao', models.CharField(blank=True, max_length=250, null=True, verbose_name='Função Contato')),
                ('Telefone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Telefone')),
                ('Celular', models.CharField(blank=True, max_length=20, null=True, verbose_name='Celular')),
                ('Observacao', models.CharField(blank=True, max_length=250, null=True, verbose_name='Observação')),
                ('Data_Inclusao', models.DateField(blank=True, null=True, verbose_name='Data Inclusão')),
                ('Data_Ult_Alter', models.DateField(blank=True, null=True, verbose_name='Data Ultima Alteração')),
            ],
            options={
                'verbose_name': 'Contato_Empresa',
                'verbose_name_plural': 'Contatos Empresa',
            },
        ),
        migrations.CreateModel(
            name='Eventos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Data_Criacao_Evento', models.DateField(blank=True, null=True, verbose_name='Data Criação Evento')),
                ('Tipo_Doc_Fiscal', models.CharField(blank=True, choices=[('NFE', 'NFE'), ('NFCE', 'NFCE')], max_length=50, null=True, verbose_name='Tipo Doc')),
                ('Data_Emissao', models.DateField(blank=True, null=True, verbose_name='Data Emissão')),
                ('Num_Doc', models.CharField(blank=True, max_length=50, null=True, verbose_name='Numero Doc')),
                ('Serie_Dov', models.CharField(blank=True, max_length=50, null=True, verbose_name='Serie Doc')),
                ('Status_Doc', models.CharField(blank=True, choices=[('Enviada', 'Enviada'), ('Pendente', 'Pendente'), ('Contigencia', 'Contigencia'), ('Erro', 'Erro')], max_length=50, null=True, verbose_name='Status Doc')),
                ('Id_Tab_Orig', models.CharField(blank=True, max_length=50, null=True, verbose_name='Id Tabela Origem')),
                ('Registro_Sincronizado', models.CharField(blank=True, choices=[('Sim', 'Sim'), ('Nao', 'Nao')], max_length=50, null=True, verbose_name='Registro Sincronizado')),
            ],
            options={
                'verbose_name': 'Evento',
                'verbose_name_plural': 'Eventos',
            },
        ),
        migrations.CreateModel(
            name='Log_Sincronizacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Data_Tentativa_Envio', models.DateField(blank=True, null=True, verbose_name='Data Tentativa Envio')),
                ('Id_Eventos', models.IntegerField(blank=True, null=True, verbose_name='Id Eventos')),
                ('Status_Envio', models.CharField(blank=True, max_length=50, null=True, verbose_name='Status Envio')),
            ],
            options={
                'verbose_name': 'Log_Sincronizacao',
                'verbose_name_plural': 'Logs_Sincronizacao',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Parametros_Gerais',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Tempo_Sincr_Minutos', models.IntegerField(blank=True, null=True, verbose_name='Tempo de Sincronização em Minutos')),
                ('Mod_Sincron_Nfe', models.CharField(blank=True, choices=[('Enviada', 'Enviada'), ('Pendente', 'Pendente'), ('Contigencia', 'Contigencia'), ('Erro', 'Erro'), ('Todas', 'Todas')], max_length=50, null=True, verbose_name='Modalidade Nfe - Sincronizar (Enviadas, Pendentes, Contigencia, Erro)')),
                ('Mod_Sincron_Nfce', models.CharField(blank=True, choices=[('Enviada', 'Enviada'), ('Pendente', 'Pendente'), ('Contigencia', 'Contigencia'), ('Erro', 'Erro'), ('Todas', 'Todas')], max_length=50, null=True, verbose_name='Modalidade Nfce - Sincronizar (Enviadas, Pendentes, Contigencia, Erro)')),
                ('Situacao_Sincronizacao', models.CharField(blank=True, choices=[('Ativo', 'Ativo'), ('Inativo', 'Inativo')], max_length=50, null=True, verbose_name='Situação - Sincronização dos Dados')),
                ('Sistema_Sincronizacao', models.CharField(blank=True, choices=[('Sistema Merchant', 'Sistema Merchant'), ('Sistema Smc_Light', 'Sistema Smc_Light')], max_length=50, null=True, verbose_name='Sistema')),
                ('Ender_Endpoint_Servidor', models.CharField(blank=True, max_length=400, null=True, verbose_name='Endereco Do Servidor End Point De Eventos')),
                ('Data_Insercao', models.DateField(blank=True, null=True, verbose_name='Data De Insercao Do Registro')),
                ('Data_Ult_Alter', models.DateField(blank=True, null=True, verbose_name='Data Da Ultima Alteracao Do Registro')),
                ('Data_Inicial_Sinc', models.DateField(verbose_name='Data Inicial da Sincronização')),
            ],
            options={
                'verbose_name': 'Parametros_Gerais',
                'verbose_name_plural': 'Parametros_Gerais',
            },
        ),
        migrations.CreateModel(
            name='CustomUsuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='E-mail')),
                ('fone', models.CharField(max_length=15, verbose_name='Telefone')),
                ('is_staff', models.BooleanField(default=True, verbose_name='Membro da equipe')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', aplicacao.models.UsuarioManager()),
            ],
        ),
    ]