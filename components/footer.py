from nicegui import ui
from datetime import datetime
from core.theme import theme_manager

class Footer:
    """Composant Footer réutilisable avec système de thème centralisé"""
    
    def __init__(self, app_name: str = "MindCare", year: int = None):
        self.app_name = app_name
        self.year = year or datetime.now().year
        
        # Liens du footer
        self.footer_links = [
            {"label": "Confidentialité", "url": "/privacy"},
            {"label": "Conditions", "url": "/terms"},
            {"label": "Plan du site", "url": "/sitemap"},
            {"label": "Aide", "url": "/help"}
        ]
        
        # Réseaux sociaux
        self.social_links = [
            {"label": "Facebook", "url": "#", "icon": "facebook"},
            {"label": "Twitter", "url": "#", "icon": "twitter"}, 
            {"label": "LinkedIn", "url": "#", "icon": "linkedin"},
            {"label": "Instagram", "url": "#", "icon": "instagram"}
        ]
    
    def set_footer_links(self, links: list):
        """Définir les liens du footer"""
        self.footer_links = links
        return self
    
    def set_social_links(self, links: list):
        """Définir les liens des réseaux sociaux"""
        self.social_links = links
        return self
    
    def add_footer_link(self, label: str, url: str):
        """Ajouter un lien au footer"""
        self.footer_links.append({"label": label, "url": url})
        return self
    
    def render(self):
        """Rendre le footer complet avec le système de thème centralisé"""
        with ui.element('div').classes('w-full border-default border-t mt-auto footer bg-surface'):
            with ui.element('div').classes('page-container py-8'):
                
                # Section principale
                with ui.row().classes('justify-between items-start mb-6 flex-wrap gap-8'):
                    # Informations de l'app
                    self._render_app_info()
                    
                    # Liens rapides
                    self._render_quick_links()
                    
                    # Contact
                    self._render_contact_info()
                    
                    # Réseaux sociaux
                    self._render_social_links()
                
                ui.separator().classes('my-6')
                
                # Copyright
                self._render_copyright()
    
    def render_simple(self):
        """Rendre une version simplifiée du footer avec classes de thème"""
        with ui.element('div').classes('w-full border-default border-t mt-auto footer bg-surface'):
            with ui.element('div').classes('page-container py-6'):
                with ui.row().classes('justify-between items-center flex-wrap gap-4'):
                    ui.label(f'© {self.year} {self.app_name}. Tous droits réservés.').classes('text-muted')
                    with ui.row().classes('gap-4 flex-wrap'):
                        for link in self.footer_links[:2]:  # Seulement 2 premiers liens
                            ui.link(link["label"], link["url"]).classes('text-muted hover:text-primary transition-colors')
    
    def _render_app_info(self):
        """Rendre les informations de l'application avec classes de thème"""
        with ui.column().classes('max-w-xs'):
            ui.label(f'🌱 {self.app_name}').classes('text-xl font-bold mb-3 text-primary')
            ui.label('Votre partenaire pour une meilleure santé mentale. Ressources, conseils et support pour votre bien-être.').classes('text-sm text-muted leading-relaxed')
    
    def _render_quick_links(self):
        """Rendre les liens rapides avec classes de thème"""
        with ui.column().classes(''):
            ui.label('Liens rapides').classes('font-semibold text-main mb-3')
            with ui.column().classes('gap-2'):
                for link in self.footer_links:
                    ui.link(
                        link["label"], 
                        link["url"]
                    ).classes('text-sm text-muted hover:text-primary transition-colors')
    
    def _render_contact_info(self):
        """Rendre les informations de contact avec classes de thème"""
        with ui.column().classes(''):
            ui.label('Contact').classes('font-semibold text-main mb-3')
            with ui.column().classes('gap-2'):
                with ui.row().classes('items-center gap-2'):
                    ui.icon('email').classes('text-sm text-primary')
                    ui.label('contact@mindcare.ma').classes('text-sm text-muted')
                
                with ui.row().classes('items-center gap-2'):
                    ui.icon('phone').classes('text-sm text-primary')
                    ui.label('+212 5 22 XX XX XX').classes('text-sm text-muted')
                
                with ui.row().classes('items-center gap-2'):
                    ui.icon('location_on').classes('text-sm text-primary')
                    ui.label('Casablanca, Maroc').classes('text-sm text-muted')
    
    def _render_social_links(self):
        """Rendre les liens des réseaux sociaux avec classes de thème"""
        with ui.column().classes(''):
            ui.label('Suivez-nous').classes('font-semibold text-main mb-3')
            with ui.row().classes('gap-3 flex-wrap'):
                for social in self.social_links:
                    ui.button(
                        icon=social.get("icon", "link"),
                        on_click=lambda url=social["url"]: self._handle_social_click(url, social["label"])
                    ).classes(theme_manager.get_button_classes('primary', 'sm') + ' w-8 h-8 rounded-full').props('flat').tooltip(social["label"])
    
    def _handle_social_click(self, url: str, name: str):
        """Gérer le clic sur un réseau social"""
        if url == "#":
            ui.notify(f'Lien {name} bientôt disponible', type='info')
        else:
            ui.navigate.to(url)
    
    def _render_copyright(self):
        """Rendre la section copyright avec classes de thème"""
        with ui.row().classes('justify-between items-center flex-wrap gap-4'):
            ui.label(f'© {self.year} {self.app_name}. Tous droits réservés.').classes('text-sm text-muted')
            
            with ui.row().classes('gap-4 flex-wrap'):
                ui.label('Développé avec 💚 pour votre bien-être').classes('text-sm text-muted')
    
    def render_minimal(self):
        """Rendre une version minimale du footer avec classes de thème"""
        with ui.element('div').classes('w-full border-default border-t mt-auto footer bg-surface'):
            with ui.element('div').classes('page-container py-4'):
                with ui.row().classes('justify-center items-center'):
                    ui.label(f'© {self.year} {self.app_name}. Tous droits réservés.').classes('text-sm text-muted text-center')