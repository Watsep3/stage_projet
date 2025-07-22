from nicegui import ui
from core.i18n import i18n, _
from core.theme import theme_manager
from config.database import SessionLocal, ArticleService
import json

class ArticlesPage:
    """Page des articles utilisant la base de données"""
    
    def __init__(self):
        self.articles = []
        self.current_category = "all"
        
        self.categories = {
            "all": "Tous",
            "anxiety": "Anxiété",
            "depression": "Dépression", 
            "stress": "Stress",
            "wellness": "Bien-être",
            "therapy": "Thérapie",
            "mindfulness": "Pleine conscience"
        }
        
        # Charger les articles depuis la base de données
        self.load_articles_from_db()
    
    def load_articles_from_db(self):
        """Charger les articles depuis la base de données"""
        try:
            db = SessionLocal()
            # Utiliser le service pour récupérer tous les articles
            db_articles = ArticleService.get_all(db)
            
            # Convertir les objets SQLAlchemy en dictionnaires
            self.articles = []
            for article in db_articles:
                article_dict = {
                    "id": article.id,
                    "title": article.title,
                    "summary": article.summary,
                    "category": article.category,
                    "author": article.author,
                    "date": article.date_created.strftime("%Y-%m-%d") if article.date_created else "",
                    "read_time": article.read_time or 5,
                    "image": article.image,
                    "tags": json.loads(article.tags) if article.tags else [],
                    "views": article.views or 0,
                    "likes": article.likes or 0,
                    "shares": article.shares or 0,
                    "featured": article.featured or False,
                    "published": article.published or True,
                    "difficulty": article.difficulty or "beginner",
                    "content": article.content or ""
                }
                self.articles.append(article_dict)
            
            db.close()
            print(f"✅ {len(self.articles)} articles chargés depuis la base de données")
            
        except Exception as e:
            print(f"❌ Erreur lors du chargement des articles: {e}")
            # En cas d'erreur, utiliser une liste vide
            self.articles = []
    
    def get_articles_by_category(self, category: str):
        """Obtenir les articles d'une catégorie spécifique depuis la BDD"""
        if category == "all":
            return self.articles
        
        try:
            db = SessionLocal()
            db_articles = ArticleService.get_by_category(db, category)
            
            filtered_articles = []
            for article in db_articles:
                article_dict = {
                    "id": article.id,
                    "title": article.title,
                    "summary": article.summary,
                    "category": article.category,
                    "author": article.author,
                    "date": article.date_created.strftime("%Y-%m-%d") if article.date_created else "",
                    "read_time": article.read_time or 5,
                    "image": article.image,
                    "tags": json.loads(article.tags) if article.tags else [],
                    "views": article.views or 0,
                    "likes": article.likes or 0,
                    "shares": article.shares or 0,
                    "featured": article.featured or False,
                    "published": article.published or True,
                    "difficulty": article.difficulty or "beginner"
                }
                filtered_articles.append(article_dict)
            
            db.close()
            return filtered_articles
            
        except Exception as e:
            print(f"❌ Erreur lors du filtrage par catégorie: {e}")
            return []
    
    def search_articles(self, query: str):
        """Rechercher des articles dans la base de données"""
        if not query.strip():
            return self.articles
        
        try:
            db = SessionLocal()
            db_articles = ArticleService.search(db, query)
            
            search_results = []
            for article in db_articles:
                article_dict = {
                    "id": article.id,
                    "title": article.title,
                    "summary": article.summary,
                    "category": article.category,
                    "author": article.author,
                    "date": article.date_created.strftime("%Y-%m-%d") if article.date_created else "",
                    "read_time": article.read_time or 5,
                    "image": article.image,
                    "tags": json.loads(article.tags) if article.tags else [],
                    "views": article.views or 0,
                    "likes": article.likes or 0,
                    "shares": article.shares or 0,
                    "featured": article.featured or False,
                    "published": article.published or True,
                    "difficulty": article.difficulty or "beginner"
                }
                search_results.append(article_dict)
            
            db.close()
            return search_results
            
        except Exception as e:
            print(f"❌ Erreur lors de la recherche: {e}")
            return []
    
    def get_featured_articles(self):
        """Obtenir les articles en vedette"""
        try:
            db = SessionLocal()
            db_articles = ArticleService.get_featured(db)
            
            featured_articles = []
            for article in db_articles:
                article_dict = {
                    "id": article.id,
                    "title": article.title,
                    "summary": article.summary,
                    "category": article.category,
                    "author": article.author,
                    "date": article.date_created.strftime("%Y-%m-%d") if article.date_created else "",
                    "read_time": article.read_time or 5,
                    "image": article.image,
                    "tags": json.loads(article.tags) if article.tags else [],
                    "views": article.views or 0,
                    "likes": article.likes or 0,
                    "shares": article.shares or 0,
                    "featured": article.featured or False,
                    "published": article.published or True,
                    "difficulty": article.difficulty or "beginner"
                }
                featured_articles.append(article_dict)
            
            db.close()
            return featured_articles
            
        except Exception as e:
            print(f"❌ Erreur lors du chargement des articles en vedette: {e}")
            return []
    
    def render(self):
        """Rendre la page des articles"""
        # Header
        self.render_header()
        
        # Filtres
        self.render_filters()
        
        # Articles
        self.render_articles_grid()
    
    def render_header(self):
        """Rendre l'en-tête avec gradient de thème"""
        with ui.element('div').classes('w-full py-16 px-4 gradient-hero'):
            with ui.column().classes('max-w-4xl mx-auto text-center text-inverse'):
                ui.label('Articles').classes('text-5xl font-bold mb-4')
                ui.label('Découvrez nos articles sur la santé mentale').classes('text-xl opacity-90')
    
    def render_filters(self):
        """Rendre les filtres avec classes de thème"""
        with ui.element('div').classes('w-full py-6 px-4 bg-card border-default border-b'):
            with ui.row().classes('page-container mx-auto gap-4 items-center'):
                ui.label('Catégorie :').classes('font-medium text-main')
                
                # Boutons de catégorie avec classes de thème
                with ui.row().classes('gap-2 flex-wrap'):
                    for key, label in self.categories.items():
                        if key == self.current_category:
                            ui.button(
                                label,
                                on_click=lambda k=key: self.filter_by_category(k)
                            ).classes(theme_manager.get_button_classes('primary', 'sm'))
                        else:
                            ui.button(
                                label,
                                on_click=lambda k=key: self.filter_by_category(k)
                            ).classes('px-4 py-2 rounded bg-surface text-muted hover:bg-hover hover:text-primary transition-colors')
    
    def render_articles_grid(self):
        """Rendre la grille des articles avec classes de thème"""
        filtered_articles = self.get_filtered_articles()
        
        with ui.element('div').classes('w-full py-8 px-4 bg-surface'):
            with ui.column().classes('page-container mx-auto'):
                
                if not filtered_articles:
                    self.render_empty_state()
                    return
                
                # Grille d'articles
                with ui.element('div').classes('grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8'):
                    for article in filtered_articles:
                        self.render_article_card(article)
    
    def render_empty_state(self):
        """Rendre l'état vide"""
        with ui.column().classes('items-center justify-center py-16 text-center'):
            ui.icon('article').classes('text-6xl text-muted mb-4')
            ui.label('Aucun article trouvé pour cette catégorie').classes('text-xl text-muted mb-4')
            ui.button(
                'Voir tous les articles',
                on_click=lambda: self.filter_by_category('all')
            ).classes(theme_manager.get_button_classes('primary', 'md'))
    
    def render_article_card(self, article):
        """Rendre une carte d'article avec classes de thème"""
        with ui.card().classes(theme_manager.get_card_classes(hover=True) + ' cursor-pointer'):
            # Image placeholder ou réelle
            with ui.element('div').classes('h-48 bg-surface flex items-center justify-center relative overflow-hidden'):
                if article.get("image"):
                    ui.image(article["image"]).classes('w-full h-full object-cover')
                else:
                    ui.icon('article').classes('text-4xl text-muted')
                
                # Badge featured
                if article.get("featured"):
                    with ui.element('div').classes('absolute top-2 right-2'):
                        ui.chip('⭐ En vedette').classes('bg-yellow-500 text-white text-xs')
                
                # Badge difficulté
                if article.get("difficulty"):
                    with ui.element('div').classes('absolute top-2 left-2'):
                        difficulty_colors = {
                            "beginner": "bg-green-500 text-white",
                            "intermediate": "bg-yellow-500 text-white", 
                            "advanced": "bg-red-500 text-white"
                        }
                        color_class = difficulty_colors.get(article["difficulty"], "bg-gray-500 text-white")
                        ui.chip(article["difficulty"].title()).classes(f'{color_class} text-xs')
            
            with ui.card_section().classes('p-6'):
                # Catégorie avec couleur de thème
                category_name = self.categories.get(article["category"], article["category"])
                ui.chip(category_name).classes(theme_manager.get_button_classes('primary', 'sm') + ' text-xs mb-3')
                
                # Titre
                ui.label(article["title"]).classes('text-xl font-bold mb-2 line-clamp-2 text-main')
                
                # Résumé
                ui.label(article["summary"]).classes('text-muted mb-4 line-clamp-3')
                
                # Métadonnées
                with ui.row().classes('items-center gap-4 text-sm text-muted mb-4'):
                    ui.label(f"👤 {article['author']}")
                    ui.label(f"📅 {article['date']}")
                    ui.label(f"⏱️ {article['read_time']} min")
                
                # Tags
                with ui.row().classes('gap-1 mb-4 flex-wrap'):
                    for tag in article["tags"][:3]:
                        ui.chip(f"#{tag}").classes('text-xs bg-surface text-muted')
                
                # Actions avec bouton de thème
                with ui.row().classes('justify-between items-center'):
                    ui.button(
                        'Lire plus',
                        on_click=lambda a=article: self.read_article(a),
                        icon='read_more'
                    ).classes(theme_manager.get_button_classes('primary', 'md'))
                    
                    with ui.row().classes('gap-2 items-center text-sm text-muted'):
                        ui.label(f"👁 {article['views']}")
                        ui.label(f"❤️ {article['likes']}")
                        if article.get('shares', 0) > 0:
                            ui.label(f"📤 {article['shares']}")
    
    def get_filtered_articles(self):
        """Obtenir les articles filtrés"""
        if self.current_category == "all":
            return self.articles
        else:
            return self.get_articles_by_category(self.current_category)
    
    def filter_by_category(self, category):
        """Filtrer par catégorie"""
        self.current_category = category
        # Recharger la page avec la nouvelle catégorie
        ui.notify(f'Filtrage par catégorie: {self.categories[category]}', type='info')
        
        # Dans une vraie app avec état, on mettrait à jour l'affichage ici
        # Pour l'instant, on simule avec une notification
        ui.run_javascript('window.location.reload()')
    
    def read_article(self, article):
        """Lire un article"""
        # Incrémenter le nombre de vues dans la base de données
        try:
            db = SessionLocal()
            db_article = db.query(ArticleService.Article).filter_by(id=article["id"]).first()
            if db_article:
                db_article.views = (db_article.views or 0) + 1
                db.commit()
            db.close()
        except Exception as e:
            print(f"❌ Erreur lors de l'incrémentation des vues: {e}")
        
        ui.notify(f'Ouverture de l\'article: {article["title"]}', type='info')
        # Dans une vraie app: ui.navigate.to(f'/article/{article["id"]}')
        
    def increment_article_views(self, article_id: int):
        """Incrémenter le nombre de vues d'un article"""
        try:
            db = SessionLocal()
            from config.database import Article
            article = db.query(Article).filter_by(id=article_id).first()
            if article:
                article.views = (article.views or 0) + 1
                db.commit()
                print(f"✅ Vues incrémentées pour l'article {article_id}")
            db.close()
        except Exception as e:
            print(f"❌ Erreur lors de l'incrémentation des vues: {e}")