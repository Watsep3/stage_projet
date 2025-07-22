from nicegui import ui
from typing import Dict, Optional
from core.i18n import i18n, _

class LanguageSelector:
    """Composant sélecteur de langue compatible NiceGUI"""
    
    def __init__(self):
        self.languages = i18n.get_supported_languages()
        self.current_language = i18n.get_language()
        self.language_flags = {
            'fr': '🇫🇷',
            'en': '🇺🇸', 
            'ar': '🇸🇦'
        }
        self.language_codes = {
            'fr': 'FR',
            'en': 'EN',
            'ar': 'AR'
        }
    
    def get_language_flag(self, lang_code: str) -> str:
        """Obtenir le drapeau d'une langue"""
        return self.language_flags.get(lang_code, '🌐')
    
    def get_language_code(self, lang_code: str) -> str:
        """Obtenir le code court d'une langue"""
        return self.language_codes.get(lang_code, lang_code.upper())
    
    def change_language(self, lang_code: str):
        """Changer la langue"""
        if i18n.set_language(lang_code):
            self.current_language = lang_code
            
            # Notification de changement
            lang_name = self.languages.get(lang_code, lang_code)
            ui.notify(f'Language changed to {lang_name}', type='positive')
            
            # Recharger la page pour appliquer les changements
            ui.run_javascript('setTimeout(() => window.location.reload(), 500)')
    
    def render(self):
        """Rendre le sélecteur de langue (version dropdown compatible NiceGUI)"""
        current_flag = self.get_language_flag(self.current_language)
        current_name = self.languages[self.current_language]
        current_code = self.get_language_code(self.current_language)
        
        with ui.button().classes('p-2 rounded-lg hover:bg-surface transition-all flex items-center gap-2 text-muted hover:text-primary').props('flat'):
            # Affichage actuel
            with ui.row().classes('items-center gap-2'):
                ui.label(current_flag).classes('text-lg')
                # Afficher le code sur desktop, le nom complet sur les grands écrans
                ui.label(current_code).classes('hidden sm:block lg:hidden font-medium')
                ui.label(current_name).classes('hidden lg:block font-medium')
                ui.icon('expand_more').classes('text-sm')
            
            # Menu dropdown (version simplifiée compatible NiceGUI)
            with ui.menu().classes('min-w-48'):
                # En-tête du menu
                with ui.row().classes('px-4 py-2 bg-surface'):
                    ui.label('🌐 Langue / Language / اللغة').classes('text-xs font-semibold text-muted')
                
                # Options de langue
                for lang_code, lang_name in self.languages.items():
                    with ui.menu_item(on_click=lambda lc=lang_code: self.change_language(lc)):
                        with ui.row().classes('items-center gap-3 min-w-40 py-1'):
                            ui.label(self.get_language_flag(lang_code)).classes('text-lg')
                            
                            with ui.column().classes('gap-0'):
                                ui.label(lang_name).classes('font-medium')
                                ui.label(f'{self.get_language_code(lang_code)} - {lang_code}').classes('text-xs text-muted')
                            
                            if lang_code == self.current_language:
                                ui.icon('check').classes('text-success ml-auto')
    
    def render_compact(self):
        """Rendre le sélecteur compact pour mobile"""
        # Créer les options avec drapeaux et noms
        options = {}
        for code, name in self.languages.items():
            flag = self.get_language_flag(code)
            options[code] = f"{flag} {name}"
        
        select = ui.select(
            options=options,
            value=self.current_language,
            label='Langue / Language / اللغة'
        ).classes('w-full')
        
        # Gérer le changement avec la méthode correcte pour NiceGUI
        def handle_change(e):
            new_value = None
            
            # Essayer différents formats de données d'événement
            if hasattr(e, 'value'):
                new_value = e.value
            elif hasattr(e, 'args') and e.args:
                new_value = e.args
            elif isinstance(e, dict) and 'value' in e:
                new_value = e['value']
            elif isinstance(e, str):
                new_value = e
            
            # Si c'est un objet avec 'value' et 'label', extraire la valeur
            if isinstance(new_value, dict) and 'value' in new_value:
                new_value = new_value['value']
            
            # Valider que c'est une langue supportée
            if new_value and new_value in self.languages:
                self.change_language(new_value)
            else:
                print(f"⚠️ Valeur d'événement non reconnue: {e}")
        
        select.on('update:model-value', handle_change)
        
        return select
    
    def render_buttons(self):
        """Rendre sous forme de boutons"""
        with ui.row().classes('gap-1'):
            for lang_code, lang_name in self.languages.items():
                is_current = lang_code == self.current_language
                
                classes = 'p-2 rounded-lg text-sm transition-all'
                if is_current:
                    classes += ' bg-primary text-inverse'
                else:
                    classes += ' hover:bg-surface text-muted hover:text-primary'
                
                ui.button(
                    f"{self.get_language_flag(lang_code)} {self.get_language_code(lang_code)}",
                    on_click=lambda lc=lang_code: self.change_language(lc)
                ).classes(classes).props('flat').tooltip(lang_name)
    
    def render_tabs(self):
        """Rendre sous forme d'onglets (version simplifiée)"""
        with ui.row().classes('gap-2'):
            for lang_code, lang_name in self.languages.items():
                is_current = lang_code == self.current_language
                flag = self.get_language_flag(lang_code)
                code = self.get_language_code(lang_code)
                
                classes = 'px-3 py-2 rounded-lg text-sm transition-all cursor-pointer'
                if is_current:
                    classes += ' bg-primary text-inverse'
                else:
                    classes += ' hover:bg-surface text-muted hover:text-primary'
                
                ui.button(
                    f"{flag} {code}",
                    on_click=lambda lc=lang_code: self.change_language(lc)
                ).classes(classes).props('flat').tooltip(lang_name)
    
    def render_minimal(self):
        """Rendre une version minimale avec juste les drapeaux"""
        with ui.row().classes('gap-1'):
            for lang_code in self.languages.keys():
                is_current = lang_code == self.current_language
                
                classes = 'w-8 h-8 rounded-full flex items-center justify-center transition-all'
                if is_current:
                    classes += ' bg-primary text-inverse shadow-md scale-110'
                else:
                    classes += ' hover:bg-surface hover:scale-105'
                
                ui.button(
                    self.get_language_flag(lang_code),
                    on_click=lambda lc=lang_code: self.change_language(lc)
                ).classes(classes).props('flat').tooltip(self.languages[lang_code])
    
    def render_sidebar(self):
        """Rendre pour une sidebar"""
        ui.label('Langue / Language / اللغة').classes('text-sm font-semibold text-main mb-2')
        
        with ui.column().classes('gap-2'):
            for lang_code, lang_name in self.languages.items():
                is_current = lang_code == self.current_language
                
                classes = 'w-full justify-start p-3 rounded-lg transition-all'
                if is_current:
                    classes += ' bg-primary text-inverse'
                else:
                    classes += ' hover:bg-surface text-muted hover:text-primary'
                
                with ui.button(on_click=lambda lc=lang_code: self.change_language(lc)).classes(classes).props('flat'):
                    with ui.row().classes('items-center gap-3 w-full'):
                        ui.label(self.get_language_flag(lang_code)).classes('text-lg')
                        
                        with ui.column().classes('gap-0 flex-1 text-left'):
                            ui.label(lang_name).classes('font-medium')
                            ui.label(self.get_language_code(lang_code)).classes('text-xs opacity-75')
                        
                        if is_current:
                            ui.icon('check').classes('text-success')
    
    def render_floating(self):
        """Rendre un sélecteur flottant"""
        with ui.element('div').classes('fixed bottom-4 right-4 z-50'):
            with ui.card().classes('shadow-lg bg-card'):
                with ui.card_section().classes('p-3'):
                    ui.label('🌐 Langue').classes('text-sm font-semibold text-main mb-2')
                    self.render_buttons()
    
    def get_current_language_info(self) -> Dict[str, str]:
        """Obtenir les informations de la langue actuelle"""
        return {
            'code': self.current_language,
            'name': self.languages[self.current_language],
            'flag': self.get_language_flag(self.current_language),
            'short_code': self.get_language_code(self.current_language),
            'direction': i18n.get_language_direction(),
            'is_rtl': i18n.is_rtl()
        }
    
    def update_current_language(self):
        """Mettre à jour la langue actuelle depuis i18n"""
        self.current_language = i18n.get_language()
    
    def render_with_style(self, style: str = 'dropdown'):
        """Rendre avec un style spécifique"""
        styles = {
            'dropdown': self.render,
            'compact': self.render_compact,
            'buttons': self.render_buttons,
            'tabs': self.render_tabs,
            'minimal': self.render_minimal,
            'sidebar': self.render_sidebar,
            'floating': self.render_floating
        }
        
        render_func = styles.get(style, self.render)
        return render_func()

# Fonction utilitaire pour créer rapidement un sélecteur
def create_language_selector(style: str = 'dropdown'):
    """Créer rapidement un sélecteur de langue"""
    selector = LanguageSelector()
    return selector.render_with_style(style)

# Test et exemples d'utilisation
if __name__ == "__main__":
    print("🌐 Test du sélecteur de langue")
    
    selector = LanguageSelector()
    info = selector.get_current_language_info()
    
    print(f"Langue actuelle: {info['name']} ({info['code']})")
    print(f"Drapeau: {info['flag']}")
    print(f"Direction: {info['direction']}")
    print(f"RTL: {info['is_rtl']}")