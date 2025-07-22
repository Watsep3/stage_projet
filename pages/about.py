from nicegui import ui
from core.i18n import i18n, _
from core.theme import theme_manager

class AboutPage:
    """Page à propos avec système de thème centralisé corrigé"""
    
    def __init__(self):
        self.team_members = [
            {
                "name": "Dr. Sarah Ahmed",
                "role": "Directrice Médicale",
                "description": "Psychiatre avec 15 ans d'expérience en santé mentale communautaire.",
                "specialties": ["Psychiatrie", "Anxiété", "Dépression"]
            },
            {
                "name": "Dr. Marc Dubois", 
                "role": "Psychologue Clinicien",
                "description": "Spécialiste en thérapie cognitive comportementale et gestion du stress.",
                "specialties": ["TCC", "Stress", "Trauma"]
            },
            {
                "name": "Fatima El Alami",
                "role": "Responsable Recherche", 
                "description": "Docteure en psychologie, spécialisée dans la recherche en santé mentale.",
                "specialties": ["Recherche", "Mindfulness", "Bien-être"]
            }
        ]
        
        self.values = [
            {
                "title": "Accessibilité",
                "description": "Rendre les ressources de santé mentale accessibles à tous",
                "icon": "accessible"
            },
            {
                "title": "Qualité",
                "description": "Fournir du contenu de haute qualité basé sur la recherche",
                "icon": "verified"
            },
            {
                "title": "Empathie",
                "description": "Approche empathique et bienveillante dans tous nos services",
                "icon": "favorite"
            },
            {
                "title": "Innovation",
                "description": "Utiliser la technologie pour améliorer les soins de santé mentale",
                "icon": "innovation"
            }
        ]
    
    def render(self):
        """Rendre la page à propos"""
        # Header
        self.render_header()
        
        # Mission
        self.render_mission_section()
        
        # Values
        self.render_values_section()
        
        # Team
        self.render_team_section()
        
        # CTA
        self.render_cta_section()
    
    def render_header(self):
        """Rendre l'en-tête avec gradient de thème"""
        with ui.element('div').classes('w-full py-20 px-4 gradient-hero'):
            with ui.column().classes('page-container text-center text-inverse'):
                ui.label('À propos').classes('text-5xl font-bold mb-4')
                ui.label('Découvrez notre mission et notre équipe').classes('text-xl opacity-90')
    
    def render_mission_section(self):
        """Rendre la section mission"""
        with ui.element('div').classes('w-full py-20 px-4 bg-card'):
            with ui.column().classes('page-container'):
                
                # Version responsive : colonne sur mobile, row sur desktop
                with ui.element('div').classes('flex flex-col lg:flex-row gap-12 items-center'):
                    
                    # Texte - prend toute la largeur sur mobile, moitié sur desktop
                    with ui.column().classes('w-full lg:w-1/2 lg:pr-8'):
                        ui.label('Notre Mission').classes('text-4xl font-bold mb-6 text-main')
                        ui.label('Améliorer l\'accès aux ressources de santé mentale et sensibiliser le public à l\'importance du bien-être psychologique.').classes('text-lg text-muted leading-relaxed mb-8')
                        
                        # Statistiques en grid responsive
                        with ui.element('div').classes('grid grid-cols-2 sm:grid-cols-3 gap-6 mt-8'):
                            with ui.column().classes('text-center'):
                                ui.label('150+').classes('text-3xl font-bold text-primary')
                                ui.label('Articles').classes('text-muted text-sm')
                            
                            with ui.column().classes('text-center'):
                                ui.label('25+').classes('text-3xl font-bold text-primary')
                                ui.label('Rapports').classes('text-muted text-sm')
                            
                            with ui.column().classes('text-center'):
                                ui.label('1200+').classes('text-3xl font-bold text-primary')
                                ui.label('Utilisateurs').classes('text-muted text-sm')
                    
                    # Image/Illustration - prend toute la largeur sur mobile, moitié sur desktop
                    with ui.column().classes('w-full lg:w-1/2'):
                        with ui.element('div').classes('h-80 bg-surface rounded-2xl flex items-center justify-center shadow-lg'):
                            with ui.column().classes('text-center'):
                                ui.icon('psychology').classes('text-8xl mb-4 text-primary')
                                ui.label('Santé Mentale').classes('text-2xl font-bold text-main')
                                ui.label('Notre expertise à votre service').classes('text-muted')
    
    def render_values_section(self):
        """Rendre la section valeurs"""
        with ui.element('div').classes('w-full py-20 px-4 bg-surface'):
            with ui.column().classes('page-container'):
                ui.label('Nos Valeurs').classes('text-4xl font-bold text-center mb-16 text-main')
                
                # Grid responsive pour les valeurs
                with ui.element('div').classes('grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8'):
                    for value in self.values:
                        self.render_value_card(value)
    
    def render_value_card(self, value):
        """Rendre une carte de valeur"""
        with ui.card().classes(theme_manager.get_card_classes(hover=True) + ' text-center p-8'):
            ui.icon(value["icon"]).classes('text-6xl mb-6 text-primary')
            ui.label(value["title"]).classes('text-2xl font-bold mb-4 text-main')
            ui.label(value["description"]).classes('text-muted leading-relaxed')
    
    def render_team_section(self):
        """Rendre la section équipe"""
        with ui.element('div').classes('w-full py-20 px-4 bg-card'):
            with ui.column().classes('page-container'):
                ui.label('Notre Équipe').classes('text-4xl font-bold text-center mb-6 text-main')
                ui.label('Une équipe de professionnels dévoués à votre bien-être').classes('text-lg text-center text-muted mb-16')
                
                # Grid responsive pour l'équipe
                with ui.element('div').classes('grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8'):
                    for member in self.team_members:
                        self.render_team_member_card(member)
    
    def render_team_member_card(self, member):
        """Rendre une carte de membre de l'équipe"""
        with ui.card().classes(theme_manager.get_card_classes(hover=True) + ' text-center overflow-hidden'):
            # Image placeholder avec gradient
            with ui.element('div').classes('h-64 bg-surface flex items-center justify-center'):
                ui.icon('person').classes('text-8xl text-primary')
            
            with ui.card_section().classes('p-6'):
                ui.label(member["name"]).classes('text-xl font-bold mb-2 text-main')
                ui.label(member["role"]).classes('font-semibold mb-4 text-primary')
                ui.label(member["description"]).classes('text-muted mb-4 leading-relaxed text-sm')
                
                # Spécialités avec style amélioré
                ui.label('Spécialités').classes('font-semibold text-main mb-3 text-sm')
                with ui.row().classes('gap-2 justify-center flex-wrap'):
                    for specialty in member["specialties"]:
                        ui.chip(specialty).classes('text-xs px-3 py-1 bg-surface text-primary border border-primary')
    
    def render_cta_section(self):
        """Rendre la section call-to-action avec gradient"""
        with ui.element('div').classes('w-full py-20 px-4 gradient-primary'):
            with ui.column().classes('page-container text-center text-inverse'):
                ui.label('Rejoignez Notre Mission').classes('text-4xl font-bold mb-6')
                ui.label('Ensemble, nous pouvons faire la différence dans la santé mentale.').classes('text-xl mb-8 opacity-90')
                
                # Boutons responsive
                with ui.element('div').classes('flex flex-col sm:flex-row gap-4 justify-center items-center'):
                    ui.button(
                        'Nous Contacter',
                        on_click=lambda: ui.navigate.to('/contact'),
                        icon='contact_mail'
                    ).classes('bg-card text-primary px-8 py-4 rounded-lg font-semibold hover:bg-surface transition-all w-full sm:w-auto shadow-lg')
                    
                    ui.button(
                        'Voir Nos Articles',
                        on_click=lambda: ui.navigate.to('/articles'),
                        icon='article'
                    ).classes('border-2 border-white text-white px-8 py-4 rounded-lg font-semibold hover:bg-white hover:text-primary transition-all w-full sm:w-auto')
    
    def render_additional_info_section(self):
        """Section additionnelle avec plus d'informations"""
        with ui.element('div').classes('w-full py-16 px-4 bg-surface'):
            with ui.column().classes('page-container'):
                ui.label('Pourquoi MindCare ?').classes('text-3xl font-bold text-center mb-12 text-main')
                
                # Avantages en grid
                advantages = [
                    {
                        "icon": "verified_user",
                        "title": "Expertise Reconnue",
                        "description": "Une équipe de professionnels certifiés avec des années d'expérience"
                    },
                    {
                        "icon": "schedule",
                        "title": "Disponibilité 24/7",
                        "description": "Des ressources accessibles à tout moment pour votre bien-être"
                    },
                    {
                        "icon": "security",
                        "title": "Confidentialité Garantie",
                        "description": "Vos données et votre vie privée sont notre priorité absolue"
                    },
                    {
                        "icon": "trending_up",
                        "title": "Approche Moderne",
                        "description": "Méthodes thérapeutiques basées sur les dernières recherches"
                    }
                ]
                
                with ui.element('div').classes('grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6'):
                    for advantage in advantages:
                        with ui.card().classes(theme_manager.get_card_classes(hover=True) + ' text-center p-6'):
                            ui.icon(advantage["icon"]).classes('text-5xl mb-4 text-primary')
                            ui.label(advantage["title"]).classes('text-lg font-bold mb-3 text-main')
                            ui.label(advantage["description"]).classes('text-muted text-sm leading-relaxed')