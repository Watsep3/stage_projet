from nicegui import ui
from core.i18n import i18n, _
from core.theme import theme_manager
from config.database import SessionLocal, ReportService, Report
from typing import List, Dict, Optional
import json

class ReportsPage:
    """Page des rapports utilisant la base de données"""
    
    def __init__(self):
        self.reports = []
        self.filtered_reports = []
        self.current_page = 1
        self.items_per_page = 4
        self.current_type = "all"
        self.current_sort = "newest"
        self.search_query = ""
        
        self.report_types = {
            "all": "Tous les types",
            "research": "Recherche",
            "survey": "Enquête", 
            "analysis": "Analyse",
            "white_paper": "Livre blanc"
        }
        
        self.sort_options = {
            "newest": "Plus récents",
            "oldest": "Plus anciens",
            "popular": "Plus populaires",
            "title": "Par titre"
        }
        
        # Charger les rapports depuis la base de données
        self.load_reports_from_db()
        self.filter_reports()
    
    def load_reports_from_db(self):
        """Charger les rapports depuis la base de données"""
        try:
            db = SessionLocal()
            db_reports = ReportService.get_all(db)
            
            # Convertir les objets SQLAlchemy en dictionnaires
            self.reports = []
            for report in db_reports:
                report_dict = {
                    "id": report.id,
                    "title": report.title,
                    "description": report.description,
                    "abstract": report.abstract,
                    "type": report.type,
                    "author": report.author,
                    "date": report.date_created.strftime("%Y-%m-%d") if report.date_created else "",
                    "pages": report.pages or 0,
                    "downloads": report.downloads or 0,
                    "file_size": report.file_size or "0 MB",
                    "file_url": report.file_url or "",
                    "cover_image": report.cover_image,
                    "tags": json.loads(report.tags) if report.tags else [],
                    "featured": report.featured or False,
                    "published": report.published or True
                }
                self.reports.append(report_dict)
            
            db.close()
            print(f"✅ {len(self.reports)} rapports chargés depuis la base de données")
            
        except Exception as e:
            print(f"❌ Erreur lors du chargement des rapports: {e}")
            self.reports = []
    
    def get_reports_by_type(self, report_type: str):
        """Obtenir les rapports d'un type spécifique depuis la BDD"""
        if report_type == "all":
            return self.reports
        
        try:
            db = SessionLocal()
            db_reports = ReportService.get_by_type(db, report_type)
            
            filtered_reports = []
            for report in db_reports:
                report_dict = {
                    "id": report.id,
                    "title": report.title,
                    "description": report.description,
                    "abstract": report.abstract,
                    "type": report.type,
                    "author": report.author,
                    "date": report.date_created.strftime("%Y-%m-%d") if report.date_created else "",
                    "pages": report.pages or 0,
                    "downloads": report.downloads or 0,
                    "file_size": report.file_size or "0 MB",
                    "file_url": report.file_url or "",
                    "cover_image": report.cover_image,
                    "tags": json.loads(report.tags) if report.tags else [],
                    "featured": report.featured or False,
                    "published": report.published or True
                }
                filtered_reports.append(report_dict)
            
            db.close()
            return filtered_reports
            
        except Exception as e:
            print(f"❌ Erreur lors du filtrage par type: {e}")
            return []
    
    def get_featured_reports(self):
        """Obtenir les rapports en vedette"""
        try:
            db = SessionLocal()
            db_reports = ReportService.get_featured(db)
            
            featured_reports = []
            for report in db_reports:
                report_dict = {
                    "id": report.id,
                    "title": report.title,
                    "description": report.description,
                    "abstract": report.abstract,
                    "type": report.type,
                    "author": report.author,
                    "date": report.date_created.strftime("%Y-%m-%d") if report.date_created else "",
                    "pages": report.pages or 0,
                    "downloads": report.downloads or 0,
                    "file_size": report.file_size or "0 MB",
                    "file_url": report.file_url or "",
                    "cover_image": report.cover_image,
                    "tags": json.loads(report.tags) if report.tags else [],
                    "featured": report.featured or False,
                    "published": report.published or True
                }
                featured_reports.append(report_dict)
            
            db.close()
            return featured_reports
            
        except Exception as e:
            print(f"❌ Erreur lors du chargement des rapports en vedette: {e}")
            return []
    
    def search_reports(self, query: str):
        """Rechercher des rapports dans la base de données"""
        if not query.strip():
            return self.reports
        
        # Recherche simple dans le titre, description et tags
        query_lower = query.lower()
        results = []
        
        for report in self.reports:
            if (query_lower in report["title"].lower() or 
                query_lower in report["description"].lower() or
                (report["abstract"] and query_lower in report["abstract"].lower()) or
                any(query_lower in tag.lower() for tag in report["tags"])):
                results.append(report)
        
        return results
    
    def filter_reports(self):
        """Filtrer les rapports selon les critères"""
        filtered = self.reports.copy()
        
        # Filtrer par type
        if self.current_type != "all":
            filtered = [r for r in filtered if r["type"] == self.current_type]
        
        # Filtrer par recherche
        if self.search_query:
            filtered = self.search_reports(self.search_query)
            if self.current_type != "all":
                filtered = [r for r in filtered if r["type"] == self.current_type]
        
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
        with ui.column().classes('gradient-hero py-16 px-4'):
            with ui.column().classes('max-w-4xl mx-auto text-center text-inverse'):
                ui.label("Rapports").classes('text-5xl font-bold mb-4')
                ui.label("Découvrez nos rapports et études en santé mentale").classes('text-xl opacity-90')
    
    def render_filters(self):
        """Rendre les filtres principaux"""
        with ui.row().classes('max-w-7xl mx-auto px-4 py-6 gap-4 flex-wrap items-center bg-card'):
            # Recherche
            search_input = ui.input(
                placeholder="Rechercher dans les rapports...",
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
                label="Trier par"
            ).classes('w-48')
            sort_select.on('change', lambda e: self.on_sort_change(e.value))
    
    def render_sidebar(self):
        """Rendre la sidebar"""
        with ui.card().classes(theme_manager.get_card_classes()):
            with ui.card_section().classes('p-6'):
                ui.label("Statistiques").classes('text-lg font-semibold text-main mb-4')
                
                # Stats générales
                total_reports = len(self.reports)
                total_downloads = sum(r["downloads"] for r in self.reports)
                total_pages = sum(r["pages"] for r in self.reports)
                
                with ui.column().classes('gap-3'):
                    with ui.row().classes('items-center gap-2'):
                        ui.icon('description').classes('text-primary')
                        ui.label(f"{total_reports} rapports").classes('text-main')
                    
                    with ui.row().classes('items-center gap-2'):
                        ui.icon('download').classes('text-primary')
                        ui.label(f"{total_downloads:,} téléchargements").classes('text-main')
                    
                    with ui.row().classes('items-center gap-2'):
                        ui.icon('menu_book').classes('text-primary')
                        ui.label(f"{total_pages:,} pages au total").classes('text-main')
                
                ui.separator().classes('my-4')
                
                # Types de rapports
                ui.label("Types").classes('font-medium text-main mb-2')
                
                type_counts = {}
                for report in self.reports:
                    type_counts[report["type"]] = type_counts.get(report["type"], 0) + 1
                
                with ui.column().classes('gap-1'):
                    for type_key, count in type_counts.items():
                        type_name = self.report_types.get(type_key, type_key)
                        ui.button(
                            f"{type_name} ({count})",
                            on_click=lambda t=type_key: self.filter_by_type(t)
                        ).classes('text-left justify-start text-sm text-muted hover:text-primary').props('flat')
    
    def render_reports_grid(self):
        """Rendre la grille des rapports"""
        reports = self.get_paginated_reports()
        
        if not reports:
            self.render_empty_state()
            return
        
        # Info pagination
        total_filtered = len(self.filtered_reports)
        start_item = (self.current_page - 1) * self.items_per_page + 1
        end_item = min(self.current_page * self.items_per_page, total_filtered)
        
        ui.label(f'Affichage de {start_item}-{end_item} sur {total_filtered} rapports').classes('text-sm text-muted mb-6')
        
        with ui.column().classes('gap-6'):
            for report in reports:
                self.render_report_card(report)
    
    def render_report_card(self, report: Dict):
        """Rendre une carte de rapport"""
        with ui.card().classes(theme_manager.get_card_classes(hover=True)):
            with ui.row().classes('p-6 gap-6'):
                # Image de couverture ou placeholder
                if report.get("cover_image"):
                    ui.image(report["cover_image"]).classes('w-32 h-40 object-cover rounded-lg shadow-md')
                else:
                    with ui.column().classes('w-32 h-40 bg-surface rounded-lg items-center justify-center'):
                        ui.icon('description').classes('text-4xl text-muted')
                
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
                                    ui.chip("⭐ En vedette", color='accent').classes('text-xs')
                            
                            # Titre
                            ui.label(report["title"]).classes('text-2xl font-bold text-main mb-2 line-clamp-2')
                            
                            # Auteur et date
                            with ui.row().classes('items-center gap-4 text-sm text-muted mb-3'):
                                ui.label(f"👤 {report['author']}")
                                ui.label(f"📅 {report['date']}")
                        
                        # Métriques
                        with ui.column().classes('text-right'):
                            ui.label(f"📊 {report['downloads']:,} téléchargements").classes('text-sm text-muted')
                            ui.label(f"📄 {report['pages']} pages").classes('text-sm text-muted')
                            ui.label(f"💾 {report['file_size']}").classes('text-sm text-muted')
                    
                    # Description
                    ui.label(report["description"]).classes('text-muted mb-4 line-clamp-2')
                    
                    # Abstract (si disponible)
                    if report.get("abstract"):
                        ui.label(report["abstract"]).classes('text-muted text-sm mb-4 line-clamp-3')
                    
                    # Tags
                    with ui.row().classes('gap-1 mb-4 flex-wrap'):
                        for tag in report["tags"][:4]:
                            ui.chip(f"#{tag}").classes('text-xs text-muted bg-surface')
                    
                    # Actions
                    with ui.row().classes('gap-3'):
                        ui.button(
                            "Télécharger",
                            on_click=lambda r=report: self.download_report(r),
                            icon='download'
                        ).classes(theme_manager.get_button_classes('primary', 'md'))
                        
                        ui.button(
                            "Aperçu",
                            on_click=lambda r=report: self.view_report(r),
                            icon='visibility'
                        ).classes(theme_manager.get_button_classes('outline', 'md'))
    
    def render_empty_state(self):
        """Rendre l'état vide"""
        with ui.column().classes('items-center justify-center py-16 text-center'):
            ui.icon('description').classes('text-6xl text-muted mb-4')
            ui.label("Aucun rapport trouvé").classes('text-xl text-muted mb-4')
            ui.button(
                "Voir tous les rapports",
                on_click=self.reset_filters
            ).classes(theme_manager.get_button_classes('primary', 'md'))
    
    def render_pagination(self):
        """Rendre la pagination simple"""
        total_pages = self.get_total_pages()
        
        with ui.row().classes('justify-center items-center gap-4 mt-8'):
            # Bouton précédent
            ui.button(
                "Précédent",
                on_click=lambda: self.change_page(self.current_page - 1),
                icon='chevron_left'
            ).classes('').props('outline').set_enabled(self.current_page > 1)
            
            # Numéros de page
            for page in range(max(1, self.current_page - 2), min(total_pages + 1, self.current_page + 3)):
                if page == self.current_page:
                    ui.button(
                        str(page),
                        on_click=lambda p=page: self.change_page(p)
                    ).classes(theme_manager.get_button_classes('primary', 'md'))
                else:
                    ui.button(
                        str(page),
                        on_click=lambda p=page: self.change_page(p)
                    ).classes('').props('outline')
            
            # Bouton suivant
            ui.button(
                "Suivant",
                on_click=lambda: self.change_page(self.current_page + 1),
                icon='chevron_right'
            ).classes('').props('outline').set_enabled(self.current_page < total_pages)
            
            # Info page
            ui.label(f'Page {self.current_page} sur {total_pages}').classes('text-sm text-muted ml-4')
    
    def change_page(self, page: int):
        """Changer de page"""
        if 1 <= page <= self.get_total_pages():
            self.current_page = page
            ui.notify(f'Page {page}', type='info')
    
    def on_search_change(self, query: str):
        """Gérer le changement de recherche"""
        self.search_query = query
        self.filter_reports()
        ui.notify('Recherche mise à jour', type='info')
    
    def on_type_change(self, report_type: str):
        """Gérer le changement de type"""
        self.current_type = report_type
        self.filter_reports()
        ui.notify(f'Filtrage par type: {self.report_types[report_type]}', type='info')
    
    def on_sort_change(self, sort_option: str):
        """Gérer le changement de tri"""
        self.current_sort = sort_option
        self.filter_reports()
        ui.notify(f'Tri: {self.sort_options[sort_option]}', type='info')
    
    def filter_by_type(self, report_type: str):
        """Filtrer par type depuis la sidebar"""
        self.current_type = report_type
        self.filter_reports()
        ui.notify(f'Filtrage par type: {self.report_types[report_type]}', type='info')
    
    def reset_filters(self):
        """Réinitialiser tous les filtres"""
        self.current_type = "all"
        self.current_sort = "newest"
        self.search_query = ""
        self.current_page = 1
        self.filter_reports()
        ui.notify('Filtres réinitialisés', type='info')
    
    def download_report(self, report: Dict):
        """Télécharger un rapport"""
        # Incrémenter le nombre de téléchargements dans la BDD
        self.increment_report_downloads(report["id"])
        
        # Simuler le téléchargement
        ui.notify(f"Téléchargement de '{report['title']}' commencé", type='positive')
        
        # Dans une vraie application, on déclencherait le téléchargement
        if report.get('file_url'):
            ui.run_javascript(f"""
                const link = document.createElement('a');
                link.href = '{report['file_url']}';
                link.download = '{report['title']}.pdf';
                link.click();
            """)
    
    def view_report(self, report: Dict):
        """Voir un rapport"""
        ui.notify(f"Aperçu de '{report['title']}'", type='info')
        # Dans une vraie app: ui.navigate.to(f'/report/{report["id"]}')
    
    def increment_report_downloads(self, report_id: int):
        """Incrémenter le nombre de téléchargements d'un rapport"""
        try:
            db = SessionLocal()
            report = db.query(Report).filter_by(id=report_id).first()
            if report:
                report.downloads = (report.downloads or 0) + 1
                db.commit()
                print(f"✅ Téléchargements incrémentés pour le rapport {report_id}")
            db.close()
        except Exception as e:
            print(f"❌ Erreur lors de l'incrémentation des téléchargements: {e}")