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
    """Application principale MindCare avec détection de thème système et support i18n"""
    
    def __init__(self):
        # Créer les dossiers nécessaires
        create_directories()
        
        # Variables d'état
        self.current_theme = "light"
        
        # Initialiser le système i18n
        self.initialize_i18n()
        
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
        
        # Configurer les routes API pour la détection système et i18n
        self.setup_api_routes()
        
        # Ajouter le CSS pour le support RTL
        self.setup_rtl_support()
    
    def initialize_i18n(self):
        """Initialiser le système d'internationalisation"""
        try:
            # Charger la langue de l'utilisateur depuis le storage
            i18n.load_language()
            
            # Afficher les statistiques de traduction pour le debug
            if settings.debug:
                from core.i18n import print_translation_stats
                print_translation_stats()
                
            print(f"🌐 Système i18n initialisé - Langue: {i18n.get_language()}")
            
        except Exception as e:
            print(f"⚠️ Erreur lors de l'initialisation i18n: {e}")
            # Utiliser la langue par défaut en cas d'erreur
            i18n.current_language = settings.default_language
    
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
        
        # Route pour le changement de langue
        @ui.page('/lang/{language}')
        def change_language(language: str):
            if i18n.set_language(language):
                # Rediriger vers la page d'accueil après changement
                ui.navigate.to('/')
            else:
                # Langue invalide, retourner à l'accueil
                ui.navigate.to('/')
    
    def setup_api_routes(self):
        """Configuration des routes API pour la gestion du thème et de la langue"""
        
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
        
        @app.post('/api/language/change')
        async def change_language_api(request):
            """API pour changer la langue"""
            try:
                data = await request.json()
                language = data.get('language')
                
                if i18n.set_language(language):
                    return {
                        "status": "success", 
                        "language": language,
                        "language_name": i18n.get_language_name(language)
                    }
                else:
                    return {"status": "error", "message": "Langue non supportée"}
                    
            except Exception as e:
                print(f"Erreur changement langue: {e}")
                return {"status": "error", "message": str(e)}
        
        @app.get('/api/language/current')
        async def get_current_language():
            """Obtenir la langue actuelle"""
            return {
                "language": i18n.get_language(),
                "language_name": i18n.get_language_name(i18n.get_language()),
                "supported_languages": i18n.get_supported_languages(),
                "locale_info": i18n.get_locale_info()
            }
    
    def setup_rtl_support(self):
        """Ajouter le support RTL pour les langues arabes"""
        ui.add_head_html("""
        <style>
        /* === SUPPORT RTL === */
        
        /* Direction du texte selon la langue */
        html[dir="rtl"] {
            direction: rtl;
        }
        
        html[dir="ltr"] {
            direction: ltr;
        }
        
        /* RTL pour les langues arabes */
        .rtl {
            direction: rtl;
            text-align: right;
        }
        
        .ltr {
            direction: ltr;
            text-align: left;
        }
        
        /* Ajustements spécifiques pour RTL */
        html[dir="rtl"] .navbar-container {
            flex-direction: row-reverse;
        }
        
        html[dir="rtl"] .desktop-nav {
            flex-direction: row-reverse;
        }
        
        html[dir="rtl"] .actions-container {
            flex-direction: row-reverse;
        }
        
        /* Ajustements pour les cartes en RTL */
        html[dir="rtl"] .card {
            text-align: right;
        }
        
        html[dir="rtl"] .card .q-card__section {
            text-align: right;
        }
        
        /* Ajustements pour les boutons en RTL */
        html[dir="rtl"] .q-btn {
            direction: rtl;
        }
        
        /* Ajustements pour les inputs en RTL */
        html[dir="rtl"] .q-field {
            direction: rtl;
        }
        
        html[dir="rtl"] .q-field__native,
        html[dir="rtl"] .q-field__input {
            text-align: right;
        }
        
        /* Ajustements pour les menus en RTL */
        html[dir="rtl"] .q-menu {
            direction: rtl;
        }
        
        html[dir="rtl"] .q-item {
            direction: rtl;
            text-align: right;
        }
        
        /* Typography pour l'arabe */
        [lang="ar"], .arabic-text {
            font-family: 'Amiri', 'Noto Sans Arabic', 'Arabic UI Text', Arial, sans-serif;
            line-height: 1.8;
        }
        
        /* Ajustements des espacements pour l'arabe */
        [lang="ar"] .text-sm {
            font-size: 0.9rem;
        }
        
        [lang="ar"] .text-lg {
            font-size: 1.2rem;
        }
        
        [lang="ar"] .text-xl {
            font-size: 1.4rem;
        }
        
        /* Classes utilitaires pour RTL */
        .rtl-flip {
            transform: scaleX(-1);
        }
        
        html[dir="rtl"] .rtl-flip {
            transform: scaleX(1);
        }
        
        /* Responsive pour RTL */
        @media (max-width: 768px) {
            html[dir="rtl"] .mobile-menu-btn {
                order: -1;
            }
            
            html[dir="rtl"] .logo-text {
                order: 1;
            }
        }
        </style>
        """)
        
        # Ajouter les polices pour l'arabe
        ui.add_head_html("""
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Noto+Sans+Arabic:wght@400;500;600;700&display=swap" rel="stylesheet">
        """)
    
    def render_page(self, page_instance):
        """Rendre une page avec layout et support RTL"""
        # Déterminer la direction du texte
        direction = i18n.get_language_direction()
        language = i18n.get_language()
        
        # Ajouter les attributs de langue et direction au HTML
        ui.run_javascript(f"""
            document.documentElement.setAttribute('lang', '{language}');
            document.documentElement.setAttribute('dir', '{direction}');
            document.body.className = document.body.className.replace(/\\b(rtl|ltr)\\b/g, '') + ' {direction}';
        """)

        # Créer le wrapper principal avec classe de thème et direction
        classes = f'content-wrapper {self.current_theme}-theme {direction}'
        with ui.element('div').classes(classes):
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
    
    def get_app_info(self) -> dict:
        """Obtenir les informations de l'application"""
        return {
            "name": settings.app_name,
            "version": settings.app_version,
            "theme": self.get_theme_status_display(),
            "language": i18n.get_language(),
            "language_name": i18n.get_language_name(i18n.get_language()),
            "direction": i18n.get_language_direction(),
            "debug": settings.debug
        }
    
    def run(self):
        """Démarrer l'application"""
        app_info = self.get_app_info()
        
        print(f"🚀 Démarrage de {app_info['name']} v{app_info['version']}")
        print(f"📱 Serveur: http://localhost:{settings.port}")
        print(f"🎨 Thème: {app_info['theme']}")
        print(f"🌐 Langue: {app_info['language']} ({app_info['language_name']})")
        print(f"📝 Direction: {app_info['direction']}")
        print(f"🐛 Debug: {app_info['debug']}")
        print("🌱 Couleur principale: Vert")
        print("=" * 60)
        
        # Afficher les statistiques de traduction en mode debug
        if settings.debug:
            try:
                from core.i18n import print_translation_validation
                print_translation_validation()
            except Exception as e:
                print(f"⚠️ Erreur validation traductions: {e}")
        
        # Lancer NiceGUI
        ui.run(
            port=settings.port,
            storage_secret=settings.secret_key,
            reload=settings.reload,
            show=True,
            title=f"{settings.app_name} - {_('nav.home')}"
        )

# Point d'entrée principal
if __name__ in {"__main__", "__mp_main__"}:
    mindcare_app = MindCareApp()
    mindcare_app.run()