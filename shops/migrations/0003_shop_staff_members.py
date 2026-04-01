from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shops', '0002_alter_menu_shop_alter_shop_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='staff_members',
            field=models.ManyToManyField(
                blank=True,
                limit_choices_to={'role': 'staff'},
                related_name='staff_shops',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
