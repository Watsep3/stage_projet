"""
Fonctions utilitaires pour l'application MindCare
"""

import re
import json
import hashlib
import secrets
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from pathlib import Path
import unicodedata
from urllib.parse import urlparse, quote
import base64

def slugify(text: str) -> str:
    """
    Convertir un texte en slug URL-friendly
    
    Args:
        text: Texte à convertir
        
    Returns:
        Slug générée
    """
    # Normaliser les caractères unicode
    text = unicodedata.normalize('NFKD', text)
    
    # Enlever les accents
    text = ''.join(c for c in text if not unicodedata.combining(c))
    
    # Convertir en minuscules
    text = text.lower()
    
    # Remplacer les espaces et caractères spéciaux par des tirets
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    
    # Enlever les tirets en début et fin
    text = text.strip('-')
    
    return text

def generate_unique_id(prefix: str = "") -> str:
    """
    Générer un ID unique
    
    Args:
        prefix: Préfixe optionnel
        
    Returns:
        ID unique
    """
    unique_id = str(uuid.uuid4())
    if prefix:
        return f"{prefix}_{unique_id}"
    return unique_id

def generate_secure_token(length: int = 32) -> str:
    """
    Générer un token sécurisé
    
    Args:
        length: Longueur du token
        
    Returns:
        Token sécurisé
    """
    return secrets.token_urlsafe(length)

def hash_password(password: str) -> str:
    """
    Hasher un mot de passe
    
    Args:
        password: Mot de passe en clair
        
    Returns:
        Hash du mot de passe
    """
    # Utiliser bcrypt en production
    salt = secrets.token_hex(16)
    pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
    return salt + pwdhash.hex()

def verify_password(password: str, hashed: str) -> bool:
    """
    Vérifier un mot de passe
    
    Args:
        password: Mot de passe en clair
        hashed: Hash stocké
        
    Returns:
        True si le mot de passe est correct
    """
    salt = hashed[:32]
    stored_hash = hashed[32:]
    pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
    return pwdhash.hex() == stored_hash

def sanitize_html(text: str) -> str:
    """
    Nettoyer le HTML pour éviter les injections
    
    Args:
        text: Texte à nettoyer
        
    Returns:
        Texte nettoyé
    """
    # Remplacer les caractères HTML dangereux
    replacements = {
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#x27;',
        '&': '&amp;'
    }
    
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    
    return text

def validate_email(email: str) -> bool:
    """
    Valider une adresse email
    
    Args:
        email: Adresse email
        
    Returns:
        True si l'email est valide
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_url(url: str) -> bool:
    """
    Valider une URL
    
    Args:
        url: URL à valider
        
    Returns:
        True si l'URL est valide
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Tronquer un texte
    
    Args:
        text: Texte à tronquer
        max_length: Longueur maximale
        suffix: Suffixe à ajouter
        
    Returns:
        Texte tronqué
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix

def extract_text_preview(text: str, max_words: int = 30) -> str:
    """
    Extraire un aperçu de texte
    
    Args:
        text: Texte complet
        max_words: Nombre maximum de mots
        
    Returns:
        Aperçu du texte
    """
    words = text.split()
    if len(words) <= max_words:
        return text
    
    return ' '.join(words[:max_words]) + '...'

def calculate_reading_time(text: str, wpm: int = 200) -> int:
    """
    Calculer le temps de lecture
    
    Args:
        text: Texte à analyser
        wpm: Mots par minute (défaut: 200)
        
    Returns:
        Temps de lecture en minutes
    """
    word_count = len(text.split())
    reading_time = max(1, round(word_count / wpm))
    return reading_time

def format_file_size(size_bytes: int) -> str:
    """
    Formater la taille d'un fichier
    
    Args:
        size_bytes: Taille en bytes
        
    Returns:
        Taille formatée
    """
    if size_bytes == 0:
        return "0 B"
    
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    i = 0
    
    while size_bytes >= 1024 and i < len(units) - 1:
        size_bytes /= 1024
        i += 1
    
    return f"{size_bytes:.1f} {units[i]}"

def format_number(number: Union[int, float], locale: str = 'fr') -> str:
    """
    Formater un nombre selon la locale
    
    Args:
        number: Nombre à formater
        locale: Locale (fr, en, ar)
        
    Returns:
        Nombre formaté
    """
    if locale == 'fr':
        return f"{number:,.0f}".replace(',', ' ')
    elif locale == 'ar':
        return f"{number:,.0f}".replace(',', '،')
    else:  # en
        return f"{number:,.0f}"

def format_date(date: datetime, format_type: str = 'medium', locale: str = 'fr') -> str:
    """
    Formater une date
    
    Args:
        date: Date à formater
        format_type: Type de format (short, medium, long)
        locale: Locale
        
    Returns:
        Date formatée
    """
    if locale == 'fr':
        if format_type == 'short':
            return date.strftime('%d/%m/%Y')
        elif format_type == 'medium':
            return date.strftime('%d %B %Y')
        else:  # long
            return date.strftime('%A %d %B %Y')
    elif locale == 'ar':
        if format_type == 'short':
            return date.strftime('%d/%m/%Y')
        else:
            return date.strftime('%d %B %Y')
    else:  # en
        if format_type == 'short':
            return date.strftime('%m/%d/%Y')
        elif format_type == 'medium':
            return date.strftime('%B %d, %Y')
        else:  # long
            return date.strftime('%A, %B %d, %Y')

def get_relative_time(date: datetime, locale: str = 'fr') -> str:
    """
    Obtenir le temps relatif
    
    Args:
        date: Date de référence
        locale: Locale
        
    Returns:
        Temps relatif
    """
    now = datetime.now()
    diff = now - date
    
    if diff.days > 0:
        if locale == 'fr':
            return f"il y a {diff.days} jour{'s' if diff.days > 1 else ''}"
        elif locale == 'ar':
            return f"منذ {diff.days} يوم"
        else:  # en
            return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        if locale == 'fr':
            return f"il y a {hours} heure{'s' if hours > 1 else ''}"
        elif locale == 'ar':
            return f"منذ {hours} ساعة"
        else:  # en
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        if locale == 'fr':
            return f"il y a {minutes} minute{'s' if minutes > 1 else ''}"
        elif locale == 'ar':
            return f"منذ {minutes} دقيقة"
        else:  # en
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
    else:
        if locale == 'fr':
            return "à l'instant"
        elif locale == 'ar':
            return "الآن"
        else:  # en
            return "just now"

def parse_tags(tags_string: str) -> List[str]:
    """
    Parser une chaîne de tags
    
    Args:
        tags_string: Chaîne contenant les tags
        
    Returns:
        Liste des tags
    """
    try:
        # Essayer de parser comme JSON
        if tags_string.startswith('['):
            return json.loads(tags_string)
        
        # Sinon, diviser par des virgules
        tags = [tag.strip() for tag in tags_string.split(',')]
        return [tag for tag in tags if tag]
    except:
        return []

def tags_to_string(tags: List[str]) -> str:
    """
    Convertir une liste de tags en chaîne JSON
    
    Args:
        tags: Liste des tags
        
    Returns:
        Chaîne JSON
    """
    return json.dumps(tags, ensure_ascii=False)

def create_breadcrumb(path: str) -> List[Dict[str, str]]:
    """
    Créer un fil d'Ariane
    
    Args:
        path: Chemin URL
        
    Returns:
        Liste des éléments du breadcrumb
    """
    parts = path.strip('/').split('/')
    breadcrumb = [{'name': 'Accueil', 'url': '/'}]
    
    current_path = ''
    for part in parts:
        if part:
            current_path += f'/{part}'
            breadcrumb.append({
                'name': part.replace('-', ' ').title(),
                'url': current_path
            })
    
    return breadcrumb

def generate_meta_description(content: str, max_length: int = 160) -> str:
    """
    Générer une meta description
    
    Args:
        content: Contenu source
        max_length: Longueur maximale
        
    Returns:
        Meta description
    """
    # Enlever les balises HTML
    content = re.sub(r'<[^>]+>', '', content)
    
    # Nettoyer et tronquer
    content = ' '.join(content.split())
    return truncate_text(content, max_length)

def generate_sitemap_entry(url: str, lastmod: datetime = None, changefreq: str = 'monthly', priority: float = 0.5) -> Dict[str, Any]:
    """
    Générer une entrée de sitemap
    
    Args:
        url: URL de la page
        lastmod: Date de dernière modification
        changefreq: Fréquence de changement
        priority: Priorité
        
    Returns:
        Entrée de sitemap
    """
    entry = {
        'url': url,
        'changefreq': changefreq,
        'priority': priority
    }
    
    if lastmod:
        entry['lastmod'] = lastmod.strftime('%Y-%m-%d')
    
    return entry

def encode_base64(data: str) -> str:
    """
    Encoder en base64
    
    Args:
        data: Données à encoder
        
    Returns:
        Données encodées
    """
    return base64.b64encode(data.encode('utf-8')).decode('utf-8')

def decode_base64(data: str) -> str:
    """
    Décoder du base64
    
    Args:
        data: Données encodées
        
    Returns:
        Données décodées
    """
    return base64.b64decode(data).decode('utf-8')

def is_mobile_user_agent(user_agent: str) -> bool:
    """
    Détecter si l'user agent est mobile
    
    Args:
        user_agent: User agent du navigateur
        
    Returns:
        True si mobile
    """
    mobile_patterns = [
        r'Mobile', r'Android', r'iPhone', r'iPad', r'iPod',
        r'BlackBerry', r'Windows Phone', r'Opera Mini'
    ]
    
    for pattern in mobile_patterns:
        if re.search(pattern, user_agent, re.IGNORECASE):
            return True
    
    return False

def get_client_ip(request) -> str:
    """
    Obtenir l'IP du client
    
    Args:
        request: Objet request
        
    Returns:
        Adresse IP
    """
    # Vérifier les headers de proxy
    forwarded_for = request.headers.get('X-Forwarded-For')
    if forwarded_for:
        return forwarded_for.split(',')[0].strip()
    
    real_ip = request.headers.get('X-Real-IP')
    if real_ip:
        return real_ip
    
    return request.client.host if hasattr(request, 'client') else '127.0.0.1'

def create_error_response(message: str, code: int = 400, details: Dict = None) -> Dict[str, Any]:
    """
    Créer une réponse d'erreur standardisée
    
    Args:
        message: Message d'erreur
        code: Code d'erreur
        details: Détails supplémentaires
        
    Returns:
        Réponse d'erreur
    """
    response = {
        'error': True,
        'message': message,
        'code': code,
        'timestamp': datetime.now().isoformat()
    }
    
    if details:
        response['details'] = details
    
    return response

def create_success_response(data: Any = None, message: str = "Success") -> Dict[str, Any]:
    """
    Créer une réponse de succès standardisée
    
    Args:
        data: Données à retourner
        message: Message de succès
        
    Returns:
        Réponse de succès
    """
    response = {
        'error': False,
        'message': message,
        'timestamp': datetime.now().isoformat()
    }
    
    if data is not None:
        response['data'] = data
    
    return response

def paginate_results(items: List[Any], page: int = 1, per_page: int = 10) -> Dict[str, Any]:
    """
    Paginer des résultats
    
    Args:
        items: Liste des éléments
        page: Numéro de page
        per_page: Éléments par page
        
    Returns:
        Résultats paginés
    """
    total = len(items)
    start = (page - 1) * per_page
    end = start + per_page
    
    return {
        'items': items[start:end],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': (total + per_page - 1) // per_page,
            'has_next': end < total,
            'has_prev': page > 1
        }
    }

def filter_dict_by_keys(data: Dict[str, Any], allowed_keys: List[str]) -> Dict[str, Any]:
    """
    Filtrer un dictionnaire par clés autorisées
    
    Args:
        data: Dictionnaire source
        allowed_keys: Clés autorisées
        
    Returns:
        Dictionnaire filtré
    """
    return {key: value for key, value in data.items() if key in allowed_keys}

def deep_merge_dicts(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
    """
    Fusionner deux dictionnaires en profondeur
    
    Args:
        dict1: Premier dictionnaire
        dict2: Deuxième dictionnaire
        
    Returns:
        Dictionnaire fusionné
    """
    result = dict1.copy()
    
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge_dicts(result[key], value)
        else:
            result[key] = value
    
    return result

def load_json_file(file_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Charger un fichier JSON
    
    Args:
        file_path: Chemin du fichier
        
    Returns:
        Contenu du fichier
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

def save_json_file(data: Dict[str, Any], file_path: Union[str, Path]) -> bool:
    """
    Sauvegarder un fichier JSON
    
    Args:
        data: Données à sauvegarder
        file_path: Chemin du fichier
        
    Returns:
        True si réussi
    """
    try:
        # Créer le dossier parent s'il n'existe pas
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Erreur lors de la sauvegarde: {e}")
        return False

def get_file_extension(filename: str) -> str:
    """
    Obtenir l'extension d'un fichier
    
    Args:
        filename: Nom du fichier
        
    Returns:
        Extension du fichier
    """
    return Path(filename).suffix.lower()

def is_allowed_file(filename: str, allowed_extensions: List[str]) -> bool:
    """
    Vérifier si un fichier est autorisé
    
    Args:
        filename: Nom du fichier
        allowed_extensions: Extensions autorisées
        
    Returns:
        True si autorisé
    """
    extension = get_file_extension(filename)
    return extension in allowed_extensions

def generate_secure_filename(filename: str) -> str:
    """
    Générer un nom de fichier sécurisé
    
    Args:
        filename: Nom original
        
    Returns:
        Nom sécurisé
    """
    # Garder seulement le nom et l'extension
    name = Path(filename).stem
    extension = Path(filename).suffix
    
    # Nettoyer le nom
    name = slugify(name)
    
    # Ajouter un timestamp pour éviter les collisions
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    return f"{name}_{timestamp}{extension}"

def create_cache_key(*args) -> str:
    """
    Créer une clé de cache
    
    Args:
        *args: Arguments à utiliser pour la clé
        
    Returns:
        Clé de cache
    """
    key_string = '_'.join(str(arg) for arg in args)
    return hashlib.md5(key_string.encode()).hexdigest()

def rate_limit_key(identifier: str, action: str) -> str:
    """
    Créer une clé pour le rate limiting
    
    Args:
        identifier: Identifiant (IP, user_id, etc.)
        action: Action effectuée
        
    Returns:
        Clé de rate limiting
    """
    return f"rate_limit:{action}:{identifier}"

def extract_keywords(text: str, max_keywords: int = 10) -> List[str]:
    """
    Extraire des mots-clés d'un texte
    
    Args:
        text: Texte à analyser
        max_keywords: Nombre maximum de mots-clés
        
    Returns:
        Liste des mots-clés
    """
    # Mots vides à ignorer
    stop_words = {
        'fr': ['le', 'de', 'et', 'à', 'un', 'il', 'être', 'et', 'en', 'avoir', 'que', 'pour', 'dans', 'ce', 'son', 'une', 'sur', 'avec', 'ne', 'se', 'pas', 'tout', 'plus', 'par', 'grand', 'ou', 'mais', 'du', 'des', 'la', 'les', 'au', 'aux', 'qui', 'comme', 'aussi', 'donc', 'alors', 'où', 'quand', 'comment', 'pourquoi'],
        'en': ['the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'between', 'among', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those', 'a', 'an'],
        'ar': ['في', 'من', 'إلى', 'على', 'أن', 'هذا', 'هذه', 'التي', 'الذي', 'مع', 'كل', 'عن', 'أو', 'كان', 'يكون', 'ما', 'لا', 'قد', 'أم', 'أما', 'بل', 'لكن', 'غير', 'سوى', 'خلا', 'عدا', 'حاشا']
    }
    
    # Nettoyer le texte
    text = re.sub(r'[^\w\s]', '', text.lower())
    words = text.split()
    
    # Filtrer les mots vides
    all_stop_words = set()
    for lang_stops in stop_words.values():
        all_stop_words.update(lang_stops)
    
    keywords = [word for word in words if len(word) > 2 and word not in all_stop_words]
    
    # Compter les fréquences
    word_freq = {}
    for word in keywords:
        word_freq[word] = word_freq.get(word, 0) + 1
    
    # Trier par fréquence
    sorted_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    
    return [word for word, freq in sorted_keywords[:max_keywords]]

def generate_search_query(keywords: List[str]) -> str:
    """
    Générer une requête de recherche
    
    Args:
        keywords: Liste des mots-clés
        
    Returns:
        Requête de recherche
    """
    return ' '.join(keywords)

def calculate_similarity(text1: str, text2: str) -> float:
    """
    Calculer la similitude entre deux textes
    
    Args:
        text1: Premier texte
        text2: Deuxième texte
        
    Returns:
        Score de similitude (0-1)
    """
    # Méthode simple basée sur les mots communs
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    if not union:
        return 0.0
    
    return len(intersection) / len(union)

def generate_color_from_string(string: str) -> str:
    """
    Générer une couleur à partir d'une chaîne
    
    Args:
        string: Chaîne source
        
    Returns:
        Couleur hexadécimale
    """
    hash_value = hashlib.md5(string.encode()).hexdigest()
    return f"#{hash_value[:6]}"

def is_dark_color(hex_color: str) -> bool:
    """
    Déterminer si une couleur est sombre
    
    Args:
        hex_color: Couleur hexadécimale
        
    Returns:
        True si la couleur est sombre
    """
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    brightness = sum(rgb) / 3
    return brightness < 128

def get_contrast_color(hex_color: str) -> str:
    """
    Obtenir une couleur contrastée
    
    Args:
        hex_color: Couleur de base
        
    Returns:
        Couleur contrastée
    """
    return '#ffffff' if is_dark_color(hex_color) else '#000000'

def compress_json(data: Dict[str, Any]) -> str:
    """
    Compresser des données JSON
    
    Args:
        data: Données à compresser
        
    Returns:
        JSON compressé
    """
    import gzip
    import base64
    
    json_str = json.dumps(data, separators=(',', ':'))
    compressed = gzip.compress(json_str.encode('utf-8'))
    return base64.b64encode(compressed).decode('utf-8')

def decompress_json(compressed_data: str) -> Dict[str, Any]:
    """
    Décompresser des données JSON
    
    Args:
        compressed_data: Données compressées
        
    Returns:
        Données décompressées
    """
    import gzip
    import base64
    
    try:
        compressed_bytes = base64.b64decode(compressed_data)
        decompressed = gzip.decompress(compressed_bytes)
        return json.loads(decompressed.decode('utf-8'))
    except Exception:
        return {}

def get_system_info() -> Dict[str, Any]:
    """
    Obtenir des informations système
    
    Returns:
        Informations système
    """
    import platform
    import sys
    
    return {
        'platform': platform.system(),
        'platform_version': platform.version(),
        'python_version': sys.version,
        'architecture': platform.architecture()[0],
        'processor': platform.processor(),
        'hostname': platform.node()
    }

def log_performance(func):
    """
    Décorateur pour logger les performances
    
    Args:
        func: Fonction à décorer
        
    Returns:
        Fonction décorée
    """
    import time
    from functools import wraps
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        execution_time = end_time - start_time
        print(f"⏱️ {func.__name__} executed in {execution_time:.3f}s")
        
        return result
    
    return wrapper

def retry_on_failure(max_retries: int = 3, delay: float = 1.0):
    """
    Décorateur pour retry automatique
    
    Args:
        max_retries: Nombre maximum de tentatives
        delay: Délai entre les tentatives
        
    Returns:
        Décorateur
    """
    import time
    from functools import wraps
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e
                    
                    print(f"⚠️ Attempt {attempt + 1} failed for {func.__name__}: {e}")
                    time.sleep(delay)
            
            return None
        
        return wrapper
    
    return decorator

# Classe utilitaire pour les opérations courantes
class TextUtils:
    """Utilitaires pour le traitement de texte"""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Nettoyer un texte"""
        # Supprimer les espaces multiples
        text = re.sub(r'\s+', ' ', text)
        # Supprimer les espaces en début et fin
        text = text.strip()
        return text
    
    @staticmethod
    def highlight_search_terms(text: str, search_terms: List[str]) -> str:
        """Surligner les termes de recherche"""
        for term in search_terms:
            pattern = re.compile(re.escape(term), re.IGNORECASE)
            text = pattern.sub(f'<mark>{term}</mark>', text)
        return text
    
    @staticmethod
    def extract_mentions(text: str) -> List[str]:
        """Extraire les mentions (@username)"""
        pattern = r'@([a-zA-Z0-9_]+)'
        return re.findall(pattern, text)
    
    @staticmethod
    def extract_hashtags(text: str) -> List[str]:
        """Extraire les hashtags (#hashtag)"""
        pattern = r'#([a-zA-Z0-9_]+)'
        return re.findall(pattern, text)

# Classe utilitaire pour les dates
class DateUtils:
    """Utilitaires pour les dates"""
    
    @staticmethod
    def get_week_range(date: datetime = None) -> tuple:
        """Obtenir la plage de la semaine"""
        if date is None:
            date = datetime.now()
        
        start = date - timedelta(days=date.weekday())
        end = start + timedelta(days=6)
        
        return start, end
    
    @staticmethod
    def get_month_range(date: datetime = None) -> tuple:
        """Obtenir la plage du mois"""
        if date is None:
            date = datetime.now()
        
        start = date.replace(day=1)
        
        # Dernier jour du mois
        if start.month == 12:
            end = start.replace(year=start.year + 1, month=1) - timedelta(days=1)
        else:
            end = start.replace(month=start.month + 1) - timedelta(days=1)
        
        return start, end
    
    @staticmethod
    def is_business_day(date: datetime) -> bool:
        """Vérifier si c'est un jour ouvrable"""
        return date.weekday() < 5  # Lundi = 0, Dimanche = 6