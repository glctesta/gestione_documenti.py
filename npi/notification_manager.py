# npi/notification_manager.py

import logging
import requests
import json
from typing import Optional
from datetime import datetime
from icalendar import Calendar, Event
import tempfile
import os

# Importa il connettore email fornito e i modelli dei dati
from email_connector import EmailSender
from .data_models import TaskProdotto, Soggetto, NotificationLog
from utils import send_email  # Aggiungi questo import

logger = logging.getLogger(__name__)


class NotificationManager:
    """
    Gestisce l'invio di notifiche per il modulo NPI tramite diversi canali.
    """

    def __init__(self, email_sender: EmailSender, teams_webhook_url: Optional[str] = None, session=None):
        """
        Inizializza il gestore delle notifiche.

        Args:
            email_sender: Istanza pre-configurata di EmailSender.
            teams_webhook_url: L'URL dell'Incoming Webhook di MS Teams.
            session: Sessione SQLAlchemy per il logging nel database.
        """
        self.email_sender = email_sender
        self.teams_webhook_url = teams_webhook_url
        self.session = session

        if not self.teams_webhook_url:
            logger.warning("URL Webhook di MS Teams non fornito. Le notifiche su Teams sono disabilitate.")

    def _log_notification(self, progetto_id: int, task_id: int, soggetto_id: int,
                          canale: str, stato: str, errore: str = None):
        """Registra l'invio della notifica nel database."""
        if not self.session:
            logger.warning("Sessione database non disponibile per il logging delle notifiche")
            return

        try:
            log_entry = NotificationLog(
                ProgettoID=progetto_id,
                TaskProdottoID=task_id,
                SoggettoID=soggetto_id,
                CanaleInvio=canale,
                StatoInvio=stato,
                MessaggioErrore=errore
            )
            self.session.add(log_entry)
            self.session.commit()
        except Exception as e:
            logger.error(f"Errore durante il logging della notifica: {e}")

    def _crea_invito_calendario(self, task: TaskProdotto) -> str:
        """Crea un file .ics per l'invito calendario."""
        cal = Calendar()
        cal.add('prodid', '-//NPI System//NPI Calendar//')
        cal.add('version', '2.0')

        event = Event()
        event.add('summary', f"NPI Task: {task.task_template.NomeTask}")
        event.add('description',
                  f"Progetto: {task.wave.progetto.prodotto.NomeProdotto}\n"
                  f"Task: {task.task_template.NomeTask}\n"
                  f"Note: {task.Note or 'Nessuna nota'}")

        if task.DataInizio:
            event.add('dtstart', task.DataInizio)
        if task.DataScadenza:
            event.add('dtend', task.DataScadenza)

        event.add('dtstamp', datetime.now())
        event.add('uid', f"npi_task_{task.TaskProdottoID}@company.com")

        cal.add_component(event)

        # Crea file temporaneo
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ics', delete=False) as f:
            f.write(cal.to_ical().decode('utf-8'))
            return f.name

        return None

    def _invia_notifica_interno(self, task: TaskProdotto, soggetto: Soggetto):
        """Invia notifica a soggetto interno (Teams + Calendar)."""
        try:
            # Notifica Teams
            scheda_teams = self._crea_scheda_teams_task(task, "Nuovo Task Assegnato")
            self._send_teams_notification(scheda_teams)
            self._log_notification(
                task.wave.progetto.ProgettoID,
                task.TaskProdottoID,
                soggetto.SoggettoID,
                'Teams',
                'Inviato'
            )

            # Invito calendario
            ics_file = self._crea_invito_calendario(task)
            if ics_file and soggetto.Email:
                try:
                    # Invia email con invito calendario
                    subject = f"Invito Calendario - Task NPI: {task.task_template.NomeTask}"
                    body = f"""
                       Gentile {soggetto.NomeSoggetto},

                       Ti è stato assegnato un nuovo task NPI.
                       Progetto: {task.wave.progetto.prodotto.NomeProdotto}
                       Task: {task.task_template.NomeTask}
                       Scadenza: {task.DataScadenza.strftime('%d/%m/%Y') if task.DataScadenza else 'Non specificata'}

                       In allegato trovi l'invito per il calendario.

                       Cordiali saluti,
                       Sistema NPI
                       """

                    # Qui dovresti implementare l'invio email con allegato
                    # Per ora logghiamo solo
                    logger.info(f"Invito calendario creato per {soggetto.Email}: {ics_file}")

                    # Pulizia file temporaneo
                    os.unlink(ics_file)

                    self._log_notification(
                        task.wave.progetto.ProgettoID,
                        task.TaskProdottoID,
                        soggetto.SoggettoID,
                        'Calendar',
                        'Inviato'
                    )

                except Exception as e:
                    logger.error(f"Errore invio calendario: {e}")
                    self._log_notification(
                        task.wave.progetto.ProgettoID,
                        task.TaskProdottoID,
                        soggetto.SoggettoID,
                        'Calendar',
                        'Fallito',
                        str(e)
                    )

        except Exception as e:
            logger.error(f"Errore notifica interno: {e}")
            self._log_notification(
                task.wave.progetto.ProgettoID,
                task.TaskProdottoID,
                soggetto.SoggettoID,
                'Teams',
                'Fallito',
                str(e)
            )

    def _invia_notifica_esterno(self, task: TaskProdotto, soggetto: Soggetto):
        """Invia notifica a soggetto esterno (Email con istruzioni calendario)."""
        try:
            titolo = f"Nuovo Task NPI Assegnato: {task.task_template.NomeTask}"
            messaggio = (f"Gentile {soggetto.NomeSoggetto},<br><br>"
                         f"Vi è stata assegnata una nuova attività nell'ambito del progetto NPI.<br>"
                         f"<strong>Progetto:</strong> {task.wave.progetto.prodotto.NomeProdotto}<br>"
                         f"<strong>Task:</strong> {task.task_template.NomeTask}<br>"
                         f"<strong>Scadenza:</strong> {task.DataScadenza.strftime('%d/%m/%Y') if task.DataScadenza else 'Da definire'}<br><br>"
                         f"Per aggiungere questo evento al vostro calendario, utilizzate i seguenti link:<br>"
                         f"- <a href='https://calendar.google.com/calendar/render?action=TEMPLATE&text=NPI Task: {task.task_template.NomeTask}&details=Progetto: {task.wave.progetto.prodotto.NomeProdotto} - Task: {task.task_template.NomeTask} - Note: {task.Note or 'Nessuna nota'}&dates={task.DataInizio.strftime('%Y%m%d') if task.DataInizio else ''}/{task.DataScadenza.strftime('%Y%m%d') if task.DataScadenza else ''}'>Aggiungi a Google Calendar</a><br>"
                         f"- <a href='#' onclick='window.open(\"webcal://add/event/to/calendar?title=NPI Task: {task.task_template.NomeTask}&startdate={task.DataInizio.strftime('%Y-%m-%d') if task.DataInizio else ''}&enddate={task.DataScadenza.strftime('%Y-%m-%d') if task.DataScadenza else ''}&description=Progetto: {task.wave.progetto.prodotto.NomeProdotto} - Task: {task.task_template.NomeTask} - Note: {task.Note or 'Nessuna nota'}\")'>Aggiungi ad Apple Calendar</a><br><br>"
                         f"Cordiali saluti,<br>Il Team NPI")

            body_html = self._crea_body_html_email(task, titolo, messaggio)
            self._send_email_notification(soggetto, titolo, body_html)

            self._log_notification(
                task.wave.progetto.ProgettoID,
                task.TaskProdottoID,
                soggetto.SoggettoID,
                'Email',
                'Inviato'
            )

        except Exception as e:
            logger.error(f"Errore notifica esterno: {e}")
            self._log_notification(
                task.wave.progetto.ProgettoID,
                task.TaskProdottoID,
                soggetto.SoggettoID,
                'Email',
                'Fallito',
                str(e)
            )

    def invia_notifiche_task(self, task: TaskProdotto, conferma_utente: bool = True, lang: dict = None):
        """
        Invia le notifiche per un task, con eventuale conferma utente.

        Args:
            task: Il task da notificare
            conferma_utente: Se True, chiede conferma prima di inviare
            lang: Dizionario con le traduzioni
        """
        if not task or not task.owner:
            logger.warning("Tentativo di notificare un task non valido o senza owner.")
            return False

        soggetto_target = task.owner

        # Se richiesta conferma utente
        if conferma_utente:
            # Qui dovresti implementare la dialog di conferma
            # Per ora assumiamo che sia gestita dall'UI
            pass

        try:
            if soggetto_target.Tipo == 'Interno':
                self._invia_notifica_interno(task, soggetto_target)
            elif soggetto_target.Tipo in ['Cliente', 'Fornitore']:
                self._invia_notifica_esterno(task, soggetto_target)

            return True

        except Exception as e:
            logger.error(f"Errore generale nell'invio notifiche: {e}")
            return False

    def _send_email_notification(self, soggetto: Soggetto, subject: str, body: str):
        """Metodo privato per inviare una notifica via email."""
        if not soggetto.Email:
            logger.error(
                f"Tentativo di inviare email a '{soggetto.NomeSoggetto}' ma l'indirizzo email non è specificato.")
            return

        try:
            self.email_sender.send_email(
                to_email=soggetto.Email,
                subject=subject,
                body=body,
                is_html=True
            )
            logger.info(f"Email di notifica inviata con successo a {soggetto.Email}.")
        except Exception as e:
            logger.error(f"Errore durante l'invio dell'email a {soggetto.Email}: {e}", exc_info=True)

    def _send_teams_notification(self, message_card: dict):
        """Metodo privato per inviare una notifica a un canale Teams tramite Webhook."""
        if not self.teams_webhook_url:
            return  # Notifiche Teams disabilitate

        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.post(self.teams_webhook_url, headers=headers, data=json.dumps(message_card))
            response.raise_for_status()  # Solleva un'eccezione per risposte HTTP 4xx/5xx
            logger.info("Notifica inviata con successo al canale Teams.")
        except requests.exceptions.RequestException as e:
            logger.error(f"Errore durante l'invio della notifica a Teams: {e}", exc_info=True)

    def _crea_scheda_teams_task(self, task: TaskProdotto, titolo: str) -> dict:
        """Crea una Adaptive Card JSON per notificare un task su Teams."""
        progetto = task.wave.progetto
        task_template = task.task_template

        card = {
            "type": "message",
            "attachments": [
                {
                    "contentType": "application/vnd.microsoft.card.adaptive",
                    "content": {
                        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                        "type": "AdaptiveCard",
                        "version": "1.4",
                        "msteams": {"width": "Full"},
                        "body": [
                            {
                                "type": "TextBlock",
                                "text": titolo,
                                "weight": "Bolder",
                                "size": "Medium"
                            },
                            {
                                "type": "FactSet",
                                "facts": [
                                    {"title": "Progetto:", "value": f"{progetto.prodotto.NomeProdotto}"},
                                    {"title": "Task:", "value": f"{task_template.NomeTask}"},
                                    {"title": "Assegnato a:", "value": f"{task.owner.NomeSoggetto}"},
                                    {"title": "Scadenza:",
                                     "value": f"{{{{DATE({task.DataScadenza.strftime('%Y-%m-%dT%H:%M:%SZ')}, SHORT)}}}}"},
                                    {"title": "Stato:", "value": f"{task.Stato}"}
                                ]
                            }
                        ]
                    }
                }
            ]
        }
        return card

    def _crea_body_html_email(self, task: TaskProdotto, titolo: str, messaggio_introduttivo: str) -> str:
        """Crea un corpo email HTML per notificare un task a un soggetto esterno."""
        progetto = task.wave.progetto
        task_template = task.task_template

        body = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Calibri, sans-serif; }}
                .container {{ border: 1px solid #ccc; padding: 15px; border-radius: 5px; max-width: 600px; }}
                h2 {{ color: #005A9E; }}
                .fact-set {{ margin-top: 20px; }}
                .fact {{ margin-bottom: 10px; }}
                .fact-title {{ font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>{titolo}</h2>
                <p>{messaggio_introduttivo}</p>
                <div class="fact-set">
                    <div class="fact"><span class="fact-title">Progetto NPI:</span> {progetto.prodotto.NomeProdotto}</div>
                    <div class="fact"><span class="fact-title">Attività Richiesta:</span> {task_template.NomeTask}</div>
                    <div class="fact"><span class="fact-title">Data di Scadenza:</span> {task.DataScadenza.strftime('%d/%m/%Y')}</div>
                </div>
                <hr>
                <p><i>Questa è un'email generata automaticamente dal sistema di gestione NPI.</i></p>
            </div>
        </body>
        </html>
        """
        return body

    def notifica_assegnazione_task(self, task: TaskProdotto):
        """
        Invia una notifica quando un nuovo task viene assegnato.
        Decide il canale in base al tipo di soggetto.
        """
        if not task or not task.owner:
            logger.warning("Tentativo di notificare un task non valido o senza owner.")
            return

        soggetto_target = task.owner
        titolo = f"Nuovo Task NPI Assegnato: {task.task_template.NomeTask}"

        if soggetto_target.Tipo == 'Interno':
            scheda_teams = self._crea_scheda_teams_task(task, "Nuovo Task Assegnato")
            self._send_teams_notification(scheda_teams)

        elif soggetto_target.Tipo in ['Cliente', 'Fornitore']:
            messaggio = (f"Gentile {soggetto_target.NomeSoggetto},<br><br>"
                         f"Vi è stata assegnata una nuova attività nell'ambito del progetto NPI per il prodotto in oggetto. "
                         f"Per favore, prendete visione dei dettagli di seguito.")
            body_html = self._crea_body_html_email(task, titolo, messaggio)
            self._send_email_notification(soggetto_target, titolo, body_html)