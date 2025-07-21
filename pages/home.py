from nicegui import ui
from core.i18n import i18n, _
from core.theme import theme_manager

class HomePage:
    """Page d'accueil avec système de thème centralisé"""
    
    def __init__(self):
        self.features = [
            {
                'icon': 'article',
                'title': 'Articles spécialisés',
                'description': 'Découvrez des articles rédigés par des professionnels de la santé mentale',
                'url': '/articles'
            },
            {
                'icon': 'description', 
                'title': 'Rapports détaillés',
                'description': 'Consultez des rapports approfondis sur les enjeux de santé mentale',
                'url': '/reports'
            },
            {
                'icon': 'psychology',
                'title': 'Ressources utiles',
                'description': 'Accédez à des outils et ressources pratiques pour votre bien-être',
                'url': '/resources'
            },
            {
                'icon': 'support_agent',
                'title': 'Support 24/7',
                'description': 'Obtenez de l\'aide et des conseils quand vous en avez besoin',
                'url': '/support'
            }
        ]
    
    def render(self):
        """Rendre la page d'accueil"""
        # Section Hero
        self.render_hero_section()
        
        # Section Features
        self.render_features_section()
        
        # Section Stats
        self.render_stats_section()
        
        # Section CTA
        self.render_cta_section()
    
    def render_hero_section(self):
        """Rendre la section héro avec classes de thème"""
        with ui.element('div').classes('w-full py-20 px-4 gradient-hero'):
            with ui.column().classes('text-center max-w-4xl mx-auto text-inverse'):
                ui.label('Prenez soin de votre santé mentale').classes('text-5xl font-bold mb-6')
                ui.label('Accédez à des ressources fiables et des conseils professionnels pour améliorer votre bien-être mental').classes('text-xl mb-8 opacity-90')
                
                with ui.row().classes('gap-4 justify-center flex-wrap'):
                    ui.button(
                        'Explorer maintenant',
                        on_click=lambda: ui.navigate.to('/articles'),
                        icon='explore'
                    ).classes('bg-card text-primary px-8 py-4 rounded-lg font-semibold hover:bg-surface transition-all')
                    
                    ui.button(
                        'En savoir plus',
                        on_click=lambda: ui.navigate.to('/about'),
                        icon='info'
                    ).classes(theme_manager.get_button_classes('outline', 'lg') + ' border-2 border-white text-white hover:bg-white hover:text-primary')
    
    def render_features_section(self):
        """Rendre la section des fonctionnalités avec classes de thème"""
        with ui.element('div').classes('w-full py-20 px-4 bg-surface'):
            with ui.column().classes('page-container mx-auto'):
                # Header
                ui.label('Pourquoi choisir MindCare ?').classes('text-4xl font-bold text-center mb-16 text-main')
                
                # Grille des fonctionnalités
                with ui.element('div').classes('grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8'):
                    for feature in self.features:
                        self.render_feature_card(feature)
    
    def render_feature_card(self, feature):
        """Rendre une carte de fonctionnalité avec classes de thème"""
        with ui.card().classes(theme_manager.get_card_classes(hover=True) + ' p-6 text-center cursor-pointer'):
            # Icône avec couleur de thème
            ui.icon(feature['icon']).classes('text-6xl mb-4 text-primary')
            
            # Titre
            ui.label(feature['title']).classes('text-xl font-bold mb-4 text-main')
            
            # Description
            ui.label(feature['description']).classes('text-muted mb-6 leading-relaxed')
            
            # Bouton avec classes de thème
            ui.button(
                'En savoir plus',
                on_click=lambda url=feature['url']: ui.navigate.to(url),
                icon='arrow_forward'
            ).classes(theme_manager.get_button_classes('primary', 'md'))
    
    def render_stats_section(self):
        """Rendre la section des statistiques avec gradient de thème"""
        with ui.element('div').classes('w-full py-20 px-4 gradient-primary'):
            with ui.column().classes('page-container mx-auto text-inverse'):
                
                # Grille des statistiques
                with ui.element('div').classes('grid grid-cols-2 md:grid-cols-4 gap-8 text-center'):
                    
                    stats = [
                        {'value': '150+', 'label': 'Articles'},
                        {'value': '25+', 'label': 'Rapports'},
                        {'value': '1200+', 'label': 'Utilisateurs'},
                        {'value': '45+', 'label': 'Spécialistes'}
                    ]
                    
                    for stat in stats:
                        with ui.column().classes('p-6'):
                            ui.label(stat['value']).classes('text-5xl font-bold mb-2')
                            ui.label(stat['label']).classes('text-lg opacity-90')
    
    def render_cta_section(self):
        """Rendre la section call-to-action avec classes de thème"""
        with ui.element('div').classes('w-full py-20 px-4 bg-card'):
            with ui.column().classes('max-w-4xl mx-auto text-center'):
                ui.label('Prêt à prendre soin de votre bien-être mental ?').classes('text-4xl font-bold mb-6 text-main')
                ui.label('Commencez votre parcours vers un meilleur équilibre mental dès aujourd\'hui').classes('text-xl text-muted mb-8')
                
                with ui.row().classes('gap-4 justify-center flex-wrap'):
                    ui.button(
                        'Explorer les articles',
                        on_click=lambda: ui.navigate.to('/articles'),
                        icon='article'
                    ).classes(theme_manager.get_button_classes('primary', 'lg'))
                    
                    ui.button(
                        'Nous contacter',
                        on_click=lambda: ui.navigate.to('/contact'),
                        icon='contact_mail'
                    ).classes(theme_manager.get_button_classes('outline', 'lg'))
    
    def render_testimonials_section(self):
        """Section témoignages avec classes de thème"""
        testimonials = [
            {
                'name': 'Dr. Sarah Ahmed',
                'role': 'Psychiatre',
                'text': 'MindCare est une excellente ressource pour mes patients.'
            },
            {
                'name': 'Marc Dubois',
                'role': 'Utilisateur',
                'text': 'J\'ai trouvé des articles très utiles pour comprendre l\'anxiété.'
            },
            {
                'name': 'Fatima El Alami',
                'role': 'Psychologue',
                'text': 'Les rapports sont très bien documentés et fiables.'
            }
        ]
        
        with ui.element('div').classes('w-full py-20 px-4 bg-surface'):
            with ui.column().classes('page-container mx-auto'):
                ui.label('Témoignages').classes('text-4xl font-bold text-center mb-16 text-main')
                
                with ui.element('div').classes('grid grid-cols-1 md:grid-cols-3 gap-8'):
                    for testimonial in testimonials:
                        with ui.card().classes(theme_manager.get_card_classes(hover=True) + ' p-6 text-center'):
                            ui.icon('person').classes('text-4xl mb-4 text-primary')
                            ui.label(f'"{testimonial["text"]}"').classes('text-muted mb-4 italic')
                            ui.label(testimonial['name']).classes('font-semibold text-main')
                            ui.label(testimonial['role']).classes('text-sm text-muted')
    
    def render_additional_features_section(self):
        """Section de fonctionnalités additionnelles avec classes de thème"""
        additional_features = [
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
        
        with ui.element('div').classes('w-full py-16 px-4 bg-surface'):
            with ui.column().classes('page-container'):
                ui.label('Nos Avantages').classes('text-3xl font-bold text-center mb-12 text-main')
                
                with ui.element('div').classes('grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6'):
                    for feature in additional_features:
                        with ui.card().classes(theme_manager.get_card_classes(hover=True) + ' text-center p-6'):
                            ui.icon(feature["icon"]).classes('text-5xl mb-4 text-primary')
                            ui.label(feature["title"]).classes('text-lg font-bold mb-3 text-main')
                            ui.label(feature["description"]).classes('text-muted text-sm leading-relaxed')