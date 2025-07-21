"""
Validateurs pour l'application MindCare
"""

import re
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, date
from pathlib import Path
from urllib.parse import urlparse

class ValidationError(Exception):
    """Exception pour les erreurs de validation"""
    def __init__(self, message: str, field: str = None):
        self.message = message
        self.field = field
        super().__init__(self.message)

class ValidationResult:
    """Résultat de validation"""
    def __init__(self, is_valid: bool = True, errors: List[str] = None):
        self.is_valid = is_valid
        self.errors = errors or []
    
    def add_error(self, error: str):
        """Ajouter une erreur"""
        self.errors.append(error)
        self.is_valid = False

class BaseValidator:
    """Classe de base pour les validateurs"""
    
    def __init__(self, required: bool = True, allow_empty: bool = False):
        self.required = required
        self.allow_empty = allow_empty
    
    def validate(self, value: Any, field_name: str = None) -> ValidationResult:
        """Valider une valeur"""
        result = ValidationResult()
        
        # Vérifier si la valeur est requise
        if self.required and (value is None or value == ''):
            result.add_error(f"Le champ {field_name or 'value'} est requis")
            return result
        
        # Si la valeur est vide et autorisée, pas besoin de validation
        if not self.allow_empty and value == '':
            result.add_error(f"Le champ {field_name or 'value'} ne peut pas être vide")
            return result
        
        # Si la valeur est vide mais autorisée, validation réussie
        if value == '' and self.allow_empty:
            return result
        
        # Validation spécifique (à implémenter dans les sous-classes)
        return self._validate_value(value, field_name)
    
    def _validate_value(self, value: Any, field_name: str = None) -> ValidationResult:
        """Validation spécifique à implémenter dans les sous-classes"""
        return ValidationResult()

class StringValidator(BaseValidator):
    """Validateur pour les chaînes de caractères"""
    
    def __init__(self, min_length: int = None, max_length: int = None, 
                 pattern: str = None, choices: List[str] = None, **kwargs):
        super().__init__(**kwargs)
        self.min_length = min_length
        self.max_length = max_length
        self.pattern = pattern
        self.choices = choices
    
    def _validate_value(self, value: Any, field_name: str = None) -> ValidationResult:
        result = ValidationResult()
        
        if not isinstance(value, str):
            result.add_error(f"{field_name or 'Value'} doit être une chaîne de caractères")
            return result
        
        # Vérifier la longueur minimale
        if self.min_length is not None and len(value) < self.min_length:
            result.add_error(f"{field_name or 'Value'} doit contenir au moins {self.min_length} caractères")
        
        # Vérifier la longueur maximale
        if self.max_length is not None and len(value) > self.max_length:
            result.add_error(f"{field_name or 'Value'} ne peut pas dépasser {self.max_length} caractères")
        
        # Vérifier le pattern
        if self.pattern and not re.match(self.pattern, value):
            result.add_error(f"{field_name or 'Value'} ne correspond pas au format attendu")
        
        # Vérifier les choix
        if self.choices and value not in self.choices:
            result.add_error(f"{field_name or 'Value'} doit être l'une des valeurs suivantes: {', '.join(self.choices)}")
        
        return result

class EmailValidator(BaseValidator):
    """Validateur pour les emails"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    def _validate_value(self, value: Any, field_name: str = None) -> ValidationResult:
        result = ValidationResult()
        
        if not isinstance(value, str):
            result.add_error(f"{field_name or 'Email'} doit être une chaîne de caractères")
            return result
        
        if not re.match(self.pattern, value):
            result.add_error(f"{field_name or 'Email'} n'est pas un email valide")
        
        return result

class URLValidator(BaseValidator):
    """Validateur pour les URLs"""
    
    def __init__(self, schemes: List[str] = None, **kwargs):
        super().__init__(**kwargs)
        self.schemes = schemes or ['http', 'https']
    
    def _validate_value(self, value: Any, field_name: str = None) -> ValidationResult:
        result = ValidationResult()
        
        if not isinstance(value, str):
            result.add_error(f"{field_name or 'URL'} doit être une chaîne de caractères")
            return result
        
        try:
            parsed = urlparse(value)
            if not parsed.scheme or not parsed.netloc:
                result.add_error(f"{field_name or 'URL'} n'est pas une URL valide")
            elif parsed.scheme not in self.schemes:
                result.add_error(f"{field_name or 'URL'} doit utiliser un schéma valide ({', '.join(self.schemes)})")
        except Exception:
            result.add_error(f"{field_name or 'URL'} n'est pas une URL valide")
        
        return result

class IntegerValidator(BaseValidator):
    """Validateur pour les entiers"""
    
    def __init__(self, min_value: int = None, max_value: int = None, **kwargs):
        super().__init__(**kwargs)
        self.min_value = min_value
        self.max_value = max_value
    
    def _validate_value(self, value: Any, field_name: str = None) -> ValidationResult:
        result = ValidationResult()
        
        # Essayer de convertir en entier
        try:
            if isinstance(value, str):
                value = int(value)
            elif not isinstance(value, int):
                result.add_error(f"{field_name or 'Value'} doit être un nombre entier")
                return result
        except ValueError:
            result.add_error(f"{field_name or 'Value'} doit être un nombre entier")
            return result
        
        # Vérifier la valeur minimale
        if self.min_value is not None and value < self.min_value:
            result.add_error(f"{field_name or 'Value'} doit être au moins {self.min_value}")
        
        # Vérifier la valeur maximale
        if self.max_value is not None and value > self.max_value:
            result.add_error(f"{field_name or 'Value'} ne peut pas dépasser {self.max_value}")
        
        return result

class FloatValidator(BaseValidator):
    """Validateur pour les nombres à virgule"""
    
    def __init__(self, min_value: float = None, max_value: float = None, **kwargs):
        super().__init__(**kwargs)
        self.min_value = min_value
        self.max_value = max_value
    
    def _validate_value(self, value: Any, field_name: str = None) -> ValidationResult:
        result = ValidationResult()
        
        # Essayer de convertir en float
        try:
            if isinstance(value, str):
                value = float(value)
            elif not isinstance(value, (int, float)):
                result.add_error(f"{field_name or 'Value'} doit être un nombre")
                return result
        except ValueError:
            result.add_error(f"{field_name or 'Value'} doit être un nombre")
            return result
        
        # Vérifier la valeur minimale
        if self.min_value is not None and value < self.min_value:
            result.add_error(f"{field_name or 'Value'} doit être au moins {self.min_value}")
        
        # Vérifier la valeur maximale
        if self.max_value is not None and value > self.max_value:
            result.add_error(f"{field_name or 'Value'} ne peut pas dépasser {self.max_value}")
        
        return result

class DateValidator(BaseValidator):
    """Validateur pour les dates"""
    
    def __init__(self, date_format: str = '%Y-%m-%d', min_date: date = None, 
                 max_date: date = None, **kwargs):
        super().__init__(**kwargs)
        self.date_format = date_format
        self.min_date = min_date
        self.max_date = max_date
    
    def _validate_value(self, value: Any, field_name: str = None) -> ValidationResult:
        result = ValidationResult()
        
        # Convertir en date si nécessaire
        if isinstance(value, str):
            try:
                value = datetime.strptime(value, self.date_format).date()
            except ValueError:
                result.add_error(f"{field_name or 'Date'} doit être au format {self.date_format}")
                return result
        elif isinstance(value, datetime):
            value = value.date()
        elif not isinstance(value, date):
            result.add_error(f"{field_name or 'Date'} doit être une date")
            return result
        
        # Vérifier la date minimale
        if self.min_date and value < self.min_date:
            result.add_error(f"{field_name or 'Date'} ne peut pas être antérieure au {self.min_date}")
        
        # Vérifier la date maximale
        if self.max_date and value > self.max_date:
            result.add_error(f"{field_name or 'Date'} ne peut pas être postérieure au {self.max_date}")
        
        return result

class ListValidator(BaseValidator):
    """Validateur pour les listes"""
    
    def __init__(self, item_validator: BaseValidator = None, min_items: int = None, 
                 max_items: int = None, **kwargs):
        super().__init__(**kwargs)
        self.item_validator = item_validator
        self.min_items = min_items
        self.max_items = max_items
    
    def _validate_value(self, value: Any, field_name: str = None) -> ValidationResult:
        result = ValidationResult()
        
        if not isinstance(value, list):
            result.add_error(f"{field_name or 'Value'} doit être une liste")
            return result
        
        # Vérifier le nombre minimum d'éléments
        if self.min_items is not None and len(value) < self.min_items:
            result.add_error(f"{field_name or 'List'} doit contenir au moins {self.min_items} élément(s)")
        
        # Vérifier le nombre maximum d'éléments
        if self.max_items is not None and len(value) > self.max_items:
            result.add_error(f"{field_name or 'List'} ne peut pas contenir plus de {self.max_items} élément(s)")
        
        # Valider chaque élément si un validateur est fourni
        if self.item_validator:
            for i, item in enumerate(value):
                item_result = self.item_validator.validate(item, f"{field_name or 'Item'}[{i}]")
                if not item_result.is_valid:
                    result.errors.extend(item_result.errors)
                    result.is_valid = False
        
        return result

class DictValidator(BaseValidator):
    """Validateur pour les dictionnaires"""
    
    def __init__(self, schema: Dict[str, BaseValidator] = None, **kwargs):
        super().__init__(**kwargs)
        self.schema = schema or {}
    
    def _validate_value(self, value: Any, field_name: str = None) -> ValidationResult:
        result = ValidationResult()
        
        if not isinstance(value, dict):
            result.add_error(f"{field_name or 'Value'} doit être un dictionnaire")
            return result
        
        # Valider chaque champ selon le schéma
        for key, validator in self.schema.items():
            field_value = value.get(key)
            field_result = validator.validate(field_value, key)
            if not field_result.is_valid:
                result.errors.extend(field_result.errors)
                result.is_valid = False
        
        return result

class FileValidator(BaseValidator):
    """Validateur pour les fichiers"""
    
    def __init__(self, allowed_extensions: List[str] = None, max_size: int = None, 
                 min_size: int = None, **kwargs):
        super().__init__(**kwargs)
        self.allowed_extensions = allowed_extensions or []
        self.max_size = max_size  # en bytes
        self.min_size = min_size  # en bytes
    
    def _validate_value(self, value: Any, field_name: str = None) -> ValidationResult:
        result = ValidationResult()
        
        # Vérifier le type de fichier (pour FastAPI UploadFile)
        if hasattr(value, 'filename') and hasattr(value, 'size'):
            filename = value.filename
            size = value.size
        elif isinstance(value, str):
            # Si c'est un chemin de fichier
            file_path = Path(value)
            if not file_path.exists():
                result.add_error(f"Le fichier {field_name or 'file'} n'existe pas")
                return result
            filename = file_path.name
            size = file_path.stat().st_size
        else:
            result.add_error(f"{field_name or 'File'} doit être un fichier valide")
            return result
        
        # Vérifier l'extension
        if self.allowed_extensions:
            extension = Path(filename).suffix.lower()
            if extension not in self.allowed_extensions:
                result.add_error(f"L'extension {extension} n'est pas autorisée. Extensions autorisées: {', '.join(self.allowed_extensions)}")
        
        # Vérifier la taille
        if self.max_size and size > self.max_size:
            result.add_error(f"Le fichier {field_name or 'file'} est trop volumineux (max: {self.max_size} bytes)")
        
        if self.min_size and size < self.min_size:
            result.add_error(f"Le fichier {field_name or 'file'} est trop petit (min: {self.min_size} bytes)")
        
        return result

class PhoneValidator(BaseValidator):
    """Validateur pour les numéros de téléphone"""
    
    def __init__(self, country_code: str = 'MA', **kwargs):
        super().__init__(**kwargs)
        self.country_code = country_code
        
        # Patterns pour différents pays
        self.patterns = {
            'MA': r'^(\+212|0)[5-7]\d{8}$',  # Maroc
            'FR': r'^(\+33|0)[1-9]\d{8}$',   # France
            'US': r'^(\+1)?[2-9]\d{2}[2-9]\d{2}\d{4}$',  # USA
        }
    
    def _validate_value(self, value: Any, field_name: str = None) -> ValidationResult:
        result = ValidationResult()
        
        if not isinstance(value, str):
            result.add_error(f"{field_name or 'Phone'} doit être une chaîne de caractères")
            return result
        
        # Nettoyer le numéro (enlever les espaces et tirets)
        clean_phone = re.sub(r'[\s-]', '', value)
        
        # Vérifier le pattern selon le pays
        pattern = self.patterns.get(self.country_code, self.patterns['MA'])
        if not re.match(pattern, clean_phone):
            result.add_error(f"{field_name or 'Phone'} n'est pas un numéro de téléphone valide pour {self.country_code}")
        
        return result

class PasswordValidator(BaseValidator):
    """Validateur pour les mots de passe"""
    
    def __init__(self, min_length: int = 8, require_uppercase: bool = True,
                 require_lowercase: bool = True, require_digit: bool = True,
                 require_special: bool = True, **kwargs):
        super().__init__(**kwargs)
        self.min_length = min_length
        self.require_uppercase = require_uppercase
        self.require_lowercase = require_lowercase
        self.require_digit = require_digit
        self.require_special = require_special
    
    def _validate_value(self, value: Any, field_name: str = None) -> ValidationResult:
        result = ValidationResult()
        
        if not isinstance(value, str):
            result.add_error(f"{field_name or 'Password'} doit être une chaîne de caractères")
            return result
        
        # Vérifier la longueur
        if len(value) < self.min_length:
            result.add_error(f"{field_name or 'Password'} doit contenir au moins {self.min_length} caractères")
        
        # Vérifier la présence de majuscules
        if self.require_uppercase and not re.search(r'[A-Z]', value):
            result.add_error(f"{field_name or 'Password'} doit contenir au moins une majuscule")
        
        # Vérifier la présence de minuscules
        if self.require_lowercase and not re.search(r'[a-z]', value):
            result.add_error(f"{field_name or 'Password'} doit contenir au moins une minuscule")
        
        # Vérifier la présence de chiffres
        if self.require_digit and not re.search(r'\d', value):
            result.add_error(f"{field_name or 'Password'} doit contenir au moins un chiffre")
        
        # Vérifier la présence de caractères spéciaux
        if self.require_special and not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            result.add_error(f"{field_name or 'Password'} doit contenir au moins un caractère spécial")
        
        return result

class SlugValidator(BaseValidator):
    """Validateur pour les slugs"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pattern = r'^[a-z0-9]+(?:-[a-z0-9]+)*$'
    
    def _validate_value(self, value: Any, field_name: str = None) -> ValidationResult:
        result = ValidationResult()
        
        if not isinstance(value, str):
            result.add_error(f"{field_name or 'Slug'} doit être une chaîne de caractères")
            return result
        
        if not re.match(self.pattern, value):
            result.add_error(f"{field_name or 'Slug'} doit contenir seulement des lettres minuscules, des chiffres et des tirets")
        
        return result

class JSONValidator(BaseValidator):
    """Validateur pour les chaînes JSON"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def _validate_value(self, value: Any, field_name: str = None) -> ValidationResult:
        result = ValidationResult()
        
        if not isinstance(value, str):
            result.add_error(f"{field_name or 'JSON'} doit être une chaîne de caractères")
            return result
        
        try:
            import json
            json.loads(value)
        except json.JSONDecodeError:
            result.add_error(f"{field_name or 'JSON'} n'est pas un JSON valide")
        
        return result

class RegexValidator(BaseValidator):
    """Validateur basé sur une expression régulière"""
    
    def __init__(self, pattern: str, message: str = None, **kwargs):
        super().__init__(**kwargs)
        self.pattern = pattern
        self.message = message or f"La valeur ne correspond pas au pattern {pattern}"
    
    def _validate_value(self, value: Any, field_name: str = None) -> ValidationResult:
        result = ValidationResult()
        
        if not isinstance(value, str):
            result.add_error(f"{field_name or 'Value'} doit être une chaîne de caractères")
            return result
        
        if not re.match(self.pattern, value):
            result.add_error(self.message)
        
        return result

class FormValidator:
    """Validateur pour les formulaires complets"""
    
    def __init__(self, schema: Dict[str, BaseValidator]):
        self.schema = schema
    
    def validate(self, data: Dict[str, Any]) -> ValidationResult:
        """Valider un formulaire complet"""
        result = ValidationResult()
        
        for field_name, validator in self.schema.items():
            field_value = data.get(field_name)
            field_result = validator.validate(field_value, field_name)
            
            if not field_result.is_valid:
                result.errors.extend(field_result.errors)
                result.is_valid = False
        
        return result
    
    def validate_and_raise(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Valider et lever une exception si erreur"""
        result = self.validate(data)
        
        if not result.is_valid:
            raise ValidationError('; '.join(result.errors))
        
        return data

# Validateurs prédéfinis pour MindCare
class MindCareValidators:
    """Validateurs spécifiques à MindCare"""
    
    # Validateur pour les articles
    ARTICLE_VALIDATOR = FormValidator({
        'title': StringValidator(min_length=10, max_length=200, required=True),
        'summary': StringValidator(min_length=50, max_length=500, required=True),
        'content': StringValidator(min_length=200, required=True),
        'category': StringValidator(choices=['anxiety', 'depression', 'stress', 'wellness', 'therapy', 'mindfulness'], required=True),
        'author': StringValidator(min_length=2, max_length=100, required=True),
        'tags': ListValidator(item_validator=StringValidator(min_length=2, max_length=50), min_items=1, max_items=10),
        'read_time': IntegerValidator(min_value=1, max_value=120),
        'featured': StringValidator(choices=['true', 'false'], required=False),
        'published': StringValidator(choices=['true', 'false'], required=False),
    })
    
    # Validateur pour les rapports
    REPORT_VALIDATOR = FormValidator({
        'title': StringValidator(min_length=10, max_length=200, required=True),
        'description': StringValidator(min_length=50, max_length=1000, required=True),
        'type': StringValidator(choices=['research', 'survey', 'analysis', 'white_paper'], required=True),
        'author': StringValidator(min_length=2, max_length=100, required=True),
        'pages': IntegerValidator(min_value=1, max_value=1000),
        'file_size': StringValidator(pattern=r'^\d+(\.\d+)?\s*(KB|MB|GB)$'),
        'tags': ListValidator(item_validator=StringValidator(min_length=2, max_length=50), min_items=1, max_items=10),
        'featured': StringValidator(choices=['true', 'false'], required=False),
        'published': StringValidator(choices=['true', 'false'], required=False),
    })
    
    # Validateur pour les contacts
    CONTACT_VALIDATOR = FormValidator({
        'name': StringValidator(min_length=2, max_length=100, required=True),
        'email': EmailValidator(required=True),
        'subject': StringValidator(min_length=5, max_length=200, required=True),
        'message': StringValidator(min_length=20, max_length=2000, required=True),
    })
    
    # Validateur pour les utilisateurs
    USER_VALIDATOR = FormValidator({
        'email': EmailValidator(required=True),
        'username': StringValidator(min_length=3, max_length=50, pattern=r'^[a-zA-Z0-9_]+$'),
        'full_name': StringValidator(min_length=2, max_length=100, required=True),
        'password': PasswordValidator(min_length=8, required=True),
        'preferred_language': StringValidator(choices=['fr', 'en', 'ar'], required=False),
        'preferred_theme': StringValidator(choices=['light', 'dark'], required=False),
    })
    
    # Validateur pour les commentaires
    COMMENT_VALIDATOR = FormValidator({
        'content': StringValidator(min_length=10, max_length=500, required=True),
        'author_name': StringValidator(min_length=2, max_length=100, required=True),
        'author_email': EmailValidator(required=True),
    })

# Fonctions utilitaires pour la validation
def validate_file_upload(file, max_size: int = 10 * 1024 * 1024, 
                        allowed_extensions: List[str] = None) -> ValidationResult:
    """Valider un upload de fichier"""
    validator = FileValidator(
        max_size=max_size,
        allowed_extensions=allowed_extensions or ['.jpg', '.jpeg', '.png', '.gif', '.pdf', '.doc', '.docx']
    )
    return validator.validate(file, 'file')

def validate_pagination_params(page: int, per_page: int, max_per_page: int = 100) -> ValidationResult:
    """Valider les paramètres de pagination"""
    result = ValidationResult()
    
    if page < 1:
        result.add_error("Le numéro de page doit être au moins 1")
    
    if per_page < 1:
        result.add_error("Le nombre d'éléments par page doit être au moins 1")
    
    if per_page > max_per_page:
        result.add_error(f"Le nombre d'éléments par page ne peut pas dépasser {max_per_page}")
    
    return result

def validate_search_query(query: str, min_length: int = 2, max_length: int = 100) -> ValidationResult:
    """Valider une requête de recherche"""
    validator = StringValidator(min_length=min_length, max_length=max_length)
    return validator.validate(query, 'search_query')

def validate_api_key(api_key: str) -> ValidationResult:
    """Valider une clé API"""
    validator = RegexValidator(
        pattern=r'^[a-zA-Z0-9]{32,}$',
        message="La clé API doit contenir au moins 32 caractères alphanumériques"
    )
    return validator.validate(api_key, 'api_key')

def validate_language_code(lang_code: str) -> ValidationResult:
    """Valider un code de langue"""
    validator = StringValidator(choices=['fr', 'en', 'ar'])
    return validator.validate(lang_code, 'language')

def validate_theme_name(theme: str) -> ValidationResult:
    """Valider un nom de thème"""
    validator = StringValidator(choices=['light', 'dark'])
    return validator.validate(theme, 'theme')

# Décorateur pour valider les paramètres de fonction
def validate_params(**validators):
    """Décorateur pour valider les paramètres d'une fonction"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Valider les paramètres nommés
            for param_name, validator in validators.items():
                if param_name in kwargs:
                    result = validator.validate(kwargs[param_name], param_name)
                    if not result.is_valid:
                        raise ValidationError(f"Paramètre {param_name}: {'; '.join(result.errors)}")
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Fonction pour créer un validateur conditionnel
def conditional_validator(condition_func, validator_if_true, validator_if_false=None):
    """Créer un validateur conditionnel"""
    class ConditionalValidator(BaseValidator):
        def _validate_value(self, value: Any, field_name: str = None) -> ValidationResult:
            if condition_func(value):
                return validator_if_true.validate(value, field_name)
            elif validator_if_false:
                return validator_if_false.validate(value, field_name)
            else:
                return ValidationResult()
    
    return ConditionalValidator()

# Exemple d'utilisation
if __name__ == "__main__":
    # Test des validateurs
    
    # Valider un email
    email_validator = EmailValidator()
    result = email_validator.validate("test@example.com")
    print(f"Email valide: {result.is_valid}")
    
    # Valider un article
    article_data = {
        'title': 'Comment gérer le stress au travail',
        'summary': 'Un guide pratique pour apprendre à gérer le stress dans un environnement professionnel.',
        'content': 'Le stress au travail est un problème courant qui peut affecter notre productivité et notre bien-être. Voici quelques stratégies efficaces...',
        'category': 'stress',
        'author': 'Dr. Marie Dubois',
        'tags': ['stress', 'travail', 'gestion'],
        'read_time': 8,
        'featured': 'false',
        'published': 'true'
    }
    
    try:
        validated_data = MindCareValidators.ARTICLE_VALIDATOR.validate_and_raise(article_data)
        print("Article valide:", validated_data['title'])
    except ValidationError as e:
        print(f"Erreur de validation: {e.message}")
    
    # Test d'un mot de passe
    password_validator = PasswordValidator()
    password_result = password_validator.validate("MonMotDePasse123!")
    print(f"Mot de passe valide: {password_result.is_valid}")
    if not password_result.is_valid:
        print("Erreurs:", password_result.errors)