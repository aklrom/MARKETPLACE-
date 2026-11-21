from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_alter_review_options_alter_review_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.IntegerField(
                choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')],
                validators=[MinValueValidator(1), MaxValueValidator(5)],
            ),
        ),
    ]
