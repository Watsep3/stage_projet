from enum import Enum
from typing import Dict, Any, Optional
from nicegui import ui, app
from config.settings import settings

class Theme(Enum):
    """Énumération des thèmes disponibles"""
    LIGHT = "light"
    DARK = "dark"

class ThemeManager:
    def __init__(self):
        # État du thème - initialisé avec le thème système
        self.current_theme = Theme.LIGHT
        self.system_theme_detected = False
        
        # Palette de couleurs centralisée
        self.theme_colors = {
            Theme.LIGHT: {
                # Couleurs principales
                'primary': '#10b981',
                'primary_dark': '#059669',
                'primary_light': '#34d399',
                'secondary': '#6366f1',
                'secondary_dark': '#4f46e5',
                'accent': '#f59e0b',
                
                # Couleurs de fond et surface
                'background': '#ffffff',
                'surface': '#f8fafc',
                'surface_elevated': '#ffffff',
                'card_background': '#ffffff',
                
                # Texte
                'text': '#1f2937',
                'text_secondary': '#6b7280',
                'text_muted': '#9ca3af',
                'text_inverse': '#ffffff',
                
                # Bordures
                'border': '#e5e7eb',
                'border_focus': '#10b981',
                'divider': '#f3f4f6',
                
                # États
                'success': '#10b981',
                'warning': '#f59e0b',
                'error': '#ef4444',
                'info': '#3b82f6',
                
                # États de couleur de fond
                'success_bg': '#f0fdf4',
                'warning_bg': '#fffbeb',
                'error_bg': '#fef2f2',
                'info_bg': '#eff6ff',
                
                # Hover states
                'hover': '#f9fafb',
                'hover_primary': '#059669',
                'hover_secondary': '#4f46e5',
                
                # Gradients
                'gradient_primary': 'linear-gradient(135deg, #10b981, #34d399)',
                'gradient_secondary': 'linear-gradient(135deg, #6366f1, #8b5cf6)',
                'gradient_hero': 'linear-gradient(135deg, #10b981, #34d399)',
            },
            
            Theme.DARK: {
                # Couleurs principales (adaptées pour le dark mode)
                'primary': '#34d399',
                'primary_dark': '#10b981',
                'primary_light': '#6ee7b7',
                'secondary': '#818cf8',
                'secondary_dark': '#6366f1',
                'accent': '#fbbf24',
                
                # Couleurs de fond et surface
                'background': '#0f172a',  # Très sombre
                'surface': '#1e293b',     # Sombre
                'surface_elevated': '#334155', # Moyen sombre
                'card_background': '#1e293b',
                
                # Texte
                'text': '#f1f5f9',           # Blanc cassé
                'text_secondary': '#cbd5e1', # Gris clair
                'text_muted': '#94a3b8',     # Gris moyen
                'text_inverse': '#0f172a',   # Noir pour contraste
                
                # Bordures
                'border': '#334155',         # Gris moyen pour bordures
                'border_focus': '#34d399',   # Vert pour focus
                'divider': '#334155',        # Gris moyen pour dividers
                
                # États
                'success': '#34d399',
                'warning': '#fbbf24',
                'error': '#f87171',
                'info': '#60a5fa',
                
                # États de couleur de fond
                'success_bg': '#064e3b',
                'warning_bg': '#78350f',
                'error_bg': '#7f1d1d',
                'info_bg': '#1e3a8a',
                
                # Hover states
                'hover': '#334155',
                'hover_primary': '#10b981',
                'hover_secondary': '#6366f1',
                
                # Gradients
                'gradient_primary': 'linear-gradient(135deg, #34d399, #6ee7b7)',
                'gradient_secondary': 'linear-gradient(135deg, #818cf8, #a78bfa)',
                'gradient_hero': 'linear-gradient(135deg, #34d399, #6ee7b7)',
            }
        }
        
        # Tailles et espacements centralisés
        self.spacing = {
            'xs': '0.25rem', 'sm': '0.5rem', 'md': '1rem', 'lg': '1.5rem',
            'xl': '2rem', '2xl': '2.5rem', '3xl': '3rem', '4xl': '4rem',
        }
        
        self.border_radius = {
            'none': '0', 'sm': '0.25rem', 'md': '0.375rem', 'lg': '0.5rem',
            'xl': '0.75rem', '2xl': '1rem', 'full': '9999px',
        }
        
        self.shadows = {
            'none': 'none',
            'sm': '0 1px 2px 0 rgb(0 0 0 / 0.05)',
            'md': '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)',
            'lg': '0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)',
            'xl': '0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)',
        }

    def detect_and_apply_system_theme(self):
        """Détecter le thème système et l'appliquer immédiatement"""
        try:
            ui.run_javascript("""
                // Détecter le thème système immédiatement
                const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
                const systemTheme = prefersDark ? 'dark' : 'light';
                
                // Appliquer immédiatement le thème détecté
                document.documentElement.setAttribute('data-theme', systemTheme);
                document.body.className = document.body.className.replace(/theme-(light|dark)/g, '') + ' theme-' + systemTheme;
                
                console.log('🎨 Thème système détecté et appliqué:', systemTheme);
                
                // Envoyer au serveur pour sauvegarder
                fetch('/api/theme/system-detected', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({theme: systemTheme})
                }).catch(console.error);
                
                // Écouter les changements
                window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
                    const newTheme = e.matches ? 'dark' : 'light';
                    document.documentElement.setAttribute('data-theme', newTheme);
                    document.body.className = document.body.className.replace(/theme-(light|dark)/g, '') + ' theme-' + newTheme;
                    
                    fetch('/api/theme/system-changed', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({theme: newTheme})
                    }).catch(console.error);
                    
                    console.log('🔄 Thème système changé:', newTheme);
                });
            """)
        except Exception as e:
            print(f"⚠️ Erreur détection thème système: {e}")
            # Fallback vers le thème clair
            self.current_theme = Theme.LIGHT

    def load_user_theme_preference(self):
        """Charger la préférence utilisateur depuis le storage"""
        try:
            stored_theme = app.storage.user.get('preferred_theme')
            if stored_theme in ['light', 'dark']:
                self.current_theme = Theme(stored_theme)
                print(f"✅ Préférence utilisateur chargée: {stored_theme}")
                return True
            else:
                print("💡 Aucune préférence utilisateur, utilisation du thème système")
                return False
        except (RuntimeError, ValueError, KeyError):
            print("⚠️ Impossible de charger la préférence utilisateur")
            return False

    def save_user_theme_preference(self):
        """Sauvegarder la préférence utilisateur"""
        try:
            app.storage.user['preferred_theme'] = self.current_theme.value
            print(f"💾 Préférence sauvegardée: {self.current_theme.value}")
        except (RuntimeError, ValueError):
            print("⚠️ Impossible de sauvegarder la préférence")

    def toggle_theme(self):
        """Basculer simplement entre clair et sombre"""
        # Basculer le thème
        self.current_theme = Theme.DARK if self.current_theme == Theme.LIGHT else Theme.LIGHT
        
        # Sauvegarder la préférence
        self.save_user_theme_preference()
        
        # Appliquer le nouveau thème
        self.apply_theme_dynamically()
        
        # Notification
        theme_name = "sombre" if self.current_theme == Theme.DARK else "clair"
        ui.notify(f'Thème {theme_name} activé', type='info')
        
        print(f"🎨 Thème basculé vers: {self.current_theme.value}")

    def set_theme(self, theme: Theme):
        """Définir un thème spécifique"""
        self.current_theme = theme
        self.save_user_theme_preference()
        self.apply_theme_dynamically()

    def get_color(self, color_name: str) -> str:
        """Obtenir une couleur du thème actuel"""
        return self.theme_colors[self.current_theme].get(color_name, '#000000')
    
    def get_colors(self) -> Dict[str, str]:
        """Obtenir toutes les couleurs du thème actuel"""
        return self.theme_colors[self.current_theme].copy()

    def generate_css(self) -> str:
        """Générer le CSS du thème avec détection système automatique"""
        light_colors = self.theme_colors[Theme.LIGHT]
        dark_colors = self.theme_colors[Theme.DARK]
        
        # Générer les variables CSS pour le thème clair
        light_vars = []
        for name, color in light_colors.items():
            light_vars.append(f"--theme-{name.replace('_', '-')}: {color}")
        
        # Générer les variables CSS pour le thème sombre
        dark_vars = []
        for name, color in dark_colors.items():
            dark_vars.append(f"--theme-{name.replace('_', '-')}: {color}")
        
        # Ajouter les variables d'espacement, bordures et ombres
        spacing_vars = []
        for name, value in self.spacing.items():
            spacing_vars.append(f"--spacing-{name}: {value}")
        
        for name, value in self.border_radius.items():
            spacing_vars.append(f"--radius-{name}: {value}")
        
        for name, value in self.shadows.items():
            spacing_vars.append(f"--shadow-{name}: {value}")

        return f"""
        /* === VARIABLES DE THÈME === */
        :root {{
            {'; '.join(spacing_vars)};
        }}
        
        /* Thème clair (défaut) */
        :root,
        :root[data-theme="light"],
        .theme-light {{
            {'; '.join(light_vars)};
        }}
        
        /* Thème sombre */
        :root[data-theme="dark"],
        .theme-dark {{
            {'; '.join(dark_vars)};
        }}
        
        /* Détection automatique du thème système */
        @media (prefers-color-scheme: dark) {{
            :root:not([data-theme]) {{
                {'; '.join(dark_vars)};
            }}
        }}
        
        /* === STYLES DE BASE === */
        body {{
            background-color: var(--theme-background) !important;
            color: var(--theme-text) !important;
            transition: background-color 0.3s ease, color 0.3s ease;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }}
        
        /* === CLASSES UTILITAIRES === */
        .bg-primary {{ background-color: var(--theme-primary) !important; }}
        .bg-secondary {{ background-color: var(--theme-secondary) !important; }}
        .bg-surface {{ background-color: var(--theme-surface) !important; }}
        .bg-card {{ background-color: var(--theme-card-background) !important; }}
        .bg-success {{ background-color: var(--theme-success) !important; }}
        .bg-warning {{ background-color: var(--theme-warning) !important; }}
        .bg-error {{ background-color: var(--theme-error) !important; }}
        .bg-info {{ background-color: var(--theme-info) !important; }}
        
        .text-primary {{ color: var(--theme-primary) !important; }}
        .text-secondary {{ color: var(--theme-secondary) !important; }}
        .text-main {{ color: var(--theme-text) !important; }}
        .text-muted {{ color: var(--theme-text-secondary) !important; }}
        .text-light {{ color: var(--theme-text-muted) !important; }}
        .text-inverse {{ color: var(--theme-text-inverse) !important; }}
        .text-success {{ color: var(--theme-success) !important; }}
        .text-warning {{ color: var(--theme-warning) !important; }}
        .text-error {{ color: var(--theme-error) !important; }}
        .text-info {{ color: var(--theme-info) !important; }}
        
        .border-primary {{ border-color: var(--theme-primary) !important; }}
        .border-default {{ border-color: var(--theme-border) !important; }}
        .border-focus {{ border-color: var(--theme-border-focus) !important; }}
        
        /* === BOUTONS === */
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
        
        /* === CARTES === */
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
        
        /* === LAYOUT === */
        .page-container {{
            max-width: 1200px;
            margin: 0 auto;
            padding-left: var(--spacing-lg);
            padding-right: var(--spacing-lg);
        }}
        
        /* === OVERRIDES NICEGUI === */
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
        
        /* === FORMULAIRES (CORRIGÉ POUR THÈME SOMBRE) === */
        .q-input,
        .q-select,
        .q-textarea {{
            color: var(--theme-text) !important;
        }}
        
        .q-field__native,
        .q-field__input {{
            color: var(--theme-text) !important;
            background-color: transparent !important;
        }}
        
        .q-field__label {{
            color: var(--theme-text-secondary) !important;
        }}
        
        .q-field--focused .q-field__label {{
            color: var(--theme-primary) !important;
        }}
        
        .q-field__native::placeholder,
        .q-field__input::placeholder {{
            color: var(--theme-text-muted) !important;
            opacity: 0.7 !important;
        }}
        
        .q-field--outlined .q-field__control:before {{
            border-color: var(--theme-border) !important;
        }}
        
        .q-field--outlined .q-field__control:hover:before {{
            border-color: var(--theme-primary) !important;
        }}
        
        .q-field--outlined.q-field--focused .q-field__control:before {{
            border-color: var(--theme-border-focus) !important;
        }}
        
        .q-field--outlined .q-field__control {{
            background-color: var(--theme-surface) !important;
        }}
        
        /* Select dropdown */
        .q-menu {{
            background-color: var(--theme-card-background) !important;
            color: var(--theme-text) !important;
            border: 1px solid var(--theme-border) !important;
        }}
        
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
        
        /* === ANIMATIONS === */
        .theme-transition {{
            transition: all 0.3s ease !important;
        }}
        
        .hover-lift:hover {{
            transform: translateY(-4px);
            box-shadow: var(--shadow-lg);
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
        """

    def apply_theme(self):
        """Appliquer le thème initial"""
        # Essayer de charger la préférence utilisateur
        has_user_preference = self.load_user_theme_preference()
        
        # Générer et appliquer le CSS
        css_content = self.generate_css()
        ui.add_head_html(f'<style id="theme-css">{css_content}</style>')
        
        # Si pas de préférence utilisateur, détecter le thème système
        if not has_user_preference:
            # Programmer la détection système après l'initialisation
            ui.timer(0.1, self.detect_and_apply_system_theme, once=True)
        else:
            # Appliquer le thème utilisateur immédiatement
            ui.timer(0.1, lambda: self.apply_theme_immediately(self.current_theme.value), once=True)

    def apply_theme_immediately(self, theme: str):
        """Appliquer un thème immédiatement via JavaScript"""
        try:
            ui.run_javascript(f"""
                document.documentElement.setAttribute('data-theme', '{theme}');
                document.body.className = document.body.className.replace(/theme-(light|dark)/g, '') + ' theme-{theme}';
                console.log('🎨 Thème appliqué:', '{theme}');
            """)
        except Exception as e:
            print(f"⚠️ Erreur application thème: {e}")

    def apply_theme_dynamically(self):
        """Appliquer le thème de manière dynamique (pour le toggle)"""
        try:
            # Régénérer le CSS avec le nouveau thème
            css_content = self.generate_css()
            
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
                
                // Appliquer le thème
                document.documentElement.setAttribute('data-theme', '{self.current_theme.value}');
                document.body.className = document.body.className.replace(/theme-(light|dark)/g, '') + ' theme-{self.current_theme.value}';
                
                console.log('🎨 Thème mis à jour dynamiquement:', '{self.current_theme.value}');
            """)
        except Exception as e:
            print(f"⚠️ Erreur mise à jour dynamique: {e}")

    def get_theme_icon(self) -> str:
        """Obtenir l'icône du thème actuel"""
        return 'dark_mode' if self.current_theme == Theme.LIGHT else 'light_mode'

    def get_theme_name(self) -> str:
        """Obtenir le nom du thème actuel"""
        return "Clair" if self.current_theme == Theme.LIGHT else "Sombre"

    def is_dark_theme(self) -> bool:
        """Vérifier si le thème actuel est sombre"""
        return self.current_theme == Theme.DARK

    def get_button_classes(self, variant: str = 'primary', size: str = 'md') -> str:
        """Obtenir les classes CSS pour un bouton"""
        base_classes = 'transition-all duration-200 font-medium rounded-lg'
        
        variant_classes = {
            'primary': 'btn-primary',
            'secondary': 'btn-secondary',
            'outline': 'btn-outline',
            'ghost': 'text-primary hover:bg-surface'
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
            classes.append('shadow-lg')
        
        if hover:
            classes.append('hover-lift')
        
        return ' '.join(classes)

# Instance globale du gestionnaire de thème
theme_manager = ThemeManager()