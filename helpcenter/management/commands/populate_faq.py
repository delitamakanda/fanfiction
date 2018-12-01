from django.core.management.base import BaseCommand

from helpcenter.models import FoireAuxQuestions

class Command(BaseCommand):
    help = 'create dummy data to initialize fanfiction'

    def handle(self, *args, **options):
        faq = FoireAuxQuestions.objects.filter(question="Qu'est-ce qu'une fanfiction ?")
        if not faq.exists():
            FoireAuxQuestions.objects.bulk_create(
                [FoireAuxQuestions(libelle="fan", question="Qu'est-ce qu'une fanfiction ?", reponse="Définition tirée du site [Wikipedia](https://fr.wikipedia.org/wiki/Fanfiction) : 'Une fanfiction, ou fanfic (parfois écrit fan-fiction), est un récit que certains fans écrivent pour prolonger, amender ou même totalement transformer un produit médiatique qu'ils affectionnent, qu'il s'agisse d'un roman, d'un manga, d'une série télévisée, d'un film, d'un jeu vidéo ou encore d'une célébrité'."),
                FoireAuxQuestions(libelle="sit", question="Mon fandom n'existe pas sur le site ! Que faire ?", reponse="Si votre fandom est inexistant sur le site. Contactez nous via le formulaire de contact ou le forum."),
                FoireAuxQuestions(libelle="fan", question="Que signifie le rating des fanfictions ?", reponse="Voici la signification des différents ratings :<br><br>Tout public (G) : Cette fanfiction peut être lue de tous.<br><br>13+ : Ne convient pas aux enfants de moins de 13 ans. Peut contenir quelques scènes de violence, du langage plutôt grossier, et de légères allusions à des thèmes plus adultes.<br><br>T (16+) : A partir de 16 ans. Peut contenir des références fortes (mais non explicites) à des thèmes adultes, des scènes de violence, et un langage fortement grossier.<br><br>M (18+) : Pour adultes seulement. Références explicites dans le langage ou dans les thèmes employés.")]
            )
            self.stdout.write(self.style.SUCCESS('Created faqs'))
