from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
from typing import Generator
from config.settings import settings

# Configuration de la base de données
engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modèles de base de données
class Article(Base):
    """Modèle pour les articles"""
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    title_en = Column(String(200))
    title_ar = Column(String(200))
    summary = Column(Text)
    summary_en = Column(Text)
    summary_ar = Column(Text)
    content = Column(Text, nullable=False)
    content_en = Column(Text)
    content_ar = Column(Text)
    category = Column(String(50), nullable=False)
    author = Column(String(100), nullable=False)
    author_bio = Column(Text)
    date_created = Column(DateTime, default=datetime.utcnow)
    date_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    read_time = Column(Integer, default=5)
    image = Column(String(255))
    tags = Column(Text)  # JSON string
    tags_en = Column(Text)  # JSON string
    tags_ar = Column(Text)  # JSON string
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    featured = Column(Boolean, default=False)
    published = Column(Boolean, default=True)
    meta_description = Column(Text)
    difficulty = Column(String(20), default="beginner")
    related_articles = Column(Text)  # JSON string avec IDs

class Report(Base):
    """Modèle pour les rapports"""
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    title_en = Column(String(200))
    title_ar = Column(String(200))
    description = Column(Text)
    description_en = Column(Text)
    description_ar = Column(Text)
    type = Column(String(50), nullable=False)  # research, survey, analysis, white_paper
    author = Column(String(100), nullable=False)
    date_created = Column(DateTime, default=datetime.utcnow)
    date_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    pages = Column(Integer)
    downloads = Column(Integer, default=0)
    file_size = Column(String(20))
    file_url = Column(String(255))
    cover_image = Column(String(255))
    tags = Column(Text)  # JSON string
    tags_en = Column(Text)  # JSON string
    tags_ar = Column(Text)  # JSON string
    featured = Column(Boolean, default=False)
    published = Column(Boolean, default=True)
    abstract = Column(Text)
    abstract_en = Column(Text)
    abstract_ar = Column(Text)

class User(Base):
    """Modèle pour les utilisateurs (pour futures fonctionnalités)"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    username = Column(String(50), unique=True, index=True)
    full_name = Column(String(100))
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    date_created = Column(DateTime, default=datetime.utcnow)
    date_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime)
    preferred_language = Column(String(10), default="fr")
    preferred_theme = Column(String(10), default="light")

class Contact(Base):
    """Modèle pour les messages de contact"""
    __tablename__ = "contacts"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    subject = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    date_created = Column(DateTime, default=datetime.utcnow)
    is_read = Column(Boolean, default=False)
    replied = Column(Boolean, default=False)
    ip_address = Column(String(50))

class Analytics(Base):
    """Modèle pour les analytics (pour futures fonctionnalités)"""
    __tablename__ = "analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    page_url = Column(String(255), nullable=False)
    user_agent = Column(String(500))
    ip_address = Column(String(50))
    referrer = Column(String(255))
    visit_date = Column(DateTime, default=datetime.utcnow)
    session_id = Column(String(100))
    user_id = Column(Integer)  # Foreign key vers users si connecté

# Fonctions utilitaires
def get_db() -> Generator[Session, None, None]:
    """Générateur de session de base de données"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """Créer toutes les tables"""
    Base.metadata.create_all(bind=engine)
    print("✅ Tables de base de données créées")

def drop_tables():
    """Supprimer toutes les tables (attention!)"""
    Base.metadata.drop_all(bind=engine)
    print("⚠️ Tables de base de données supprimées")

def init_sample_data():
    """Initialiser avec des données d'exemple"""
    db = SessionLocal()
    try:
        # Vérifier si des données existent déjà
        if db.query(Article).count() > 0:
            print("ℹ️ Données d'exemple déjà présentes")
            return
        
        # Ajouter des articles d'exemple
        sample_articles = [
            Article(
                title="Gérer l'anxiété au quotidien",
                title_en="Managing Daily Anxiety",
                title_ar="إدارة القلق اليومي",
                summary="Des techniques pratiques pour réduire l'anxiété et retrouver la sérénité.",
                content="L'anxiété est une réaction normale face au stress...",
                category="anxiety",
                author="Dr. Sarah Ahmed",
                read_time=8,
                tags='["anxiété", "gestion", "techniques"]',
                views=1250,
                likes=89,
                featured=True
            ),
            Article(
                title="L'importance du sommeil pour la santé mentale",
                title_en="The Importance of Sleep for Mental Health",
                title_ar="أهمية النوم للصحة النفسية",
                summary="Comment un bon sommeil améliore votre bien-être mental.",
                content="Le sommeil joue un rôle crucial dans notre santé mentale...",
                category="wellness",
                author="Dr. Marc Dubois",
                read_time=6,
                tags='["sommeil", "bien-être", "santé"]',
                views=950,
                likes=67
            )
        ]
        
        for article in sample_articles:
            db.add(article)
        
        # Ajouter des rapports d'exemple
        sample_reports = [
            Report(
                title="État de la santé mentale au Maroc 2024",
                title_en="Mental Health Status in Morocco 2024",
                title_ar="حالة الصحة النفسية في المغرب 2024",
                description="Rapport complet sur l'état de la santé mentale au Maroc.",
                type="research",
                author="Institut National de Recherche",
                pages=156,
                downloads=2500,
                file_size="12.5 MB",
                tags='["statistiques", "Maroc", "santé mentale"]',
                featured=True
            )
        ]
        
        for report in sample_reports:
            db.add(report)
        
        db.commit()
        print("✅ Données d'exemple ajoutées")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation des données: {e}")
        db.rollback()
    finally:
        db.close()

# Classes de service pour les opérations CRUD
class ArticleService:
    """Service pour les opérations sur les articles"""
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Article).filter(Article.published == True).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_id(db: Session, article_id: int):
        return db.query(Article).filter(Article.id == article_id).first()
    
    @staticmethod
    def get_by_category(db: Session, category: str):
        return db.query(Article).filter(Article.category == category, Article.published == True).all()
    
    @staticmethod
    def get_featured(db: Session):
        return db.query(Article).filter(Article.featured == True, Article.published == True).all()
    
    @staticmethod
    def search(db: Session, query: str):
        return db.query(Article).filter(
            Article.title.contains(query) | 
            Article.summary.contains(query) |
            Article.content.contains(query)
        ).all()

class ReportService:
    """Service pour les opérations sur les rapports"""
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Report).filter(Report.published == True).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_id(db: Session, report_id: int):
        return db.query(Report).filter(Report.id == report_id).first()
    
    @staticmethod
    def get_by_type(db: Session, report_type: str):
        return db.query(Report).filter(Report.type == report_type, Report.published == True).all()
    
    @staticmethod
    def get_featured(db: Session):
        return db.query(Report).filter(Report.featured == True, Report.published == True).all()

class ContactService:
    """Service pour les opérations sur les contacts"""
    
    @staticmethod
    def create(db: Session, name: str, email: str, subject: str, message: str, ip_address: str = None):
        contact = Contact(
            name=name,
            email=email,
            subject=subject,
            message=message,
            ip_address=ip_address
        )
        db.add(contact)
        db.commit()
        db.refresh(contact)
        return contact
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Contact).offset(skip).limit(limit).all()
    
    @staticmethod
    def mark_as_read(db: Session, contact_id: int):
        contact = db.query(Contact).filter(Contact.id == contact_id).first()
        if contact:
            contact.is_read = True
            db.commit()
        return contact

# Initialisation
if __name__ == "__main__":
    print("🗄️ Initialisation de la base de données...")
    create_tables()
    init_sample_data()
    print("✅ Base de données initialisée avec succès")