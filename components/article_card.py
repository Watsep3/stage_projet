from nicegui import ui
from typing import Dict, Optional, List, Callable
from core.i18n import i18n, _
from datetime import datetime
import json

class ArticleCard:
    """Composant carte d'article réutilisable"""
    
    def __init__(self, article: Dict, 
                 size: str = "medium",
                 show_author: bool = True,
                 show_date: bool = True,
                 show_category: bool = True,
                 show_tags: bool = True,
                 show_stats: bool = True,
                 clickable: bool = True,
                 on_click: Optional[Callable] = None):
        
        self.article = article
        self.size = size
        self.show_author = show_author
        self.show_date = show_date
        self.show_category = show_category
        self.show_tags = show_tags
        self.show_stats = show_stats
        self.clickable = clickable
        self.on_click = on_click
        
        # Configurations selon la taille
        self.size_configs = {
            "small": {
                "max_width": "max-w-xs",
                "image_height": "h-32",
                "title_size": "text-lg",
                "summary_lines": "line-clamp-2",
                "padding": "p-4"
            },
            "medium": {
                "max_width": "max-w-sm",
                "image_height": "h-48",
                "title_size": "text-xl",
                "summary_lines": "line-clamp-3",
                "padding": "p-6"
            },
            "large": {
                "max_width": "max-w-md",
                "image_height": "h-64",
                "title_size": "text-2xl",
                "summary_lines": "line-clamp-4",
                "padding": "p-8"
            }
        }
        
        self.config = self.size_configs.get(size, self.size_configs["medium"])
    
    def get_localized_content(self, field: str) -> str:
        """Obtenir le contenu localisé selon la langue actuelle"""
        current_lang = i18n.get_language()
        
        if current_lang == "en" and f"{field}_en" in self.article:
            return self.article[f"{field}_en"] or self.article[field]
        elif current_lang == "ar" and f"{field}_ar" in self.article:
            return self.article[f"{field}_ar"] or self.article[field]
        else:
            return self.article[field]
    
    def get_localized_tags(self) -> List[str]:
        """Obtenir les tags localisés"""
        current_lang = i18n.get_language()
        
        if current_lang == "en" and "tags_en" in self.article:
            tags_str = self.article["tags_en"]
        elif current_lang == "ar" and "tags_ar" in self.article:
            tags_str = self.article["tags_ar"]
        else:
            tags_str = self.article.get("tags", "[]")
        
        try:
            if isinstance(tags_str, str):
                return json.loads(tags_str)
            elif isinstance(tags_str, list):
                return tags_str
            else:
                return []
        except:
            return []
    
    def format_date(self, date_str: str) -> str:
        """Formater la date selon la locale"""
        try:
            if isinstance(date_str, str):
                date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            else:
                date_obj = date_str
            
            current_lang = i18n.get_language()
            
            if current_lang == "fr":
                return date_obj.strftime("%d %B %Y")
            elif current_lang == "ar":
                return date_obj.strftime("%d/%m/%Y")
            else:  # en
                return date_obj.strftime("%B %d, %Y")
        except:
            return date_str
    
    def get_category_color(self, category: str) -> str:
        """Obtenir la couleur d'une catégorie"""
        colors = {
            "anxiety": "bg-red-100 text-red-800",
            "depression": "bg-blue-100 text-blue-800",
            "stress": "bg-yellow-100 text-yellow-800",
            "wellness": "bg-green-100 text-green-800",
            "therapy": "bg-purple-100 text-purple-800",
            "mindfulness": "bg-indigo-100 text-indigo-800"
        }
        return colors.get(category, "bg-gray-100 text-gray-800")
    
    def get_difficulty_color(self, difficulty: str) -> str:
        """Obtenir la couleur selon la difficulté"""
        colors = {
            "beginner": "bg-green-100 text-green-800",
            "intermediate": "bg-yellow-100 text-yellow-800",
            "advanced": "bg-red-100 text-red-800"
        }
        return colors.get(difficulty, "bg-gray-100 text-gray-800")
    
    def render(self):
        """Rendre la carte d'article"""
        card_classes = f"{self.config['max_width']} theme-surface hover-lift transition-all duration-300"
        
        if self.clickable:
            card_classes += " cursor-pointer"
        
        with ui.card().classes(card_classes) as card:
            if self.clickable and self.on_click:
                card.on('click', lambda: self.on_click(self.article))
            
            # Image
            if self.article.get("image"):
                with ui.row().classes('relative'):
                    ui.image(self.article["image"]).classes(f'w-full {self.config["image_height"]} object-cover')
                    
                    # Badges overlay
                    with ui.column().classes('absolute top-2 right-2 gap-1'):
                        if self.article.get("featured"):
                            ui.chip("⭐ Featured").classes('bg-yellow-500 text-white text-xs')
                        
                        if self.article.get("difficulty"):
                            ui.chip(
                                self.article["difficulty"].title()
                            ).classes(f'{self.get_difficulty_color(self.article["difficulty"])} text-xs')
            
            with ui.card_section().classes(self.config["padding"]):
                # Catégorie
                if self.show_category and self.article.get("category"):
                    ui.chip(
                        _(f"articles.categories.{self.article['category']}")
                    ).classes(f'{self.get_category_color(self.article["category"])} text-xs mb-3')
                
                # Titre
                ui.label(
                    self.get_localized_content("title")
                ).classes(f'{self.config["title_size"]} font-bold theme-text mb-2 {self.config["summary_lines"]}')
                
                # Résumé
                ui.label(
                    self.get_localized_content("summary")
                ).classes(f'theme-text-secondary mb-4 {self.config["summary_lines"]} leading-relaxed')
                
                # Métadonnées
                if self.show_author or self.show_date:
                    with ui.row().classes('items-center gap-4 text-sm theme-text-secondary mb-3'):
                        if self.show_author and self.article.get("author"):
                            with ui.row().classes('items-center gap-1'):
                                ui.icon('person').classes('text-xs')
                                ui.label(self.article["author"])
                        
                        if self.show_date and self.article.get("date"):
                            with ui.row().classes('items-center gap-1'):
                                ui.icon('calendar_today').classes('text-xs')
                                ui.label(self.format_date(self.article["date"]))
                        
                        if self.article.get("read_time"):
                            with ui.row().classes('items-center gap-1'):
                                ui.icon('schedule').classes('text-xs')
                                ui.label(f"{self.article['read_time']} min")
                
                # Tags
                if self.show_tags:
                    tags = self.get_localized_tags()
                    if tags:
                        with ui.row().classes('gap-1 mb-4 flex-wrap'):
                            for tag in tags[:3]:  # Limiter à 3 tags
                                ui.chip(f"#{tag}").classes('text-xs theme-text-secondary bg-gray-100')
                
                # Statistiques
                if self.show_stats:
                    with ui.row().classes('items-center gap-4 text-sm theme-text-secondary mb-4'):
                        if self.article.get("views"):
                            with ui.row().classes('items-center gap-1'):
                                ui.icon('visibility').classes('text-xs')
                                ui.label(f"{self.article['views']:,}")
                        
                        if self.article.get("likes"):
                            with ui.row().classes('items-center gap-1'):
                                ui.icon('favorite').classes('text-xs')
                                ui.label(str(self.article['likes']))
                        
                        if self.article.get("shares"):
                            with ui.row().classes('items-center gap-1'):
                                ui.icon('share').classes('text-xs')
                                ui.label(str(self.article['shares']))
                
                # Actions
                self.render_actions()
        
        return card
    
    def render_actions(self):
        """Rendre les actions de la carte"""
        with ui.row().classes('gap-2'):
            ui.button(
                _("common.read_more"),
                on_click=lambda: self.read_article(),
                icon='article'
            ).classes('bg-primary text-white px-4 py-2 rounded hover:bg-secondary transition-colors')
            
            # Bouton partage
            ui.button(
                icon='share',
                on_click=lambda: self.share_article()
            ).classes('border border-primary text-primary px-3 py-2 rounded hover:bg-primary hover:text-white transition-colors').props('flat')
            
            # Bouton favoris
            ui.button(
                icon='favorite_border',
                on_click=lambda: self.toggle_favorite()
            ).classes('border border-gray-300 text-gray-600 px-3 py-2 rounded hover:bg-gray-100 transition-colors').props('flat')
    
    def read_article(self):
        """Action pour lire l'article"""
        if self.on_click:
            self.on_click(self.article)
        else:
            ui.navigate.to(f'/article/{self.article["id"]}')
    
    def share_article(self):
        """Action pour partager l'article"""
        article_url = f"{ui.context.request.base_url}article/{self.article['id']}"
        
        # Copier l'URL dans le presse-papiers
        ui.run_javascript(f"""
            navigator.clipboard.writeText('{article_url}').then(() => {{
                console.log('URL copiée dans le presse-papiers');
            }});
        """)
        
        ui.notify("Lien copié dans le presse-papiers", type='positive')
    
    def toggle_favorite(self):
        """Action pour ajouter/retirer des favoris"""
        # Ici on pourrait implémenter la logique des favoris
        ui.notify("Ajouté aux favoris", type='positive')

class ArticleCardHorizontal(ArticleCard):
    """Variant horizontal de la carte d'article"""
    
    def render(self):
        """Rendre la carte horizontale"""
        with ui.card().classes('theme-surface hover-lift transition-all duration-300 w-full') as card:
            if self.clickable and self.on_click:
                card.on('click', lambda: self.on_click(self.article))
            
            with ui.row().classes('p-6 gap-6'):
                # Image
                if self.article.get("image"):
                    with ui.column().classes('relative'):
                        ui.image(self.article["image"]).classes('w-32 h-32 object-cover rounded-lg')
                        
                        if self.article.get("featured"):
                            ui.chip("⭐").classes('absolute -top-2 -right-2 bg-yellow-500 text-white text-xs w-6 h-6 rounded-full')
                
                # Contenu
                with ui.column().classes('flex-1'):
                    # Catégorie
                    if self.show_category and self.article.get("category"):
                        ui.chip(
                            _(f"articles.categories.{self.article['category']}")
                        ).classes(f'{self.get_category_color(self.article["category"])} text-xs mb-2')
                    
                    # Titre
                    ui.label(
                        self.get_localized_content("title")
                    ).classes('text-xl font-bold theme-text mb-2 line-clamp-2')
                    
                    # Résumé
                    ui.label(
                        self.get_localized_content("summary")
                    ).classes('theme-text-secondary mb-3 line-clamp-2')
                    
                    # Métadonnées
                    with ui.row().classes('items-center gap-4 text-sm theme-text-secondary mb-3'):
                        if self.show_author and self.article.get("author"):
                            ui.label(f"👤 {self.article['author']}")
                        
                        if self.show_date and self.article.get("date"):
                            ui.label(f"📅 {self.format_date(self.article['date'])}")
                        
                        if self.article.get("read_time"):
                            ui.label(f"⏱️ {self.article['read_time']} min")
                    
                    # Actions
                    with ui.row().classes('gap-2'):
                        ui.button(
                            _("common.read_more"),
                            on_click=lambda: self.read_article()
                        ).classes('bg-primary text-white px-4 py-2 rounded text-sm hover:bg-secondary transition-colors')
        
        return card

class ArticleCardCompact(ArticleCard):
    """Variant compact de la carte d'article"""
    
    def render(self):
        """Rendre la carte compacte"""
        with ui.card().classes('theme-surface hover-lift transition-all duration-300 max-w-xs') as card:
            if self.clickable and self.on_click:
                card.on('click', lambda: self.on_click(self.article))
            
            with ui.card_section().classes('p-4'):
                # Titre
                ui.label(
                    self.get_localized_content("title")
                ).classes('text-lg font-semibold theme-text mb-2 line-clamp-2')
                
                # Métadonnées
                with ui.row().classes('items-center gap-3 text-xs theme-text-secondary mb-3'):
                    if self.article.get("category"):
                        ui.chip(
                            _(f"articles.categories.{self.article['category']}")
                        ).classes(f'{self.get_category_color(self.article["category"])} text-xs')
                    
                    if self.article.get("read_time"):
                        ui.label(f"⏱️ {self.article['read_time']} min")
                
                # Action
                ui.button(
                    _("common.read_more"),
                    on_click=lambda: self.read_article()
                ).classes('bg-primary text-white px-3 py-1 rounded text-sm hover:bg-secondary transition-colors w-full')
        
        return card