from nicegui import ui
from core.i18n import i18n, _
from core.theme import theme_manager
from utils.validators import MindCareValidators
from typing import Optional

class ContactPage:
    """Page de contact avec système de thème centralisé"""
    
    def __init__(self):
        self.contact_info = {
            "email": "contact@mindcare.ma",
            "phone": "+212 5 22 XX XX XX",
            "address": "123 Rue de la Santé, Casablanca",
            "hours": "Lun-Ven: 9h-18h"
        }
        
        self.emergency_contacts = [
            {"name": "SOS Amitié", "phone": "09 72 39 40 50", "description": "Écoute 24h/24"},
            {"name": "Suicide Écoute", "phone": "01 45 39 40 00", "description": "Prévention suicide"},
            {"name": "Urgences", "phone": "112", "description": "Urgences médicales"}
        ]
        
        self.social_links = [
            {"name": "Facebook", "url": "#", "icon": "facebook"},
            {"name": "Twitter", "url": "#", "icon": "twitter"},
            {"name": "LinkedIn", "url": "#", "icon": "linkedin"},
            {"name": "Instagram", "url": "#", "icon": "instagram"}
        ]
    
    def render(self):
        """Rendre la page de contact complète"""
        # Header
        self.render_header()
        
        # Contenu principal
        self.render_main_content()
        
        # Section d'aide
        self.render_help_section()
    
    def render_header(self):
        """Rendre l'en-tête avec gradient de thème"""
        with ui.element('div').classes('w-full py-16 px-4 gradient-hero'):
            with ui.column().classes('page-container text-center text-inverse'):
                ui.label('Contactez-nous').classes('text-5xl font-bold mb-4')
                ui.label('Nous sommes là pour vous accompagner dans votre parcours de bien-être').classes('text-xl opacity-90 max-w-2xl mx-auto')
    
    def render_main_content(self):
        """Rendre le contenu principal avec formulaire et infos"""
        with ui.element('div').classes('w-full py-16 px-4 bg-card'):
            with ui.element('div').classes('page-container'):
                with ui.row().classes('gap-12 items-start'):
                    # Formulaire de contact
                    with ui.column().classes('flex-1'):
                        self.render_contact_form()
                    
                    # Informations de contact
                    with ui.column().classes('flex-1'):
                        self.render_contact_info()
    
    def render_contact_form(self):
        """Rendre le formulaire de contact avec classes de thème"""
        ui.label('Envoyez-nous un message').classes('text-3xl font-bold mb-6 text-main')
        
        with ui.card().classes(theme_manager.get_card_classes(elevated=True) + ' p-8'):
            with ui.column().classes('gap-4'):
                # Champs du formulaire
                name_input = ui.input('Nom complet *').classes('w-full').props('outlined')
                email_input = ui.input('Adresse email *').classes('w-full').props('outlined')
                subject_input = ui.input('Sujet du message *').classes('w-full').props('outlined')
                
                # Type de demande
                with ui.column().classes('w-full'):
                    ui.label('Type de demande').classes('text-sm font-medium text-main mb-2')
                    request_type = ui.select(
                        options={
                            'general': 'Question générale',
                            'support': 'Demande de support',
                            'feedback': 'Commentaire/Suggestion',
                            'partnership': 'Partenariat',
                            'urgent': 'Urgence'
                        },
                        value='general'
                    ).classes('w-full').props('outlined')
                
                # Message
                message_input = ui.textarea('Votre message *').classes('w-full').props('outlined rows=5')
                
                # Checkbox confidentialité
                privacy_checkbox = ui.checkbox('J\'accepte que mes données soient utilisées pour répondre à ma demande').classes('mb-4')
                
                # Bouton d'envoi
                ui.button(
                    'Envoyer le message',
                    on_click=lambda: self.send_contact_form(
                        name_input.value or '',
                        email_input.value or '',
                        subject_input.value or '',
                        message_input.value or '',
                        request_type.value or 'general',
                        privacy_checkbox.value
                    ),
                    icon='send'
                ).classes(theme_manager.get_button_classes('primary', 'lg') + ' w-full')
        
        # Note de confidentialité
        with ui.card().classes('p-4 mt-6 bg-info-light border-l-4 border-info'):
            with ui.row().classes('items-start gap-3'):
                ui.icon('info').classes('text-info mt-1')
                with ui.column():
                    ui.label('Protection des données').classes('font-semibold text-info')
                    ui.label('Vos informations personnelles sont protégées et utilisées uniquement pour répondre à votre demande. Nous ne les partageons jamais avec des tiers.').classes('text-info text-sm')
    
    def render_contact_info(self):
        """Rendre les informations de contact avec classes de thème"""
        ui.label('Nos coordonnées').classes('text-3xl font-bold mb-6 text-main')
        
        # Informations principales
        with ui.card().classes(theme_manager.get_card_classes(elevated=True) + ' p-6 mb-6'):
            with ui.column().classes('gap-4'):
                # Email
                with ui.row().classes('items-center gap-3'):
                    ui.icon('email').classes('text-2xl text-primary')
                    with ui.column().classes('gap-1'):
                        ui.label('Email').classes('font-semibold text-main')
                        ui.link(self.contact_info["email"], f'mailto:{self.contact_info["email"]}').classes('text-muted hover:text-primary')
                
                ui.separator()
                
                # Téléphone
                with ui.row().classes('items-center gap-3'):
                    ui.icon('phone').classes('text-2xl text-primary')
                    with ui.column().classes('gap-1'):
                        ui.label('Téléphone').classes('font-semibold text-main')
                        ui.link(self.contact_info["phone"], f'tel:{self.contact_info["phone"].replace(" ", "")}').classes('text-muted hover:text-primary')
                
                ui.separator()
                
                # Adresse
                with ui.row().classes('items-start gap-3'):
                    ui.icon('location_on').classes('text-2xl text-primary')
                    with ui.column().classes('gap-1'):
                        ui.label('Adresse').classes('font-semibold text-main')
                        ui.label(self.contact_info["address"]).classes('text-muted')
                
                ui.separator()
                
                # Horaires
                with ui.row().classes('items-center gap-3'):
                    ui.icon('schedule').classes('text-2xl text-primary')
                    with ui.column().classes('gap-1'):
                        ui.label('Horaires').classes('font-semibold text-main')
                        ui.label(self.contact_info["hours"]).classes('text-muted')
        
        # Réseaux sociaux
        with ui.card().classes(theme_manager.get_card_classes(elevated=True) + ' p-6'):
            ui.label('Suivez-nous').classes('text-lg font-semibold mb-4 text-main')
            
            with ui.row().classes('gap-3 flex-wrap'):
                for social in self.social_links:
                    ui.button(
                        social["name"],
                        icon=social.get("icon", "link"),
                        on_click=lambda url=social["url"]: ui.navigate.to(url) if url != "#" else ui.notify("Lien bientôt disponible")
                    ).classes(theme_manager.get_button_classes('outline', 'sm'))
    
    def render_help_section(self):
        """Rendre la section d'aide d'urgence avec classes de thème"""
        with ui.element('div').classes('w-full py-16 px-4 bg-error-light'):
            with ui.column().classes('page-container text-center'):
                ui.label('Besoin d\'aide immédiate ?').classes('text-3xl font-bold mb-6 text-error')
                ui.label('Si vous êtes en détresse ou en situation d\'urgence, contactez immédiatement ces numéros :').classes('text-lg text-error mb-8')
                
                # Contacts d'urgence
                with ui.element('div').classes('grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto'):
                    for emergency in self.emergency_contacts:
                        with ui.card().classes(theme_manager.get_card_classes(hover=True) + ' p-6 text-center bg-card'):
                            ui.icon('phone' if emergency["name"] != "Urgences" else 'local_hospital').classes('text-4xl text-error mb-4')
                            ui.label(emergency["name"]).classes('text-xl font-bold mb-2 text-main')
                            ui.link(
                                emergency["phone"], 
                                f'tel:{emergency["phone"].replace(" ", "")}'
                            ).classes('text-2xl font-bold text-error hover:text-error block mb-2')
                            ui.label(emergency["description"]).classes('text-muted')
                
                # Message important
                with ui.card().classes('p-6 mt-8 bg-error-light border-l-4 border-error max-w-2xl mx-auto'):
                    with ui.row().classes('items-start gap-3'):
                        ui.icon('warning').classes('text-error text-2xl mt-1')
                        with ui.column():
                            ui.label('Important').classes('font-bold text-error text-lg')
                            ui.label('En cas d\'urgence vitale ou de pensées suicidaires immédiates, appelez le 112 ou rendez-vous aux urgences de l\'hôpital le plus proche.').classes('text-error')
    
    def send_contact_form(self, name: str, email: str, subject: str, message: str, request_type: str, privacy_accepted: bool):
        """Envoyer le formulaire de contact avec validation"""
        
        # Validation des champs requis
        if not all([name.strip(), email.strip(), subject.strip(), message.strip()]):
            ui.notify('Veuillez remplir tous les champs obligatoires (*)', type='negative', position='top')
            return
        
        # Validation de la confidentialité
        if not privacy_accepted:
            ui.notify('Veuillez accepter l\'utilisation de vos données pour continuer', type='negative', position='top')
            return
        
        try:
            # Validation avec le validateur MindCare
            contact_data = {
                'name': name,
                'email': email,
                'subject': subject,
                'message': message
            }
            
            MindCareValidators.CONTACT_VALIDATOR.validate_and_raise(contact_data)
            
            # Simulation de l'envoi (ici vous pouvez ajouter l'enregistrement en base)
            self.save_contact_message(name, email, subject, message, request_type)
            
            # Notification de succès
            ui.notify(
                'Message envoyé avec succès ! Nous vous répondrons dans les plus brefs délais.', 
                type='positive', 
                position='top',
                timeout=5000
            )
            
            # Log pour le développement
            print(f"📧 Nouveau message de contact:")
            print(f"   Nom: {name}")
            print(f"   Email: {email}")
            print(f"   Type: {request_type}")
            print(f"   Sujet: {subject}")
            print(f"   Message: {message[:100]}...")
            
        except Exception as e:
            ui.notify(f'Erreur de validation: {str(e)}', type='negative', position='top')
    
    def save_contact_message(self, name: str, email: str, subject: str, message: str, request_type: str):
        """Sauvegarder le message de contact (à implémenter avec votre base de données)"""
        # Ici vous pouvez ajouter la logique pour sauvegarder en base de données
        pass
    
    def render_faq_section(self):
        """Rendre une section FAQ avec classes de thème"""
        faq_items = [
            {
                "question": "Combien de temps faut-il pour recevoir une réponse ?",
                "answer": "Nous nous efforçons de répondre à tous les messages dans les 24-48 heures ouvrables."
            },
            {
                "question": "Mes informations personnelles sont-elles sécurisées ?",
                "answer": "Oui, toutes vos données sont chiffrées et protégées selon les standards RGPD."
            },
            {
                "question": "Puis-je prendre rendez-vous directement ?",
                "answer": "Pour l'instant, contactez-nous via ce formulaire et nous vous orienterons vers les bonnes ressources."
            }
        ]
        
        with ui.element('div').classes('w-full py-16 px-4 bg-surface'):
            with ui.column().classes('page-container'):
                ui.label('Questions fréquentes').classes('text-3xl font-bold text-center mb-12 text-main')
                
                with ui.column().classes('max-w-3xl mx-auto gap-4'):
                    for faq in faq_items:
                        with ui.card().classes(theme_manager.get_card_classes() + ' p-6'):
                            ui.label(faq["question"]).classes('text-lg font-semibold mb-3 text-main')
                            ui.label(faq["answer"]).classes('text-muted leading-relaxed')