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
        
        # Charger la langue depuis le storage après l'initialisation
        self._initialize_user_language()
    
    def _initialize_user_language(self):
        """Initialiser la langue utilisateur après que l'app soit prête"""
        try:
            # Tenter de charger depuis le storage
            self.load_language()
        except:
            # Si le storage n'est pas accessible, utiliser la langue par défaut
            self.current_language = settings.default_language
    
    def load_translations(self):
        """Charger toutes les traductions depuis les fichiers JSON"""
        locales_dir = settings.locales_dir
        
        for language in settings.supported_languages:
            translation_file = locales_dir / f"{language}.json"
            
            if translation_file.exists():
                try:
                    with open(translation_file, 'r', encoding='utf-8') as f:
                        self.translations[language] = json.load(f)
                    print(f"✅ Traductions {language} chargées ({len(self.translations[language])} clés)")
                except Exception as e:
                    print(f"❌ Erreur lors du chargement des traductions {language}: {e}")
                    self.translations[language] = {}
            else:
                print(f"⚠️ Fichier de traduction {language} non trouvé: {translation_file}")
                self.translations[language] = {}
                
                # Créer un fichier de traduction vide pour le développement
                self._create_empty_translation_file(language, translation_file)
    
    def _create_empty_translation_file(self, language: str, file_path: Path):
        """Créer un fichier de traduction vide pour le développement"""
        try:
            # Créer le dossier s'il n'existe pas
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Structure de base
            empty_structure = {
                "nav": {
                    "home": "Home" if language == "en" else ("الرئيسية" if language == "ar" else "Accueil"),
                    "articles": "Articles" if language == "en" else ("المقالات" if language == "ar" else "Articles"),
                    "about": "About" if language == "en" else ("حول" if language == "ar" else "À propos"),
                    "contact": "Contact" if language == "en" else ("اتصل بنا" if language == "ar" else "Contact")
                },
                "common": {
                    "search": "Search..." if language == "en" else ("البحث..." if language == "ar" else "Rechercher..."),
                    "loading": "Loading..." if language == "en" else ("جاري التحميل..." if language == "ar" else "Chargement...")
                }
            }
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(empty_structure, f, indent=2, ensure_ascii=False)
            
            print(f"📝 Fichier de traduction {language} créé: {file_path}")
            self.translations[language] = empty_structure
            
        except Exception as e:
            print(f"❌ Impossible de créer le fichier {language}: {e}")
    
    def load_language(self):
        """Charger la langue depuis le storage du navigateur"""
        try:
            stored_language = app.storage.user.get('language', settings.default_language)
            if stored_language in settings.supported_languages:
                self.current_language = stored_language
                print(f"🌐 Langue chargée depuis le storage: {stored_language}")
            else:
                print(f"⚠️ Langue stockée invalide: {stored_language}, utilisation de {settings.default_language}")
                self.current_language = settings.default_language
        except (RuntimeError, ValueError, KeyError, AttributeError) as e:
            print(f"⚠️ Impossible de charger la langue depuis le storage: {e}")
            self.current_language = settings.default_language
    
    def save_language(self):
        """Sauvegarder la langue dans le storage du navigateur"""
        try:
            app.storage.user['language'] = self.current_language
            print(f"💾 Langue sauvegardée: {self.current_language}")
        except (RuntimeError, ValueError, AttributeError) as e:
            print(f"⚠️ Impossible de sauvegarder la langue: {e}")
    
    def set_language(self, language: str) -> bool:
        """Définir la langue actuelle"""
        if language in settings.supported_languages:
            old_language = self.current_language
            self.current_language = language
            self.save_language()
            print(f"🔄 Langue changée: {old_language} → {language}")
            return True
        else:
            print(f"❌ Langue non supportée: {language}")
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
    
    def get_language_name(self, language_code: str) -> str:
        """Obtenir le nom d'une langue"""
        return self.get_supported_languages().get(language_code, language_code)
    
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
        
        # Si toujours pas de traduction, essayer le français
        if translation is None and self.current_language != "fr":
            translation = self._get_nested_translation(
                self.translations.get("fr", {}), key
            )
        
        # Si toujours pas de traduction, retourner la clé avec un indicateur
        if translation is None:
            print(f"⚠️ Traduction manquante: {key} (langue: {self.current_language})")
            return f"[{key}]"  # Indicateur visuel pour les traductions manquantes
        
        # Formater avec les arguments
        try:
            return translation.format(**kwargs)
        except (KeyError, ValueError) as e:
            print(f"⚠️ Erreur de formatage pour {key}: {e}")
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
            "language_name": self.get_language_name(self.current_language),
            "direction": self.get_language_direction(),
            "is_rtl": self.is_rtl(),
            "supported_languages": self.get_supported_languages()
        }
    
    def get_translation_stats(self) -> Dict[str, Any]:
        """Obtenir les statistiques des traductions"""
        stats = {}
        
        for lang, translations in self.translations.items():
            stats[lang] = {
                "total_keys": self._count_keys(translations),
                "language_name": self.get_language_name(lang)
            }
        
        return stats
    
    def _count_keys(self, obj: Any) -> int:
        """Compter récursivement le nombre de clés de traduction"""
        if isinstance(obj, dict):
            count = 0
            for value in obj.values():
                if isinstance(value, str):
                    count += 1
                elif isinstance(value, dict):
                    count += self._count_keys(value)
            return count
        return 0
    
    def validate_translations(self) -> Dict[str, Any]:
        """Valider la complétude des traductions"""
        if not self.translations:
            return {"status": "error", "message": "Aucune traduction chargée"}
        
        # Utiliser le français comme référence
        reference_lang = "fr"
        if reference_lang not in self.translations:
            return {"status": "error", "message": f"Langue de référence {reference_lang} non trouvée"}
        
        reference_keys = self._get_all_keys(self.translations[reference_lang])
        results = {}
        
        for lang, translations in self.translations.items():
            if lang == reference_lang:
                continue
                
            lang_keys = self._get_all_keys(translations)
            missing_keys = reference_keys - lang_keys
            extra_keys = lang_keys - reference_keys
            
            results[lang] = {
                "total_keys": len(lang_keys),
                "missing_keys": list(missing_keys),
                "extra_keys": list(extra_keys),
                "completion_rate": len(lang_keys) / len(reference_keys) * 100 if reference_keys else 0
            }
        
        return {"status": "success", "results": results}
    
    def _get_all_keys(self, obj: Any, prefix: str = "") -> set:
        """Obtenir toutes les clés de traduction d'un objet"""
        keys = set()
        
        if isinstance(obj, dict):
            for key, value in obj.items():
                current_key = f"{prefix}.{key}" if prefix else key
                
                if isinstance(value, str):
                    keys.add(current_key)
                elif isinstance(value, dict):
                    keys.update(self._get_all_keys(value, current_key))
        
        return keys

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

# Fonction pour changer de langue depuis l'interface
def switch_language(language_code: str) -> bool:
    """Changer de langue et recharger l'interface"""
    if i18n.set_language(language_code):
        # La page sera rechargée par le sélecteur de langue
        return True
    return False

# Fonctions utilitaires pour le développement
def print_translation_stats():
    """Afficher les statistiques des traductions"""
    stats = i18n.get_translation_stats()
    print("\n📊 Statistiques des traductions:")
    for lang, info in stats.items():
        print(f"  {lang} ({info['language_name']}): {info['total_keys']} clés")

def print_translation_validation():
    """Afficher la validation des traductions"""
    validation = i18n.validate_translations()
    if validation["status"] == "error":
        print(f"❌ Erreur de validation: {validation['message']}")
        return
    
    print("\n🔍 Validation des traductions:")
    for lang, results in validation["results"].items():
        completion = results["completion_rate"]
        print(f"  {lang}: {completion:.1f}% complet ({results['total_keys']} clés)")
        
        if results["missing_keys"]:
            print(f"    ⚠️ Clés manquantes: {len(results['missing_keys'])}")
            for key in results["missing_keys"][:5]:  # Afficher seulement les 5 premières
                print(f"      - {key}")
            if len(results["missing_keys"]) > 5:
                print(f"      ... et {len(results['missing_keys']) - 5} autres")

# Initialisation pour le développement
if __name__ == "__main__":
    print("🌐 Test du système i18n")
    print(f"Langue actuelle: {i18n.get_language()}")
    print(f"Langues supportées: {list(i18n.get_supported_languages().keys())}")
    
    # Test de quelques traductions
    print(f"\nTest de traductions:")
    print(f"nav.home (fr): {i18n.translate('nav.home')}")
    
    i18n.set_language('en')
    print(f"nav.home (en): {i18n.translate('nav.home')}")
    
    i18n.set_language('ar')
    print(f"nav.home (ar): {i18n.translate('nav.home')}")
    
    # Statistiques
    print_translation_stats()
    print_translation_validation()