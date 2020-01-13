from django.core.management.base import BaseCommand

from api.models import FlatPages

class Command(BaseCommand):
    help = 'Pages mentions légales et politique de confidentialité'

    def handle(self, *args, **kwargs):

        flatpage_legal = FlatPages.objects.filter(type='legal')
        flatpage_rgpd = FlatPages.objects.filter(type='rgpd')

        if not flatpage_legal.exists():
            FlatPages.objects.create(
                title='Mentions légales',
                content='bla bla bla bla',
                type='legal'
            )
            self.stdout.write(self.style.SUCCESS('Created "%s"' % flatpage_legal))

        if not flatpage_rgpd.exists():
            FlatPages.objects.create(
                title='Politique de confidentialité',
                content='bla bla bla bla',
                type='rgpd'
            )
            self.stdout.write(self.style.SUCCESS('Created "%s"' % flatpage_rgpd))

