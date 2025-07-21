from nicegui import ui
from core.i18n import i18n, _
from core.theme import theme_manager
import json
from pathlib import Path

class ArticlesPage:
    """Page des articles avec système de thème centralisé"""
    
    def __init__(self):
        self.articles = self.load_articles()
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
    
    def load_articles(self):
        """Charger les articles depuis le fichier JSON"""
        articles_file = Path("data/articles.json")
        
        if articles_file.exists():
            try:
                with open(articles_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Erreur lors du chargement des articles: {e}")
        
        # Articles d'exemple
        return [
            {
                "id": 1,
                "title": "Gérer l'anxiété au quotidien",
                "summary": "Des techniques pratiques pour réduire l'anxiété et retrouver la sérénité.",
                "category": "anxiety",
                "author": "Dr. Sarah Ahmed",
                "date": "2024-01-15",
                "read_time": 8,
                "image": "/static/images/anxiety.jpg",
                "tags": ["anxiété", "gestion", "techniques"],
                "views": 1250,
                "featured": True
            },
            {
                "id": 2,
                "title": "L'importance du sommeil pour la santé mentale",
                "summary": "Comment un bon sommeil améliore votre bien-être mental.",
                "category": "wellness",
                "author": "Dr. Marc Dubois",
                "date": "2024-01-10",
                "read_time": 6,
                "image": "/static/images/sleep.jpg",
                "tags": ["sommeil", "bien-être", "santé"],
                "views": 950,
                "featured": False
            },
            {
                "id": 3,
                "title": "Méditation et pleine conscience",
                "summary": "Les bienfaits de la méditation sur l'esprit et le corps.",
                "category": "mindfulness",
                "author": "Fatima El Alami",
                "date": "2024-01-05",
                "read_time": 10,
                "image": "/static/images/meditation.jpg",
                "tags": ["méditation", "pleine conscience", "relaxation"],
                "views": 1800,
                "featured": True
            }
        ]
    
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
                    ui.label('Aucun article trouvé pour cette catégorie').classes('text-center text-muted py-8')
                    return
                
                # Grille d'articles
                with ui.element('div').classes('grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8'):
                    for article in filtered_articles:
                        self.render_article_card(article)
    
    def render_article_card(self, article):
        """Rendre une carte d'article avec classes de thème"""
        with ui.card().classes(theme_manager.get_card_classes(hover=True) + ' cursor-pointer'):
            # Image placeholder
            with ui.element('div').classes('h-48 bg-surface flex items-center justify-center'):
                ui.icon('article').classes('text-4xl text-muted')
            
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
                    
                    ui.label(f"👁 {article['views']}").classes('text-sm text-muted')
    
    def get_filtered_articles(self):
        """Obtenir les articles filtrés"""
        if self.current_category == "all":
            return self.articles
        
        return [a for a in self.articles if a["category"] == self.current_category]
    
    def filter_by_category(self, category):
        """Filtrer par catégorie"""
        self.current_category = category
        # Dans une vraie app, on rechargerait les données
        # Pour l'instant, on simule avec une notification
        ui.notify(f'Filtrage par catégorie: {self.categories[category]}', type='info')
    
    def read_article(self, article):
        """Lire un article"""
        ui.notify(f'Ouverture de l\'article: {article["title"]}', type='info')
        # Dans une vraie app: ui.navigate.to(f'/article/{article["id"]}')