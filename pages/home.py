from nicegui import ui
from core.theme import theme_manager

class HomePage:
    """Page d'accueil avec système de thème centralisé corrigé"""
    
    def __init__(self):
        self.features = [
            {
                'icon': 'article',
                'title_key': 'home.features.articles.title',
                'description_key': 'home.features.articles.description',
                'url': '/articles'
            },
            {
                'icon': 'description', 
                'title_key': 'home.features.reports.title',
                'description_key': 'home.features.reports.description',
                'url': '/reports'
            },
            {
                'icon': 'psychology',
                'title_key': 'home.features.resources.title',
                'description_key': 'home.features.resources.description',
                'url': '/resources'
            },
            {
                'icon': 'support_agent',
                'title_key': 'home.features.support.title',
                'description_key': 'home.features.support.description',
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
        """Rendre la section héro avec gradient de thème"""
        try:
            from core.i18n import _
        except:
            def _(key): return key.split('.')[-1].replace('_', ' ').title()
        
        with ui.element('div').classes('w-full py-20 px-4 gradient-hero'):
            with ui.column().classes('text-center max-w-4xl mx-auto text-inverse'):
                ui.label(_('home.title')).classes('text-5xl font-bold mb-6')
                ui.label(_('home.subtitle')).classes('text-xl mb-8 opacity-90')
                
                with ui.row().classes('gap-4 justify-center flex-wrap'):
                    ui.button(
                        _('home.explore_now'),
                        on_click=lambda: ui.navigate.to('/articles'),
                        icon='explore'
                    ).classes('bg-card text-primary px-8 py-4 rounded-lg font-semibold hover:bg-surface transition-all shadow-lg')
                    
                    ui.button(
                        _('home.learn_more'),
                        on_click=lambda: ui.navigate.to('/about'),
                        icon='info'
                    ).classes('border-2 border-white text-white px-8 py-4 rounded-lg font-semibold hover:bg-white hover:text-primary transition-all')
    
    def render_features_section(self):
        """Rendre la section des fonctionnalités"""
        try:
            from core.i18n import _
        except:
            def _(key): return key.split('.')[-1].replace('_', ' ').title()
        
        with ui.element('div').classes('w-full py-20 px-4 bg-surface'):
            with ui.column().classes('page-container mx-auto'):
                # Header
                ui.label(_('home.why_choose')).classes('text-4xl font-bold text-center mb-16 text-main')
                
                # Grille des fonctionnalités
                with ui.element('div').classes('grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8'):
                    for feature in self.features:
                        self.render_feature_card(feature)
    
    def render_feature_card(self, feature):
        """Rendre une carte de fonctionnalité"""
        try:
            from core.i18n import _
        except:
            def _(key): return key.split('.')[-1].replace('_', ' ').title()
        
        with ui.card().classes(theme_manager.get_card_classes(hover=True) + ' p-6 text-center cursor-pointer'):
            # Icône avec couleur de thème
            ui.icon(feature['icon']).classes('text-6xl mb-4 text-primary')
            
            # Titre traduit
            ui.label(_(feature['title_key'])).classes('text-xl font-bold mb-4 text-main')
            
            # Description traduite
            ui.label(_(feature['description_key'])).classes('text-muted mb-6 leading-relaxed')
            
            # Bouton avec classes de thème
            ui.button(
                _('common.read_more'),
                on_click=lambda url=feature['url']: ui.navigate.to(url),
                icon='arrow_forward'
            ).classes(theme_manager.get_button_classes('primary', 'md'))
    
    def render_stats_section(self):
        """Rendre la section des statistiques avec gradient"""
        try:
            from core.i18n import _
        except:
            def _(key): return key.split('.')[-1].replace('_', ' ').title()
        
        with ui.element('div').classes('w-full py-20 px-4 gradient-primary'):
            with ui.column().classes('page-container mx-auto text-inverse'):
                
                # Grille des statistiques
                with ui.element('div').classes('grid grid-cols-2 md:grid-cols-4 gap-8 text-center'):
                    
                    stats = [
                        {'value': '150+', 'label_key': 'home.stats.articles'},
                        {'value': '25+', 'label_key': 'home.stats.reports'},
                        {'value': '1200+', 'label_key': 'home.stats.users'},
                        {'value': '45+', 'label_key': 'home.stats.specialists'}
                    ]
                    
                    for stat in stats:
                        with ui.column().classes('p-6'):
                            ui.label(stat['value']).classes('text-5xl font-bold mb-2')
                            ui.label(_(stat['label_key'])).classes('text-lg opacity-90')
    
    def render_cta_section(self):
        """Rendre la section call-to-action"""
        try:
            from core.i18n import _
        except:
            def _(key): return key.split('.')[-1].replace('_', ' ').title()
        
        with ui.element('div').classes('w-full py-20 px-4 bg-card'):
            with ui.column().classes('max-w-4xl mx-auto text-center'):
                ui.label(_('home.cta.title')).classes('text-4xl font-bold mb-6 text-main')
                ui.label(_('home.cta.subtitle')).classes('text-xl text-muted mb-8')
                
                with ui.row().classes('gap-4 justify-center flex-wrap'):
                    ui.button(
                        _('home.cta.explore_articles'),
                        on_click=lambda: ui.navigate.to('/articles'),
                        icon='article'
                    ).classes(theme_manager.get_button_classes('primary', 'lg'))
                    
                    ui.button(
                        _('home.cta.contact_us'),
                        on_click=lambda: ui.navigate.to('/contact'),
                        icon='contact_mail'
                    ).classes(theme_manager.get_button_classes('outline', 'lg'))
    
    def render_testimonials_section(self):
        """Section témoignages avec thème"""
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
                            ui.label(f'"{testimonial["text"]}"').classes('text-muted mb-4 italic leading-relaxed')
                            ui.label(testimonial['name']).classes('font-semibold text-main')
                            ui.label(testimonial['role']).classes('text-sm text-muted')
    
    def render_additional_features_section(self):
        """Section de fonctionnalités additionnelles"""
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