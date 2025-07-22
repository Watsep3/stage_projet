#!/usr/bin/env python3
"""
Script pour populer la base de données MindCare
Usage: python populate_db.py
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
import random

# Ajouter le dossier parent au path pour les imports
sys.path.append(str(Path(__file__).parent))

from config.database import (
    create_tables, SessionLocal, 
    Article, Report, Contact, User
)

def load_json_data(file_path: Path):
    """Charger des données depuis un fichier JSON"""
    if file_path.exists():
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Erreur lors du chargement de {file_path}: {e}")
    return []

def populate_articles():
    """Populer les articles"""
    db = SessionLocal()
    
    try:
        # Vérifier si des articles existent déjà
        if db.query(Article).count() > 0:
            print("ℹ️ Articles déjà présents, ajout de nouveaux articles...")
        
        # Charger depuis le fichier JSON s'il existe
        articles_file = Path("data/articles.json")
        json_articles = load_json_data(articles_file)
        
        # Articles d'exemple supplémentaires
        sample_articles = [
            {
                "title": "Comprendre l'anxiété sociale",
                "title_en": "Understanding Social Anxiety",
                "title_ar": "فهم القلق الاجتماعي",
                "summary": "L'anxiété sociale peut être paralysante. Découvrez comment la reconnaître et la surmonter.",
                "content": """L'anxiété sociale est bien plus qu'une simple timidité. C'est une peur intense et persistante des situations sociales où l'on pourrait être jugé par les autres.

## Symptômes courants
- Rougissement
- Tremblements
- Transpiration excessive
- Difficultés à parler

## Stratégies pour la gérer
1. **Respiration profonde** : Prenez des respirations lentes et profondes
2. **Exposition graduelle** : Commencez par de petites interactions
3. **Pensées positives** : Remplacez les pensées négatives
4. **Préparation** : Préparez des sujets de conversation

## Quand consulter ?
Si l'anxiété sociale interfère avec votre vie quotidienne, n'hésitez pas à consulter un professionnel.""",
                "category": "anxiety",
                "author": "Dr. Fatima Bennani",
                "read_time": 7,
                "tags": ["anxiété sociale", "timidité", "confiance"],
                "difficulty": "beginner",
                "featured": True
            },
            {
                "title": "Techniques de méditation pour débutants",
                "title_en": "Meditation Techniques for Beginners",
                "title_ar": "تقنيات التأمل للمبتدئين",
                "summary": "Découvrez les bases de la méditation et comment commencer une pratique régulière.",
                "content": """La méditation est un outil puissant pour réduire le stress et améliorer le bien-être mental.

## Types de méditation
- **Méditation de pleine conscience** : Concentration sur le moment présent
- **Méditation guidée** : Avec un instructeur ou une application
- **Méditation transcendantale** : Répétition d'un mantra

## Comment commencer
1. Trouvez un endroit calme
2. Commencez par 5-10 minutes
3. Concentrez-vous sur votre respiration
4. Soyez patient avec vous-même

## Bienfaits prouvés
- Réduction du stress
- Amélioration de la concentration
- Meilleure gestion des émotions
- Sommeil amélioré""",
                "category": "mindfulness",
                "author": "Dr. Ahmed Alaoui",
                "read_time": 9,
                "tags": ["méditation", "pleine conscience", "relaxation"],
                "difficulty": "beginner",
                "featured": False
            },
            {
                "title": "Burnout professionnel : signes et solutions",
                "title_en": "Professional Burnout: Signs and Solutions",
                "title_ar": "الإرهاق المهني: العلامات والحلول",
                "summary": "Le burnout touche de plus en plus de professionnels. Apprenez à le reconnaître et à le prévenir.",
                "content": """Le burnout ou épuisement professionnel est un état de fatigue émotionnelle, physique et mentale.

## Signes d'alerte
- Épuisement constant
- Cynisme envers le travail
- Sentiment d'inefficacité
- Problèmes de concentration

## Facteurs de risque
- Charge de travail excessive
- Manque d'autonomie
- Relations difficiles au travail
- Déséquilibre vie pro/perso

## Solutions
1. **Établir des limites** : Apprenez à dire non
2. **Prendre des pauses** : Respectez vos temps de repos
3. **Chercher du soutien** : Parlez à vos collègues ou un professionnel
4. **Revoir ses priorités** : Focalisez sur l'essentiel

## Prévention
- Exercice régulier
- Alimentation équilibrée
- Sommeil suffisant
- Activités de détente""",
                "category": "stress",
                "author": "Dr. Khadija Moussaid",
                "read_time": 12,
                "tags": ["burnout", "travail", "épuisement", "stress"],
                "difficulty": "intermediate",
                "featured": True
            },
            {
                "title": "Dépression saisonnière : lumière et espoir",
                "title_en": "Seasonal Depression: Light and Hope",
                "title_ar": "الاكتئاب الموسمي: النور والأمل",
                "summary": "La dépression saisonnière affecte beaucoup de personnes. Découvrez comment la combattre.",
                "content": """La dépression saisonnière (TAS) survient généralement en automne et hiver.

## Symptômes typiques
- Tristesse persistante
- Fatigue excessive
- Hypersomnie
- Envies de sucre
- Isolement social

## Causes
- Manque de lumière naturelle
- Perturbation du rythme circadien
- Baisse de sérotonine
- Facteurs génétiques

## Traitements efficaces
1. **Luminothérapie** : Exposition à la lumière artificielle
2. **Exercice physique** : Activité régulière
3. **Psychothérapie** : TCC adaptée
4. **Médication** : Si nécessaire

## Conseils pratiques
- Maximiser l'exposition à la lumière naturelle
- Maintenir une routine régulière
- Rester socialement actif
- Pratiquer des activités plaisantes""",
                "category": "depression",
                "author": "Dr. Youssef Tazi",
                "read_time": 8,
                "tags": ["dépression saisonnière", "lumière", "hiver"],
                "difficulty": "beginner",
                "featured": False
            },
            {
                "title": "Thérapie cognitive comportementale (TCC)",
                "title_en": "Cognitive Behavioral Therapy (CBT)",
                "title_ar": "العلاج المعرفي السلوكي",
                "summary": "La TCC est une approche thérapeutique efficace pour de nombreux troubles mentaux.",
                "content": """La Thérapie Cognitive Comportementale est une forme de psychothérapie structurée et orientée solution.

## Principes de base
- Connexion pensées-émotions-comportements
- Focus sur le présent
- Approche collaborative
- Techniques concrètes

## Domaines d'application
- Troubles anxieux
- Dépression
- Troubles obsessionnels
- Phobies
- ESPT

## Techniques principales
1. **Restructuration cognitive** : Identifier les pensées dysfonctionnelles
2. **Exposition graduée** : Affronter progressivement les peurs
3. **Résolution de problèmes** : Approche systématique
4. **Relaxation** : Gestion du stress et de l'anxiété

## Durée et efficacité
- Généralement 12-20 séances
- Résultats souvent visibles rapidement
- Techniques utilisables à long terme
- Preuves scientifiques solides""",
                "category": "therapy",
                "author": "Dr. Laila Benjelloun",
                "read_time": 15,
                "tags": ["TCC", "psychothérapie", "techniques"],
                "difficulty": "advanced",
                "featured": True
            }
        ]
        
        # Combiner les données JSON et les exemples
        all_articles = json_articles + sample_articles
        
        for article_data in all_articles:
            # Vérifier si l'article existe déjà
            existing = db.query(Article).filter(Article.title == article_data["title"]).first()
            if existing:
                print(f"⏭️ Article '{article_data['title']}' existe déjà")
                continue
            
            # Créer l'article
            article = Article(
                title=article_data["title"],
                title_en=article_data.get("title_en"),
                title_ar=article_data.get("title_ar"),
                summary=article_data["summary"],
                summary_en=article_data.get("summary_en"),
                summary_ar=article_data.get("summary_ar"),
                content=article_data["content"],
                content_en=article_data.get("content_en"),
                content_ar=article_data.get("content_ar"),
                category=article_data["category"],
                author=article_data["author"],
                read_time=article_data.get("read_time", 5),
                tags=json.dumps(article_data.get("tags", [])),
                tags_en=json.dumps(article_data.get("tags_en", [])) if article_data.get("tags_en") else None,
                tags_ar=json.dumps(article_data.get("tags_ar", [])) if article_data.get("tags_ar") else None,
                difficulty=article_data.get("difficulty", "beginner"),
                featured=article_data.get("featured", False),
                published=article_data.get("published", True),
                views=random.randint(100, 5000),
                likes=random.randint(10, 200),
                shares=random.randint(5, 50),
                date_created=datetime.now() - timedelta(days=random.randint(1, 90))
            )
            
            db.add(article)
            print(f"✅ Article ajouté: {article_data['title']}")
        
        db.commit()
        print(f"✅ {len(all_articles)} articles traités")
        
    except Exception as e:
        print(f"❌ Erreur lors de la population des articles: {e}")
        db.rollback()
    finally:
        db.close()

def populate_reports():
    """Populer les rapports"""
    db = SessionLocal()
    
    try:
        if db.query(Report).count() > 0:
            print("ℹ️ Rapports déjà présents, ajout de nouveaux rapports...")
        
        # Charger depuis le fichier JSON s'il existe
        reports_file = Path("data/reports.json")
        json_reports = load_json_data(reports_file)
        
        # Rapports d'exemple
        sample_reports = [
            {
                "title": "Étude sur la santé mentale des jeunes au Maroc",
                "title_en": "Study on Youth Mental Health in Morocco",
                "title_ar": "دراسة حول الصحة النفسية للشباب في المغرب",
                "description": "Une étude complète sur l'état de la santé mentale chez les jeunes marocains âgés de 15 à 25 ans.",
                "abstract": "Cette étude examine les défis de santé mentale auxquels font face les jeunes au Maroc, incluant l'anxiété, la dépression et le stress académique.",
                "type": "research",
                "author": "Institut Marocain de Recherche en Santé Mentale",
                "pages": 234,
                "file_size": "15.8 MB",
                "tags": ["jeunes", "Maroc", "étude", "statistiques"],
                "featured": True
            },
            {
                "title": "Guide pratique de la télé-consultation en psychologie",
                "title_en": "Practical Guide to Tele-consultation in Psychology",
                "title_ar": "دليل عملي للاستشارة عن بعد في علم النفس",
                "description": "Un guide complet pour les psychologues souhaitant offrir des consultations à distance.",
                "abstract": "Ce guide couvre les aspects techniques, éthiques et pratiques de la télé-consultation en santé mentale.",
                "type": "white_paper",
                "author": "Association des Psychologues du Maroc",
                "pages": 87,
                "file_size": "8.2 MB",
                "tags": ["téléconsultation", "psychologie", "guide", "pratique"],
                "featured": False
            },
            {
                "title": "Analyse des thérapies alternatives en santé mentale",
                "title_en": "Analysis of Alternative Therapies in Mental Health",
                "title_ar": "تحليل العلاجات البديلة في الصحة النفسية",
                "description": "Une analyse critique des thérapies alternatives et complémentaires en santé mentale.",
                "abstract": "Cette analyse examine l'efficacité et la sécurité des approches thérapeutiques alternatives.",
                "type": "analysis",
                "author": "Dr. Khalid Benali",
                "pages": 156,
                "file_size": "12.4 MB",
                "tags": ["thérapies alternatives", "analyse", "efficacité"],
                "featured": True
            },
            {
                "title": "Enquête sur le bien-être au travail",
                "title_en": "Workplace Wellbeing Survey",
                "title_ar": "استطلاع حول الرفاهية في مكان العمل",
                "description": "Résultats d'une enquête nationale sur le bien-être mental des employés.",
                "abstract": "Cette enquête révèle les facteurs qui influencent le bien-être mental au travail.",
                "type": "survey",
                "author": "Centre National du Bien-être au Travail",
                "pages": 98,
                "file_size": "6.7 MB",
                "tags": ["travail", "bien-être", "enquête", "employés"],
                "featured": False
            }
        ]
        
        all_reports = json_reports + sample_reports
        
        for report_data in all_reports:
            # Vérifier si le rapport existe déjà
            existing = db.query(Report).filter(Report.title == report_data["title"]).first()
            if existing:
                print(f"⏭️ Rapport '{report_data['title']}' existe déjà")
                continue
            
            report = Report(
                title=report_data["title"],
                title_en=report_data.get("title_en"),
                title_ar=report_data.get("title_ar"),
                description=report_data["description"],
                description_en=report_data.get("description_en"),
                description_ar=report_data.get("description_ar"),
                abstract=report_data.get("abstract"),
                abstract_en=report_data.get("abstract_en"),
                abstract_ar=report_data.get("abstract_ar"),
                type=report_data["type"],
                author=report_data["author"],
                pages=report_data.get("pages", 50),
                file_size=report_data.get("file_size", "5.0 MB"),
                file_url=f"/static/reports/{report_data['title'].lower().replace(' ', '_')}.pdf",
                tags=json.dumps(report_data.get("tags", [])),
                tags_en=json.dumps(report_data.get("tags_en", [])) if report_data.get("tags_en") else None,
                tags_ar=json.dumps(report_data.get("tags_ar", [])) if report_data.get("tags_ar") else None,
                featured=report_data.get("featured", False),
                published=report_data.get("published", True),
                downloads=random.randint(50, 3000),
                date_created=datetime.now() - timedelta(days=random.randint(1, 180))
            )
            
            db.add(report)
            print(f"✅ Rapport ajouté: {report_data['title']}")
        
        db.commit()
        print(f"✅ {len(all_reports)} rapports traités")
        
    except Exception as e:
        print(f"❌ Erreur lors de la population des rapports: {e}")
        db.rollback()
    finally:
        db.close()

def populate_contacts():
    """Populer quelques contacts d'exemple"""
    db = SessionLocal()
    
    try:
        if db.query(Contact).count() > 0:
            print("ℹ️ Contacts déjà présents, pas d'ajout")
            return
        
        sample_contacts = [
            {
                "name": "Marie Dupont",
                "email": "marie.dupont@email.com",
                "subject": "Question sur les services",
                "message": "Bonjour, j'aimerais en savoir plus sur vos services de consultation en ligne."
            },
            {
                "name": "Ahmed Alami",
                "email": "ahmed.alami@email.com",
                "subject": "Demande de partenariat",
                "message": "Nous sommes intéressés par un partenariat avec votre organisation."
            },
            {
                "name": "Sophie Martin",
                "email": "sophie.martin@email.com",
                "subject": "Feedback sur le site",
                "message": "Excellent travail sur le site web ! Les ressources sont très utiles."
            }
        ]
        
        for contact_data in sample_contacts:
            contact = Contact(
                name=contact_data["name"],
                email=contact_data["email"],
                subject=contact_data["subject"],
                message=contact_data["message"],
                date_created=datetime.now() - timedelta(days=random.randint(1, 30)),
                is_read=random.choice([True, False])
            )
            
            db.add(contact)
            print(f"✅ Contact ajouté: {contact_data['name']}")
        
        db.commit()
        print(f"✅ {len(sample_contacts)} contacts ajoutés")
        
    except Exception as e:
        print(f"❌ Erreur lors de la population des contacts: {e}")
        db.rollback()
    finally:
        db.close()

def populate_users():
    """Populer quelques utilisateurs d'exemple"""
    db = SessionLocal()
    
    try:
        if db.query(User).count() > 0:
            print("ℹ️ Utilisateurs déjà présents, pas d'ajout")
            return
        
        sample_users = [
            {
                "email": "admin@mindcare.ma",
                "username": "admin",
                "full_name": "Administrateur MindCare",
                "is_admin": True,
                "preferred_language": "fr",
                "preferred_theme": "light"
            },
            {
                "email": "dr.sarah@mindcare.ma",
                "username": "dr_sarah",
                "full_name": "Dr. Sarah Ahmed",
                "is_admin": False,
                "preferred_language": "fr",
                "preferred_theme": "dark"
            }
        ]
        
        for user_data in sample_users:
            user = User(
                email=user_data["email"],
                username=user_data["username"],
                full_name=user_data["full_name"],
                hashed_password="hashed_password_here",  # En production, hasher vraiment
                is_admin=user_data.get("is_admin", False),
                preferred_language=user_data.get("preferred_language", "fr"),
                preferred_theme=user_data.get("preferred_theme", "light"),
                date_created=datetime.now() - timedelta(days=random.randint(30, 365))
            )
            
            db.add(user)
            print(f"✅ Utilisateur ajouté: {user_data['full_name']}")
        
        db.commit()
        print(f"✅ {len(sample_users)} utilisateurs ajoutés")
        
    except Exception as e:
        print(f"❌ Erreur lors de la population des utilisateurs: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    """Fonction principale"""
    print("🚀 Début de la population de la base de données MindCare")
    print("=" * 60)
    
    # Créer les tables si elles n'existent pas
    print("📋 Création des tables...")
    create_tables()
    
    # Créer le dossier data s'il n'existe pas
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # Populer chaque type de données
    print("\n📚 Population des articles...")
    populate_articles()
    
    print("\n📊 Population des rapports...")
    populate_reports()
    
    print("\n📧 Population des contacts...")
    populate_contacts()
    
    print("\n👤 Population des utilisateurs...")
    populate_users()
    
    print("\n" + "=" * 60)
    print("✅ Population de la base de données terminée avec succès !")
    print("💡 Vous pouvez maintenant lancer l'application : python main.py")

if __name__ == "__main__":
    main()