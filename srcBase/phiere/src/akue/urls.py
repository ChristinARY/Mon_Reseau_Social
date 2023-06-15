from django.urls import re_path as url
from django.urls import include, path

app_name = 'akue'

from . import views

urlpatterns = [
    #path('', views.index, name="index"),
    path('pageTest/', views.pageTest, name="pageTest"),
    path('jeux/', views.jeux, name="jeux"),
    path('game/', views.game, name="game"),
    path('connexion/', views.connexion, name="connexion"),
    path('deconnexion/', views.deconnexion, name="deconnexion"),
    path('enregistrement/', views.enregistrement, name="enregistrement"),
    path('profil/', views.profil, name="profil"),
    path('myProfil/', views.myProfil, name="myProfil"),
    #path('acceuil/', views.acceuil, name="acceuil"),
    path('allservices/', views.allservices, name="allservices"),
    path('alloffres/', views.alloffres, name="alloffres"),
    path('chatBot/', views.chatBot, name="chatBot"),
    path('devinettes/', views.devinettes, name="devinettes"),
    path('conseil/', views.conseil, name="conseil"),
    path('citations/', views.citations, name="citations"),
    path('blagues/', views.blagues, name="blagues"),
    path('creer_article/', views.creer_article, name="creer_article"),
    path('article/<int:article_id>/commentaire/', views.creer_commentaire, name='creer_commentaire'),
    path('like_article/<int:article_id>/', views.like_article, name='like_article'),
    path('like_commentaire/<int:commentaire_id>/', views.like_commentaire, name='like_commentaire'),
    path('creer_service/', views.creer_service, name="creer_service"),
    path('service/<int:service_id>/commentaireservice/', views.creer_commentaireservice, name='creer_commentaireservice'),
    path('like_service/<int:service_id>/', views.like_service, name='like_service'),
    path('like_commentaireservice/<int:commentaireservice_id>/', views.like_commentaireservice, name='like_commentaireservice'),
    path('creer_offre/', views.creer_offre, name="creer_offre"),
    path('offre/<int:offre_id>/commentaireoffre/', views.creer_commentaireoffre, name='creer_commentaireoffre'),
    path('like_offre/<int:offre_id>/', views.like_offre, name='like_offre'),
    path('like_commentaireoffre/<int:commentaireoffre_id>/', views.like_commentaireoffre, name='like_commentaireoffre'),
    path('creer_publication/', views.creer_publication, name="creer_publication"),
    path('publication/<int:publication_id>/commentairepublication/', views.creer_commentairepublication, name='creer_commentairepublication'),
    path('like_publication/<int:publication_id>/', views.like_publication, name='like_publication'),
    path('like_commentairepublication/<int:commentairepublication_id>/', views.like_commentairepublication, name='like_commentairepublication'),
    path('listvideo/', views.listvideo, name="listvideo"),
    path('creer_video/', views.creer_video, name="creer_video"),
    path('video/<int:video_id>/commentairevideo/', views.creer_commentairevideo, name='creer_commentairevideo'),
    path('like_video/<int:video_id>/', views.like_video, name='like_video'),
    path('like_commentairevideo/<int:commentairevideo_id>/', views.like_commentairevideo, name='like_commentairevideo'),
]