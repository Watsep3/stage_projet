from nicegui import ui
from typing import Callable, Optional

class Navbar:
    """Composant Navbar réutilisable avec support du thème simplifié"""
    
    def __init__(self, app_name: str = "MindCare", current_theme: str = "light"):
        self.app_name = app_name
        self.current_theme = current_theme
        self.on_theme_toggle: Optional[Callable] = None
        self.on_mobile_menu_click: Optional[Callable] = None
        
        # Initialiser le sélecteur de langue
        try:
            from components.language_selector import LanguageSelector
            self.language_selector = LanguageSelector()
        except:
            self.language_selector = None
        
        # Navigation items
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
    
    def render(self):
        """Rendre la navbar complète"""
        # Ajouter le CSS responsive
        self._add_responsive_css()
        
        # Navbar principale
        with ui.element('div').classes('w-full shadow-sm border-default navbar bg-card'):
            with ui.row().classes('items-center justify-between navbar-container mx-auto w-full min-h-16'):
                # Logo
                self._render_logo()
                
                # Navigation desktop
                self._render_desktop_nav()
                
                # Actions (langue + thème + menu mobile)
                self._render_actions()
    
    def _render_logo(self):
        """Rendre le logo"""
        ui.link(
            f'🌱 {self.app_name}', 
            '/'
        ).classes('logo-text text-2xl font-bold cursor-pointer flex items-center text-primary hover:text-primary-dark').style('text-decoration: none;')
    
    def _render_desktop_nav(self):
        """Rendre la navigation desktop"""
        try:
            from core.i18n import _
        except:
            def _(key): return key.split('.')[-1].title()
        
        with ui.row().classes('desktop-nav gap-6 flex items-center'):
            for item in self.nav_items:
                ui.link(_(item["label"]), item["url"]).classes(
                    'nav-link px-3 py-2 rounded-md text-muted hover:text-primary hover:bg-surface transition-all duration-200 font-medium'
                ).style('text-decoration: none;')
    
    def _render_actions(self):
        """Rendre les boutons d'action"""
        with ui.row().classes('actions-container gap-2 items-center'):
            # Sélecteur de langue (desktop)
            with ui.element('div').classes('language-selector-desktop'):
                if self.language_selector:
                    try:
                        self.language_selector.render_buttons()
                    except Exception as e:
                        print(f"⚠️ Erreur sélecteur de langue: {e}")
                        self._render_simple_language_fallback()
                else:
                    self._render_simple_language_fallback()
            
            # Bouton thème simplifié
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
        """Rendre le bouton de thème simplifié"""
        # Icône selon le thème actuel (montrer ce qui va être activé)
        icon = 'dark_mode' if self.current_theme == 'light' else 'light_mode'
        tooltip = f'Activer le thème {"sombre" if self.current_theme == "light" else "clair"}'
        
        ui.button(
            icon=icon,
            on_click=self._handle_theme_toggle
        ).classes('p-2 rounded-full hover:bg-surface transition-all text-muted hover:text-primary') \
         .props('flat') \
         .tooltip(tooltip)
    
    def _render_mobile_menu_button(self):
        """Rendre le bouton du menu mobile"""
        ui.button(
            icon='menu',
            on_click=self._handle_mobile_menu
        ).classes('mobile-menu-btn p-2 rounded-full hover:bg-surface transition-all text-muted hover:text-primary hidden').props('flat')
    
    def _handle_theme_toggle(self):
        """Gérer le clic sur le bouton de thème"""
        if self.on_theme_toggle:
            self.on_theme_toggle()
        else:
            # Comportement par défaut
            from core.theme import theme_manager
            theme_manager.toggle_theme()
            self.current_theme = theme_manager.current_theme.value
    
    def _handle_mobile_menu(self):
        """Gérer le clic sur le menu mobile"""
        if self.on_mobile_menu_callback:
            self.on_mobile_menu_callback()
        else:
            self.show_default_mobile_menu()
    
    def show_default_mobile_menu(self):
        """Afficher le menu mobile par défaut"""
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
                    
                    if self.language_selector:
                        try:
                            self.language_selector.render_buttons()
                        except:
                            self._render_simple_language_fallback()
                    else:
                        self._render_simple_language_fallback()
                    
                    ui.separator().classes('my-2')
                    
                    # Section thème
                    ui.label('Thème').classes('text-sm font-semibold text-main mb-2')
                    
                    current_theme_name = "Clair" if self.current_theme == "light" else "Sombre"
                    next_theme_name = "Sombre" if self.current_theme == "light" else "Clair"
                    theme_icon = 'dark_mode' if self.current_theme == 'light' else 'light_mode'
                    
                    ui.label(f'Thème actuel: {current_theme_name}').classes('text-sm text-muted mb-2')
                    
                    ui.button(
                        f'{theme_icon} Basculer vers {next_theme_name}',
                        on_click=lambda: (self._handle_theme_toggle(), dialog.close())
                    ).classes('w-full justify-start text-muted hover:text-primary hover:bg-surface').props('flat')
        
        dialog.open()
    
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
        """CSS responsive pour la navbar"""
        ui.add_head_html("""
        <style>
        /* === NAVBAR RESPONSIVE === */
        .navbar {
            position: sticky;
            top: 0;
            z-index: 1000;
            border-bottom: 1px solid var(--theme-border);
        }
        
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
        
        .logo-text {
            display: flex;
            align-items: center;
            height: 4rem;
            transition: color 0.2s ease;
        }
        
        .logo-text:hover {
            text-decoration: none !important;
        }
        
        .desktop-nav {
            display: flex;
            align-items: center;
            gap: var(--spacing-lg);
            height: 4rem;
        }
        
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
        
        .actions-container {
            display: flex;
            align-items: center;
            gap: var(--spacing-sm);
            height: 4rem;
        }
        
        .language-selector-desktop {
            display: flex;
            align-items: center;
        }
        
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
        
        .mobile-dialog .q-dialog__inner {
            padding: var(--spacing-md);
        }
        
        @media (max-width: 640px) {
            .mobile-dialog .q-card {
                margin: 0 !important;
                max-width: calc(100vw - 2rem) !important;
            }
        }
        
        .navbar a::before,
        .navbar .q-link::before,
        .navbar .nicegui-link::before {
            display: none !important;
            content: none !important;
        }
        
        .navbar .nicegui-link {
            text-decoration: none !important;
        }
        
        .q-tooltip {
            background-color: var(--theme-surface-elevated) !important;
            color: var(--theme-text) !important;
            border: 1px solid var(--theme-border) !important;
            font-size: 0.75rem !important;
        }
        </style>
        """)