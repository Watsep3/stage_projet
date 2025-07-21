from nicegui import ui
from typing import Dict, Optional
from core.i18n import i18n, _

class LanguageSelector:
    """Composant sélecteur de langue"""
    
    def __init__(self):
        self.languages = i18n.get_supported_languages()
        self.current_language = i18n.get_language()
        self.language_flags = {
            'fr': '🇫🇷',
            'en': '🇺🇸',
            'ar': '🇸🇦'
        }
    
    def get_language_flag(self, lang_code: str) -> str:
        """Obtenir le drapeau d'une langue"""
        return self.language_flags.get(lang_code, '🌐')
    
    def change_language(self, lang_code: str):
        """Changer la langue"""
        if i18n.set_language(lang_code):
            self.current_language = lang_code
            # Recharger la page pour appliquer les changements
            ui.run_javascript('window.location.reload()')
    
    def render(self):
        """Rendre le sélecteur de langue (version dropdown)"""
        with ui.button().classes('p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-800').props('flat'):
            with ui.row().classes('items-center gap-2'):
                ui.label(self.get_language_flag(self.current_language))
                ui.label(self.languages[self.current_language]).classes('hidden sm:block')
                ui.icon('expand_more').classes('text-sm')
            
            with ui.menu():
                for lang_code, lang_name in self.languages.items():
                    with ui.menu_item(on_click=lambda lc=lang_code: self.change_language(lc)):
                        with ui.row().classes('items-center gap-3 min-w-32'):
                            ui.label(self.get_language_flag(lang_code))
                            ui.label(lang_name)
                            if lang_code == self.current_language:
                                ui.icon('check').classes('text-green-500 ml-auto')
    
    def render_compact(self):
        """Rendre le sélecteur compact pour mobile"""
        with ui.select(
            options={code: f"{self.get_language_flag(code)} {name}" 
                    for code, name in self.languages.items()},
            value=self.current_language,
            on_change=lambda e: self.change_language(e.value)
        ).classes('w-full'):
            pass
    
    def render_buttons(self):
        """Rendre sous forme de boutons"""
        with ui.row().classes('gap-1'):
            for lang_code, lang_name in self.languages.items():
                classes = 'p-2 rounded text-sm'
                if lang_code == self.current_language:
                    classes += ' bg-primary text-white'
                else:
                    classes += ' hover:bg-gray-100 dark:hover:bg-gray-800'
                
                ui.button(
                    f"{self.get_language_flag(lang_code)}",
                    on_click=lambda lc=lang_code: self.change_language(lc)
                ).classes(classes).props('flat')
    
    def render_tabs(self):
        """Rendre sous forme d'onglets"""
        with ui.tabs().classes('bg-transparent') as tabs:
            for lang_code, lang_name in self.languages.items():
                with ui.tab(lang_code, label=f"{self.get_language_flag(lang_code)} {lang_name}"):
                    if lang_code == self.current_language:
                        tabs.set_value(lang_code)
        
        # Gérer le changement d'onglet
        tabs.on_value_change(lambda e: self.change_language(e.value))