# pages/chatbot.py

import asyncio
from nicegui import ui
from dotenv import load_dotenv
import os
from core.theme import theme_manager

from chatbot.vector import VectorDB
from chatbot.chatbot_memory import ChatbotMemory

load_dotenv()

class ChatbotPage:
    """Page du chatbot interactif MindCare avec système de thème centralisé"""

    def __init__(self):
        """Initialisation du chatbot."""
        self.loading_notification = ui.notification('Initialisation du modèle, veuillez patienter...', spinner=True, timeout=None)
        try:
            self.db = VectorDB()
            self.memory = ChatbotMemory(self.db)
            self.loading_notification.dismiss()
            ui.notify('Assistant prêt !', type='positive')
        except Exception as e:
            self.loading_notification.dismiss()
            ui.notify(f"Erreur lors de l'initialisation: {e}", type='negative')
            print(f"Erreur d'initialisation du chatbot : {e}")

    async def send_message(self):
        """Gère l'envoi d'un message par l'utilisateur."""
        user_message = self.message_input.value
        if not user_message.strip():
            return

        with self.chat_messages:
            ui.chat_message(user_message, name='Vous', sent=True)
        self.scroll_area.scroll_to(percent=1.0)
        self.message_input.value = ''

        with self.chat_messages:
            thinking_message = ui.chat_message(name='MindCare Assistant', sent=False)
            with thinking_message:
                ui.spinner(size='lg')
        self.scroll_area.scroll_to(percent=1.0)

        try:
            response = await asyncio.to_thread(self.memory.ask, user_message)
            thinking_message.clear()
            with thinking_message:
                ui.markdown(response)
        except Exception as e:
            thinking_message.clear()
            with thinking_message:
                ui.markdown(f"Désolé, une erreur est survenue. Veuillez réessayer.\n*Détail : {e}*")
        self.scroll_area.scroll_to(percent=1.0)

    def quick_suggestion(self, suggestion_text):
        """Gérer le clic sur une suggestion rapide"""
        # Nettoyer le texte (enlever l'emoji)
        clean_text = suggestion_text.split(' ', 1)[1] if ' ' in suggestion_text else suggestion_text
        self.message_input.value = clean_text
        # Envoyer automatiquement le message
        ui.run_javascript('document.querySelector(".message-input input").dispatchEvent(new KeyboardEvent("keydown", {key: "Enter"}))')

    def render(self):
        """Rendre la page complète du chatbot."""
        self.render_header()
        self.render_chat_interface()

    def render_header(self):
        """Rendre l'en-tête avec gradient de thème"""
        with ui.element('div').classes('w-full py-16 px-4 gradient-hero'):
            with ui.column().classes('w-full items-center text-center text-inverse'):
                ui.label('Assistant Virtuel MindCare').classes('text-5xl font-bold mb-4')
                ui.label('Posez vos questions et obtenez de l\'aide instantanément').classes('text-xl opacity-90')

    def render_chat_interface(self):
        """Rendre l'interface de chat avec système de thème centralisé"""
        with ui.element('div').classes('w-full px-4 pb-8 bg-surface'):
            # Container principal avec largeur étendue
            with ui.column().classes('w-full max-w-7xl mx-auto'):
                
                # Container principal du chat avec glassmorphism et thème
                with ui.card().classes(theme_manager.get_card_classes(elevated=True) + ' rounded-3xl p-6 shadow-2xl bg-card'):
                    
                    # En-tête du chat
                    with ui.row().classes('w-full items-center justify-between mb-6 pb-4 border-default border-b border-opacity-20'):
                        with ui.row().classes('items-center gap-3'):
                            ui.avatar('https://via.placeholder.com/40x40/10b981/ffffff?text=AI', size='md')
                            with ui.column().classes('gap-1'):
                                ui.label('MindCare Assistant').classes('text-main font-semibold')
                                ui.label('En ligne').classes('text-success text-xs')
                        
                        ui.button(icon='more_vert').props('flat round').classes('text-muted hover:text-primary')
                    
                    # Zone de messages - Plus haute sur grands écrans
                    with ui.scroll_area().classes('w-full h-96 xl:h-[500px] pr-4 bg-surface rounded-lg') as self.scroll_area:
                        self.chat_messages = ui.column().classes('w-full gap-4 p-4')
                    
                    # Message de bienvenue initial
                    with self.chat_messages:
                        with ui.row().classes('w-full justify-start mb-4'):
                            # Messages plus larges sur grands écrans
                            with ui.card().classes(theme_manager.get_card_classes() + ' rounded-2xl px-4 py-3 max-w-md xl:max-w-3xl'):
                                with ui.row().classes('items-start gap-3'):
                                    ui.avatar('https://via.placeholder.com/32x32/10b981/ffffff?text=AI', size='sm')
                                    with ui.column().classes('gap-2'):
                                        ui.label('Bonjour ! 👋').classes('font-semibold text-main')
                                        ui.markdown(
                                            "Je suis votre assistant virtuel MindCare. "
                                            "Je suis là pour vous accompagner et répondre à vos questions sur le bien-être mental. "
                                            "**Comment puis-je vous aider aujourd'hui ?**"
                                        ).classes('text-sm text-muted')
                    
                    # Zone de saisie moderne
                    with ui.row().classes('w-full gap-3 mt-6 pt-4 border-default border-t border-opacity-20'):
                        self.message_input = ui.input(
                            placeholder='💬 Tapez votre message ici...'
                        ).classes('flex-1 message-input').props('outlined rounded standout') \
                        .on('keydown.enter', self.send_message)
                        
                        ui.button(
                            icon='send', 
                            on_click=self.send_message
                        ).classes(theme_manager.get_button_classes('primary', 'lg') + ' send-button px-6 py-3 rounded-xl font-semibold') \
                        .props('no-caps')

                # Suggestions rapides
                with ui.row().classes('w-full gap-3 mt-6 justify-center flex-wrap'):
                    suggestions = [
                        "💡 Conseils bien-être",
                        "🧘 Exercices de relaxation", 
                        "😊 Gestion du stress",
                        "🌙 Améliorer le sommeil"
                    ]
                    
                    for suggestion in suggestions:
                        ui.button(
                            suggestion,
                            on_click=lambda s=suggestion: self.quick_suggestion(s)
                        ).classes('bg-surface text-primary px-4 py-2 rounded-full text-sm border border-primary hover:bg-primary hover:text-inverse transition-all') \
                        .props('no-caps outline')

        # Ajouter le CSS pour le glassmorphism et les animations
        self._add_chat_css()

    def _add_chat_css(self):
        """Ajouter le CSS pour l'interface de chat avec variables de thème"""
        ui.add_head_html("""
        <style>
        /* === CHAT INTERFACE STYLES === */
        
        /* Glassmorphism effect using theme variables */
        .glass-effect {
            background: rgba(255, 255, 255, 0.1) !important;
            backdrop-filter: blur(10px) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
        }
        
        /* Dark theme glassmorphism */
        .dark-theme .glass-effect {
            background: rgba(0, 0, 0, 0.2) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
        }
        
        /* Message input styling */
        .message-input .q-field__control {
            background-color: var(--theme-surface) !important;
            border-radius: var(--radius-xl) !important;
            border: 1px solid var(--theme-border) !important;
        }
        
        .message-input .q-field--focused .q-field__control {
            border-color: var(--theme-primary) !important;
            box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.1) !important;
        }
        
        /* Send button animation */
        .send-button {
            transition: all 0.3s ease !important;
        }
        
        .send-button:hover {
            transform: translateY(-2px) !important;
            box-shadow: var(--shadow-lg) !important;
        }
        
        /* Chat messages styling */
        .q-message {
            background-color: var(--theme-card-background) !important;
            border: 1px solid var(--theme-border) !important;
            border-radius: var(--radius-lg) !important;
        }
        
        .q-message--sent {
            background-color: var(--theme-primary) !important;
            color: var(--theme-text-inverse) !important;
        }
        
        /* Chat bubble animation */
        .chat-bubble {
            animation: fadeInUp 0.3s ease-out;
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        /* Suggestion buttons */
        .suggestion-btn {
            transition: all 0.2s ease !important;
            background: linear-gradient(145deg, var(--theme-surface), var(--theme-card-background)) !important;
            border: 1px solid var(--theme-border) !important;
        }
        
        .suggestion-btn:hover {
            transform: translateY(-1px) !important;
            box-shadow: var(--shadow-md) !important;
            background: var(--theme-primary) !important;
            color: var(--theme-text-inverse) !important;
        }
        
        /* Scroll area styling */
        .q-scrollarea__content {
            background-color: var(--theme-surface) !important;
        }
        
        /* Avatar styling */
        .q-avatar {
            background: var(--theme-primary) !important;
        }
        
        /* Responsive adjustments */
        @media (max-width: 768px) {
            .message-input {
                font-size: 16px !important; /* Prevent zoom on iOS */
            }
            
            .send-button {
                padding: 0.75rem !important;
            }
            
            .suggestion-btn {
                font-size: 0.75rem !important;
                padding: 0.5rem 0.75rem !important;
            }
        }
        
        /* Loading spinner */
        .q-spinner {
            color: var(--theme-primary) !important;
        }
        
        /* Markdown content in messages */
        .q-message .q-markdown {
            color: inherit !important;
        }
        
        .q-message .q-markdown h1,
        .q-message .q-markdown h2,
        .q-message .q-markdown h3 {
            color: inherit !important;
        }
        
        .q-message .q-markdown code {
            background-color: rgba(0, 0, 0, 0.1) !important;
            padding: 0.125rem 0.25rem !important;
            border-radius: var(--radius-sm) !important;
        }
        
        .q-message .q-markdown pre {
            background-color: rgba(0, 0, 0, 0.05) !important;
            border-radius: var(--radius-md) !important;
            padding: var(--spacing-md) !important;
        }
        
        /* Focus states for accessibility */
        .message-input:focus-within,
        .send-button:focus,
        .suggestion-btn:focus {
            outline: 2px solid var(--theme-border-focus) !important;
            outline-offset: 2px !important;
        }
        </style>
        """)