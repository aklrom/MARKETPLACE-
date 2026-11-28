from django.db import migrations, models


def assign_unique_emails(apps, schema_editor):
    """Donne un email unique à chaque utilisateur existant qui n'en a pas."""
    User = apps.get_model('accounts', 'User')
    for i, user in enumerate(User.objects.filter(email='')):
        user.email = f"user{i}@placeholder.com"
        user.save()


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        # 1. Ajouter le champ email SANS contrainte unique pour l'instant
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.EmailField(default='', max_length=254, verbose_name='adresse email'),
            preserve_default=False,
        ),
        
        # 2. Mettre à jour les utilisateurs existants avec des emails uniques
        migrations.RunPython(assign_unique_emails),
        
        # 3. Maintenant on peut rendre le champ unique
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='adresse email'),
        ),
        
        # 4. Créer le modèle OTPVerification
        migrations.CreateModel(
            name='OTPVerification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('otp_code', models.CharField(max_length=6)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_verified', models.BooleanField(default=False)),
            ],
        ),
    ]
    