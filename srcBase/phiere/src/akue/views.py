from django.shortcuts import render, get_object_or_404 , redirect
from django.http import HttpResponse
from django.template import loader
from datetime import date
from datetime import datetime
import random
import magic
from django.urls import reverse
from django.views.generic import ListView
import re



from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserProfile


from .forms import JokeForm

from .forms import ServiceForm,OffreForm,PublicationForm,VideoForm


#from .models import Service

from django.http import JsonResponse




from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.shortcuts import HttpResponseRedirect

from django.contrib.auth.decorators import login_required


from .models import UserProfile , Article, Commentaire, Like, Like_commentaire,Service,Commentaireservice,Likeservice,Like_commentaireservice,Offre,Commentaireoffre,Likeoffre,Like_commentaireoffre,Publication,Commentairepublication,Likepublication,Like_commentairepublication,Video,Commentairevideo,Likevideo,Like_commentairevideo 



import openai

openai.api_key = "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"

#model_engine = "davinci"

import os
from django.conf import settings







# Create your views here.











def index(request):
    today = date.today()
    now = datetime.now()
    # Format the date and time as a string
    current_time = now.strftime("%H:%M:%S")
    #print("l'heure actuel =", current_time)  
    return render(request, 'akue/index.html',{'d': today,'h': current_time})

def jeux(request):
    #message = "Salut tous le monde !"
    #template = loader.get_template('akue/jeux.html')
    #return HttpResponse(template.render(request=request))
    return render(request, 'akue/jeux.html')





# Define the view function
prizes = [
    ('$50 Amazon Gift Card', 0.05),
    ('$20 Starbucks Gift Card', 0.1),
    ('Free T-Shirt', 0.2),
    ('No Prize', 0.65),
]


def game(request):
    # If the user has submitted a guess, process it
    if request.method == 'POST':
        guess = request.POST['guess']
        prize = random.choices([p[0] for p in prizes], [p[1] for p in prizes])[0]
        #prize = 1
        print(" guess = ", guess ," & ", " prize = ", prize)
        if guess == prize:
            message = f"Félicitations, vous avez gagné un {prize}"
        else:
            message = f"Désolé, vous n'avez pas gagné de prix.  Le prix gagnant était {prize}."
        return render(request, 'akue/game.html', {'message': message})

    # Otherwise, just display the form
    return render(request, 'akue/game.html')









# Define the view function
def resultat(request):
    print("sALUT JE SUIS DANS RESULTAT")
    print("JE SUIS AU DEBUT")
    # If the user has submitted a guess, process it
    
    if request.method == 'POST':
        guess = request.POST['guess']
        prize = random.choices([p[0] for p in prizes], [p[1] for p in prizes])[0]
        if guess == prize:
            message = f'Félicitations, vous avez gagné un {prize}!'
            print(message)
        else:
            message = f"Sorry, you did not win a prize. The winning prize was {prize}."
            print(message)
        return render(request, 'akue/resultat.html', {'message': message})

    # Otherwise, just display the form
    
    print("JE SUIS À LA FIN")
    return render(request, 'akue/resultat.html')








#------------------------- Debut Enregistrement / Concection / Deconnection -------------------------------------------


def enregistrement(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Votre compte a été créé avec succès !')
            return redirect('/')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = UserCreationForm()

    # Ajout des classes Bootstrap
    form.fields['username'].widget.attrs.update({'class': 'form-control border border-info'})
    form.fields['password1'].widget.attrs.update({'class': 'form-control border border-info'})
    form.fields['password2'].widget.attrs.update({'class': 'form-control border border-info'})

    return render(request, 'akue/enregistrement.html', {'form': form})

    
    





def connexion(request):
    if request.user.is_authenticated:
        return render(request, 'akue/index.html')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            msg = "Nom d'utilisateur ou mot de passe incorrect"
            form = AuthenticationForm(request.POST)
            # Ajout des classes Bootstrap
            form.fields['username'].widget.attrs.update({'class': 'form-control border border-info'})
            form.fields['password'].widget.attrs.update({'class': 'form-control border border-info'})
            return render(request, 'akue/connexion.html', {'form': form, 'msg': msg})
    else:
        form = AuthenticationForm()
        # Ajout des classes Bootstrap
        form.fields['username'].widget.attrs.update({'class': 'form-control border border-info'})
        form.fields['password'].widget.attrs.update({'class': 'form-control border border-info'})
        return render(request, 'akue/connexion.html', {'form': form})
    

def deconnexion(request):
    logout(request)
    return redirect('akue:connexion')




#---------------------------- Fin Enregistrement / Concection / Deconnection ------------------------------------------

def profil(request):
    #message = "Salut tous le monde !"
    #template = loader.get_template('akue/jeux.html')
    #return HttpResponse(template.render(request=request))
    return render(request, 'akue/profil.html')

def myProfil(request):
    user_profile = UserProfile.objects.get(user=request.user)
    context = {
        'user_profile': user_profile,
    }
    
    return render(request, 'akue/myProfil.html', context)


#----------------------- 

def acceuil(request):
    if request.user.is_authenticated:
        form = ServiceForm(request.POST, request.FILES)
        offreform = OffreForm(request.POST, request.FILES)
        user_profile = UserProfile.objects.get(user=request.user)
        user_profiles = UserProfile.objects.all()
        publicationForm=PublicationForm(request.POST, request.FILES)
        publications= Publication.objects.order_by('-date_creation')
        services = Service.objects.order_by('-date_creation')
        dernier_service = Service.objects.last()
        offres = Offre.objects.order_by('-date_creation')
        dernier_offre = Offre.objects.last()
        videos = Video.objects.order_by('-date_creation')
        commentairesvideo = Commentairevideo.objects.order_by('-date_creation')
        articles = Article.objects.order_by('-date_creation')
        commentaires = Commentaire.objects.order_by('-date_creation')
        commentairespublication = Commentairepublication.objects.order_by('-date_creation')
        commentairesservice = Commentaireservice.objects.order_by('-date_creation')
        commentairesoffre= Commentaireoffre.objects.order_by('-date_creation')
        likes = Like.objects.all()
        likepublication = Likepublication.objects.all()
        likes_commentaire = Like_commentaire.objects.all()
        likesservice = Likeservice.objects.all()
        likes_commentaireservice = Like_commentaireservice.objects.all()
        likesoffre= Likeoffre.objects.all()
        likes_commentaireoffre= Like_commentaireoffre.objects.all()

        # Ajouter la clé "table_name" dans le contexte
        context = {
        'form': form,
        'offreform': offreform,
        'publicationForm': publicationForm,
        'user_profile': user_profile,
        'publications':publications,
        'services': services,
        'videos': videos,
        'commentairesvideo':commentairesvideo,
        'dernier_service': dernier_service,
        'articles': articles,
        'commentairespublication':commentairespublication,
        'commentaires': commentaires,
        'commentairesservice': commentairesservice,
        'commentairesoffre': commentairesoffre,
        'likes':likes,
        'likes_commentaire':likes_commentaire,
        'likesservice':likesservice,
        'likes_commentaireservice':likes_commentaireservice,
        'offres': offres,
        'dernier_offre': dernier_offre,
        'likesoffre':likesoffre,
        'likes_commentaireoffre':likes_commentaireoffre,
        'table_nameS': 'Service', # Remplacez "Service" par le nom de la table correspondante
        'table_nameO': 'Offre',
        'table_nameA': 'Actualité',
        'table_nameP': 'Publication'
        }
        return render(request, 'akue/acceuil.html', context)
    else:
        return redirect('akue:connexion')
    
    
    
    
    #------------------------------- fin vue page liste offres-------------------------------------------

def alloffres(request):
    if request.user.is_authenticated:
        form = ServiceForm(request.POST, request.FILES)
        offreform = OffreForm(request.POST, request.FILES)
        user_profile = UserProfile.objects.get(user=request.user)
        user_profiles = UserProfile.objects.all()
        publicationForm=PublicationForm(request.POST, request.FILES)
        publications= Publication.objects.order_by('-date_creation')
        services = Service.objects.order_by('-date_creation')
        dernier_service = Service.objects.last()
        offres = Offre.objects.order_by('-date_creation')
        dernier_offre = Offre.objects.last()

        articles = Article.objects.order_by('-date_creation')
        commentaires = Commentaire.objects.order_by('-date_creation')
        commentairesservice = Commentaireservice.objects.order_by('-date_creation')
        commentairesoffre= Commentaireoffre.objects.order_by('-date_creation')
        likes = Like.objects.all()
        likes_commentaire = Like_commentaire.objects.all()
        likesservice = Likeservice.objects.all()
        likes_commentaireservice = Like_commentaireservice.objects.all()
        likesoffre= Likeoffre.objects.all()
        likes_commentaireoffre= Like_commentaireoffre.objects.all()

        # Ajouter la clé "table_name" dans le contexte
        context = {
        'form': form,
        'offreform': offreform,
        'publicationForm': publicationForm,
        'user_profile': user_profile,
        'publications':publications,
        'services': services,
        'dernier_service': dernier_service,
        'articles': articles,
        'commentaires': commentaires,
        'commentairesservice': commentairesservice,
        'commentairesoffre': commentairesoffre,
        'likes':likes,
        'likes_commentaire':likes_commentaire,
        'likesservice':likesservice,
        'likes_commentaireservice':likes_commentaireservice,
        'offres': offres,
        'dernier_offre': dernier_offre,
        'likesoffre':likesoffre,
        'likes_commentaireoffre':likes_commentaireoffre,
        'table_nameS': 'Service', # Remplacez "Service" par le nom de la table correspondante
        'table_nameO': 'Offre',
        'table_nameA': 'Actualité',
        'table_nameP': 'Publication'
        }
    
        return render(request, 'akue/alloffres.html', context)
    else:
        return redirect('akue:connexion')
    


#------------------------------- fin vue page de offres-------------------------------------------

#------------------------------- fin vue page liste Services-------------------------------------------


def allservices(request):
    if request.user.is_authenticated:
        form = ServiceForm(request.POST, request.FILES)
        offreform = OffreForm(request.POST, request.FILES)
        user_profile = UserProfile.objects.get(user=request.user)
        user_profiles = UserProfile.objects.all()
        publicationForm=PublicationForm(request.POST, request.FILES)
        publications= Publication.objects.order_by('-date_creation')
        services = Service.objects.order_by('-date_creation')
        dernier_service = Service.objects.last()
        offres = Offre.objects.order_by('-date_creation')
        dernier_offre = Offre.objects.last()

        articles = Article.objects.order_by('-date_creation')
        commentaires = Commentaire.objects.order_by('-date_creation')
        commentairesservice = Commentaireservice.objects.order_by('-date_creation')
        commentairesoffre= Commentaireoffre.objects.order_by('-date_creation')
        likes = Like.objects.all()
        likes_commentaire = Like_commentaire.objects.all()
        likesservice = Likeservice.objects.all()
        likes_commentaireservice = Like_commentaireservice.objects.all()
        likesoffre= Likeoffre.objects.all()
        likes_commentaireoffre= Like_commentaireoffre.objects.all()

        # Ajouter la clé "table_name" dans le contexte
        context = {
        'form': form,
        'offreform': offreform,
        'publicationForm': publicationForm,
        'user_profile': user_profile,
        'publications':publications,
        'services': services,
        'dernier_service': dernier_service,
        'articles': articles,
        'commentaires': commentaires,
        'commentairesservice': commentairesservice,
        'commentairesoffre': commentairesoffre,
        'likes':likes,
        'likes_commentaire':likes_commentaire,
        'likesservice':likesservice,
        'likes_commentaireservice':likes_commentaireservice,
        'offres': offres,
        'dernier_offre': dernier_offre,
        'likesoffre':likesoffre,
        'likes_commentaireoffre':likes_commentaireoffre,
        'table_nameS': 'Service', # Remplacez "Service" par le nom de la table correspondante
        'table_nameO': 'Offre',
        'table_nameA': 'Actualité',
        'table_nameP': 'Publication'
        }
        return render(request, 'akue/allservices.html', context)
    else:
        return redirect('akue:connexion')





#------------------------------- fin vue page liste-------------------------------------------






#def acceuil(request):
    #articles = Article.objects.filter(date_creation__isnull=False).order_by('-date_creation')
    #services = Service.objects.filter(date_creation__isnull=False).order_by('-date_creation')
    #offres = Offre.objects.filter(date_creation__isnull=False).order_by('-date_creation')
    #publications = Publication.objects.filter(date_creation__isnull=False).order_by('-date_creation')
    #all_items = list(articles) + list(services) + list(offres) + list(publications)
    #all_items = sorted(all_items, key=lambda x: x.date_creation, reverse=True)
    #print("mes itemes : ", all_items)
    #print("mon 1er itemes : ", all_items[1])
    #for objet in all_items:
    #    if objet is not None:
    #        nom_objet_match = re.search('<(\w+):', str(objet))
    #        print("---------------------------------------")
    #        if nom_objet_match is not None:
    #            nom_objet = nom_objet_match.group(1)
    #            print("nom : ",nom_objet)
    #            print("---------------------------------------")
    #return render(request, 'akue/acceuil.html', {'all_items': all_items})














#def ia(request):
#    #message = "Salut tous le monde !"
#    #template = loader.get_template('akue/jeux.html')
#    #return HttpResponse(template.render(request=request))
#    return render(request, 'akue/ia.html')










#-------------------------------Debut API Chat GPT -------------------------------------------

def chatBot(request):
    message=""
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        response = {}
        if request.method == 'POST':
            message = request.POST.get('message')
            # Utilisation de l'API OpenAI pour obtenir une réponse
            response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"Conversation avec un utilisateur : {message}\nBot:",
            temperature=0.7,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
            )
        # Ajout de la réponse à notre contexte
            response =response.choices[0].text.strip()
            message=message
        return render(request, 'akue/chatBot.html', {'response':response,'user_profile':user_profile, 'message ':message})
    
    else:
        return redirect('akue:connexion')
    
    
    

def devinettes(request):
    user_profile = UserProfile.objects.get(user=request.user)
    riddle = {}
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        model = 'text-davinci-002' # utilisez le modèle de langue français
        completions = openai.Completion.create(
            engine=model,
            prompt=prompt,
            max_tokens=60,
            n=1,
            stop=None,
            temperature=0.5,
        )
        riddle = completions.choices[0].text.strip()
    return render(request, 'akue/devinettes.html', {'riddle': riddle, 'user_profile': user_profile})


def conseil(request):
    user_profile = UserProfile.objects.get(user=request.user)
    advice = {}
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        model = 'text-davinci-002'
        completions = openai.Completion.create(
            engine=model,
            prompt=prompt,
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.5,
        )

        advice = completions.choices[0].text.strip()
    return render(request, 'akue/conseil.html', {'advice': advice,'user_profile': user_profile})

def citations(request):
    user_profile = UserProfile.objects.get(user=request.user)
    quote ={}
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        model = 'text-davinci-002'
        completions = openai.Completion.create(
            engine=model,
            prompt=prompt,
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.7,
        )
        quote = completions.choices[0].text.strip()
    return render(request, 'akue/citations.html', {'quote': quote,'user_profile': user_profile})

# def blagues(request):
#    model_engine = "text-davinci-002"
#    prompt = (f"Générer une blague drôle à propos de {request.GET.get('topic', 'les chats')}")
   # response = openai.Completion.create(
   #     engine=model_engine,
   #     prompt=prompt,
   #     max_tokens=60,
   #     n=1,
   #     stop=None,
   #     temperature=0.7,
        #model="text-fr-002" # Ajouter cette ligne pour sélectionner le modèle français
    #)
    #joke = response.choices[0].text.strip()
    #return render(request, 'akue/blagues.html', {'joke': joke})






def blagues(request):
    user_profile = UserProfile.objects.get(user=request.user)
    model_engine = "text-davinci-002"
    form = JokeForm(request.GET or None)
    if form.is_valid():
        topic = form.cleaned_data['topic']
        prompt = (f"Générer une blague drôle à propos de {topic}")
        response = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=60,
            n=1,
            stop=None,
            temperature=0.7,
        )
        joke = response.choices[0].text.strip()
        return render(request, 'akue/blagues.html', {'joke': joke, 'form': form})
    return render(request, 'akue/blagues.html', {'form': form,'user_profile': user_profile})



#-------------------------------FIN API Chat GPT -------------------------------------------









#------------------------------- Debut Affichage Article et commentaire -------------------------------------------










def creer_article(request):
    if request.method == 'POST':
        #titre = request.POST.get('titre')
        contenu = request.POST.get('contenu')
        auteur = request.user
        article = Article(contenu=contenu, auteur=auteur)
        article.save()
        return redirect('/')
    return render(request, 'akue/acceuil.html')








def creer_commentaire(request, article_id):
    if request.method == 'POST':
        article = Article.objects.get(id=article_id)
        contenu = request.POST.get('contenu')
        commentaire = Commentaire(article=article, auteur=request.user, contenu=contenu)
        commentaire.save()
        return redirect('/')
    return render(request, 'akue/acceuil.html', {'article': article})






#------------------------------- FIN Affichage Article et commentaire -------------------------------------------


#------------------------------- debut ajout like pour Article et commentaire des article -------------------------------------------





def like_article(request, article_id):
    article = None  # initialiser avec une valeur par défaut
    if request.method == 'POST':
        article = get_object_or_404(Article, id=article_id)
        like, created = Like.objects.get_or_create(article=article, user=request.user)
        if not created:
            like.delete()
        return redirect('/')
    
    # si la méthode n'est pas POST, retourner une réponse HTTP appropriée
    return render(request, 'akue/acceuil.html', {'article': article})



def like_commentaire(request, commentaire_id):
    commentaire = None  # initialiser avec une valeur par défaut
    if request.method == 'POST':
        print("Je suis dans le premier if de like_commentaire")
        commentaire = get_object_or_404(Commentaire, id=commentaire_id)
        like_commentaire, created = Like_commentaire.objects.get_or_create(commentaire=commentaire, user=request.user)
        if not created:
            print("Je suis dans le second if de like_commentaire")
            like_commentaire.delete()
            
        return redirect('/')
        
    # si la méthode n'est pas POST, retourner une réponse HTTP appropriée
    print("Je suis pas rentrer dans les if de like_commentaire")
    return render(request, 'akue/acceuil.html', {'commentaire': commentaire})



#------------------------------- fin ajout like  pour Article et commentaire des articles-------------------------------------------










#------------------------------- debut vue creation de service -------------------------------------------




def creer_service(request):
    
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        
        if form.is_valid():
            service = form.save(commit=False)
            service.author = request.user
            print(service)
            # Vérifier si le formulaire contient une image
            print(request.FILES)
            if 'image' in request.FILES:
                # Ne pas enregistrer l'image tout de suite
                service.save()
                
                # Mettre à jour le chemin de l'image
                image_name = service.image.name
                image_path = image_name
                
                if image_path.startswith(os.path.join(settings.MEDIA_ROOT, 'akue')):
                    service.image.name = os.path.relpath(image_path, os.path.join(settings.MEDIA_ROOT, 'akue'))
                    print('--------------Je suis dans le If-------------')
                else:
                    service.image.name = os.path.join('static', 'akue', 'img', 'service_images', image_name)
                    print('--------------je suis dans le elss -------------')
                
                # Enregistrer l'image maintenant
                service.save()
                
            else:
                # Enregistrer le service sans image
                service.save()
            
            return redirect('/')
    else:
        form = ServiceForm()
    context = {'form': form}
    return render(request, 'akue/acceuil.html', context)





#def like_article(request, article_id):
    #article = get_object_or_404(Article, id=article_id)
    #like, created = Like.objects.get_or_create(article=article, user=request.user)
    #if not created:
    #    like.delete()
    #likes_count = article.num_likes()
    #response_data = {'likes': likes_count}
    #return JsonResponse(response_data)




#------------------------------- debut creation d'un commentaire pour un service -------------------------------------------

def creer_commentaireservice(request, service_id):
    if request.method == 'POST':
        service = Service.objects.get(id=service_id)
        contenu = request.POST.get('contenu')
        commentaireservice = Commentaireservice(service=service, auteur=request.user, contenu=contenu)
        commentaireservice.save()
        return redirect('/')
    return render(request, 'akue/acceuil.html', {'service': service})






#----------------------------------- fincreation d'un commentaire pour un service -------------------------------------------





#------------------------------- debut ajout like pour Service et commentaire des Services -------------------------------------------





def like_service(request, service_id):
    #print("---TEST---------TEST-------------------TEST----------------TEST------------TEST-----------TEST-----------------")
    service = None  # initialiser avec une valeur par défaut
    if request.method == 'POST':
        #print("---TEST1---------TEST1-------------------TEST1----------------TEST1------------TEST1-----------TEST1-----------------")
        print('Je suis dans le 1er if envoi de requet post')
        service = get_object_or_404(Service, id=service_id)
        likeservice, created = Likeservice.objects.get_or_create(service=service, user=request.user)
        if not created:
            #print("---TEST2---------TEST2-------------------TEST2----------------TEST2------------TEST2-----------TEST2-----------------")
            print('Je suis dans le 2nd if envoi de requet post')
            likeservice.delete()
        return redirect('/')
    #print("---TEST3---------TEST3-------------------TEST3----------------TEST3------------TEST3-----------TEST3-----------------")
    # si la méthode n'est pas POST, retourner une réponse HTTP appropriée
    return render(request, 'akue/acceuil.html', {'service': service})



def like_commentaireservice(request, commentaireservice_id):
    commentaireservice = None  # initialiser avec une valeur par défaut
    if request.method == 'POST':
        
        print("Je suis dans le premier if de like_commentaireservice")
        commentaireservice = get_object_or_404(Commentaireservice, id=commentaireservice_id)
        like_commentaireservice, created = Like_commentaireservice.objects.get_or_create(commentaireservice=commentaireservice, user=request.user)
        if not created:
            print("Je suis dans le second if de like_commentaireservice")
            like_commentaireservice.delete()
            
        return redirect('/')
        
    # si la méthode n'est pas POST, retourner une réponse HTTP appropriée
    print("Je suis pas rentrer dans les if de like_commentaireservice")
    return render(request, 'akue/acceuil.html', {'commentaireservice': commentaireservice})



#------------------------------- fin ajout like  pour Article et commentaire des Services------------------------------------------















#------------------------------- debut vue creation de offre -------------------------------------------




def creer_offre(request):
    print('------------- Je rentre dans la fonction créer offre --------------')
    if request.method == 'POST':
        form = OffreForm(request.POST, request.FILES)
        print(form)
        print("---------------J'ai recupéré la requete-------------")
        if form.is_valid():
            print("---------Je verifie si le formulaire est rempli correctement--------")
            offre = form.save(commit=False)
            offre.author = request.user
            print(offre)
            print(request.FILES)
            # Vérifier si le formulaire contient une image
            if 'image' in request.FILES:
                print("------# Vérifier si le formulaire contient une image------------")
                # Ne pas enregistrer l'image tout de suite
                offre.save()
                print("--------------J'enregistre le formulaire------------")
                # Mettre à jour le chemin de l'image
                image_name = offre.image.name
                image_path = image_name
                
                if image_path.startswith(os.path.join(settings.MEDIA_ROOT, 'akue')):
                    offre.image.name = os.path.relpath(image_path, os.path.join(settings.MEDIA_ROOT, 'akue'))
                    print('--------------Je suis dans le If-------------')
                else:
                    offre.image.name = os.path.join('static', 'akue', 'img', 'offre_images', image_name)
                    print('--------------je suis dans le elss -------------')
                
                # Enregistrer l'image maintenant
                offre.save()
                print("----------J'ai fini de modifier le chemin de l'image-------")
            else:
                # Enregistrer le offre sans image
                offre.save()
                print("--------J'enregistre les informations de l'offre---------:",offre)
            
            return redirect('/')
    else:
        form =  OffreForm()
    context = {'form': form}
    print(context)
    return render(request, 'akue/acceuil.html', context)





#def like_article(request, article_id):
    #article = get_object_or_404(Article, id=article_id)
    #like, created = Like.objects.get_or_create(article=article, user=request.user)
    #if not created:
    #    like.delete()
    #likes_count = article.num_likes()
    #response_data = {'likes': likes_count}
    #return JsonResponse(response_data)




#------------------------------- debut creation d'un commentaire pour un offre -------------------------------------------

def creer_commentaireoffre(request, offre_id):
    if request.method == 'POST':
        offre = Offre.objects.get(id=offre_id)
        contenu = request.POST.get('contenu')
        commentaireoffre = Commentaireoffre(offre=offre, auteur=request.user, contenu=contenu)
        commentaireoffre.save()
        return redirect('/')
    return render(request, 'akue/acceuil.html', {'offre': offre})






#----------------------------------- fincreation d'un commentaire pour un offre -------------------------------------------





#------------------------------- debut ajout de like pour un offre et commentaire des offres -------------------------------------------





def like_offre(request, offre_id):
    offre = None  # initialiser avec une valeur par défaut
    if request.method == 'POST':
        print('Je suis dans le 1er if envoi de requet post')
        offre = get_object_or_404(Offre, id=offre_id)
        likeoffre, created = Likeoffre.objects.get_or_create(offre=offre, user=request.user)
        if not created:
            print('Je suis dans le 2nd if envoi de requet post')
            likeoffre.delete()
        return redirect('/')
    
    # si la méthode n'est pas POST, retourner une réponse HTTP appropriée
    return render(request, 'akue/acceuil.html', {'offre': offre})



def like_commentaireoffre(request, commentaireoffre_id):
    commentaireoffre = None  # initialiser avec une valeur par défaut
    if request.method == 'POST':
        
        print("Je suis dans le premier if de like_commentaireoffre")
        commentaireoffre = get_object_or_404(Commentaireoffre, id=commentaireoffre_id)
        like_commentaireoffre, created = Like_commentaireoffre.objects.get_or_create(commentaireoffre=commentaireoffre, user=request.user)
        if not created:
            print("Je suis dans le second if de like_commentaireoffre")
            like_commentaireoffre.delete()
            
        return redirect('/')
        
    # si la méthode n'est pas POST, retourner une réponse HTTP appropriée
    print("Je suis pas rentrer dans les if de like_commentaireoffre")
    return render(request, 'akue/acceuil.html', {'commentaireoffre': commentaireoffre})



#------------------------------- fin ajout like  pour Article et commentaire des Offres------------------------------------------








#------------------------------- debut vue creation de publication  -------------------------------------------




def creer_publication (request):
    
    if request.method == 'POST':
        form = PublicationForm(request.POST, request.FILES)
        
        if form.is_valid():
            publication  = form.save(commit=False)
            publication.author = request.user
            print(publication )
            # Vérifier si le formulaire contient une image
            print(request.FILES)
            if 'image' in request.FILES:
                # Ne pas enregistrer l'image tout de suite
                publication.save()
                
                # Mettre à jour le chemin de l'image
                image_name = publication.image.name
                image_path = image_name
                
                if image_path.startswith(os.path.join(settings.MEDIA_ROOT, 'akue')):
                    publication.image.name = os.path.relpath(image_path, os.path.join(settings.MEDIA_ROOT, 'akue'))
                    print('--------------Je suis dans le If-------------')
                else:
                    publication.image.name = os.path.join('static', 'akue', 'img', 'publication_images', image_name)
                    print('--------------je suis dans le elss -------------')
                
                # Enregistrer l'image maintenant
                publication.save()
                
            else:
                # Enregistrer le publication sans image
                publication.save()
            
            return redirect('/')
    else:
        form = PublicationForm()
    context = {'form': form}
    return render(request, 'akue/acceuil.html', context)





#def like_article(request, article_id):
    #article = get_object_or_404(Article, id=article_id)
    #like, created = Like.objects.get_or_create(article=article, user=request.user)
    #if not created:
    #    like.delete()
    #likes_count = article.num_likes()
    #response_data = {'likes': likes_count}
    #return JsonResponse(response_data)




#------------------------------- debut creation d'un commentaire pour un publication -------------------------------------------

def creer_commentairepublication(request, publication_id):
    if request.method == 'POST':
        publication = Publication.objects.get(id=publication_id)
        contenu = request.POST.get('contenu')
        commentairepublication = Commentairepublication(publication=publication, auteur=request.user, contenu=contenu)
        commentairepublication.save()
        return redirect('/')
    return render(request, 'akue/acceuil.html', {'publication': publication})






#----------------------------------- fincreation d'un commentaire pour un publication -------------------------------------------





#------------------------------- debut ajout like pour publication et commentaire des publication -------------------------------------------





def like_publication(request, publication_id):
    #print("---TEST---------TEST-------------------TEST----------------TEST------------TEST-----------TEST-----------------")
    publication = None  # initialiser avec une valeur par défaut
    if request.method == 'POST':
        #print("---TEST1---------TEST1-------------------TEST1----------------TEST1------------TEST1-----------TEST1-----------------")
        print('Je suis dans le 1er if envoi de requet post')
        publication = get_object_or_404(Publication, id=publication_id)
        likepublication, created = Likepublication.objects.get_or_create(publication=publication, user=request.user)
        if not created:
            #print("---TEST2---------TEST2-------------------TEST2----------------TEST2------------TEST2-----------TEST2-----------------")
            print('Je suis dans le 2nd if envoi de requet post')
            likepublication.delete()
        return redirect('/')
    #print("---TEST3---------TEST3-------------------TEST3----------------TEST3------------TEST3-----------TEST3-----------------")
    # si la méthode n'est pas POST, retourner une réponse HTTP appropriée
    return render(request, 'akue/acceuil.html', {'publication': publication})



def like_commentairepublication(request, commentairepublication_id):
    commentaireservice = None  # initialiser avec une valeur par défaut
    if request.method == 'POST':
        
        print("Je suis dans le premier if de like_commentaireservice")
        commentairepublication = get_object_or_404(Commentairepublication, id=commentairepublication_id)
        like_commentairepublication, created = Like_commentairepublication.objects.get_or_create(commentairepublication=commentairepublication, user=request.user)
        if not created:
            print("Je suis dans le second if de like_commentairepublication")
            like_commentairepublication.delete()
            
        return redirect('/')
        
    # si la méthode n'est pas POST, retourner une réponse HTTP appropriée
    print("Je suis pas rentrer dans les if de like_commentairepublication")
    return render(request, 'akue/acceuil.html', {'commentairepublication': commentairepublication})



#------------------------------- fin ajout like  pour Article et commentaire des Services------------------------------------------


#------------------------------- debut vue page Liste video-------------------------------------------

def listvideo(request):
    if request.user.is_authenticated:
        form = ServiceForm(request.POST, request.FILES)
        offreform = OffreForm(request.POST, request.FILES)
        user_profile = UserProfile.objects.get(user=request.user)
        user_profiles = UserProfile.objects.all()
        publicationForm=PublicationForm(request.POST, request.FILES)
        dernier_service = Service.objects.last()
        dernier_offre = Offre.objects.last()
        videos = Video.objects.order_by('-date_creation')
        commentairesvideo = Commentairevideo.objects.order_by('-date_creation')
        # Ajouter la clé "table_name" dans le contexte
        context = {
        'form': form,
        'offreform': offreform,
        'publicationForm': publicationForm,
        'user_profile': user_profile,
        'videos': videos,
        'commentairesvideo':commentairesvideo,
        'dernier_service': dernier_service,
        'dernier_offre': dernier_offre,
        'table_nameS': 'Service', # Remplacez "Service" par le nom de la table correspondante
        'table_nameO': 'Offre',
        'table_nameA': 'Actualité',
        'table_nameP': 'Publication'
        }
        return render(request, 'akue/listeVideo.html', context)
    else:
        return redirect('akue:connexion')



#------------------------------- fin vue page liste Video-------------------------------------------




def creer_video_(request):
    
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        
        if form.is_valid():
            video = form.save(commit=False)
            video.author = request.user
            print(video )
            # Vérifier si le formulaire contient une video
            print(request.FILES)
            if 'video' in request.FILES:
                # Ne pas enregistrer l'video tout de suite
                video.save()
                
                # Mettre à jour le chemin de l'video
                video_name = video.name
                video_path = video_name
                
                if video_path.startswith(os.path.join(settings.MEDIA_ROOT, 'akue')):
                    video.video.name = os.path.relpath(video_path, os.path.join(settings.MEDIA_ROOT, 'akue'))
                    print('--------------Je suis dans le If-------------')
                else:
                    video.name = os.path.join('static', 'akue', 'videos', video_name)
                    print('--------------je suis dans le elss -------------')
            
                # Enregistrer l'video maintenant
                video.save()
            
            else:
                # Enregistrer la publication sans video
                video.save()
            
            return redirect('akue:listvideo')
    else:
        form = VideoForm()
    context = {'form': form}
    return render(request, 'akue/listeVideo.html', context)







def creer_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video_file = form.cleaned_data['video']
            # Vérifier le type de fichier
            file_type = magic.from_buffer(video_file.read(), mime=True)
            if file_type.startswith('video/'):
                # Enregistrer la vidéo dans le dossier de votre choix
                # Exemple : media/videos/
                with open('akue/static/akue/videos/' + video_file.name, 'wb+') as destination:
                    for chunk in video_file.chunks():
                        destination.write(chunk)

                # Créer une instance de Video et enregistrer les données dans la base de données
                video = Video(
                    content=form.cleaned_data['content'],
                    author=request.user,
                    video='static/akue/videos/' + video_file.name
                )
                video.save()

                # Effectuer les autres opérations nécessaires
                # ...

                return redirect('akue:listvideo')
            else:
                # Le fichier n'est pas une vidéo
                form.add_error('video', 'Veuillez sélectionner un fichier vidéo.')
    else:
        form = VideoForm()
    context = {'form': form}
    return render(request, 'akue/listeVideo.html', context)







#def like_article(request, article_id):
    #article = get_object_or_404(Article, id=article_id)
    #like, created = Like.objects.get_or_create(article=article, user=request.user)
    #if not created:
    #    like.delete()
    #likes_count = article.num_likes()
    #response_data = {'likes': likes_count}
    #return JsonResponse(response_data)




#------------------------------- debut creation d'un commentaire pour un video -------------------------------------------

def creer_commentairevideo(request, video_id):
    if request.method == 'POST':
        video = Video.objects.get(id=video_id)
        contenu = request.POST.get('contenu')
        commentairevideo = Commentairevideo(video=video, auteur=request.user, contenu=contenu)
        commentairevideo.save()
        return redirect('akue:listvideo')
    return render(request, 'akue/listeVideo.html', {'video': video})






#----------------------------------- fincreation d'un commentaire pour un video -------------------------------------------





#------------------------------- debut ajout like pour video et commentaire des videos -------------------------------------------





def like_video(request, video_id):
    video = None  # initialiser avec une valeur par défaut
    if request.method == 'POST':
        print('Je suis dans le 1er if envoi de requet post')
        video = get_object_or_404(Video, id=video_id)
        likevideo, created = Likevideo.objects.get_or_create(video=video, user=request.user)
        if not created:
            print('Je suis dans le 2nd if envoi de requet post')
            likevideo.delete()
        return redirect('akue:listvideo')
    return render(request, 'akue/acceuil.html', {'video': video})

#def like_video(request, video_id):
#    video = None
#    if request.method == 'POST':
#        video = get_object_or_404(Video, id=video_id)
#        likevideo, created = Likevideo.objects.get_or_create(video=video, user=request.user)
#        if not created:
#            likevideo.delete()
#        like_count = video.likevideo_set.count()
#        return JsonResponse({'like_count': like_count})
#    return render(request, 'akue/acceuil.html', {'video': video})


def like_commentairevideo(request, commentairevideo_id):
    commentaireservice = None  # initialiser avec une valeur par défaut
    if request.method == 'POST':
        
        print("Je suis dans le premier if de like_commentaireservice")
        commentairevideo = get_object_or_404(Commentairevideo, id=commentairevideo_id)
        like_commentairevideo, created = Like_commentairevideo.objects.get_or_create(commentairevideo =commentairevideo, user=request.user)
        if not created:
            print("Je suis dans le second if de like_commentairevideo")
            like_commentairevideo.delete()
            
        return redirect('akue:listvideo')
        
    # si la méthode n'est pas POST, retourner une réponse HTTP appropriée
    print("Je suis pas rentrer dans les if de like_commentairevideo")
    return render(request, 'akue/listeVideo.html', {'commentairevideo': commentairevideo})



#------------------------------- fin ajout like  pour Article et commentaire des Services------------------------------------------









#------------------------------- debut vue page de test-------------------------------------------



def pageTest(request):
    services = Service.objects.order_by('-date_creation')
    
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False)
            service.author = request.user
            
            # Vérifier si le formulaire contient une image
            if 'image' in request.FILES:
                # Ne pas enregistrer l'image tout de suite
                service.save()
                
                # Mettre à jour le chemin de l'image
                image_name = service.image.name
                image_path = image_name
                
                if image_path.startswith(os.path.join(settings.MEDIA_ROOT, 'akue')):
                    service.image.name = os.path.relpath(image_path, os.path.join(settings.MEDIA_ROOT, 'akue'))
                    print('--------------Je suis dans le If-------------')
                else:
                    service.image.name = os.path.join('static', 'akue', 'img', 'service_images', image_name)
                    print('--------------je suis dans le elss -------------')
                
                # Enregistrer l'image maintenant
                service.save()
                
            else:
                # Enregistrer le service sans image
                service.save()
            
            return redirect('akue:pageTest')
    else:
        form = ServiceForm()
    context = {'form': form, 'services': services}
    
    return render(request, 'akue/custom_file_input.html', context)















#------------------------------- debut vue page de test-------------------------------------------

