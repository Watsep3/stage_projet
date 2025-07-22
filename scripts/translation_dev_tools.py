#!/usr/bin/env python3
"""
Outils de développement pour la gestion des traductions MindCare
"""

import json
import sys
import argparse
from pathlib import Path
from typing import Dict, Set, List, Any
from datetime import datetime

# Ajouter le répertoire parent au path pour importer les modules
sys.path.append(str(Path(__file__).parent.parent))

from core.i18n import i18n
from config.settings import settings

class TranslationDevTools:
    """Outils de développement pour les traductions"""
    
    def __init__(self):
        self.locales_dir = settings.locales_dir
        self.supported_languages = settings.supported_languages
        self.reference_language = "fr"  # Langue de référence
    
    def scan_code_for_translations(self, directories: List[str] = None) -> Set[str]:
        """Scanner le code pour trouver les clés de traduction utilisées"""
        if directories is None:
            directories = ["pages", "components", "main.py"]
        
        translation_keys = set()
        
        # Patterns à rechercher
        patterns = [
            r'_\([\'"]([^\'"\)]+)[\'"]',  # _('key') ou _("key")
            r'_\([\'"]([^\'"\)]+)[\'"][^\)]*\)',  # _('key', **kwargs)
        ]
        
        import re
        
        for directory in directories:
            dir_path = Path(directory)
            if dir_path.is_file():
                files = [dir_path]
            else:
                files = list(dir_path.rglob("*.py"))
            
            for file_path in files:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                        for pattern in patterns:
                            matches = re.findall(pattern, content)
                            translation_keys.update(matches)
                            
                except Exception as e:
                    print(f"⚠️ Erreur lors de la lecture de {file_path}: {e}")
        
        return translation_keys
    
    def find_missing_translations(self) -> Dict[str, List[str]]:
        """Trouver les traductions manquantes"""
        # Scanner le code pour les clés utilisées
        used_keys = self.scan_code_for_translations()
        
        # Charger les traductions de référence
        reference_file = self.locales_dir / f"{self.reference_language}.json"
        if not reference_file.exists():
            print(f"❌ Fichier de référence {reference_file} non trouvé")
            return {}
        
        with open(reference_file, 'r', encoding='utf-8') as f:
            reference_translations = json.load(f)
        
        reference_keys = self._get_all_keys(reference_translations)
        
        results = {}
        
        # Vérifier chaque langue
        for lang in self.supported_languages:
            if lang == self.reference_language:
                # Pour la langue de référence, vérifier les clés utilisées vs définies
                missing_in_code = used_keys - reference_keys
                missing_in_reference = reference_keys - used_keys
                
                results[f"{lang}_code_vs_file"] = {
                    "used_but_not_defined": list(missing_in_code),
                    "defined_but_not_used": list(missing_in_reference)
                }
            else:
                # Pour les autres langues, comparer avec la référence
                lang_file = self.locales_dir / f"{lang}.json"
                if lang_file.exists():
                    with open(lang_file, 'r', encoding='utf-8') as f:
                        lang_translations = json.load(f)
                    
                    lang_keys = self._get_all_keys(lang_translations)
                    missing_keys = reference_keys - lang_keys
                    extra_keys = lang_keys - reference_keys
                    
                    results[lang] = {
                        "missing_keys": list(missing_keys),
                        "extra_keys": list(extra_keys),
                        "completion_rate": len(lang_keys) / len(reference_keys) * 100 if reference_keys else 0
                    }
                else:
                    results[lang] = {
                        "missing_keys": list(reference_keys),
                        "extra_keys": [],
                        "completion_rate": 0
                    }
        
        return results
    
    def _get_all_keys(self, obj: Any, prefix: str = "") -> Set[str]:
        """Obtenir toutes les clés d'un objet JSON de manière récursive"""
        keys = set()
        
        if isinstance(obj, dict):
            for key, value in obj.items():
                current_key = f"{prefix}.{key}" if prefix else key
                
                if isinstance(value, str):
                    keys.add(current_key)
                elif isinstance(value, dict):
                    keys.update(self._get_all_keys(value, current_key))
        
        return keys
    
    def generate_missing_translations(self, target_language: str = "en"):
        """Générer un fichier avec les traductions manquantes"""
        missing = self.find_missing_translations()
        
        if target_language not in missing:
            print(f"❌ Langue {target_language} non trouvée dans l'analyse")
            return
        
        missing_keys = missing[target_language]["missing_keys"]
        
        if not missing_keys:
            print(f"✅ Aucune traduction manquante pour {target_language}")
            return
        
        # Charger les traductions de référence
        reference_file = self.locales_dir / f"{self.reference_language}.json"
        with open(reference_file, 'r', encoding='utf-8') as f:
            reference_translations = json.load(f)
        
        # Créer la structure pour les traductions manquantes
        missing_structure = {}
        
        for key in missing_keys:
            # Obtenir la valeur de référence
            ref_value = self._get_nested_value(reference_translations, key)
            if ref_value:
                # Créer la structure imbriquée
                self._set_nested_value(missing_structure, key, f"[TO_TRANSLATE] {ref_value}")
        
        # Sauvegarder dans un fichier temporaire
        output_file = self.locales_dir / f"{target_language}_missing.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(missing_structure, f, indent=2, ensure_ascii=False)
        
        print(f"📝 Traductions manquantes sauvegardées dans {output_file}")
        print(f"📊 {len(missing_keys)} traductions à compléter")
    
    def _get_nested_value(self, obj: Dict, key: str) -> Any:
        """Obtenir une valeur imbriquée"""
        keys = key.split('.')
        current = obj
        
        for k in keys:
            if isinstance(current, dict) and k in current:
                current = current[k]
            else:
                return None
        
        return current if isinstance(current, str) else None
    
    def _set_nested_value(self, obj: Dict, key: str, value: Any):
        """Définir une valeur imbriquée"""
        keys = key.split('.')
        current = obj
        
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        
        current[keys[-1]] = value
    
    def validate_json_files(self) -> bool:
        """Valider la syntaxe JSON de tous les fichiers de traduction"""
        all_valid = True
        
        for lang in self.supported_languages:
            lang_file = self.locales_dir / f"{lang}.json"
            
            if not lang_file.exists():
                print(f"⚠️ Fichier {lang_file} n'existe pas")
                continue
            
            try:
                with open(lang_file, 'r', encoding='utf-8') as f:
                    json.load(f)
                print(f"✅ {lang}.json : Syntaxe JSON valide")
            except json.JSONDecodeError as e:
                print(f"❌ {lang}.json : Erreur JSON ligne {e.lineno}: {e.msg}")
                all_valid = False
            except Exception as e:
                print(f"❌ {lang}.json : Erreur: {e}")
                all_valid = False
        
        return all_valid
    
    def generate_translation_report(self, output_file: str = None):
        """Générer un rapport complet des traductions"""
        if output_file is None:
            output_file = f"translation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        missing = self.find_missing_translations()
        used_keys = self.scan_code_for_translations()
        
        report = []
        report.append("# Rapport des Traductions MindCare")
        report.append(f"\nGénéré le: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"\nLangues supportées: {', '.join(self.supported_languages)}")
        report.append(f"Langue de référence: {self.reference_language}")
        
        report.append(f"\n## Clés de traduction utilisées dans le code")
        report.append(f"Total: {len(used_keys)} clés")
        
        if used_keys:
            report.append("\n### Clés trouvées:")
            for key in sorted(used_keys):
                report.append(f"- `{key}`")
        
        report.append("\n## Analyse par langue")
        
        for lang_info, data in missing.items():
            if isinstance(data, dict) and "completion_rate" in data:
                lang = lang_info
                completion = data["completion_rate"]
                
                report.append(f"\n### {lang.upper()}")
                report.append(f"Taux de completion: {completion:.1f}%")
                
                if data["missing_keys"]:
                    report.append(f"\n#### Traductions manquantes ({len(data['missing_keys'])}):")
                    for key in sorted(data["missing_keys"])[:20]:  # Limiter à 20
                        report.append(f"- `{key}`")
                    
                    if len(data["missing_keys"]) > 20:
                        report.append(f"- ... et {len(data['missing_keys']) - 20} autres")
                
                if data["extra_keys"]:
                    report.append(f"\n#### Traductions supplémentaires ({len(data['extra_keys'])}):")
                    for key in sorted(data["extra_keys"])[:10]:  # Limiter à 10
                        report.append(f"- `{key}`")
        
        # Recommandations
        report.append("\n## Recommandations")
        
        total_issues = sum(len(data.get("missing_keys", [])) for data in missing.values() 
                          if isinstance(data, dict) and "missing_keys" in data)
        
        if total_issues == 0:
            report.append("✅ Toutes les traductions sont complètes!")
        else:
            report.append(f"⚠️ {total_issues} traductions manquantes au total")
            report.append("\n### Actions suggérées:")
            report.append("1. Compléter les traductions manquantes")
            report.append("2. Vérifier les traductions supplémentaires")
            report.append("3. Utiliser `python scripts/translation_dev_tools.py --generate-missing` pour générer les fichiers de traduction")
        
        # Sauvegarder le rapport
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))
        
        print(f"📊 Rapport généré: {output_file}")
        
        return report
    
    def merge_translation_file(self, lang: str, source_file: str):
        """Fusionner un fichier de traduction avec le fichier principal"""
        main_file = self.locales_dir / f"{lang}.json"
        source_path = Path(source_file)
        
        if not source_path.exists():
            print(f"❌ Fichier source {source_file} non trouvé")
            return
        
        # Charger le fichier source
        with open(source_path, 'r', encoding='utf-8') as f:
            source_data = json.load(f)
        
        # Charger le fichier principal (ou créer vide)
        if main_file.exists():
            with open(main_file, 'r', encoding='utf-8') as f:
                main_data = json.load(f)
        else:
            main_data = {}
        
        # Fusionner récursivement
        def merge_dicts(target, source):
            for key, value in source.items():
                if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                    merge_dicts(target[key], value)
                else:
                    target[key] = value
        
        merge_dicts(main_data, source_data)
        
        # Sauvegarder
        with open(main_file, 'w', encoding='utf-8') as f:
            json.dump(main_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Fichier {source_file} fusionné dans {main_file}")

def main():
    """Point d'entrée principal"""
    parser = argparse.ArgumentParser(description="Outils de développement pour les traductions MindCare")
    parser.add_argument('--validate', action='store_true', help="Valider la syntaxe JSON")
    parser.add_argument('--scan', action='store_true', help="Scanner le code pour les clés de traduction")
    parser.add_argument('--missing', action='store_true', help="Trouver les traductions manquantes")
    parser.add_argument('--generate-missing', type=str, help="Générer un fichier pour les traductions manquantes (langue)")
    parser.add_argument('--report', type=str, nargs='?', const='auto', help="Générer un rapport complet")
    parser.add_argument('--merge', nargs=2, metavar=('LANG', 'FILE'), help="Fusionner un fichier de traduction")
    
    args = parser.parse_args()
    
    tools = TranslationDevTools()
    
    if args.validate:
        print("🔍 Validation des fichiers JSON...")
        is_valid = tools.validate_json_files()
        print(f"\n{'✅ Tous les fichiers sont valides' if is_valid else '❌ Erreurs trouvées'}")
    
    elif args.scan:
        print("🔍 Scan du code pour les clés de traduction...")
        keys = tools.scan_code_for_translations()
        print(f"\n📊 {len(keys)} clés trouvées:")
        for key in sorted(keys):
            print(f"  - {key}")
    
    elif args.missing:
        print("🔍 Analyse des traductions manquantes...")
        missing = tools.find_missing_translations()
        
        for lang, data in missing.items():
            if isinstance(data, dict) and "completion_rate" in data:
                completion = data["completion_rate"]
                missing_count = len(data["missing_keys"])
                print(f"\n{lang.upper()}: {completion:.1f}% complet ({missing_count} manquantes)")
                
                if missing_count > 0 and missing_count <= 10:
                    for key in data["missing_keys"]:
                        print(f"  - {key}")
    
    elif args.generate_missing:
        print(f"📝 Génération des traductions manquantes pour {args.generate_missing}...")
        tools.generate_missing_translations(args.generate_missing)
    
    elif args.report:
        output_file = None if args.report == 'auto' else args.report
        print("📊 Génération du rapport complet...")
        tools.generate_translation_report(output_file)
    
    elif args.merge:
        lang, file_path = args.merge
        print(f"🔄 Fusion du fichier {file_path} dans {lang}.json...")
        tools.merge_translation_file(lang, file_path)
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()