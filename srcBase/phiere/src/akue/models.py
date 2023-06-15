from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta
from django.conf import settings
from django.utils.text import slugify
from django.core.files.storage import FileSystemStorage
from pathlib import Path
import os
from django.dispatch import receiver
from django.db.models.signals import pre_save


from django.contrib.auth.models import User
from django.db.models.signals import post_save






#from datetime import datetime, 


# Create your models here.




#------------------Creation Mode Utilistateur-------------------------



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telephone = models.CharField(max_length=20, default='1234567890')
    adresse = models.CharField(max_length=255, default='adresse par défaut')
    metier = models.CharField(max_length=255, default='métier par défaut')
    image = models.ImageField(upload_to='akue/static/akue/img/photo_de_profile/', null=True, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

#------------------Fin Creation Mode Utilistateur-------------------------








#------------------Creation Mode  acticle pour les actualités-------------------------

class Article(models.Model):
    #titre = models.CharField(max_length=200)
    contenu = models.TextField()
    auteur = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    date_creation = models.DateTimeField(default=timezone.now)
    date_publication = models.DateTimeField(default=timezone.now)
    #date_publication = models.DateTimeField(blank=True, null=True)
    #image = models.ImageField(upload_to='akue/static/akue/img/publication_images/', null=True, blank=True)

    def publier(self):
        self.date_publication = timezone.now()
        self.save()
    
    def num_likes(self):
        return self.like_set.count()
    

    def __str__(self):
        return self.contenu 
    
    #------------------fin Creation Mode  acticle pour les actualités-------------------------
    
    
    
    
    #------------------Creation calcule de temps depuis la création d'un article pour les actualités-------------------------
    
    
    
    def temps_publication(self):
        actu = timezone.now()
        diff = actu - self.date_creation
        if diff < timedelta(minutes=1):
            return f"{diff.seconds} secondes"
        elif diff < timedelta(hours=1):
            return f"{diff.seconds//60} minutes"
        elif diff < timedelta(days=1):
            return f"{diff.seconds//3600} heures"
        elif diff < timedelta(days=30):
            return f"{diff.days} jours"
        elif diff < timedelta(days=365):
            return f"{diff.days//30} mois"
        else:
            return f"{diff.days//365} ans"

#------------------finCreation calcule de temps depuis la création d'un article pour les actualités-------------------------



#------------------Creation d'un commentaire pour les actualités-------------------------



class Commentaire(models.Model):
    article = models.ForeignKey('Article', on_delete=models.CASCADE, related_name='commentaires')
    auteur = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    contenu = models.TextField()
    date_creation = models.DateTimeField(default=timezone.now)
    approuve = models.BooleanField(default=False)

    def approuver(self):
        self.approuve = True
        self.save()

    def __str__(self):
        return self.contenu





#------------------fin Creation du like d'un article pour les actualités-------------------------


class Like(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} likes {self.article.contenu}'



#------------------fin Creation du like d'un article pour les actualités-------------------------





#------------------Creation du like d'un commentaire pour les actualités-------------------------

class Like_commentaire(models.Model):
    commentaire = models.ForeignKey(Commentaire, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} likes {self.commentaire.contenu}'


#------------------fin Creation du like d'un commentaire pour les actualités-------------------------





#------------------Creation d'un service -------------------------


class Service(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_publication = models.DateTimeField(null=True, blank=True)
    image = models.ImageField(upload_to='akue/static/akue/img/service_images/', null=True, blank=True)

    def __str__(self):
        return self.title
    
    
    
    #------------------Creation calcule de temps depuis la création d'un article pour les actualités-------------------------
    
    
    
    def temps_publication(self):
        actu = timezone.now()
        diff = actu - self.date_creation
        if diff < timedelta(minutes=1):
            return f"{diff.seconds} secondes"
        elif diff < timedelta(hours=1):
            return f"{diff.seconds//60} minutes"
        elif diff < timedelta(days=1):
            return f"{diff.seconds//3600} heures"
        elif diff < timedelta(days=30):
            return f"{diff.days} jours"
        elif diff < timedelta(days=365):
            return f"{diff.days//30} mois"
        else:
            return f"{diff.days//365} ans"
    

#------------------fin de Creation d'un service -------------------------



#------------------Creation d'un commentaire pour les services-------------------------



class Commentaireservice(models.Model):
    service = models.ForeignKey('Service', on_delete=models.CASCADE, related_name='commentairesservice')
    auteur = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    contenu = models.TextField()
    date_creation = models.DateTimeField(default=timezone.now)
    approuve = models.BooleanField(default=False)

    def approuver(self):
        self.approuve = True
        self.save()

    def __str__(self):
        return self.contenu





#------------------fin Creation d'un commentaire pour les services-------------------------



#------------------Creation du like d'un Servise-------------------------


class Likeservice(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} likes {self.service.title}'



#------------------fin Creation du like d'un Servise-------------------------




#------------------Creation du like d'un commentaire pour les servises-------------------------

class Like_commentaireservice(models.Model):
    commentaireservice = models.ForeignKey(Commentaireservice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} likes {self.commentaireservice.contenu}'


#------------------fin Creation du like d'un commentaire pour les services-------------------------








#------------------Creation d'une Offre -------------------------


class Offre(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_publication = models.DateTimeField(null=True, blank=True)
    image = models.ImageField(upload_to='akue/static/akue/img/offre_images/', null=True, blank=True)

    def __str__(self):
        return self.title
    
    
    
    #------------------Creation calcule de temps depuis la création d'un article pour les actualités-------------------------
    
    
    
    def temps_publication(self):
        actu = timezone.now()
        diff = actu - self.date_creation
        if diff < timedelta(minutes=1):
            return f"{diff.seconds} secondes"
        elif diff < timedelta(hours=1):
            return f"{diff.seconds//60} minutes"
        elif diff < timedelta(days=1):
            return f"{diff.seconds//3600} heures"
        elif diff < timedelta(days=30):
            return f"{diff.days} jours"
        elif diff < timedelta(days=365):
            return f"{diff.days//30} mois"
        else:
            return f"{diff.days//365} ans"

#------------------fin de Creation d'une Offre -------------------------



#------------------Creation d'un commentaire pour les Offres-------------------------



class Commentaireoffre(models.Model):
    offre = models.ForeignKey('Offre', on_delete=models.CASCADE, related_name='commentairesoffre')
    auteur = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    contenu = models.TextField()
    date_creation = models.DateTimeField(default=timezone.now)
    approuve = models.BooleanField(default=False)

    def approuver(self):
        self.approuve = True
        self.save()

    def __str__(self):
        return self.contenu





#------------------fin Creation d'un commentaire pour les Offres-------------------------



#------------------Creation du like d'un Servise-------------------------


class Likeoffre(models.Model):
    offre = models.ForeignKey(Offre, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} likes {self.offre.title}'



#------------------fin Creation du like d'un Servise-------------------------




#------------------Creation du like d'un commentaire pour les servises-------------------------

class Like_commentaireoffre(models.Model):
    commentaireoffre = models.ForeignKey(Commentaireoffre, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} likes {self.commentaireoffre.contenu}'


#------------------fin Creation du like d'un commentaire pour les offres-------------------------






#------------------Creation d'une Publication -------------------------


class Publication(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_publication = models.DateTimeField(null=True, blank=True)
    image = models.ImageField(upload_to='akue/static/akue/img/publication _images/', null=True, blank=True)

    def __str__(self):
        return self.content
    
    
    
    
    #------------------Creation calcule de temps depuis la création d'un article pour les actualités-------------------------
    
    
    
    def temps_publication(self):
        actu = timezone.now()
        diff = actu - self.date_creation
        if diff < timedelta(minutes=1):
            return f"{diff.seconds} secondes"
        elif diff < timedelta(hours=1):
            return f"{diff.seconds//60} minutes"
        elif diff < timedelta(days=1):
            return f"{diff.seconds//3600} heures"
        elif diff < timedelta(days=30):
            return f"{diff.days} jours"
        elif diff < timedelta(days=365):
            return f"{diff.days//30} mois"
        else:
            return f"{diff.days//365} ans"
    

#------------------fin de Creation d'une publication -------------------------



#------------------Creation d'un commentaire pour les publications-------------------------



class Commentairepublication (models.Model):
    publication = models.ForeignKey('Publication', on_delete=models.CASCADE, related_name='commentairespublication')
    auteur = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    contenu = models.TextField()
    date_creation = models.DateTimeField(default=timezone.now)
    approuve = models.BooleanField(default=False)

    def approuver(self):
        self.approuve = True
        self.save()

    def __str__(self):
        return self.contenu





#------------------fin Creation d'un commentaire pour les publications-------------------------



#------------------Creation du like d'un publication-------------------------


class Likepublication(models.Model):
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} likes {self.publication.content}'



#------------------fin Creation du like d'une publication-------------------------




#------------------Creation du like d'un commentaire pour les publications-------------------------

class Like_commentairepublication(models.Model):
    commentairepublication = models.ForeignKey(Commentairepublication, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} likes {self.commentairepublication.contenu}'


#------------------fin Creation du like d'un commentaire pour les publications-------------------------




#------------------Debut Creation modele video -------------------------

class Video(models.Model):
    content = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(default=timezone.now)
    date_publication = models.DateTimeField(default=timezone.now)
    video = models.FileField(upload_to='akue/static/akue/videos/', null=True, blank=True)

    def __str__(self):
        return self.content
    
    
    
    
    
#------------------fin Creation  modele video-------------------------
#------------------Creation calcule de temps depuis la création d'un article pour les actualités-------------------------
    
    
    
    def temps_publication(self):
        actu = timezone.now()
        diff = actu - self.date_creation
        if diff < timedelta(minutes=1):
            return f"{diff.seconds} secondes"
        elif diff < timedelta(hours=1):
            return f"{diff.seconds//60} minutes"
        elif diff < timedelta(days=1):
            return f"{diff.seconds//3600} heures"
        elif diff < timedelta(days=30):
            return f"{diff.days} jours"
        elif diff < timedelta(days=365):
            return f"{diff.days//30} mois"
        else:
            return f"{diff.days//365} ans"
    

#------------------fin de Creation d'une video -------------------------



#------------------Creation d'un commentaire pour les videos-------------------------



class Commentairevideo (models.Model):
    video = models.ForeignKey('Video', on_delete=models.CASCADE, related_name='commentairesvideo')
    auteur = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    contenu = models.TextField()
    date_creation = models.DateTimeField(default=timezone.now)
    approuve = models.BooleanField(default=False)

    def approuver(self):
        self.approuve = True
        self.save()

    def __str__(self):
        return self.contenu





#------------------fin Creation d'un commentaire pour les videos-------------------------



#------------------Creation du like d'un video-------------------------


class Likevideo(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} likes {self.video.content}'
    
    def get_like_count(self):
        return self.likevideo_set.count()



#------------------fin Creation du like d'une video-------------------------




#------------------Creation du like d'un commentaire pour les videos-------------------------

class Like_commentairevideo(models.Model):
    commentairevideo = models.ForeignKey(Commentairevideo, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} likes {self.commentairevideo.contenu}'


#------------------fin Creation du like d'un commentaire pour les videos-------------------------