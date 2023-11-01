from django.db import migrations
from shared.utils import Roles


def apply_migration(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.bulk_create(
        [
            Group(name=Roles.CLIENT),
            Group(name=Roles.SELLER),
        ]
    )


class Migration(migrations.Migration):
    dependencies = [
        ("auth", "__latest__"),
    ]

    operations = [migrations.RunPython(apply_migration)]
