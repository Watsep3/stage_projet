from nicegui import ui
from core.i18n import i18n, _
from core.theme import theme_manager
from utils.validators import MindCareValidators
from utils.translation_helpers import MultilingualForm, with_language_support
from typing import Optional

class ContactPage:
    """Page de contact avec système de thème centralisé et traductions complètes"""
    
    def __init__(self):
        self.contact_info = {
            "email": "contact@mindcare.ma",
            "phone": "+212 5 22 XX XX XX",
            "address": "123 Rue de la Santé, Casablanca",
            "hours": _('contact.info.hours_value')  # "Lun-Ven: 9h-18h"
        }
        
        self.emergency_contacts = [
            {
                "name": "SOS Amitié", 
                "phone": "09 72 39 40 50", 
                "description": _('contact.emergency.sos_description')
            },
            {
                "name": "Suicide Écoute", 
                "phone": "01 45 39 40 00", 
                "description": _('contact.emergency.suicide_description')
            },
            {
                "name": _('contact.emergency.emergency_title'), 
                "phone": "112", 
                "description": _('contact.emergency.medical_description')
            }
        ]
        
        self.social_links = [
            {"name": "Facebook", "url": "#", "icon": "facebook"},
            {"name": "Twitter", "url": "#", "icon": "twitter"},
            {"name": "LinkedIn", "url": "#", "icon": "linkedin"},
            {"name": "Instagram", "url": "#", "icon": "instagram"}
        ]
        
        # Initialiser le formulaire multilingue
        self.form = MultilingualForm()
    
    @with_language_support
    def render(self):
        """Rendre la page de contact complète"""
        # Header
        self.render_header()
        
        # Contenu principal
        self.render_main_content()
        
        # Section d'aide
        self.render_help_section()
    
    def render_header(self):
        """Rendre l'en-tête avec gradient de thème et traductions"""
        with ui.element('div').classes('w-full py-16 px-4 gradient-hero'):
            with ui.column().classes('page-container text-center text-inverse'):
                ui.label(_('contact.title')).classes('text-5xl font-bold mb-4')
                ui.label(_('contact.subtitle')).classes('text-xl opacity-90 max-w-2xl mx-auto')
    
    def render_main_content(self):
        """Rendre le contenu principal avec formulaire et infos"""
        with ui.element('div').classes('w-full py-16 px-4 bg-card'):
            with ui.element('div').classes('page-container'):
                
                # Layout responsive : colonne sur mobile, row sur desktop
                direction_class = 'flex-col lg:flex-row' if not i18n.is_rtl() else 'flex-col lg:flex-row-reverse'
                with ui.element('div').classes(f'flex {direction_class} gap-12 items-start'):
                    # Formulaire de contact
                    with ui.column().classes('flex-1'):
                        self.render_contact_form()
                    
                    # Informations de contact
                    with ui.column().classes('flex-1'):
                        self.render_contact_info()
    
    def render_contact_form(self):
        """Rendre le formulaire de contact avec classes de thème et traductions"""
        ui.label(_('contact.form.title')).classes('text-3xl font-bold mb-6 text-main')
        
        with ui.card().classes(theme_manager.get_card_classes(elevated=True) + ' p-8'):
            with ui.column().classes('gap-4'):
                # Champs du formulaire avec traductions
                name_input = ui.input(_('contact.form.name')).classes('w-full').props('outlined')
                email_input = ui.input(_('contact.form.email')).classes('w-full').props('outlined')
                subject_input = ui.input(_('contact.form.subject')).classes('w-full').props('outlined')
                
                # Type de demande avec options traduites
                with ui.column().classes('w-full'):
                    ui.label(_('contact.form.type')).classes('text-sm font-medium text-main mb-2')
                    
                    # Options traduites
                    request_types = {
                        'general': _('contact.form.types.general'),
                        'support': _('contact.form.types.support'),
                        'feedback': _('contact.form.types.feedback'),
                        'partnership': _('contact.form.types.partnership'),
                        'urgent': _('contact.form.types.urgent')
                    }
                    
                    request_type = ui.select(
                        options=request_types,
                        value='general'
                    ).classes('w-full').props('outlined')
                
                # Message
                message_input = ui.textarea(_('contact.form.message')).classes('w-full').props('outlined rows=5')
                
                # Checkbox confidentialité avec traduction
                privacy_checkbox = ui.checkbox(_('contact.form.privacy')).classes('mb-4')
                
                # Bouton d'envoi avec traduction
                ui.button(
                    _('contact.form.send'),
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
        
        # Note de confidentialité avec traduction
        self.render_privacy_note()
    
    def render_privacy_note(self):
        """Rendre la note de confidentialité"""
        with ui.card().classes('p-4 mt-6 bg-info-light border-l-4 border-info'):
            with ui.row().classes('items-start gap-3'):
                ui.icon('info').classes('text-info mt-1')
                with ui.column():
                    ui.label(_('contact.privacy.title')).classes('font-semibold text-info')
                    ui.label(_('contact.privacy.description')).classes('text-info text-sm')
    
    def render_contact_info(self):
        """Rendre les informations de contact avec classes de thème et traductions"""
        ui.label(_('contact.info.title')).classes('text-3xl font-bold mb-6 text-main')
        
        # Informations principales
        with ui.card().classes(theme_manager.get_card_classes(elevated=True) + ' p-6 mb-6'):
            with ui.column().classes('gap-4'):
                # Email
                with ui.row().classes('items-center gap-3'):
                    ui.icon('email').classes('text-2xl text-primary')
                    with ui.column().classes('gap-1'):
                        ui.label(_('contact.info.email')).classes('font-semibold text-main')
                        ui.link(self.contact_info["email"], f'mailto:{self.contact_info["email"]}').classes('text-muted hover:text-primary')
                
                ui.separator()
                
                # Téléphone
                with ui.row().classes('items-center gap-3'):
                    ui.icon('phone').classes('text-2xl text-primary')
                    with ui.column().classes('gap-1'):
                        ui.label(_('contact.info.phone')).classes('font-semibold text-main')
                        ui.link(self.contact_info["phone"], f'tel:{self.contact_info["phone"].replace(" ", "")}').classes('text-muted hover:text-primary')
                
                ui.separator()
                
                # Adresse
                with ui.row().classes('items-start gap-3'):
                    ui.icon('location_on').classes('text-2xl text-primary')
                    with ui.column().classes('gap-1'):
                        ui.label(_('contact.info.address')).classes('font-semibold text-main')
                        ui.label(self.contact_info["address"]).classes('text-muted')
                
                ui.separator()
                
                # Horaires
                with ui.row().classes('items-center gap-3'):
                    ui.icon('schedule').classes('text-2xl text-primary')
                    with ui.column().classes('gap-1'):
                        ui.label(_('contact.info.hours')).classes('font-semibold text-main')
                        ui.label(self.contact_info["hours"]).classes('text-muted')
        
        # Réseaux sociaux
        self.render_social_media()
    
    def render_social_media(self):
        """Rendre la section réseaux sociaux"""
        with ui.card().classes(theme_manager.get_card_classes(elevated=True) + ' p-6'):
            ui.label(_('footer.follow_us')).classes('text-lg font-semibold mb-4 text-main')
            
            with ui.row().classes('gap-3 flex-wrap'):
                for social in self.social_links:
                    ui.button(
                        social["name"],
                        icon=social.get("icon", "link"),
                        on_click=lambda url=social["url"], name=social["name"]: self.handle_social_click(url, name)
                    ).classes(theme_manager.get_button_classes('outline', 'sm'))
    
    def handle_social_click(self, url: str, name: str):
        """Gérer le clic sur un réseau social"""
        if url == "#":
            ui.notify(_('contact.social.coming_soon', platform=name), type='info')
        else:
            ui.navigate.to(url)
    
    def render_help_section(self):
        """Rendre la section d'aide d'urgence avec classes de thème et traductions"""
        with ui.element('div').classes('w-full py-16 px-4 bg-error-light'):
            with ui.column().classes('page-container text-center'):
                ui.label(_('contact.emergency.title')).classes('text-3xl font-bold mb-6 text-error')
                ui.label(_('contact.emergency.subtitle')).classes('text-lg text-error mb-8')
                
                # Contacts d'urgence
                self.render_emergency_contacts()
                
                # Message important
                self.render_emergency_warning()
    
    def render_emergency_contacts(self):
        """Rendre les contacts d'urgence"""
        with ui.element('div').classes('grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto'):
            for emergency in self.emergency_contacts:
                with ui.card().classes(theme_manager.get_card_classes(hover=True) + ' p-6 text-center bg-card'):
                    # Icône selon le type
                    icon = 'local_hospital' if emergency["name"] == _('contact.emergency.emergency_title') else 'phone'
                    ui.icon(icon).classes('text-4xl text-error mb-4')
                    
                    ui.label(emergency["name"]).classes('text-xl font-bold mb-2 text-main')
                    ui.link(
                        emergency["phone"], 
                        f'tel:{emergency["phone"].replace(" ", "")}'
                    ).classes('text-2xl font-bold text-error hover:text-error block mb-2')
                    ui.label(emergency["description"]).classes('text-muted')
    
    def render_emergency_warning(self):
        """Rendre l'avertissement d'urgence"""
        with ui.card().classes('p-6 mt-8 bg-error-light border-l-4 border-error max-w-2xl mx-auto'):
            with ui.row().classes('items-start gap-3'):
                ui.icon('warning').classes('text-error text-2xl mt-1')
                with ui.column():
                    ui.label(_('contact.emergency.warning_title')).classes('font-bold text-error text-lg')
                    ui.label(_('contact.emergency.warning')).classes('text-error')
    
    def send_contact_form(self, name: str, email: str, subject: str, message: str, request_type: str, privacy_accepted: bool):
        """Envoyer le formulaire de contact avec validation multilingue"""
        
        # Nettoyer les erreurs précédentes
        self.form.clear_errors()
        
        # Validation avec messages traduits
        is_valid = True
        
        if not self.form.validate_required(name, 'name'):
            is_valid = False
        
        if not self.form.validate_required(email, 'email'):
            is_valid = False
        elif not self.form.validate_email(email):
            is_valid = False
        
        if not self.form.validate_required(subject, 'subject'):
            is_valid = False
        elif not self.form.validate_length(subject, 'subject', min_len=5, max_len=200):
            is_valid = False
        
        if not self.form.validate_required(message, 'message'):
            is_valid = False
        elif not self.form.validate_length(message, 'message', min_len=20, max_len=2000):
            is_valid = False
        
        # Validation de la confidentialité
        if not privacy_accepted:
            self.form.errors['privacy'] = _('contact.form.privacy_required')
            is_valid = False
        
        # Afficher les erreurs s'il y en a
        if not is_valid:
            error_messages = []
            for field, error in self.form.get_errors().items():
                error_messages.append(error)
            
            ui.notify(
                '\n'.join(error_messages[:3]),  # Limiter à 3 erreurs
                type='negative',
                position='top',
                timeout=5000
            )
            return
        
        try:
            # Simulation de l'envoi (ici vous pouvez ajouter l'enregistrement en base)
            self.save_contact_message(name, email, subject, message, request_type)
            
            # Notification de succès traduite
            ui.notify(
                _('contact.form.success'), 
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
            print(f"   Langue: {i18n.get_language()}")
            
        except Exception as e:
            ui.notify(_('contact.form.error'), type='negative', position='top')
            print(f"❌ Erreur lors de l'envoi: {e}")
    
    def save_contact_message(self, name: str, email: str, subject: str, message: str, request_type: str):
        """Sauvegarder le message de contact (à implémenter avec votre base de données)"""
        # Ici vous pouvez ajouter la logique pour sauvegarder en base de données
        # En incluant la langue actuelle pour les réponses
        contact_data = {
            'name': name,
            'email': email,
            'subject': subject,
            'message': message,
            'type': request_type,
            'language': i18n.get_language(),
            'created_at': datetime.now().isoformat()
        }
        
        # Exemple de sauvegarde (remplacer par votre logique)
        print(f"💾 Sauvegarde du contact: {contact_data}")
    
    def render_faq_section(self):
        """Rendre une section FAQ avec classes de thème et traductions"""
        # FAQ traduite
        faq_items = [
            {
                "question_key": "contact.faq.response_time.question",
                "answer_key": "contact.faq.response_time.answer"
            },
            {
                "question_key": "contact.faq.data_security.question", 
                "answer_key": "contact.faq.data_security.answer"
            },
            {
                "question_key": "contact.faq.appointment.question",
                "answer_key": "contact.faq.appointment.answer"
            }
        ]
        
        with ui.element('div').classes('w-full py-16 px-4 bg-surface'):
            with ui.column().classes('page-container'):
                ui.label(_('contact.faq.title')).classes('text-3xl font-bold text-center mb-12 text-main')
                
                with ui.column().classes('max-w-3xl mx-auto gap-4'):
                    for faq in faq_items:
                        with ui.card().classes(theme_manager.get_card_classes() + ' p-6'):
                            ui.label(_(faq["question_key"])).classes('text-lg font-semibold mb-3 text-main')
                            ui.label(_(faq["answer_key"])).classes('text-muted leading-relaxed')
    
    def render_language_specific_content(self):
        """Rendre du contenu spécifique à la langue"""
        current_lang = i18n.get_language()
        
        # Contenu spécifique selon la langue
        if current_lang == "ar":
            # Contenu spécial pour l'arabe (numéros locaux, etc.)
            pass
        elif current_lang == "fr":
            # Contenu français
            pass
        elif current_lang == "en":
            # Contenu anglais
            pass