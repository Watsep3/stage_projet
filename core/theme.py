from enum import Enum
from typing import Dict, Any, Optional
from nicegui import ui, app
from config.settings import settings

class Theme(Enum):
    """Énumération des thèmes disponibles"""
    LIGHT = "light"
    DARK = "dark"

class ThemePreference(Enum):
    """Préférences de thème"""
    AUTO = "auto"  # Suit le système
    LIGHT = "light"  # Forcé en clair
    DARK = "dark"   # Forcé en sombre

class ThemeManager:
    def __init__(self):
        # État du thème
        self.current_theme = Theme.LIGHT
        self.theme_preference = ThemePreference.AUTO  # Par défaut, suit le système
        self.system_theme = Theme.LIGHT  # Thème détecté du système
        
        # Palette de couleurs centralisée (votre code existant)
        self.theme_colors = {
            Theme.LIGHT: {
                # Couleurs principales
                'primary': '#10b981',        # Vert principal
                'primary_dark': '#059669',   # Vert foncé pour hover
                'primary_light': '#34d399',  # Vert clair
                'secondary': '#6366f1',      # Indigo
                'secondary_dark': '#4f46e5', # Indigo foncé
                'accent': '#f59e0b',         # Amber
                
                # Couleurs de fond et surface
                'background': '#ffffff',
                'surface': '#f8fafc',        # Gris très clair
                'surface_elevated': '#ffffff',
                'card_background': '#ffffff',
                
                # Texte
                'text': '#1f2937',           # Gris très foncé
                'text_secondary': '#6b7280', # Gris moyen
                'text_muted': '#9ca3af',     # Gris clair
                'text_inverse': '#ffffff',   # Blanc pour contraste
                
                # Bordures
                'border': '#e5e7eb',         # Gris clair pour bordures
                'border_focus': '#10b981',   # Vert pour focus
                'divider': '#f3f4f6',        # Gris très clair pour dividers
                
                # États
                'success': '#10b981',        # Vert
                'warning': '#f59e0b',        # Amber
                'error': '#ef4444',          # Rouge
                'info': '#3b82f6',           # Bleu
                
                # États de couleur de fond
                'success_bg': '#f0fdf4',     # Vert très clair
                'warning_bg': '#fffbeb',     # Amber très clair
                'error_bg': '#fef2f2',       # Rouge très clair
                'info_bg': '#eff6ff',        # Bleu très clair
                
                # Hover states
                'hover': '#f9fafb',          # Gris très léger
                'hover_primary': '#059669',  # Vert foncé
                'hover_secondary': '#4f46e5', # Indigo foncé
                
                # Gradients
                'gradient_primary': 'linear-gradient(135deg, #10b981, #34d399)',
                'gradient_secondary': 'linear-gradient(135deg, #6366f1, #8b5cf6)',
                'gradient_hero': 'linear-gradient(135deg, #10b981, #34d399)',
            },
            
            Theme.DARK: {
                # Couleurs principales (adaptées pour le dark mode)
                'primary': '#34d399',        # Vert plus clair pour le dark
                'primary_dark': '#10b981',   # Vert standard pour hover
                'primary_light': '#6ee7b7',  # Vert très clair
                'secondary': '#818cf8',      # Indigo plus clair
                'secondary_dark': '#6366f1', # Indigo standard
                'accent': '#fbbf24',         # Amber plus clair
                
                # Couleurs de fond et surface
                'background': '#111827',     # Gris très foncé
                'surface': '#1f2937',        # Gris foncé
                'surface_elevated': '#374151', # Gris moyen foncé
                'card_background': '#1f2937',
                
                # Texte
                'text': '#f9fafb',           # Blanc cassé
                'text_secondary': '#d1d5db', # Gris clair
                'text_muted': '#9ca3af',     # Gris moyen
                'text_inverse': '#111827',   # Noir pour contraste
                
                # Bordures
                'border': '#374151',         # Gris moyen pour bordures
                'border_focus': '#34d399',   # Vert pour focus
                'divider': '#374151',        # Gris moyen pour dividers
                
                # États
                'success': '#34d399',        # Vert clair
                'warning': '#fbbf24',        # Amber clair
                'error': '#f87171',          # Rouge clair
                'info': '#60a5fa',           # Bleu clair
                
                # États de couleur de fond
                'success_bg': '#064e3b',     # Vert très foncé
                'warning_bg': '#78350f',     # Amber très foncé
                'error_bg': '#7f1d1d',       # Rouge très foncé
                'info_bg': '#1e3a8a',        # Bleu très foncé
                
                # Hover states
                'hover': '#374151',          # Gris moyen
                'hover_primary': '#10b981',  # Vert standard
                'hover_secondary': '#6366f1', # Indigo standard
                
                # Gradients
                'gradient_primary': 'linear-gradient(135deg, #34d399, #6ee7b7)',
                'gradient_secondary': 'linear-gradient(135deg, #818cf8, #a78bfa)',
                'gradient_hero': 'linear-gradient(135deg, #34d399, #6ee7b7)',
            }
        }
        
        # Tailles et espacements centralisés (votre code existant)
        self.spacing = {
            'xs': '0.25rem',    # 4px
            'sm': '0.5rem',     # 8px
            'md': '1rem',       # 16px
            'lg': '1.5rem',     # 24px
            'xl': '2rem',       # 32px
            '2xl': '2.5rem',    # 40px
            '3xl': '3rem',      # 48px
            '4xl': '4rem',      # 64px
        }
        
        # Rayons de bordure
        self.border_radius = {
            'none': '0',
            'sm': '0.25rem',    # 4px
            'md': '0.375rem',   # 6px
            'lg': '0.5rem',     # 8px
            'xl': '0.75rem',    # 12px
            '2xl': '1rem',      # 16px
            'full': '9999px',   # Cercle parfait
        }
        
        # Ombres
        self.shadows = {
            'none': 'none',
            'sm': '0 1px 2px 0 rgb(0 0 0 / 0.05)',
            'md': '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)',
            'lg': '0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)',
            'xl': '0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)',
        }

    def delayed_system_detection(self):
        """Détecter le thème système après l'initialisation"""
        try:
            # Maintenant on peut utiliser JavaScript
            self.detect_system_theme()
            
            # Ajouter la classe de thème
            ui.run_javascript(f"""
                document.documentElement.className = 'theme-{self.theme_preference.value}';
                console.log('🎨 Thème initialisé:', '{self.current_theme.value}', 'Préférence:', '{self.theme_preference.value}');
            """)
        except Exception as e:
            print(f"⚠️ Détection système échouée: {e}")

    def detect_system_theme(self):
        """Détecter le thème système via JavaScript (de manière sécurisée)"""
        try:
            ui.run_javascript("""
                // Détecter le thème système
                const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
                const systemTheme = prefersDark ? 'dark' : 'light';
                
                // Envoyer le résultat au serveur via un événement personnalisé
                fetch('/api/theme/system-detected', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({theme: systemTheme})
                }).catch(() => {
                    // Fallback: utiliser le localStorage temporaire
                    localStorage.setItem('detected_system_theme', systemTheme);
                    console.log('🎨 Thème système détecté (fallback):', systemTheme);
                });
                
                // Écouter les changements de thème système
                window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
                    const newSystemTheme = e.matches ? 'dark' : 'light';
                    fetch('/api/theme/system-changed', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({theme: newSystemTheme})
                    }).catch(() => {
                        localStorage.setItem('detected_system_theme', newSystemTheme);
                        console.log('🔄 Changement thème système (fallback):', newSystemTheme);
                    });
                });
                
                console.log('🎨 Détection thème système initialisée');
            """)
        except Exception as e:
            # Fallback si JavaScript échoue
            print(f"⚠️ Impossible de détecter le thème système: {e}")
            self.system_theme = Theme.LIGHT

    def load_theme_preferences(self):
        """Charger les préférences de thème depuis le storage"""
        try:
            # Charger la préférence utilisateur
            stored_preference = app.storage.user.get('theme_preference', 'auto')
            self.theme_preference = ThemePreference(stored_preference)
            
            # Charger le thème système détecté (si disponible)
            stored_system_theme = app.storage.user.get('system_theme', 'light')
            self.system_theme = Theme(stored_system_theme)
            
            # Appliquer le thème approprié
            self.apply_theme_preference()
            
        except (RuntimeError, ValueError, KeyError):
            # Fallback en cas d'erreur
            self.theme_preference = ThemePreference.AUTO
            self.system_theme = Theme.LIGHT
            self.current_theme = Theme.LIGHT

    def load_theme(self):
        """Méthode de compatibilité - redirige vers load_theme_preferences"""
        return self.load_theme_preferences()

    def save_theme_preferences(self):
        """Sauvegarder les préférences de thème"""
        try:
            app.storage.user['theme_preference'] = self.theme_preference.value
            app.storage.user['system_theme'] = self.system_theme.value
            app.storage.user['current_theme'] = self.current_theme.value
        except (RuntimeError, ValueError):
            print("⚠️ Impossible de sauvegarder les préférences de thème")

    def apply_theme_preference(self):
        """Appliquer le thème selon la préférence utilisateur"""
        if self.theme_preference == ThemePreference.AUTO:
            # Suivre le thème système
            self.current_theme = self.system_theme
        elif self.theme_preference == ThemePreference.LIGHT:
            # Forcer le thème clair
            self.current_theme = Theme.LIGHT
        elif self.theme_preference == ThemePreference.DARK:
            # Forcer le thème sombre
            self.current_theme = Theme.DARK

    def set_system_theme(self, system_theme: Theme):
        """Mettre à jour le thème système détecté"""
        self.system_theme = system_theme
        
        # Si l'utilisateur suit le système, appliquer le changement
        if self.theme_preference == ThemePreference.AUTO:
            old_theme = self.current_theme
            self.current_theme = system_theme
            
            # Sauvegarder et appliquer seulement si le thème a changé
            if old_theme != self.current_theme:
                self.save_theme_preferences()
                self.update_theme_dynamically()
                
                theme_name = 'sombre' if self.current_theme == Theme.DARK else 'clair'
                ui.notify(f'Thème système changé vers {theme_name}', type='info')

    def toggle_theme(self):
        """Basculer entre les thèmes (cycle: auto → light → dark → auto)"""
        if self.theme_preference == ThemePreference.AUTO:
            # Auto → Light
            self.theme_preference = ThemePreference.LIGHT
            self.current_theme = Theme.LIGHT
            message = "Thème clair forcé"
        elif self.theme_preference == ThemePreference.LIGHT:
            # Light → Dark
            self.theme_preference = ThemePreference.DARK
            self.current_theme = Theme.DARK
            message = "Thème sombre forcé"
        else:
            # Dark → Auto
            self.theme_preference = ThemePreference.AUTO
            self.current_theme = self.system_theme
            theme_name = 'sombre' if self.current_theme == Theme.DARK else 'clair'
            message = f"Thème automatique ({theme_name})"
        
        self.save_theme_preferences()
        self.update_theme_dynamically()
        self.force_refresh_form_fields()
        self.ensure_high_css_specificity()
        
        ui.notify(message, type='info')

    def set_theme_preference(self, preference: ThemePreference):
        """Définir une préférence de thème spécifique"""
        self.theme_preference = preference
        self.apply_theme_preference()
        self.save_theme_preferences()
        self.update_theme_dynamically()

    def get_theme_status(self) -> Dict[str, str]:
        """Obtenir le statut complet du thème"""
        return {
            'current_theme': self.current_theme.value,
            'theme_preference': self.theme_preference.value,
            'system_theme': self.system_theme.value,
            'is_following_system': self.theme_preference == ThemePreference.AUTO
        }

    def get_color(self, color_name: str) -> str:
        """Obtenir une couleur du thème actuel"""
        return self.theme_colors[self.current_theme].get(color_name, '#000000')
    
    def get_colors(self) -> Dict[str, str]:
        """Obtenir toutes les couleurs du thème actuel"""
        return self.theme_colors[self.current_theme].copy()
    
    def get_spacing(self, size: str) -> str:
        """Obtenir une valeur d'espacement"""
        return self.spacing.get(size, '1rem')
    
    def get_border_radius(self, size: str) -> str:
        """Obtenir un rayon de bordure"""
        return self.border_radius.get(size, '0.375rem')
    
    def get_shadow(self, size: str) -> str:
        """Obtenir une ombre"""
        return self.shadows.get(size, 'none')
    
    def generate_css(self) -> str:
        """Générer le CSS du thème avec détection système"""
        colors = self.get_colors()
        
        # Générer les variables CSS
        css_vars = []
        for name, color in colors.items():
            css_vars.append(f"--theme-{name.replace('_', '-')}: {color}")
        
        # Ajouter les variables d'espacement
        for name, value in self.spacing.items():
            css_vars.append(f"--spacing-{name}: {value}")
        
        # Ajouter les variables de border-radius
        for name, value in self.border_radius.items():
            css_vars.append(f"--radius-{name}: {value}")
        
        # Ajouter les variables d'ombre
        for name, value in self.shadows.items():
            css_vars.append(f"--shadow-{name}: {value}")
        
        return f"""
        :root {{
            {'; '.join(css_vars)};
        }}
        
        /* Détection automatique du thème système (fallback) */
        @media (prefers-color-scheme: dark) {{
            :root.theme-auto {{
                --theme-primary: #34d399;
                --theme-primary-dark: #10b981;
                --theme-background: #111827;
                --theme-surface: #1f2937;
                --theme-card-background: #1f2937;
                --theme-text: #f9fafb;
                --theme-text-secondary: #d1d5db;
                --theme-text-muted: #9ca3af;
                --theme-border: #374151;
                /* Autres variables dark... */
            }}
        }}
        
        /* === STYLES DE BASE === */
        body {{
            background-color: var(--theme-background);
            color: var(--theme-text);
            transition: background-color 0.3s ease, color 0.3s ease;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }}
        
        /* === CLASSES UTILITAIRES POUR LES COULEURS === */
        
        /* Backgrounds */
        .bg-primary {{ background-color: var(--theme-primary) !important; }}
        .bg-primary-dark {{ background-color: var(--theme-primary-dark) !important; }}
        .bg-primary-light {{ background-color: var(--theme-primary-light) !important; }}
        .bg-secondary {{ background-color: var(--theme-secondary) !important; }}
        .bg-surface {{ background-color: var(--theme-surface) !important; }}
        .bg-card {{ background-color: var(--theme-card-background) !important; }}
        .bg-success {{ background-color: var(--theme-success) !important; }}
        .bg-warning {{ background-color: var(--theme-warning) !important; }}
        .bg-error {{ background-color: var(--theme-error) !important; }}
        .bg-info {{ background-color: var(--theme-info) !important; }}
        
        /* Background states */
        .bg-success-light {{ background-color: var(--theme-success-bg) !important; }}
        .bg-warning-light {{ background-color: var(--theme-warning-bg) !important; }}
        .bg-error-light {{ background-color: var(--theme-error-bg) !important; }}
        .bg-info-light {{ background-color: var(--theme-info-bg) !important; }}
        
        /* Text colors */
        .text-primary {{ color: var(--theme-primary) !important; }}
        .text-primary-dark {{ color: var(--theme-primary-dark) !important; }}
        .text-secondary {{ color: var(--theme-secondary) !important; }}
        .text-main {{ color: var(--theme-text) !important; }}
        .text-muted {{ color: var(--theme-text-secondary) !important; }}
        .text-light {{ color: var(--theme-text-muted) !important; }}
        .text-inverse {{ color: var(--theme-text-inverse) !important; }}
        .text-success {{ color: var(--theme-success) !important; }}
        .text-warning {{ color: var(--theme-warning) !important; }}
        .text-error {{ color: var(--theme-error) !important; }}
        .text-info {{ color: var(--theme-info) !important; }}
        
        /* Borders */
        .border-primary {{ border-color: var(--theme-primary) !important; }}
        .border-default {{ border-color: var(--theme-border) !important; }}
        .border-focus {{ border-color: var(--theme-border-focus) !important; }}
        
        /* === CLASSES UTILITAIRES POUR LES BOUTONS === */
        .btn-primary {{
            background-color: var(--theme-primary) !important;
            color: var(--theme-text-inverse) !important;
            border: none !important;
            transition: all 0.2s ease !important;
        }}
        
        .btn-primary:hover {{
            background-color: var(--theme-primary-dark) !important;
            transform: translateY(-1px);
            box-shadow: var(--shadow-md);
        }}
        
        .btn-secondary {{
            background-color: var(--theme-secondary) !important;
            color: var(--theme-text-inverse) !important;
            border: none !important;
            transition: all 0.2s ease !important;
        }}
        
        .btn-secondary:hover {{
            background-color: var(--theme-secondary-dark) !important;
            transform: translateY(-1px);
            box-shadow: var(--shadow-md);
        }}
        
        .btn-outline {{
            background-color: transparent !important;
            color: var(--theme-primary) !important;
            border: 2px solid var(--theme-primary) !important;
            transition: all 0.2s ease !important;
        }}
        
        .btn-outline:hover {{
            background-color: var(--theme-primary) !important;
            color: var(--theme-text-inverse) !important;
        }}
        
        .btn-ghost {{
            background-color: transparent !important;
            color: var(--theme-primary) !important;
            border: none !important;
        }}
        
        .btn-ghost:hover {{
            background-color: var(--theme-hover) !important;
        }}
        
        /* === CLASSES UTILITAIRES POUR LES CARTES === */
        .card {{
            background-color: var(--theme-card-background) !important;
            border: 1px solid var(--theme-border) !important;
            border-radius: var(--radius-lg) !important;
            box-shadow: var(--shadow-sm) !important;
            transition: all 0.3s ease !important;
        }}
        
        .card:hover {{
            box-shadow: var(--shadow-lg) !important;
            transform: translateY(-2px);
        }}
        
        .card-elevated {{
            background-color: var(--theme-surface-elevated) !important;
            box-shadow: var(--shadow-md) !important;
        }}
        
        /* === GRADIENTS === */
        .gradient-primary {{
            background: var(--theme-gradient-primary) !important;
        }}
        
        .gradient-secondary {{
            background: var(--theme-gradient-secondary) !important;
        }}
        
        .gradient-hero {{
            background: var(--theme-gradient-hero) !important;
        }}
        
        /* === CLASSES UTILITAIRES POUR LA MISE EN PAGE === */
        .page-container {{
            max-width: 1200px;
            margin: 0 auto;
            padding-left: var(--spacing-lg);
            padding-right: var(--spacing-lg);
        }}
        
        @media (min-width: 1201px) {{
            .page-container {{
                max-width: 1400px;
                padding-left: var(--spacing-xl);
                padding-right: var(--spacing-xl);
            }}
        }}
        
        @media (max-width: 768px) {{
            .page-container {{
                padding-left: var(--spacing-md);
                padding-right: var(--spacing-md);
            }}
        }}
        
        /* === ANIMATIONS ET TRANSITIONS === */
        .theme-transition {{
            transition: all 0.3s ease !important;
        }}
        
        .hover-lift:hover {{
            transform: translateY(-4px);
            box-shadow: var(--shadow-lg);
        }}
        
        .hover-scale:hover {{
            transform: scale(1.02);
        }}
        
        /* === OVERRIDE NICEGUI === */
        .q-page {{
            background-color: var(--theme-background) !important;
        }}
        
        .q-card {{
            background-color: var(--theme-card-background) !important;
            color: var(--theme-text) !important;
        }}
        
        .q-btn--standard {{
            background-color: var(--theme-primary) !important;
            color: var(--theme-text-inverse) !important;
        }}
        
        .q-btn--outline {{
            border-color: var(--theme-primary) !important;
            color: var(--theme-primary) !important;
        }}
        
        /* === FORM FIELDS FIXES === */
        
        /* Input fields - Text color */
        .q-input,
        .q-select,
        .q-textarea {{
            color: var(--theme-text) !important;
        }}
        
        /* Input native text (le texte que l'utilisateur tape) */
        .q-field__native,
        .q-field__input {{
            color: var(--theme-text) !important;
        }}
        
        /* Labels des champs */
        .q-field__label {{
            color: var(--theme-text-secondary) !important;
        }}
        
        /* Label en focus */
        .q-field--focused .q-field__label {{
            color: var(--theme-primary) !important;
        }}
        
        /* Placeholder text */
        .q-field__native::placeholder,
        .q-field__input::placeholder {{
            color: var(--theme-text-muted) !important;
            opacity: 0.7 !important;
        }}
        
        /* Bordures des champs outlined */
        .q-field--outlined .q-field__control:before {{
            border-color: var(--theme-border) !important;
        }}
        
        .q-field--outlined .q-field__control:hover:before {{
            border-color: var(--theme-primary) !important;
        }}
        
        .q-field--outlined.q-field--focused .q-field__control:before {{
            border-color: var(--theme-border-focus) !important;
        }}
        
        /* Background des champs */
        .q-field--outlined .q-field__control {{
            background-color: var(--theme-surface) !important;
        }}
        
        /* Select dropdown */
        .q-select .q-field__native {{
            color: var(--theme-text) !important;
        }}
        
        /* Select dropdown arrow */
        .q-select .q-field__append {{
            color: var(--theme-text-secondary) !important;
        }}
        
        /* Menu dropdown */
        .q-menu {{
            background-color: var(--theme-card-background) !important;
            color: var(--theme-text) !important;
            border: 1px solid var(--theme-border) !important;
        }}
        
        /* Items dans le dropdown */
        .q-item {{
            color: var(--theme-text) !important;
        }}
        
        .q-item:hover {{
            background-color: var(--theme-hover) !important;
        }}
        
        .q-item--active {{
            background-color: var(--theme-primary) !important;
            color: var(--theme-text-inverse) !important;
        }}
        
        /* === SCROLLBAR === */
        ::-webkit-scrollbar {{
            width: 8px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: var(--theme-surface);
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: var(--theme-border);
            border-radius: var(--radius-full);
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: var(--theme-primary);
        }}
        
        /* === UTILITAIRES RESPONSIVE === */
        @media (max-width: 640px) {{
            .responsive-text {{
                font-size: 0.875rem;
            }}
            
            .responsive-padding {{
                padding: var(--spacing-sm);
            }}
        }}
        """
    
    def apply_theme(self):
        """Appliquer le thème à l'interface (SANS JavaScript pendant l'init)"""
        # Charger les préférences (sans JavaScript)
        self.load_theme_preferences()
        
        # Générer et appliquer le CSS
        css_content = self.generate_css()
        ui.add_head_html(f'<style id="theme-css">{css_content}</style>')
        
        # Ajouter les styles à haute spécificité
        self.ensure_high_css_specificity()
        
        # Programmer la détection système pour après l'initialisation
        ui.timer(0.1, lambda: self.delayed_system_detection(), once=True)
    
    def update_theme_dynamically(self):
        """Mettre à jour le thème de manière dynamique (pour le toggle)"""
        try:
            # Générer le nouveau CSS
            css_content = self.generate_css()
            
            # Supprimer l'ancien style et ajouter le nouveau via JavaScript
            ui.run_javascript(f"""
                // Supprimer l'ancien style
                const existingStyle = document.getElementById('theme-css');
                if (existingStyle) {{
                    existingStyle.remove();
                }}
                
                // Ajouter le nouveau style
                const style = document.createElement('style');
                style.id = 'theme-css';
                style.textContent = `{css_content}`;
                document.head.appendChild(style);
                
                // Mettre à jour la classe de thème
                document.documentElement.className = 'theme-{self.theme_preference.value}';
                
                // Forcer la mise à jour des champs de formulaire existants
                const fields = document.querySelectorAll('.q-field__native, .q-field__input, .q-field__label');
                fields.forEach(field => {{
                    field.style.color = '';
                    field.offsetHeight; // Force reflow
                }});
                
                console.log('Theme updated successfully to {self.current_theme.value} (preference: {self.theme_preference.value})');
            """)
        except:
            # Si JavaScript échoue, utiliser la méthode simple
            self.apply_theme()
    
    def get_theme_icon(self) -> str:
        """Obtenir l'icône du thème selon la préférence"""
        if self.theme_preference == ThemePreference.AUTO:
            return 'auto_mode'  # ou 'brightness_auto'
        elif self.theme_preference == ThemePreference.LIGHT:
            return 'light_mode'
        else:
            return 'dark_mode'
    
    def get_theme_name(self) -> str:
        """Obtenir le nom du thème actuel"""
        if self.theme_preference == ThemePreference.AUTO:
            system_name = "sombre" if self.system_theme == Theme.DARK else "clair"
            return f"Automatique ({system_name})"
        elif self.theme_preference == ThemePreference.LIGHT:
            return "Clair"
        else:
            return "Sombre"
    
    def is_dark_theme(self) -> bool:
        """Vérifier si le thème actuel est sombre"""
        return self.current_theme == Theme.DARK
    
    # === VOS MÉTHODES EXISTANTES ===
    
    def get_button_classes(self, variant: str = 'primary', size: str = 'md') -> str:
        """Obtenir les classes CSS pour un bouton"""
        base_classes = 'transition-all duration-200 font-medium rounded-lg'
        
        variant_classes = {
            'primary': 'btn-primary',
            'secondary': 'btn-secondary',
            'outline': 'btn-outline',
            'ghost': 'btn-ghost'
        }
        
        size_classes = {
            'sm': 'px-3 py-1 text-sm',
            'md': 'px-4 py-2',
            'lg': 'px-6 py-3 text-lg',
            'xl': 'px-8 py-4 text-xl'
        }
        
        return f"{base_classes} {variant_classes.get(variant, 'btn-primary')} {size_classes.get(size, 'px-4 py-2')}"
    
    def get_card_classes(self, elevated: bool = False, hover: bool = True) -> str:
        """Obtenir les classes CSS pour une carte"""
        classes = ['card']
        
        if elevated:
            classes.append('card-elevated')
        
        if hover:
            classes.append('hover-lift')
        
        return ' '.join(classes)
    
    def get_text_classes(self, variant: str = 'main', size: str = 'base') -> str:
        """Obtenir les classes CSS pour le texte"""
        variant_classes = {
            'main': 'text-main',
            'muted': 'text-muted',
            'light': 'text-light',
            'primary': 'text-primary',
            'secondary': 'text-secondary',
            'success': 'text-success',
            'warning': 'text-warning',
            'error': 'text-error',
            'info': 'text-info'
        }
        
        size_classes = {
            'xs': 'text-xs',
            'sm': 'text-sm',
            'base': 'text-base',
            'lg': 'text-lg',
            'xl': 'text-xl',
            '2xl': 'text-2xl',
            '3xl': 'text-3xl',
            '4xl': 'text-4xl'
        }
        
        return f"{variant_classes.get(variant, 'text-main')} {size_classes.get(size, 'text-base')}"
    
    def force_refresh_form_fields(self):
        """Forcer la mise à jour de tous les champs de formulaire"""
        try:
            ui.run_javascript("""
                // Fonction pour forcer la mise à jour des styles
                function refreshFormFields() {
                    console.log('Refreshing form fields...');
                    
                    // Sélectionner tous les éléments de formulaire
                    const selectors = [
                        '.q-field__native',
                        '.q-field__input', 
                        '.q-field__label',
                        '.q-select .q-field__native',
                        '.q-textarea .q-field__native',
                        '.q-checkbox__label',
                        '.q-radio__label'
                    ];
                    
                    selectors.forEach(selector => {
                        const elements = document.querySelectorAll(selector);
                        console.log(`Found ${elements.length} elements for ${selector}`);
                        
                        elements.forEach(element => {
                            // Forcer un recalcul des styles
                            element.style.color = '';
                            element.offsetHeight; // Force reflow
                            
                            // Ajouter une classe temporaire pour forcer la mise à jour
                            element.classList.add('theme-refresh');
                            setTimeout(() => {
                                element.classList.remove('theme-refresh');
                            }, 10);
                        });
                    });
                    
                    console.log('Form fields refresh completed');
                }
                
                // Exécuter immédiatement
                refreshFormFields();
                
                // Et après un petit délai pour s'assurer que le CSS est appliqué
                setTimeout(refreshFormFields, 100);
            """)
        except Exception as e:
            print(f"Force refresh error: {e}")
    
    def ensure_high_css_specificity(self):
        """S'assurer que nos styles ont une spécificité plus élevée"""
        ui.add_head_html("""
        <style>
        /* Force higher specificity for form fields */
        html body .q-field .q-field__native,
        html body .q-field .q-field__input {
            color: var(--theme-text) !important;
        }
        
        html body .q-field .q-field__label {
            color: var(--theme-text-secondary) !important;
        }
        
        html body .q-field--focused .q-field__label {
            color: var(--theme-primary) !important;
        }
        
        html body .q-select .q-field__native {
            color: var(--theme-text) !important;
        }
        
        html body .q-textarea .q-field__native {
            color: var(--theme-text) !important;
        }
        
        /* Placeholder avec spécificité élevée */
        html body .q-field__native::placeholder,
        html body .q-field__input::placeholder {
            color: var(--theme-text-muted) !important;
            opacity: 0.7 !important;
        }
        
        /* Classe helper pour forcer la mise à jour */
        .theme-refresh {
            transition: color 0.1s ease !important;
        }
        </style>
        """)

# Instance globale du gestionnaire de thème
theme_manager = ThemeManager()
