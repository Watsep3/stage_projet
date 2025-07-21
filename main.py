from nicegui import ui, app
from pathlib import Path

# Configuration
from config.settings import settings, create_directories
from core.theme import theme_manager, ThemePreference, Theme
from core.i18n import i18n, _

# Pages
from pages.home import HomePage
from pages.articles import ArticlesPage
from pages.reports import ReportsPage
from pages.about import AboutPage
from pages.contact import ContactPage 
from pages.chatbot import ChatbotPage

# Composants
from components.navbar import Navbar
from components.footer import Footer

class MindCareApp:
    """Application principale MindCare avec détection de thème système"""
    
    def __init__(self):
        # Créer les dossiers nécessaires
        create_directories()
        
        # Variables d'état
        self.current_theme = "light"
        
        # Initialiser et appliquer le thème (SANS JavaScript pendant l'init)
        theme_manager.apply_theme()
        
        # Récupérer l'état du thème après initialisation
        self.current_theme = theme_manager.current_theme.value
        
        # Initialiser la navbar avec callbacks
        self.navbar = Navbar("MindCare", self.current_theme)
        self.navbar.set_theme_toggle_callback(self.toggle_theme)
        self.navbar.set_mobile_menu_callback(self.show_mobile_menu)

        # Initialiser la footer avec callbacks
        self.footer = Footer("MindCare", self.current_theme)
        
        # Configurer les routes
        self.setup_routes()
        
        # Configurer les routes API pour la détection système
        self.setup_theme_api_routes()
    
    def setup_routes(self):
        """Configuration des routes principales"""
        
        @ui.page('/')
        def index():
            self.render_page(HomePage())
        
        @ui.page('/articles')
        def articles():
            self.render_page(ArticlesPage())
        
        @ui.page('/reports')
        def reports():
            self.render_page(ReportsPage())
        
        @ui.page('/about')
        def about():
            self.render_page(AboutPage())
        
        @ui.page('/contact')
        def contact():
            self.render_page(ContactPage())

        @ui.page('/chatbot') 
        def chatbot():
            self.render_page(ChatbotPage())
    
    def setup_theme_api_routes(self):
        """Configuration des routes API pour la gestion du thème"""
        
        @app.post('/api/theme/system-detected')
        async def system_theme_detected(request):
            """Recevoir la notification de détection du thème système"""
            try:
                data = await request.json()
                system_theme = Theme.DARK if data.get('theme') == 'dark' else Theme.LIGHT
                
                # Mettre à jour le thème système dans le manager
                old_theme = theme_manager.system_theme
                theme_manager.system_theme = system_theme
                
                # Sauvegarder dans le storage
                theme_manager.save_theme_preferences()
                
                # Si l'utilisateur suit le système et que le thème a changé
                if (theme_manager.theme_preference == ThemePreference.AUTO and 
                    old_theme != system_theme):
                    theme_manager.apply_theme_preference()
                
                print(f"🎨 Thème système détecté: {system_theme.value}")
                return {"status": "success", "system_theme": system_theme.value}
                
            except Exception as e:
                print(f"Erreur détection thème système: {e}")
                return {"status": "error", "message": str(e)}
        
        @app.post('/api/theme/system-changed')
        async def system_theme_changed(request):
            """Recevoir la notification de changement du thème système"""
            try:
                data = await request.json()
                new_system_theme = Theme.DARK if data.get('theme') == 'dark' else Theme.LIGHT
                
                # Mettre à jour via le manager (il gère automatiquement l'application)
                theme_manager.set_system_theme(new_system_theme)
                
                print(f"🔄 Changement thème système: {new_system_theme.value}")
                return {"status": "success", "new_system_theme": new_system_theme.value}
                
            except Exception as e:
                print(f"Erreur changement thème système: {e}")
                return {"status": "error", "message": str(e)}
    
    def render_page(self, page_instance):
        """Rendre une page avec layout"""

        # Créer le wrapper principal avec classe de thème
        with ui.element('div').classes(f'content-wrapper {self.current_theme}-theme'):
            # Navbar - utilise le composant séparé
            self.navbar.render()
            
            # Contenu principal
            with ui.element('div').classes('content-area'):
                page_instance.render()
            
            # Footer
            self.footer.render()
    
    def toggle_theme(self):
        """Basculer le thème avec le nouveau système (auto → light → dark → auto)"""
        # Utiliser le ThemeManager pour changer le thème
        theme_manager.toggle_theme()
        
        # Mettre à jour l'état local
        self.current_theme = theme_manager.current_theme.value
        
        # Mettre à jour le thème dans la navbar
        self.navbar.update_theme(self.current_theme)
        self.navbar.update_theme_preference(theme_manager.theme_preference.value)
        
        # La notification est déjà gérée par le ThemeManager
    
    def get_theme_status_display(self) -> str:
        """Obtenir un affichage du statut du thème pour le debug"""
        status = theme_manager.get_theme_status()
        return (f"Actuel: {status['current_theme']} | "
                f"Préférence: {status['theme_preference']} | "
                f"Système: {status['system_theme']} | "
                f"Auto: {status['is_following_system']}")
    
    def show_mobile_menu(self):
        """Afficher le menu mobile - Callback de la navbar"""
        # Utilise le menu mobile par défaut de la navbar
        self.navbar.show_default_mobile_menu()
    
    def run(self):
        """Démarrer l'application"""
        print(f"🚀 Démarrage de {settings.app_name} v{settings.app_version}")
        print(f"📱 Serveur: http://localhost:{settings.port}")
        print(f"🎨 Thème: {self.get_theme_status_display()}")
        print(f"🌐 Langue: {i18n.current_language}")
        print("🌱 Couleur principale: Vert")
        print("=" * 50)
        
        # Lancer NiceGUI
        ui.run(
            port=settings.port,
            storage_secret=settings.secret_key,
            reload=settings.reload,
            show=True,
            title="MindCare - Santé Mentale"
        )

# Point d'entrée principal
if __name__ in {"__main__", "__mp_main__"}:
    mindcare_app = MindCareApp()
    mindcare_app.run()