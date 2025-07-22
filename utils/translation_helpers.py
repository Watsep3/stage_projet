"""
Utilitaires pour faciliter l'utilisation des traductions dans MindCare
"""

from typing import Dict, List, Any, Optional, Union
from datetime import datetime
from core.i18n import i18n, _
import json
import re

class TranslationHelper:
    """Helper pour faciliter l'utilisation des traductions"""
    
    @staticmethod
    def get_localized_field(data: Dict[str, Any], field: str, default: str = "") -> str:
        """
        Obtenir un champ localisé selon la langue actuelle
        
        Args:
            data: Dictionnaire contenant les données
            field: Nom du champ de base
            default: Valeur par défaut si aucune traduction trouvée
            
        Returns:
            Texte localisé
        """
        current_lang = i18n.get_language()
        
        # Essayer la langue actuelle avec suffixe
        if current_lang != "fr":  # fr est la langue par défaut
            localized_field = f"{field}_{current_lang}"
            if localized_field in data and data[localized_field]:
                return data[localized_field]
        
        # Fallback vers le champ de base
        if field in data and data[field]:
            return data[field]
        
        return default
    
    @staticmethod
    def get_localized_list(data: Dict[str, Any], field: str) -> List[str]:
        """
        Obtenir une liste localisée (pour les tags par exemple)
        
        Args:
            data: Dictionnaire contenant les données
            field: Nom du champ de base
            
        Returns:
            Liste localisée
        """
        current_lang = i18n.get_language()
        
        # Essayer la langue actuelle
        if current_lang != "fr":
            localized_field = f"{field}_{current_lang}"
            if localized_field in data:
                try:
                    if isinstance(data[localized_field], str):
                        return json.loads(data[localized_field])
                    elif isinstance(data[localized_field], list):
                        return data[localized_field]
                except:
                    pass
        
        # Fallback vers le champ de base
        if field in data:
            try:
                if isinstance(data[field], str):
                    return json.loads(data[field])
                elif isinstance(data[field], list):
                    return data[field]
            except:
                pass
        
        return []
    
    @staticmethod
    def format_date(date_obj: Union[datetime, str], format_type: str = "medium") -> str:
        """
        Formater une date selon la langue actuelle
        
        Args:
            date_obj: Date à formater
            format_type: Type de format (short, medium, long, relative)
            
        Returns:
            Date formatée
        """
        if isinstance(date_obj, str):
            try:
                date_obj = datetime.fromisoformat(date_obj.replace('Z', '+00:00'))
            except:
                return date_obj
        
        if not isinstance(date_obj, datetime):
            return str(date_obj)
        
        current_lang = i18n.get_language()
        
        if format_type == "relative":
            return TranslationHelper.get_relative_time(date_obj)
        
        # Formats par langue
        if current_lang == "fr":
            formats = {
                "short": "%d/%m/%Y",
                "medium": "%d %B %Y",
                "long": "%A %d %B %Y"
            }
        elif current_lang == "en":
            formats = {
                "short": "%m/%d/%Y",
                "medium": "%B %d, %Y",
                "long": "%A, %B %d, %Y"
            }
        elif current_lang == "ar":
            formats = {
                "short": "%d/%m/%Y",
                "medium": "%d %B %Y",
                "long": "%A %d %B %Y"
            }
        else:
            formats = {
                "short": "%Y-%m-%d",
                "medium": "%B %d, %Y",
                "long": "%A, %B %d, %Y"
            }
        
        try:
            return date_obj.strftime(formats.get(format_type, formats["medium"]))
        except:
            return date_obj.strftime("%Y-%m-%d")
    
    @staticmethod
    def get_relative_time(date_obj: datetime) -> str:
        """
        Obtenir le temps relatif selon la langue actuelle
        
        Args:
            date_obj: Date de référence
            
        Returns:
            Temps relatif traduit
        """
        now = datetime.now()
        if date_obj.tzinfo:
            from datetime import timezone
            now = now.replace(tzinfo=timezone.utc)
        
        diff = now - date_obj
        
        current_lang = i18n.get_language()
        
        if diff.days > 0:
            if current_lang == "fr":
                return f"il y a {diff.days} jour{'s' if diff.days > 1 else ''}"
            elif current_lang == "ar":
                return f"منذ {diff.days} يوم"
            else:  # en
                return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            if current_lang == "fr":
                return f"il y a {hours} heure{'s' if hours > 1 else ''}"
            elif current_lang == "ar":
                return f"منذ {hours} ساعة"
            else:  # en
                return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            if current_lang == "fr":
                return f"il y a {minutes} minute{'s' if minutes > 1 else ''}"
            elif current_lang == "ar":
                return f"منذ {minutes} دقيقة"
            else:  # en
                return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        else:
            if current_lang == "fr":
                return "à l'instant"
            elif current_lang == "ar":
                return "الآن"
            else:  # en
                return "just now"
    
    @staticmethod
    def format_number(number: Union[int, float], format_type: str = "default") -> str:
        """
        Formater un nombre selon la langue actuelle
        
        Args:
            number: Nombre à formater
            format_type: Type de format (default, currency, percentage)
            
        Returns:
            Nombre formaté
        """
        current_lang = i18n.get_language()
        
        if format_type == "percentage":
            if current_lang == "fr":
                return f"{number:.1f} %"
            elif current_lang == "ar":
                return f"٪ {number:.1f}"
            else:  # en
                return f"{number:.1f}%"
        
        # Format par défaut
        if current_lang == "fr":
            return f"{number:,.0f}".replace(',', ' ')
        elif current_lang == "ar":
            return f"{number:,.0f}".replace(',', '،')
        else:  # en
            return f"{number:,.0f}"
    
    @staticmethod
    def get_reading_time_text(minutes: int) -> str:
        """
        Obtenir le texte du temps de lecture selon la langue
        
        Args:
            minutes: Nombre de minutes
            
        Returns:
            Texte traduit du temps de lecture
        """
        current_lang = i18n.get_language()
        
        if current_lang == "fr":
            return f"{minutes} min de lecture"
        elif current_lang == "ar":
            return f"{minutes} دقيقة قراءة"
        else:  # en
            return f"{minutes} min read"
    
    @staticmethod
    def translate_category(category: str, context: str = "articles") -> str:
        """
        Traduire une catégorie selon le contexte
        
        Args:
            category: Catégorie à traduire
            context: Contexte (articles, reports, etc.)
            
        Returns:
            Catégorie traduite
        """
        translation_key = f"{context}.categories.{category}"
        translated = _(translation_key)
        
        # Si la traduction n'existe pas, retourner le texte original capitalisé
        if translated.startswith('[') and translated.endswith(']'):
            return category.replace('_', ' ').title()
        
        return translated
    
    @staticmethod
    def get_error_message(error_key: str, **kwargs) -> str:
        """
        Obtenir un message d'erreur traduit
        
        Args:
            error_key: Clé de l'erreur
            **kwargs: Arguments pour le formatage
            
        Returns:
            Message d'erreur traduit
        """
        return _(f"errors.{error_key}", **kwargs)
    
    @staticmethod
    def create_meta_description(content: str, max_length: int = 160) -> str:
        """
        Créer une meta description dans la langue actuelle
        
        Args:
            content: Contenu source
            max_length: Longueur maximale
            
        Returns:
            Meta description tronquée
        """
        # Nettoyer le HTML
        clean_content = re.sub(r'<[^>]+>', '', content)
        # Nettoyer les espaces multiples
        clean_content = re.sub(r'\s+', ' ', clean_content).strip()
        
        if len(clean_content) <= max_length:
            return clean_content
        
        # Tronquer au mot le plus proche
        truncated = clean_content[:max_length]
        last_space = truncated.rfind(' ')
        
        if last_space > max_length * 0.8:  # Si on peut tronquer proprement
            truncated = truncated[:last_space]
        
        # Ajouter les points de suspension selon la langue
        current_lang = i18n.get_language()
        if current_lang == "ar":
            return truncated + "..."
        else:
            return truncated + "..."

class LocalizedContent:
    """Classe pour gérer du contenu localisé"""
    
    def __init__(self, data: Dict[str, Any]):
        self.data = data
        self.helper = TranslationHelper()
    
    def get_title(self) -> str:
        """Obtenir le titre localisé"""
        return self.helper.get_localized_field(self.data, 'title')
    
    def get_description(self) -> str:
        """Obtenir la description localisée"""
        return self.helper.get_localized_field(self.data, 'description')
    
    def get_summary(self) -> str:
        """Obtenir le résumé localisé"""
        return self.helper.get_localized_field(self.data, 'summary')
    
    def get_content(self) -> str:
        """Obtenir le contenu localisé"""
        return self.helper.get_localized_field(self.data, 'content')
    
    def get_tags(self) -> List[str]:
        """Obtenir les tags localisés"""
        return self.helper.get_localized_list(self.data, 'tags')
    
    def get_formatted_date(self, field: str = 'date', format_type: str = "medium") -> str:
        """Obtenir une date formatée"""
        if field in self.data:
            return self.helper.format_date(self.data[field], format_type)
        return ""
    
    def get_category_translated(self, context: str = "articles") -> str:
        """Obtenir la catégorie traduite"""
        if 'category' in self.data:
            return self.helper.translate_category(self.data['category'], context)
        return ""

class ValidationMessages:
    """Messages de validation traduits"""
    
    @staticmethod
    def required_field(field_name: str) -> str:
        """Message pour champ requis"""
        return _(f"errors.required_field").replace("Ce champ", field_name)
    
    @staticmethod
    def invalid_email() -> str:
        """Message pour email invalide"""
        return _("errors.invalid_email")
    
    @staticmethod
    def invalid_phone() -> str:
        """Message pour téléphone invalide"""
        return _("errors.invalid_phone")
    
    @staticmethod
    def min_length(field_name: str, min_len: int) -> str:
        """Message pour longueur minimale"""
        current_lang = i18n.get_language()
        if current_lang == "fr":
            return f"{field_name} doit contenir au moins {min_len} caractères"
        elif current_lang == "ar":
            return f"يجب أن يحتوي {field_name} على {min_len} أحرف على الأقل"
        else:  # en
            return f"{field_name} must be at least {min_len} characters long"
    
    @staticmethod
    def max_length(field_name: str, max_len: int) -> str:
        """Message pour longueur maximale"""
        current_lang = i18n.get_language()
        if current_lang == "fr":
            return f"{field_name} ne peut pas dépasser {max_len} caractères"
        elif current_lang == "ar":
            return f"لا يمكن أن يتجاوز {field_name} {max_len} حرفاً"
        else:  # en
            return f"{field_name} cannot exceed {max_len} characters"

# Fonctions utilitaires globales
def t(key: str, **kwargs) -> str:
    """Alias court pour la traduction"""
    return _(key, **kwargs)

def tl(data: Dict[str, Any], field: str) -> str:
    """Traduction localisée pour un champ de données"""
    return TranslationHelper.get_localized_field(data, field)

def td(date_obj: Union[datetime, str], format_type: str = "medium") -> str:
    """Traduction de date"""
    return TranslationHelper.format_date(date_obj, format_type)

def tn(number: Union[int, float], format_type: str = "default") -> str:
    """Traduction de nombre"""
    return TranslationHelper.format_number(number, format_type)

def tc(category: str, context: str = "articles") -> str:
    """Traduction de catégorie"""
    return TranslationHelper.translate_category(category, context)

# Décorateur pour les pages avec support de langue
def with_language_support(func):
    """Décorateur pour ajouter le support de langue à une page"""
    def wrapper(*args, **kwargs):
        # Ajouter les classes de langue au body
        current_lang = i18n.get_language()
        direction = i18n.get_language_direction()
        
        # Fonction à exécuter après le rendu
        def apply_language_classes():
            from nicegui import ui
            ui.run_javascript(f"""
                document.documentElement.setAttribute('lang', '{current_lang}');
                document.documentElement.setAttribute('dir', '{direction}');
                document.body.classList.add('{direction}');
                if ('{current_lang}' === 'ar') {{
                    document.body.classList.add('arabic-text');
                }}
            """)
        
        # Exécuter la fonction originale
        result = func(*args, **kwargs)
        
        # Appliquer les classes de langue
        apply_language_classes()
        
        return result
    
    return wrapper

# Classe pour la gestion des formulaires multilingues
class MultilingualForm:
    """Classe pour gérer les formulaires multilingues"""
    
    def __init__(self):
        self.validation_messages = ValidationMessages()
        self.errors = {}
    
    def validate_required(self, value: Any, field_name: str) -> bool:
        """Valider un champ requis"""
        if not value or (isinstance(value, str) and not value.strip()):
            self.errors[field_name] = self.validation_messages.required_field(_(f"form.{field_name}"))
            return False
        return True
    
    def validate_email(self, email: str, field_name: str = "email") -> bool:
        """Valider un email"""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            self.errors[field_name] = self.validation_messages.invalid_email()
            return False
        return True
    
    def validate_length(self, value: str, field_name: str, min_len: int = None, max_len: int = None) -> bool:
        """Valider la longueur d'un champ"""
        if min_len and len(value) < min_len:
            self.errors[field_name] = self.validation_messages.min_length(_(f"form.{field_name}"), min_len)
            return False
        
        if max_len and len(value) > max_len:
            self.errors[field_name] = self.validation_messages.max_length(_(f"form.{field_name}"), max_len)
            return False
        
        return True
    
    def has_errors(self) -> bool:
        """Vérifier s'il y a des erreurs"""
        return len(self.errors) > 0
    
    def get_errors(self) -> Dict[str, str]:
        """Obtenir toutes les erreurs"""
        return self.errors.copy()
    
    def clear_errors(self):
        """Effacer toutes les erreurs"""
        self.errors.clear()

# Export des principales fonctions
__all__ = [
    'TranslationHelper',
    'LocalizedContent', 
    'ValidationMessages',
    'MultilingualForm',
    't', 'tl', 'td', 'tn', 'tc',
    'with_language_support'
]