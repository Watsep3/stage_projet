from nicegui import ui
from typing import Callable, Optional
from core.theme import theme_manager, ThemePreference

class Navbar:
    """Composant Navbar réutilisable avec support du thème système et sélecteur de langue"""
    
    def __init__(self, app_name: str = "MindCare", current_theme: str = "light"):
        self.app_name = app_name
        self.current_theme = current_theme
        self.theme_preference = "auto"  # auto, light, dark
        self.on_theme_toggle: Optional[Callable] = None
        self.on_mobile_menu_click: Optional[Callable] = None
        
        # Initialiser le sélecteur de langue
        try:
            from components.language_selector import LanguageSelector
            self.language_selector = LanguageSelector()
        except:
            self.language_selector = None
        
        # Navigation items - CLÉS CORRIGÉES
        self.nav_items = [
            {"label": "nav.home", "url": "/", "icon": "home"},
            {"label": "nav.articles", "url": "/articles", "icon": "article"},
            {"label": "nav.reports", "url": "/reports", "icon": "description"},
            {"label": "nav.chatbot", "url": "/chatbot", "icon": "smart_toy"},
            {"label": "nav.about", "url": "/about", "icon": "info"},
            {"label": "nav.contact", "url": "/contact", "icon": "contact_mail"}
        ]
    
    def set_theme_toggle_callback(self, callback: Callable):
        """Définir le callback pour le toggle de thème"""
        self.on_theme_toggle = callback
        return self
    
    def set_mobile_menu_callback(self, callback: Callable):
        """Définir le callback pour le menu mobile"""
        self.on_mobile_menu_callback = callback
        return self
    
    def update_theme(self, new_theme: str):
        """Mettre à jour le thème actuel"""
        self.current_theme = new_theme
    
    def update_theme_preference(self, preference: str):
        """Mettre à jour la préférence de thème"""
        self.theme_preference = preference
    
    def render(self):
        """Rendre la navbar complète avec le système de thème centralisé et sélecteur de langue"""
        # Ajouter le CSS responsive AVANT de créer les éléments
        self._add_responsive_css()
        
        # Utiliser les classes de thème au lieu des couleurs hardcodées
        with ui.element('div').classes('w-full shadow-sm border-default navbar bg-card'):
            with ui.row().classes('items-center justify-between navbar-container mx-auto w-full min-h-16'):
                # Logo
                self._render_logo()
                
                # Navigation desktop
                self._render_desktop_nav()
                
                # Actions (langue + thème + menu mobile)
                self._render_actions()
    
    def _render_logo(self):
        """Rendre le logo avec classes de thème"""
        ui.link(
            f'🌱 {self.app_name}', 
            '/'
        ).classes('logo-text text-2xl font-bold cursor-pointer flex items-center text-primary hover:text-primary-dark').style('text-decoration: none;')
    
    def _render_desktop_nav(self):
        """Rendre la navigation desktop avec classes de thème"""
        try:
            from core.i18n import _
        except:
            # Fallback si i18n n'est pas disponible
            def _(key): return key.split('.')[-1].title()
        
        with ui.row().classes('desktop-nav gap-6 flex items-center'):
            for item in self.nav_items:
                ui.link(_(item["label"]), item["url"]).classes(
                    'nav-link px-3 py-2 rounded-md text-muted hover:text-primary hover:bg-surface transition-all duration-200 font-medium'
                ).style('text-decoration: none;')
    
    def _render_actions(self):
        """Rendre les boutons d'action avec sélecteur de langue, thème et menu mobile"""
        with ui.row().classes('actions-container gap-2 items-center'):
            # Sélecteur de langue (desktop) - VERSION ROBUSTE
            with ui.element('div').classes('language-selector-desktop'):
                if self.language_selector:
                    try:
                        # Utiliser la version boutons qui est plus robuste
                        self.language_selector.render_buttons()
                    except Exception as e:
                        print(f"⚠️ Erreur sélecteur de langue: {e}")
                        # Fallback ultra-simple
                        self._render_simple_language_fallback()
                else:
                    self._render_simple_language_fallback()
            
            # Bouton thème
            self._render_theme_button()
            
            # Menu mobile
            self._render_mobile_menu_button()
    
    def _render_simple_language_fallback(self):
        """Fallback simple pour le sélecteur de langue"""
        languages = {'fr': '🇫🇷', 'en': '🇺🇸', 'ar': '🇸🇦'}
        with ui.row().classes('gap-1'):
            for code, flag in languages.items():
                ui.button(
                    flag,
                    on_click=lambda c=code: ui.notify(f'Langue {c} sélectionnée')
                ).classes('w-8 h-8 rounded').props('flat').tooltip(code.upper())
    
    def _render_theme_button(self):
        """Rendre le bouton de changement de thème avec la bonne icône"""
        # Obtenir l'icône selon la préférence actuelle
        theme_icon = self.get_theme_icon()
        theme_tooltip = self.get_theme_tooltip()
        
        ui.button(
            icon=theme_icon,
            on_click=self._handle_theme_toggle
        ).classes('p-2 rounded-full hover:bg-surface transition-all text-muted hover:text-primary') \
         .props('flat') \
         .tooltip(theme_tooltip)
    
    def _render_mobile_menu_button(self):
        """Rendre le bouton du menu mobile avec classes de thème"""
        ui.button(
            icon='menu',
            on_click=self._handle_mobile_menu
        ).classes('mobile-menu-btn p-2 rounded-full hover:bg-surface transition-all text-muted hover:text-primary hidden').props('flat')
    
    def _handle_theme_toggle(self):
        """Gérer le clic sur le bouton de thème"""
        if self.on_theme_toggle:
            self.on_theme_toggle()
        else:
            # Comportement par défaut utilisant le ThemeManager
            theme_manager.toggle_theme()
            self.current_theme = theme_manager.current_theme.value
            self.theme_preference = theme_manager.theme_preference.value
            
            # Notification déjà gérée par le ThemeManager
    
    def _handle_mobile_menu(self):
        """Gérer le clic sur le menu mobile"""
        if self.on_mobile_menu_callback:
            self.on_mobile_menu_callback()
        else:
            self.show_default_mobile_menu()
    
    def show_default_mobile_menu(self):
        """Afficher le menu mobile avec sélecteur de langue et info de thème"""
        try:
            from core.i18n import _
        except:
            def _(key): return key.split('.')[-1].title()
        
        with ui.dialog().classes('mobile-dialog') as dialog:
            with ui.card().classes('w-full max-w-sm bg-card'):
                with ui.column().classes('gap-4 p-4'):
                    # Header
                    with ui.row().classes('items-center justify-between mb-4'):
                        ui.label('Navigation').classes('text-lg font-semibold text-main')
                        ui.button(icon='close', on_click=dialog.close).classes('text-muted hover:text-primary').props('flat round size=sm')
                    
                    # Navigation items
                    for item in self.nav_items:
                        ui.button(
                            _(item["label"]), 
                            icon=item.get("icon"),
                            on_click=lambda url=item["url"]: (ui.navigate.to(url), dialog.close())
                        ).classes('w-full justify-start text-left text-muted hover:text-primary hover:bg-surface').props('flat')
                    
                    ui.separator().classes('my-2')
                    
                    # Section langue
                    ui.label('Langue').classes('text-sm font-semibold text-main mb-2')
                    
                    # Sélecteur de langue mobile simple
                    if self.language_selector:
                        try:
                            self.language_selector.render_buttons()
                        except:
                            self._render_simple_language_fallback()
                    else:
                        self._render_simple_language_fallback()
                    
                    ui.separator().classes('my-2')
                    
                    # Section thème améliorée
                    ui.label('Apparence').classes('text-sm font-semibold text-main mb-2')
                    
                    # Info thème actuel
                    theme_status = self.get_theme_status_display()
                    ui.label(theme_status).classes('text-xs text-muted mb-3')
                    
                    # Bouton thème dans le menu mobile
                    ui.button(
                        f'{self.get_theme_icon()} {self.get_theme_name()}',
                        on_click=lambda: (self._handle_theme_toggle(), dialog.close())
                    ).classes('w-full justify-start text-muted hover:text-primary hover:bg-surface').props('flat')
        
        dialog.open()
    
    def get_theme_icon(self) -> str:
        """Obtenir l'icône selon la préférence de thème"""
        if self.theme_preference == "auto":
            return 'brightness_auto'  # Icône auto
        elif self.theme_preference == "light":
            return 'light_mode'       # Icône soleil
        else:  # dark
            return 'dark_mode'        # Icône lune
    
    def get_theme_tooltip(self) -> str:
        """Obtenir le tooltip du bouton de thème"""
        try:
            from core.i18n import _
            if self.theme_preference == "auto":
                system_name = _('theme.dark') if theme_manager.system_theme.value == "dark" else _('theme.light')
                return _('theme.auto_tooltip', system=system_name)
            elif self.theme_preference == "light":
                return _('theme.light_tooltip')
            else:
                return _('theme.dark_tooltip')
        except:
            # Fallback sans traduction
            if self.theme_preference == "auto":
                return "Thème automatique"
            elif self.theme_preference == "light":
                return "Thème clair"
            else:
                return "Thème sombre"
    
    def get_theme_name(self) -> str:
        """Obtenir le nom du thème pour l'affichage"""
        try:
            from core.i18n import _
            if self.theme_preference == "auto":
                return _('theme.auto')
            elif self.theme_preference == "light":
                return _('theme.light')
            else:
                return _('theme.dark')
        except:
            # Fallback sans traduction
            if self.theme_preference == "auto":
                return "Automatique"
            elif self.theme_preference == "light":
                return "Clair"
            else:
                return "Sombre"
    
    def get_theme_status_display(self) -> str:
        """Obtenir un affichage du statut pour le menu mobile"""
        try:
            from core.i18n import _
            if self.theme_preference == "auto":
                system_name = _('theme.dark') if theme_manager.system_theme.value == "dark" else _('theme.light')
                return f"Suit le système ({system_name})"
            elif self.theme_preference == "light":
                return "Forcé en mode clair"
            else:
                return "Forcé en mode sombre"
        except:
            # Fallback sans traduction
            return f"Thème: {self.theme_preference}"
    
    def add_nav_item(self, label: str, url: str, icon: str = None):
        """Ajouter un élément de navigation"""
        self.nav_items.append({
            "label": label,
            "url": url,
            "icon": icon
        })
        return self
    
    def remove_nav_item(self, url: str):
        """Supprimer un élément de navigation par URL"""
        self.nav_items = [item for item in self.nav_items if item["url"] != url]
        return self
    
    def set_nav_items(self, items: list):
        """Définir tous les éléments de navigation"""
        self.nav_items = items
        return self
    
    def _add_responsive_css(self):
        """CSS responsive avec support pour le sélecteur de langue"""
        ui.add_head_html("""
        <style>
        /* === NAVBAR RESPONSIVE === */
        .navbar {
            position: sticky;
            top: 0;
            z-index: 1000;
            border-bottom: 1px solid var(--theme-border);
        }
        
        /* Container avec largeur adaptative */
        .navbar-container {
            max-width: 1200px;
            padding-left: var(--spacing-lg);
            padding-right: var(--spacing-lg);
        }
        
        @media (min-width: 1201px) {
            .navbar-container {
                max-width: 1400px;
                padding-left: var(--spacing-xl);
                padding-right: var(--spacing-xl);
            }
        }
        
        /* Logo */
        .logo-text {
            display: flex;
            align-items: center;
            height: 4rem;
            transition: color 0.2s ease;
        }
        
        .logo-text:hover {
            text-decoration: none !important;
        }
        
        /* Navigation desktop */
        .desktop-nav {
            display: flex;
            align-items: center;
            gap: var(--spacing-lg);
            height: 4rem;
        }
        
        /* Liens de navigation */
        .nav-link {
            border-radius: var(--radius-md);
            font-weight: 500;
            text-decoration: none !important;
            transition: all 0.2s ease;
            position: relative;
            display: flex;
            align-items: center;
            height: 2.5rem;
        }
        
        .nav-link:hover {
            text-decoration: none !important;
        }
        
        /* Effet de soulignement au hover */
        .nav-link::after {
            content: '';
            position: absolute;
            width: 0;
            height: 2px;
            bottom: 2px;
            left: 50%;
            background-color: var(--theme-primary);
            transition: all 0.3s ease;
            transform: translateX(-50%);
        }
        
        .nav-link:hover::after {
            width: 80%;
        }
        
        /* Actions container */
        .actions-container {
            display: flex;
            align-items: center;
            gap: var(--spacing-sm);
            height: 4rem;
        }
        
        /* Sélecteur de langue */
        .language-selector-desktop {
            display: flex;
            align-items: center;
        }
        
        /* Bouton menu mobile - masqué par défaut */
        .mobile-menu-btn {
            display: none !important;
        }
        
        /* RESPONSIVE Mobile */
        @media (max-width: 768px) {
            .desktop-nav {
                display: none !important;
            }
            
            .language-selector-desktop {
                display: none !important;
            }
            
            .mobile-menu-btn,
            .navbar .mobile-menu-btn {
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
            }
            
            .logo-text {
                font-size: 1.25rem !important;
            }
            
            .navbar-container {
                max-width: 100% !important;
                padding-left: var(--spacing-md) !important;
                padding-right: var(--spacing-md) !important;
            }
        }
        
        @media (min-width: 769px) {
            .mobile-menu-btn,
            .navbar .mobile-menu-btn {
                display: none !important;
            }
            
            .desktop-nav {
                display: flex !important;
            }
            
            .language-selector-desktop {
                display: flex !important;
            }
        }
        
        @media (max-width: 640px) {
            .navbar-container {
                padding-left: var(--spacing-sm) !important;
                padding-right: var(--spacing-sm) !important;
            }
            
            .logo-text {
                font-size: 1.125rem !important;
            }
        }
        
        /* Dialog mobile responsive */
        .mobile-dialog .q-dialog__inner {
            padding: var(--spacing-md);
        }
        
        @media (max-width: 640px) {
            .mobile-dialog .q-card {
                margin: 0 !important;
                max-width: calc(100vw - 2rem) !important;
            }
        }
        
        /* Override des styles par défaut */
        .navbar a::before,
        .navbar .q-link::before,
        .navbar .nicegui-link::before {
            display: none !important;
            content: none !important;
        }
        
        .navbar .nicegui-link {
            text-decoration: none !important;
        }
        
        /* Tooltip styling */
        .q-tooltip {
            background-color: var(--theme-surface-elevated) !important;
            color: var(--theme-text) !important;
            border: 1px solid var(--theme-border) !important;
            font-size: 0.75rem !important;
        }
        </style>
        """)