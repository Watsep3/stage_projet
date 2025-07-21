from nicegui import ui
from typing import Optional, List, Dict, Any, Callable
from core.theme import theme_manager
from core.i18n import i18n, _

class BaseComponent:
    """Classe de base pour tous les composants"""
    
    def __init__(self):
        self.element = None
        self.props = {}
        self.classes = []
    
    def add_class(self, class_name: str):
        """Ajouter une classe CSS"""
        self.classes.append(class_name)
        if self.element:
            self.element.classes(' '.join(self.classes))
        return self
    
    def set_props(self, **props):
        """Définir les propriétés"""
        self.props.update(props)
        return self
    
    def render(self):
        """Méthode à implémenter par les sous-classes"""
        raise NotImplementedError

class Card(BaseComponent):
    """Composant carte réutilisable"""
    
    def __init__(self, title: str = "", content: str = "", 
                 image: Optional[str] = None, actions: Optional[List[Dict]] = None):
        super().__init__()
        self.title = title
        self.content = content
        self.image = image
        self.actions = actions or []
        self.add_class('theme-transition')
    
    def render(self):
        """Rendre la carte"""
        with ui.card().classes('theme-surface theme-border rounded-lg shadow-md hover:shadow-lg transition-all duration-300') as card:
            self.element = card
            
            # Image si fournie
            if self.image:
                ui.image(self.image).classes('w-full h-48 object-cover rounded-t-lg')
            
            # Contenu
            with ui.card_section():
                if self.title:
                    ui.label(self.title).classes('text-xl font-semibold theme-text mb-2')
                
                if self.content:
                    ui.label(self.content).classes('theme-text-secondary mb-4')
                
                # Actions
                if self.actions:
                    with ui.row().classes('gap-2'):
                        for action in self.actions:
                            ui.button(
                                action.get('label', ''),
                                on_click=action.get('callback')
                            ).classes('bg-primary text-white px-4 py-2 rounded')
            
            # Appliquer les classes personnalisées
            if self.classes:
                card.classes(' '.join(self.classes))
        
        return self

class Button(BaseComponent):
    """Composant bouton réutilisable"""
    
    def __init__(self, text: str, on_click: Optional[Callable] = None, 
                 variant: str = 'primary', size: str = 'md', 
                 icon: Optional[str] = None, disabled: bool = False):
        super().__init__()
        self.text = text
        self.on_click = on_click
        self.variant = variant
        self.size = size
        self.icon = icon
        self.disabled = disabled
    
    def render(self):
        """Rendre le bouton"""
        # Classes selon le variant
        variant_classes = {
            'primary': 'bg-primary text-white hover:bg-primary-dark',
            'secondary': 'bg-secondary text-white hover:bg-secondary-dark',
            'outline': 'border border-primary text-primary hover:bg-primary hover:text-white',
            'ghost': 'text-primary hover:bg-primary hover:bg-opacity-10',
            'danger': 'bg-red-500 text-white hover:bg-red-600'
        }
        
        # Classes selon la taille
        size_classes = {
            'sm': 'px-3 py-1 text-sm',
            'md': 'px-4 py-2',
            'lg': 'px-6 py-3 text-lg',
            'xl': 'px-8 py-4 text-xl'
        }
        
        classes = f"rounded transition-all duration-200 font-medium {variant_classes.get(self.variant, variant_classes['primary'])} {size_classes.get(self.size, size_classes['md'])}"
        
        if self.disabled:
            classes += " opacity-50 cursor-not-allowed"
        
        # Créer le bouton
        button = ui.button(
            self.text,
            on_click=self.on_click if not self.disabled else None,
            icon=self.icon
        ).classes(classes)
        
        self.element = button
        return self

class Modal(BaseComponent):
    """Composant modal réutilisable"""
    
    def __init__(self, title: str = "", content: str = "", 
                 size: str = 'md', closable: bool = True):
        super().__init__()
        self.title = title
        self.content = content
        self.size = size
        self.closable = closable
        self.is_open = False
        self.dialog = None
    
    def open(self):
        """Ouvrir la modal"""
        self.is_open = True
        if self.dialog:
            self.dialog.open()
    
    def close(self):
        """Fermer la modal"""
        self.is_open = False
        if self.dialog:
            self.dialog.close()
    
    def render(self):
        """Rendre la modal"""
        # Classes selon la taille
        size_classes = {
            'sm': 'max-w-sm',
            'md': 'max-w-md',
            'lg': 'max-w-lg',
            'xl': 'max-w-xl',
            '2xl': 'max-w-2xl'
        }
        
        with ui.dialog() as dialog:
            self.dialog = dialog
            
            with ui.card().classes(f'theme-surface {size_classes.get(self.size, size_classes["md"])} w-full'):
                # Header
                if self.title or self.closable:
                    with ui.card_section().classes('pb-2'):
                        with ui.row().classes('items-center justify-between'):
                            if self.title:
                                ui.label(self.title).classes('text-xl font-semibold theme-text')
                            
                            if self.closable:
                                ui.button(icon='close', on_click=self.close).classes('ml-auto').props('flat round')
                
                # Content
                with ui.card_section():
                    if self.content:
                        ui.label(self.content).classes('theme-text-secondary')
                    
                    # Zone pour contenu personnalisé
                    with ui.column() as content_area:
                        self.content_area = content_area
        
        return self

class Alert(BaseComponent):
    """Composant alerte réutilisable"""
    
    def __init__(self, message: str, type: str = 'info', 
                 dismissible: bool = True, icon: Optional[str] = None):
        super().__init__()
        self.message = message
        self.type = type
        self.dismissible = dismissible
        self.icon = icon
        self.is_visible = True
    
    def dismiss(self):
        """Masquer l'alerte"""
        self.is_visible = False
        if self.element:
            self.element.style('display: none')
    
    def render(self):
        """Rendre l'alerte"""
        # Classes et icônes selon le type
        type_config = {
            'info': {'classes': 'bg-blue-100 border-blue-500 text-blue-700', 'icon': 'info'},
            'success': {'classes': 'bg-green-100 border-green-500 text-green-700', 'icon': 'check_circle'},
            'warning': {'classes': 'bg-yellow-100 border-yellow-500 text-yellow-700', 'icon': 'warning'},
            'error': {'classes': 'bg-red-100 border-red-500 text-red-700', 'icon': 'error'}
        }
        
        config = type_config.get(self.type, type_config['info'])
        icon = self.icon or config['icon']
        
        with ui.row().classes(f'p-4 rounded-lg border-l-4 {config["classes"]} items-start gap-3') as alert:
            self.element = alert
            
            # Icône
            ui.icon(icon).classes('mt-0.5')
            
            # Message
            ui.label(self.message).classes('flex-1')
            
            # Bouton de fermeture
            if self.dismissible:
                ui.button(icon='close', on_click=self.dismiss).classes('ml-auto').props('flat round size=sm')
        
        return self

class LoadingSpinner(BaseComponent):
    """Composant spinner de chargement"""
    
    def __init__(self, size: str = 'md', message: str = ""):
        super().__init__()
        self.size = size
        self.message = message
    
    def render(self):
        """Rendre le spinner"""
        size_classes = {
            'sm': 'w-4 h-4',
            'md': 'w-8 h-8',
            'lg': 'w-12 h-12',
            'xl': 'w-16 h-16'
        }
        
        with ui.column().classes('items-center justify-center p-8') as spinner:
            self.element = spinner
            
            ui.spinner(size=self.size).classes(f'text-primary {size_classes.get(self.size, size_classes["md"])}')
            
            if self.message:
                ui.label(self.message).classes('mt-2 theme-text-secondary')
        
        return self

class Breadcrumb(BaseComponent):
    """Composant fil d'Ariane"""
    
    def __init__(self, items: List[Dict[str, str]]):
        super().__init__()
        self.items = items
    
    def render(self):
        """Rendre le fil d'Ariane"""
        with ui.row().classes('items-center gap-2 py-2') as breadcrumb:
            self.element = breadcrumb
            
            for i, item in enumerate(self.items):
                if i > 0:
                    ui.icon('chevron_right').classes('text-gray-400')
                
                if item.get('href') and i < len(self.items) - 1:
                    ui.link(item['label'], item['href']).classes('text-primary hover:underline')
                else:
                    ui.label(item['label']).classes('theme-text-secondary')
        
        return self

class Pagination(BaseComponent):
    """Composant pagination"""
    
    def __init__(self, current_page: int = 1, total_pages: int = 1, 
                 on_page_change: Optional[Callable] = None):
        super().__init__()
        self.current_page = current_page
        self.total_pages = total_pages
        self.on_page_change = on_page_change
    
    def render(self):
        """Rendre la pagination"""
        with ui.row().classes('items-center gap-2 justify-center') as pagination:
            self.element = pagination
            
            # Bouton précédent
            ui.button(
                icon='chevron_left',
                on_click=lambda: self.change_page(self.current_page - 1)
            ).classes('').props('flat').set_enabled(self.current_page > 1)
            
            # Numéros de page
            start_page = max(1, self.current_page - 2)
            end_page = min(self.total_pages, self.current_page + 2)
            
            for page in range(start_page, end_page + 1):
                ui.button(
                    str(page),
                    on_click=lambda p=page: self.change_page(p)
                ).classes('w-10 h-10' + (' bg-primary text-white' if page == self.current_page else ''))
            
            # Bouton suivant
            ui.button(
                icon='chevron_right',
                on_click=lambda: self.change_page(self.current_page + 1)
            ).classes('').props('flat').set_enabled(self.current_page < self.total_pages)
        
        return self
    
    def change_page(self, page: int):
        """Changer de page"""
        if 1 <= page <= self.total_pages and page != self.current_page:
            self.current_page = page
            if self.on_page_change:
                self.on_page_change(page)