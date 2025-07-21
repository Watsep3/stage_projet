import json
from typing import Dict, Any, Optional
from pathlib import Path
from nicegui import app
from config.settings import settings

class I18nManager:
    """Gestionnaire d'internationalisation"""
    
    def __init__(self):
        self.current_language = settings.default_language
        self.translations: Dict[str, Dict[str, Any]] = {}
        self.fallback_language = "en"
        
        # Charger toutes les traductions
        self.load_translations()
        
       
    
    def load_translations(self):
        """Charger toutes les traductions depuis les fichiers JSON"""
        locales_dir = settings.locales_dir
        
        for language in settings.supported_languages:
            translation_file = locales_dir / f"{language}.json"
            
            if translation_file.exists():
                try:
                    with open(translation_file, 'r', encoding='utf-8') as f:
                        self.translations[language] = json.load(f)
                    print(f"✅ Traductions {language} chargées")
                except Exception as e:
                    print(f"❌ Erreur lors du chargement des traductions {language}: {e}")
                    self.translations[language] = {}
            else:
                print(f"⚠️ Fichier de traduction {language} non trouvé")
                self.translations[language] = {}
    
    def load_language(self):
        """Charger la langue depuis le storage du navigateur"""
        try:
            stored_language = app.storage.user.get('language', settings.default_language)
            if stored_language in settings.supported_languages:
                self.current_language = stored_language
        except (RuntimeError, ValueError, KeyError):
            self.current_language = settings.default_language
    
    def save_language(self):
        """Sauvegarder la langue dans le storage du navigateur"""
        app.storage.user['language'] = self.current_language
    
    def set_language(self, language: str):
        """Définir la langue actuelle"""
        if language in settings.supported_languages:
            self.current_language = language
            self.save_language()
            return True
        return False
    
    def get_language(self) -> str:
        """Obtenir la langue actuelle"""
        return self.current_language
    
    def get_supported_languages(self) -> Dict[str, str]:
        """Obtenir les langues supportées avec leurs noms"""
        return {
            "fr": "Français",
            "en": "English",
            "ar": "العربية"
        }
    
    def translate(self, key: str, **kwargs) -> str:
        """Traduire une clé dans la langue actuelle"""
        # Récupérer la traduction dans la langue actuelle
        translation = self._get_nested_translation(
            self.translations.get(self.current_language, {}), key
        )
        
        # Si pas de traduction, essayer la langue de fallback
        if translation is None and self.current_language != self.fallback_language:
            translation = self._get_nested_translation(
                self.translations.get(self.fallback_language, {}), key
            )
        
        # Si toujours pas de traduction, retourner la clé
        if translation is None:
            translation = key
        
        # Formater avec les arguments
        try:
            return translation.format(**kwargs)
        except (KeyError, ValueError):
            return translation
    
    def _get_nested_translation(self, translations: Dict[str, Any], key: str) -> Optional[str]:
        """Récupérer une traduction imbriquée avec notation pointée"""
        keys = key.split('.')
        current = translations
        
        for k in keys:
            if isinstance(current, dict) and k in current:
                current = current[k]
            else:
                return None
        
        return current if isinstance(current, str) else None
    
    def get_language_direction(self) -> str:
        """Obtenir la direction du texte pour la langue actuelle"""
        rtl_languages = ["ar", "he", "fa", "ur"]
        return "rtl" if self.current_language in rtl_languages else "ltr"
    
    def is_rtl(self) -> bool:
        """Vérifier si la langue actuelle est RTL"""
        return self.get_language_direction() == "rtl"
    
    def get_locale_info(self) -> Dict[str, Any]:
        """Obtenir les informations de localisation"""
        return {
            "language": self.current_language,
            "direction": self.get_language_direction(),
            "is_rtl": self.is_rtl(),
            "supported_languages": self.get_supported_languages()
        }

# Instance globale du gestionnaire i18n
i18n = I18nManager()

# Fonction raccourci pour la traduction
def _(key: str, **kwargs) -> str:
    """Fonction raccourci pour la traduction"""
    return i18n.translate(key, **kwargs)

# Fonction pour obtenir les traductions d'une section
def get_translations_section(section: str) -> Dict[str, Any]:
    """Obtenir toutes les traductions d'une section"""
    current_translations = i18n.translations.get(i18n.current_language, {})
    return current_translations.get(section, {})