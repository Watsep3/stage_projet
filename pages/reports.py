from nicegui import ui
from core.i18n import i18n, _
from core.components import Card, Button, Pagination
from typing import List, Dict, Optional
import json
from pathlib import Path

class ReportsPage:
    """Page des rapports"""
    
    def __init__(self):
        self.reports = self.load_reports()
        self.filtered_reports = self.reports.copy()
        self.current_page = 1
        self.items_per_page = 4
        self.current_type = "all"
        self.current_sort = "newest"
        self.search_query = ""
        
        self.report_types = {
            "all": _("articles.filters.all"),
            "research": _("reports.types.research"),
            "survey": _("reports.types.survey"),
            "analysis": _("reports.types.analysis"),
            "white_paper": _("reports.types.white_paper")
        }
        
        self.sort_options = {
            "newest": _("articles.sort.newest"),
            "oldest": _("articles.sort.oldest"),
            "popular": _("articles.sort.popular"),
            "title": _("articles.sort.title")
        }
    
    def load_reports(self) -> List[Dict]:
        """Charger les rapports depuis le fichier JSON"""
        reports_file = Path("data/reports.json")
        
        if reports_file.exists():
            try:
                with open(reports_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Erreur lors du chargement des rapports: {e}")
        
        # Rapports d'exemple si le fichier n'existe pas
        return [
            {
                "id": 1,
                "title": "État de la santé mentale au Maroc 2024",
                "description": "Rapport complet sur l'état de la santé mentale au Maroc avec statistiques et analyses.",
                "type": "research",
                "author": "Institut National de Recherche",
                "date": "2024-01-20",
                "pages": 156,
                "downloads": 2500,
                "file_size": "12.5 MB",
                "file_url": "/static/reports/mental_health_morocco_2024.pdf",
                "cover_image": "/static/images/report1.jpg",
                "tags": ["statistiques", "Maroc", "santé mentale", "recherche"],
                "featured": True,
                "abstract": "Ce rapport présente une analyse complète de l'état de la santé mentale au Maroc..."
            },
            {
                "id": 2,
                "title": "Enquête sur l'anxiété chez les étudiants",
                "description": "Étude approfondie sur les niveaux d'anxiété chez les étudiants universitaires.",
                "type": "survey",
                "author": "Dr. Fatima Bennani",
                "date": "2024-01-15",
                "pages": 89,
                "downloads": 1800,
                "file_size": "8.2 MB",
                "file_url": "/static/reports/student_anxiety_survey.pdf",
                "cover_image": "/static/images/report2.jpg",
                "tags": ["anxiété", "étudiants", "enquête", "université"],
                "featured": False,
                "abstract": "Cette enquête examine les facteurs contribuant à l'anxiété chez les étudiants..."
            },
            {
                "id": 3,
                "title": "Analyse des troubles du sommeil",
                "description": "Rapport détaillé sur les troubles du sommeil et leur impact sur la santé mentale.",
                "type": "analysis",
                "author": "Centre du Sommeil",
                "date": "2024-01-10",
                "pages": 123,
                "downloads": 1200,
                "file_size": "15.8 MB",
                "file_url": "/static/reports/sleep_disorders_analysis.pdf",
                "cover_image": "/static/images/report3.jpg",
                "tags": ["sommeil", "troubles", "analyse", "santé"],
                "featured": True,
                "abstract": "Une analyse approfondie des troubles du sommeil les plus courants..."
            },
            {
                "id": 4,
                "title": "Livre blanc: Télémédecine en santé mentale",
                "description": "Guide complet sur l'implémentation de la télémédecine en santé mentale.",
                "type": "white_paper",
                "author": "Association des Psychologues",
                "date": "2024-01-05",
                "pages": 67,
                "downloads": 950,
                "file_size": "6.4 MB",
                "file_url": "/static/reports/telemedicine_white_paper.pdf",
                "cover_image": "/static/images/report4.jpg",
                "tags": ["télémédecine", "technologie", "innovation", "guide"],
                "featured": False,
                "abstract": "Ce livre blanc explore les opportunités et défis de la télémédecine..."
            },
            {
                "id": 5,
                "title": "Recherche sur la dépression post-partum",
                "description": "Étude sur la prévalence et les traitements de la dépression post-partum.",
                "type": "research",
                "author": "Dr. Amina Tazi",
                "date": "2023-12-28",
                "pages": 201,
                "downloads": 3200,
                "file_size": "18.7 MB",
                "file_url": "/static/reports/postpartum_depression_research.pdf",
                "cover_image": "/static/images/report5.jpg",
                "tags": ["dépression", "post-partum", "maternité", "recherche"],
                "featured": True,
                "abstract": "Cette recherche examine les facteurs de risque et les interventions..."
            }
        ]
    
    def filter_reports(self):
        """Filtrer les rapports selon les critères"""
        filtered = self.reports.copy()
        
        # Filtrer par type
        if self.current_type != "all":
            filtered = [r for r in filtered if r["type"] == self.current_type]
        
        # Filtrer par recherche
        if self.search_query:
            query = self.search_query.lower()
            filtered = [r for r in filtered if 
                       query in r["title"].lower() or 
                       query in r["description"].lower() or 
                       any(query in tag.lower() for tag in r["tags"])]
        
        # Trier
        if self.current_sort == "newest":
            filtered.sort(key=lambda x: x["date"], reverse=True)
        elif self.current_sort == "oldest":
            filtered.sort(key=lambda x: x["date"])
        elif self.current_sort == "popular":
            filtered.sort(key=lambda x: x["downloads"], reverse=True)
        elif self.current_sort == "title":
            filtered.sort(key=lambda x: x["title"])
        
        self.filtered_reports = filtered
        self.current_page = 1
    
    def get_paginated_reports(self) -> List[Dict]:
        """Obtenir les rapports de la page courante"""
        start_idx = (self.current_page - 1) * self.items_per_page
        end_idx = start_idx + self.items_per_page
        return self.filtered_reports[start_idx:end_idx]
    
    def get_total_pages(self) -> int:
        """Obtenir le nombre total de pages"""
        return max(1, (len(self.filtered_reports) + self.items_per_page - 1) // self.items_per_page)
    
    def render(self):
        """Rendre la page des rapports"""
        # Header
        self.render_header()
        
        # Filtres et recherche
        self.render_filters()
        
        # Contenu principal
        with ui.row().classes('max-w-7xl mx-auto px-4 py-8 gap-8'):
            # Sidebar
            with ui.column().classes('w-64 hidden lg:block'):
                self.render_sidebar()
            
            # Rapports
            with ui.column().classes('flex-1'):
                self.render_reports_grid()
                
                # Pagination
                if self.get_total_pages() > 1:
                    self.render_pagination()
    
    def render_header(self):
        """Rendre l'en-tête de la page"""
        with ui.column().classes('theme-gradient py-16 px-4'):
            with ui.column().classes('max-w-4xl mx-auto text-center'):
                ui.label(_("reports.title")).classes('text-5xl font-bold text-white mb-4')
                ui.label(_("reports.subtitle")).classes('text-xl text-white opacity-90')
    
    def render_filters(self):
        """Rendre les filtres principaux"""
        with ui.row().classes('max-w-7xl mx-auto px-4 py-6 gap-4 flex-wrap items-center'):
            # Recherche
            search_input = ui.input(
                placeholder=_("common.search"),
                value=self.search_query
            ).classes('flex-1 min-w-64')
            search_input.on('input', lambda e: self.on_search_change(e.value))
            
            # Type
            type_select = ui.select(
                options=self.report_types,
                value=self.current_type,
                label="Type de rapport"
            ).classes('w-48')
            type_select.on('change', lambda e: self.on_type_change(e.value))
            
            # Tri
            sort_select = ui.select(
                options=self.sort_options,
                value=self.current_sort,
                label=_("common.sort")
            ).classes('w-48')
            sort_select.on('change', lambda e: self.on_sort_change(e.value))
    
    def render_sidebar(self):
        """Rendre la sidebar"""
        with ui.card().classes('w-full theme-surface'):
            with ui.card_section().classes('p-6'):
                ui.label("Statistiques").classes('text-lg font-semibold theme-text mb-4')
                
                # Stats générales
                total_reports = len(self.reports)
                total_downloads = sum(r["downloads"] for r in self.reports)
                
                with ui.column().classes('gap-3'):
                    with ui.row().classes('items-center gap-2'):
                        ui.icon('description').classes('text-primary')
                        ui.label(f"{total_reports} rapports").classes('theme-text')
                    
                    with ui.row().classes('items-center gap-2'):
                        ui.icon('download').classes('text-primary')
                        ui.label(f"{total_downloads:,} téléchargements").classes('theme-text')
                
                ui.separator().classes('my-4')
                
                # Types de rapports
                ui.label("Types").classes('font-medium theme-text mb-2')
                
                type_counts = {}
                for report in self.reports:
                    type_counts[report["type"]] = type_counts.get(report["type"], 0) + 1
                
                with ui.column().classes('gap-1'):
                    for type_key, count in type_counts.items():
                        type_name = self.report_types.get(type_key, type_key)
                        ui.button(
                            f"{type_name} ({count})",
                            on_click=lambda t=type_key: self.filter_by_type(t)
                        ).classes('text-left justify-start text-sm theme-text-secondary hover:text-primary').props('flat')
    
    def render_reports_grid(self):
        """Rendre la grille des rapports"""
        reports = self.get_paginated_reports()
        
        if not reports:
            self.render_empty_state()
            return
        
        with ui.column().classes('gap-6'):
            for report in reports:
                self.render_report_card(report)
    
    def render_report_card(self, report: Dict):
        """Rendre une carte de rapport"""
        with ui.card().classes('theme-surface hover-lift transition-all duration-300'):
            with ui.row().classes('p-6 gap-6'):
                # Image de couverture
                if report.get("cover_image"):
                    ui.image(report["cover_image"]).classes('w-32 h-40 object-cover rounded-lg shadow-md')
                else:
                    with ui.column().classes('w-32 h-40 bg-gray-200 rounded-lg items-center justify-center'):
                        ui.icon('description').classes('text-4xl text-gray-500')
                
                # Contenu
                with ui.column().classes('flex-1'):
                    # Header
                    with ui.row().classes('items-start justify-between mb-2'):
                        with ui.column().classes('flex-1'):
                            # Type et featured
                            with ui.row().classes('items-center gap-2 mb-2'):
                                ui.chip(
                                    self.report_types.get(report["type"], report["type"]),
                                    color='primary'
                                ).classes('text-xs')
                                
                                if report.get("featured"):
                                    ui.chip("Featured", color='accent').classes('text-xs')
                            
                            # Titre
                            ui.label(report["title"]).classes('text-2xl font-bold theme-text mb-2')
                            
                            # Auteur et date
                            with ui.row().classes('items-center gap-4 text-sm theme-text-secondary mb-3'):
                                ui.label(f"👤 {report['author']}")
                                ui.label(f"📅 {report['date']}")
                        
                        # Métriques
                        with ui.column().classes('text-right'):
                            ui.label(f"📊 {report['downloads']:,} téléchargements").classes('text-sm theme-text-secondary')
                            ui.label(f"📄 {report['pages']} pages").classes('text-sm theme-text-secondary')
                            ui.label(f"💾 {report['file_size']}").classes('text-sm theme-text-secondary')
                    
                    # Description
                    ui.label(report["description"]).classes('theme-text-secondary mb-4 line-clamp-2')
                    
                    # Abstract (si disponible)
                    if report.get("abstract"):
                        ui.label(report["abstract"]).classes('theme-text-secondary text-sm mb-4 line-clamp-3')
                    
                    # Tags
                    with ui.row().classes('gap-1 mb-4 flex-wrap'):
                        for tag in report["tags"][:4]:
                            ui.chip(f"#{tag}").classes('text-xs theme-text-secondary')
                    
                    # Actions
                    with ui.row().classes('gap-3'):
                        ui.button(
                            _("reports.card.download"),
                            on_click=lambda r=report: self.download_report(r),
                            icon='download'
                        ).classes('bg-primary text-white px-4 py-2 rounded hover:bg-secondary transition-colors')
                        
                        ui.button(
                            _("reports.card.view"),
                            on_click=lambda r=report: self.view_report(r),
                            icon='visibility'
                        ).classes('border border-primary text-primary px-4 py-2 rounded hover:bg-primary hover:text-white transition-colors')
    
    def render_empty_state(self):
        """Rendre l'état vide"""
        with ui.column().classes('items-center justify-center py-16 text-center'):
            ui.icon('description').classes('text-6xl theme-text-secondary mb-4')
            ui.label(_("reports.empty")).classes('text-xl theme-text-secondary mb-4')
            ui.button(
                "Voir tous les rapports",
                on_click=self.reset_filters
            ).classes('bg-primary text-white px-6 py-3 rounded-lg hover:bg-secondary transition-colors')
    
    def render_pagination(self):
        """Rendre la pagination"""
        with ui.row().classes('justify-center mt-8'):
            pagination = Pagination(
                current_page=self.current_page,
                total_pages=self.get_total_pages(),
                on_page_change=self.on_page_change
            )
            pagination.render()
    
    def on_search_change(self, query: str):
        """Gérer le changement de recherche"""
        self.search_query = query
        self.filter_reports()
        self.update_reports_display()
    
    def on_type_change(self, report_type: str):
        """Gérer le changement de type"""
        self.current_type = report_type
        self.filter_reports()
        self.update_reports_display()
    
    def on_sort_change(self, sort_option: str):
        """Gérer le changement de tri"""
        self.current_sort = sort_option
        self.filter_reports()
        self.update_reports_display()
    
    def on_page_change(self, page: int):
        """Gérer le changement de page"""
        self.current_page = page
        self.update_reports_display()
    
    def filter_by_type(self, report_type: str):
        """Filtrer par type"""
        self.current_type = report_type
        self.filter_reports()
        self.update_reports_display()
    
    def reset_filters(self):
        """Réinitialiser tous les filtres"""
        self.current_type = "all"
        self.current_sort = "newest"
        self.search_query = ""
        self.current_page = 1
        self.filter_reports()
        self.update_reports_display()
    
    def download_report(self, report: Dict):
        """Télécharger un rapport"""
        # Simuler le téléchargement
        ui.notify(f"Téléchargement de '{report['title']}' commencé", type='positive')
        
        # Dans une vraie application, on déclencherait le téléchargement
        ui.run_javascript(f"""
            const link = document.createElement('a');
            link.href = '{report['file_url']}';
            link.download = '{report['title']}.pdf';
            link.click();
        """)
    
    def view_report(self, report: Dict):
        """Voir un rapport"""
        # Naviguer vers la page de visualisation du rapport
        ui.navigate.to(f'/report/{report["id"]}')
    
    def update_reports_display(self):
        """Mettre à jour l'affichage des rapports"""
        # Solution temporaire - dans une vraie application, on utiliserait un système de state
        ui.run_javascript('window.location.reload()')