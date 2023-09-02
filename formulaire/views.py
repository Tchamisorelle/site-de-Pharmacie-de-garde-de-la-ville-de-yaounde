from django.shortcuts import render, redirect
from .models import formulaire_utilisateurr, ResetLink
from django.contrib.auth.models import User
from .until import send_notification_email, send_signup_email
import re
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from email.utils import formataddr
from decouple import config
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.contrib.auth.views import PasswordResetConfirmView
from django.core.mail import send_mail
from datetime import timedelta
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
# from django.utils.text import force_bytes, force_text
from django.urls import reverse_lazy
from django.utils import timezone
from django.shortcuts import render
from django.views.generic import View
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.urls import reverse
from django.contrib import messages
# from django.contrib.auth import authenticate, login


# Create your views here.
def new_utilisateur(request):
    error_message = None
    
    if request.method == 'POST':
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        sexe = request.POST.get('sexe')
        mail = request.POST.get('mail')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        qualification_chercheur = 'qualification_chercheur' in request.POST
        qualification_mentor = 'qualification_mentor' in request.POST
        pays = request.POST.get('pays')
        
        if password != password_confirm:
            error_message = 'Les mots de passe ne correspondent pas'
        else:
            # Vérifications du mot de passe
            if len(password) < 8:
                error_message = 'Le mot de passe doit contenir au moins 8 caractères'
            elif not re.search(r'\d', password):
                error_message = 'Le mot de passe doit contenir au moins un chiffre'
            elif not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
                error_message = 'Le mot de passe doit contenir au moins un caractère spécial'
            else:
                # Hachage du mot de passe
                hashed_password = make_password(password)
                
                # Créer un nouvel objet Utilisateur et l'enregistrer dans la base de données
                nouvel_utilisateur = formulaire_utilisateurr.objects.create(
                    nom=nom, prenom=prenom, sexe=sexe, mail=mail,
                    password=hashed_password,
                    qualification_chercheur=qualification_chercheur,
                    qualification_mentor=qualification_mentor, pays=pays
                )
                nouvel_utilisateur.save()
                
                # Envoi du mail
                subject = 'Bienvenue chez TTS'
                message = (
                                f"Bienvenue {prenom}!"
                            )
                # sender_name = "APK Sorel"
                # sender_email = config('DEFAULT_FROM_EMAIL')
                # sender_formatted = formataddr((sender_name, sender_email))
                # attachment_path="f.pdf"
                # full_path = settings.STATIC_URL + attachment_path 
                full_path = [
                                "D:\small_projet\\formulaire_dyna\\formulaire\\static\\t.jpg"]
                
                recipient_list = [mail]
                send_notification_email(subject=subject, message=message, recipient_list=recipient_list, attachment_paths=full_path)
                
                # Redirection vers une page de confirmation ou toute autre page souhaitée
                return redirect('index')
    
    context = {'error_message': error_message}
    return render(request, 'form.html', context)


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = formulaire_utilisateurr.objects.get(mail=email)
        except formulaire_utilisateurr.DoesNotExist:
            user = None

        if user is not None and check_password(password, user.password):
            # L'utilisateur existe et le mot de passe est correct, effectuez les actions appropriées
            # ...

            # Redirigez l'utilisateur vers la page souhaitée après la connexion réussie
            return redirect('connect')
        else:
            # Affichez un message d'erreur si l'authentification échoue
            error_message = "Adresse e-mail ou mot de passe incorrect"
    else:
        error_message = None

    return render(request, 'index.html', {'error_message': error_message})


def index(request):
    return render(request, 'index.html')
def register(request):
    return render(request, 'form.html')

def connect(request):
    return render(request, 'food_quotidien_personnel.html')

def rmail(request):
    return render(request, 'email.html')

def reset_password_done(request):
    return render(request, 'succes.html')

def reset_password_request(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = formulaire_utilisateurr.objects.get(mail=email)
        except formulaire_utilisateurr.DoesNotExist:
            return render(request, "email.html", {"error_messages": "Cet email est invalide."})

        if user is not None:
            token = default_token_generator.make_token(user)
            # Définir la durée de validité du lien de réinitialisation (par exemple, 1 heure)
            link_expiration_time = timezone.now() + timedelta(hours=2)

            # Enregistrez le lien de réinitialisation avec sa durée de validité
            reset_link = ResetLink(
                        user=user,
                        token=token,
                        expiration_time=link_expiration_time
                        )
            reset_link.save()

            current_site = get_current_site(request)
             # Générer l'URL de réinitialisation
            reset_url = reverse("password_reset_confirm", kwargs={
                "uidb64": urlsafe_base64_encode(force_bytes(user.pk)),  # Décodez l'uidb64
                "token": token,
            })
            
            # Afficher les valeurs pour vérification
            print("Reset URL:", reset_url)
            mail_subject = "Réinitialisation de mot de passe"
            html_content = render_to_string(
                "reset_password_email.html",
                {
                    "user": user,
                    "domaine": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),  # Utilisez uidb64 ici
                    "jeton": token,
                    #"protocol": 'http',
                    # "reset_url": reset_url_full,
                    "reset_url": reset_url, 
                },
            )
            
            
            text_content = strip_tags(html_content)
            email = EmailMultiAlternatives(
                subject=mail_subject,
                body=text_content,
                from_email="tamensorelle5@gmail.com",
                to=[email],
            )
            email.attach_alternative(html_content, "text/html")
            email.send(fail_silently=False)
        else:
            return render(request, "email.html", {"error_messages": "Cet email est invalide."})
    
        return redirect("reset_password_done")
    return render(request, "email.html")


# class CustomPasswordResetConfirmView(View):
#     template_name = "modifier_pwd.html"  # Le template contenant le formulaire de réinitialisation

#     # def get_uid_from_token(token):
#     #     uidb64 = token.split("-")[0]  # Extrayez la partie UID du token (avant le premier tiret)
#     #     uid = urlsafe_base64_decode(uidb64).decode()  # Décodage de l'UID
#     #     return uid

#     def get_user(self, uid):
#         User = get_user_model()
#         try:
#             user = User.objects.get(pk=uid)
#         except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#             user = None
#         return user

#     def get(self, request, uidb64, token, *args, **kwargs):
#         user = self.get_user(uidb64)
#         if user is not None and default_token_generator.check_token(user, token):
#             context = {
#                 "valid_reset_link": True,
#                 "uidb64": uid,
#                 "token": token,
#             }
#             return render(request, self.template_name, context)
#         else:
#             context = {
#                 "invalid_reset_link": True,
#             }
#             return render(request, self.template_name, context)
        
    # def get_reset_link_data(self, user_id):
    #     try:
    #         reset_link = ResetLink.objects.get(user_id=user_id)
    #         return {
    #             "token": reset_link.token,
    #             "expiration_time": reset_link.expiration_time,
    #         }
    #     except ResetLink.DoesNotExist:
    #         return None
        
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)

    #     user_id = urlsafe_base64_decode(self.kwargs["uid"])
    #     reset_link = self.get_reset_link_data(user_id)
        
    #     if reset_link and reset_link["token"] == self.kwargs["token"]:
    #         if reset_link["expiration_time"] >= timezone.now():
    #             context["valid_reset_link"] = True
    #         else:
    #             context["expired_reset_link"] = True
    #             # Si le lien a expiré, vous pouvez prendre des mesures ici, par exemple, afficher un message ou rediriger l'utilisateur vers une page appropriée
                
    #     return context
    
#     def post(self, request, uidb64, token, *args, **kwargs):
#         user = self.get_user(uidb64)
#         new_password = request.POST.get("new_password1")  # Récupérez la saisie du nouveau mot de passe
        
#         if user is not None and default_token_generator.check_token(user, token):
#             user.set_password(new_password)
#             user.save()
#             return redirect(reverse_lazy("reset_password_complete"))
#         else:
#             context = {
#                 "invalid_reset_link": True,
#             }
#             return render(request, self.template_name, context)

class CustomPasswordResetConfirmView(View):
    template_name = "modifier_pwd.html"  # Le template contenant le formulaire de réinitialisation

    def get_user(self, token):
        try:
            reset_link = ResetLink.objects.get(token=token)
            return reset_link.user
        except ResetLink.DoesNotExist:
            return None
        
    # def get_context_data(self, **kwargs):
    #     context = **kwargs.items

    #     reset_lin = ResetLink.objects.get(token=self.kwargs["token"])
    #     user_id = reset_lin.user_id
    #     reset_link = self.get_reset_link_data(user_id)
        
    #     if user_id is not None:
    #         if reset_link["expiration_time"] <= timezone.now():
    #             context["valid_reset_link"] = True
    #         else:
    #             context["expired_reset_link"] = True
    #             # Si le lien a expiré, vous pouvez prendre des mesures ici, par exemple, afficher un message ou rediriger l'utilisateur vers une page appropriée
    #             messages.error(self.request, "Le lien de réinitialisation a expiré.")
    #             # Redirigez l'utilisateur vers une page appropriée (par exemple, la page d'accueil)
    #             # return redirect(reverse_lazy("index"))
    #     return context

    def get(self, request, uidb64, token, *args, **kwargs):
        user = self.get_user(token)
        
        if user is not None and default_token_generator.check_token(user, token):
            reset_link = self.get_reset_link_data(token)
            context = {
                "valid_reset_link": True,
                "uidb64": uidb64,
                "token": token,
            }

            if reset_link["token"] is not None:
                if reset_link["expiration_time"] <= timezone.now():
                    context["expired_reset_link"] = True
                    messages.error(self.request, "Le lien de réinitialisation a expiré.")
                    return redirect(reverse_lazy("index"))
            
            return render(request, self.template_name, context)
        else:
            return redirect(reverse_lazy("index"))

               
            
    def get_reset_link_data(self, token):
        try:
            reset_link = ResetLink.objects.get(token=token)
            return {
                "token": reset_link.token,
                "expiration_time": reset_link.expiration_time,
            }
        except ResetLink.DoesNotExist:
            return None

    def post(self, request, uidb64, token, *args, **kwargs):
        user = self.get_user(token)
        new_password = request.POST.get("new_password1")
        new_password2 = request.POST.get("new_password2")
        error_messages = []

        if user is not None and default_token_generator.check_token(user, token):
            # Vérification du mot de passe
            if new_password != new_password2:
                error_messages.append("Les mots de passe ne correspondent pas")
            if len(new_password) < 8:
                error_messages.append("Le mot de passe doit contenir au moins 8 caractères")
            if not re.search(r'\d', new_password):
                error_messages.append("Le mot de passe doit contenir au moins un chiffre")
            if not re.search(r'[!@#$%^&*(),.?":{}|<>]', new_password):
                error_messages.append("Le mot de passe doit contenir au moins un caractère spécial $ & % £")

            if error_messages:
                error_message = ". ".join(error_messages)
                messages.error(request, error_message)  # Ajouter le message d'erreur
                redirect_url = reverse("password_reset_confirm", kwargs={"token": token, "uidb64": uidb64,})
                return redirect(redirect_url)
            else:
                user.set_password(new_password)
                user.save()
                messages.success(request, "Le mot de passe a été réinitialisé avec succès.")
                return redirect(reverse_lazy("reset_password_complete"))
        else:
            context = {"invalid_reset_link": True}
            return render(request, self.template_name, context)

    # def post(self, request, uidb64, token, *args, **kwargs):
    #     user = self.get_user(token)
    #     new_password = request.POST.get("new_password1")  # Récupérez la saisie du nouveau mot de passe
    #     new_password2 = request.POST.get("new_password2")  # Récupérez la saisie du nouveau mot de passe
        
    #     if user is not None and default_token_generator.check_token(user, token):
    #         if new_password != new_password2:
    #             error_message = 'Les mots de passe ne correspondent pas'
    #         else:
    #             # Vérifications du mot de passe
    #             if len(new_password) < 8:
    #                 error_message = 'Le mot de passe doit contenir au moins 8 caractères'
    #             elif not re.search(r'\d', new_password):
    #                 error_message = 'Le mot de passe doit contenir au moins un chiffre'
    #             elif not re.search(r'[!@#$%^&*(),.?":{}|<>]', new_password):
    #                 error_message = 'Le mot de passe doit contenir au moins un caractère spécial'
    #             else:
    #                 # Hachage du mot de passe
    #                 hashed_password = make_password(new_password)

    #                 user.set_password(hashed_password)
    #                 user.save()
    #                 return redirect(reverse_lazy("reset_password_complete"))
             
    #         context = {'error_message': error_message}
    #         return render(request, self.template_name, context)
    #     else:
    #         context = {
    #             "invalid_reset_link": True,
    #         }
    #         return render(request, self.template_name, context)

    # def post(self, request, uidb64, token, *args, **kwargs):
    #     user = self.get_user(token)
    #     new_password = request.POST.get("new_password1")
    #     new_password2 = request.POST.get("new_password2")
        
    #     if user is not None and default_token_generator.check_token(user, token):
    #         # Votre vérification de mots de passe ici
            
    #         if new_password != new_password2 or error_message:
    #             error_message = "es mots de passe ne correspondent pas"
                
    #             # Construire l'URL de redirection avec le message d'erreur
    #             redirect_url = reverse("password_reset_confirm", kwargs={"uidb64": uidb64, "token": token})
    #             redirect_url += f"?error_message={error_message}"
                
    #             return redirect(redirect_url)
    #         else:
    #             # Réinitialisation réussie
    #             if len(new_password) < 8:
    #                 error_message = 'Le mot de passe doit contenir au moins 8 caractères'
    #                 redirect_url = reverse("password_reset_confirm", kwargs={"uidb64": uidb64, "token": token})
    #                 redirect_url += f"?error_message={error_message}"
                    
    #                 return redirect(redirect_url)
    #             elif not re.search(r'\d', new_password):
    #                 error_message = 'Le mot de passe doit contenir au moins un chiffre'
    #                 redirect_url = reverse("password_reset_confirm", kwargs={"uidb64": uidb64, "token": token})
    #                 redirect_url += f"?error_message={error_message}"
                    
    #                 return redirect(redirect_url)
    #             elif not re.search(r'[!@#$%^&*(),.?":{}|<>]', new_password):
    #                 error_message = 'Le mot de passe doit contenir au moins un caractère spécial'
    #                 redirect_url = reverse("password_reset_confirm", kwargs={"uidb64": uidb64, "token": token})
    #                 redirect_url += f"?error_message={error_message}"
                    
    #                 return redirect(redirect_url)
    #             else:
    #                 hashed_password = make_password(new_password)
    #                 user.set_password(hashed_password)
    #                 user.save()
    #                 return redirect(reverse_lazy("reset_password_complete"))
    #     else:
    #         context = {"invalid_reset_link": True}
    #         return render(request, self.template_name, context)

def reset_password_complete(request):
    return render(request, 'reset_password_complete.html')

