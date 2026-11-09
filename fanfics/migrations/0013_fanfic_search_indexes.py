from django.db import migrations

# django.contrib.postgres is imported lazily: psycopg is not installed on every
# SQLite development environment, and these indexes are PostgreSQL only.


def _search_index():
    from django.contrib.postgres.indexes import GinIndex
    from django.contrib.postgres.search import SearchVector

    vector = (
        SearchVector('title', weight='A', config='simple')
        + SearchVector('synopsis', weight='B', config='simple')
        + SearchVector('description', weight='C', config='simple')
    )
    return GinIndex(vector, name='fanfic_search_vector_gin')


def _title_trgm_index():
    from django.contrib.postgres.indexes import GinIndex

    return GinIndex(
        fields=['title'], name='fanfic_title_trgm_gin', opclasses=['gin_trgm_ops'])


def create_search_indexes(apps, schema_editor):
    """PostgreSQL only: full-text GIN index and pg_trgm. No-op elsewhere (SQLite)."""
    if schema_editor.connection.vendor != 'postgresql':
        return
    schema_editor.execute('CREATE EXTENSION IF NOT EXISTS pg_trgm')
    Fanfic = apps.get_model('fanfics', 'Fanfic')
    schema_editor.add_index(Fanfic, _search_index())
    schema_editor.add_index(Fanfic, _title_trgm_index())


def drop_search_indexes(apps, schema_editor):
    if schema_editor.connection.vendor != 'postgresql':
        return
    Fanfic = apps.get_model('fanfics', 'Fanfic')
    schema_editor.remove_index(Fanfic, _title_trgm_index())
    schema_editor.remove_index(Fanfic, _search_index())


class Migration(migrations.Migration):

    dependencies = [
        ('fanfics', '0012_alter_fanfic_completed_alter_fanfic_status_and_more'),
    ]

    operations = [
        migrations.RunPython(create_search_indexes, drop_search_indexes),
    ]
