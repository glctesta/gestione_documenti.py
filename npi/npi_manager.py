# File: npi/npi_manager.py
import logging
from datetime import datetime
from sqlalchemy.orm import sessionmaker, joinedload, subqueryload, selectinload
from sqlalchemy.engine import Engine
from sqlalchemy import select, update, delete, func, and_
#from .data_models import Base, ProgettoNPI, Prodotto, TaskProdotto, WaveNPI, TaskCatalogo, Soggetto, Categoria
from .data_models import ProgettoNPI, Base, Prodotto, Soggetto, TaskCatalogo, Categoria , WaveNPI , TaskProdotto
logger = logging.getLogger(__name__)


class GestoreNPI:
    """
    Classe principale che orchestra la gestione dei dati NPI tramite il DB.
    """

    def __init__(self, engine: Engine):
        if not engine:
            raise ValueError("SQLAlchemy Engine non può essere None.")
        self.engine = engine
        Base.metadata.create_all(self.engine, checkfirst=True)
        self.Session = sessionmaker(bind=self.engine)
        logger.info("GestoreNPI pronto e tabelle NPI verificate/create.")

    # --- METODI CRUD PER SOGGETTI ---
    def get_soggetti(self):
        session = self.Session()
        # try:
        #    return session.query(Soggetto).order_by(Soggetto.NomeSoggetto).all()
        # finally:
        #    session.close()
        with session:
            return session.scalars(select(Soggetto).order_by(Soggetto.NomeSoggetto)).all()

    def get_soggetto_by_id(self, soggetto_id):
        session = self.Session()
        # try:
        #     return session.query(Soggetto).get(soggetto_id)
        # finally:
        #     session.close()
        with session:
            return session.scalars(select(Soggetto).order_by(Soggetto.NomeSoggetto)).all()

    def create_soggetto(self, data):
        session = self.Session()
        try:
            nuovo_soggetto = Soggetto(**data)
            session.add(nuovo_soggetto)
            session.commit()
            return nuovo_soggetto
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def update_soggetto(self, soggetto_id, data):
        session = self.Session()
        try:
            soggetto = session.query(Soggetto).get(soggetto_id)
            if soggetto:
                for key, value in data.items():
                    setattr(soggetto, key, value)
                session.commit()
            return soggetto
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def delete_soggetto(self, soggetto_id):
        session = self.Session()
        try:
            soggetto = session.query(Soggetto).get(soggetto_id)
            if soggetto:
                session.delete(soggetto)
                session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def get_prodotti(self):
        session = self.Session()
        try:
            return session.query(Prodotto).order_by(Prodotto.NomeProdotto).all()
        finally:
            session.close()

    def get_prodotto_by_id(self, prodotto_id):
        session = self.Session()
        try:
            return session.query(Prodotto).get(prodotto_id)
        finally:
            session.close()

    def create_prodotto(self, data):
        session = self.Session()
        try:
            nuovo_prodotto = Prodotto(**data)
            session.add(nuovo_prodotto)
            session.commit()
            return nuovo_prodotto
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def update_prodotto(self, prodotto_id, data):
        session = self.Session()
        try:
            prodotto = session.query(Prodotto).get(prodotto_id)
            if prodotto:
                for key, value in data.items():
                    setattr(prodotto, key, value)
                session.commit()
            return prodotto
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def delete_prodotto(self, prodotto_id):
        session = self.Session()
        try:
            prodotto = session.query(Prodotto).get(prodotto_id)
            if prodotto:
                session.delete(prodotto)
                session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    # --- METODI CRUD PER CATEGORIE ---
    def get_categories(self):
        session = self.Session()
        try:
            return session.query(Categoria).order_by(Categoria.NrOrdin).all()
        finally:
            session.close()

    def create_category(self, data):
        """METODO MODIFICATO: Aggiunge il controllo per NrOrdin duplicato."""
        session = self.Session()
        try:
            # Controllo duplicati di NrOrdin prima di inserire
            nr_ordin_value = data.get('NrOrdin')
            if nr_ordin_value is not None:
                existing = session.query(Categoria).filter(Categoria.NrOrdin == nr_ordin_value).first()
                if existing:
                    # Solleva un'eccezione chiara che verrà gestita dalla UI
                    raise ValueError(f"Il numero d'ordine {nr_ordin_value} è già utilizzato dalla categoria '{existing.Category}'.")

            new_category = Categoria(**data)
            session.add(new_category)
            session.commit()
            return new_category # Ritorna l'oggetto creato
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def update_category(self, category_id, data):
        """METODO MODIFICATO: Aggiunge il controllo per NrOrdin duplicato durante l'aggiornamento."""
        session = self.Session()
        try:
            # Controllo duplicati di NrOrdin, escludendo la categoria corrente
            nr_ordin_value = data.get('NrOrdin')
            if nr_ordin_value is not None:
                existing = session.query(Categoria).filter(
                    and_(
                        Categoria.NrOrdin == nr_ordin_value,
                        Categoria.CategoryId != category_id
                    )
                ).first()
                if existing:
                    raise ValueError(f"Il numero d'ordine {nr_ordin_value} è già utilizzato dalla categoria '{existing.Category}'.")

            category = session.query(Categoria).get(category_id)
            if category:
                for key, value in data.items():
                    setattr(category, key, value)
                session.commit()
            return category # Ritorna l'oggetto aggiornato
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


    def delete_category(self, category_id):
        """METODO MODIFICATO: Aggiunge controllo per categoria in uso."""
        session = self.Session()
        try:
            # Controlla se la categoria è associata a qualche task
            num_tasks = session.query(TaskCatalogo).filter(TaskCatalogo.CategoryId == category_id).count()
            if num_tasks > 0:
                raise Exception(f"Impossibile eliminare la categoria: è associata a {num_tasks} task nel catalogo.")

            category = session.query(Categoria).get(category_id)
            if category:
                session.delete(category)
                session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    # --- METODI PER CATALOGO TASK ---
    def get_catalogo_task(self):
        session = self.Session()
        # try:
        #     return session.query(TaskCatalogo).options(
        #         joinedload(TaskCatalogo.category)
        #     ).order_by(TaskCatalogo.ItemID).all()
        # finally:
        #     session.close()
        with session:
            stmt = select(TaskCatalogo).options(selectinload(TaskCatalogo.category)).order_by(TaskCatalogo.NrOrdin)
            return session.scalars(stmt).all()

    def get_catalogo_task_by_id(self, task_id):
        session = self.Session()
        # try:
        #     return session.query(TaskCatalogo).options(joinedload(TaskCatalogo.category)).get(task_id)
        # finally:
        #     session.close()
        with session:
            stmt = select(TaskCatalogo).options(selectinload(TaskCatalogo.category)).where(TaskCatalogo.TaskID == task_id)
            return session.scalars(stmt).all()

    def get_catalogo_task_by_itemid(self, item_id: str):
        session = self.Session()
        # try:
        #     return session.query(TaskCatalogo).filter(TaskCatalogo.ItemID == item_id).first()
        # finally:
        #     session.close()
        with session:
            return session.scalars(select(TaskCatalogo).where(TaskCatalogo.ItemID == item_id)).first()

    def _renumber_all_tasks(self, session):
        """NUOVO METODO INTERNO: Rinumera tutti i task con un passo di 10."""
        logger.info("Rinumerazione in corso per tutti i task del catalogo...")
        all_tasks = session.scalars(select(TaskCatalogo).order_by(TaskCatalogo.NrOrdin, TaskCatalogo.ItemID)).all()
        for i, task in enumerate(all_tasks):
            task.NrOrdin = (i + 1) * 10
        session.flush()
        logger.info("Rinumerazione completata.")

    def create_catalogo_task(self, data, anchor_task_id=None):
        session = self.Session()
        # try:
        #     nuovo_task = TaskCatalogo(**data)
        #     session.add(nuovo_task)
        #     session.commit()
        #     return nuovo_task
        # except Exception:
        #     session.rollback()
        #     raise
        # finally:
        #     session.close()
        with session:
            is_title = data.get('IsTitle', False)

            if is_title and data.get('CategoryId') is not None:
                min_ordin_stmt = select(func.min(TaskCatalogo.NrOrdin)).where(TaskCatalogo.CategoryId == data['CategoryId'])
                min_ordin_result = session.scalars(min_ordin_stmt)
                if min_ordin_result is not None:
                    data['NrOrdin'] = min_ordin_result -5 #Si posiziona prima
                else:
                    cat_ordin = session.scalar(select(Categoria.NrOrdin).where(Categoria.CategoryId == data['CategoryId']))
                    data['NrOrdin'] = (cat_ordin or 0) * 100
            else:
                if anchor_task_id:
                    anchor_task = session.get(TaskCatalogo, anchor_task_id)
                    anchor_ordin = anchor_task.NrOrdin if anchor_task else 0

                    next_task_stmt = select(TaskCatalogo.NrOrdin).where(TaskCatalogo.NrOrdin > anchor_ordin).order_by(TaskCatalogo.NrOrdin.asc()).limit(1)
                    next_ordin = session.scalar(next_task_stmt)
                else:
                    anchor_ordin = session.scalar(select(func.max(TaskCatalogo.NrOrdin))) or 0
                    next_ordin = None

                if next_ordin is None:
                    next_ordin = anchor_ordin + 10
                else:
                    gap = next_ordin - anchor_ordin
                    if gap < 2:
                        self._renumber_all_tasks(session)
                        #ricalcola dopo numerazione
                        refreshed_anchor = session.get(TaskCatalogo, anchor_task_id)
                        new_anchor_ordin = refreshed_anchor.NrOrdin if refreshed_anchor else 0
                        new_ordin = new_anchor_ordin + 5
                    else:
                        new_ordin = anchor_ordin + gap // 2
            data['NrOrdin'] = new_ordin

            nuovo = TaskCatalogo(**data)
            session.add(nuovo)
            session.commit()
            return nuovo


    def update_catalogo_task(self, task_id, data):
        session = self.Session()
        # try:
        #     task = session.query(TaskCatalogo).get(task_id)
        #     if task:
        #         for key, value in data.items():
        #             setattr(task, key, value)
        #         session.commit()
        #     return task
        # except Exception:
        #     session.rollback()
        #     raise
        # finally:
        #     session.close()
        with session:
            session.execute(update(TaskCatalogo).where(TaskCatalogo.TaskID == task_id).values(**data))
            session.commit()

    def delete_catalogo_task(self, task_id):
        session = self.Session()
        # try:
        #     task = session.query(TaskCatalogo).get(task_id)
        #     if task:
        #         session.delete(task)
        #         session.commit()
        # except Exception:
        #     session.rollback()
        #     raise
        # finally:
        #     session.close()
        with session:
            task = session.get(TaskCatalogo, task_id)
            if task:
                session.delete(task)
                session.commit()


    def get_progetti_attivi(self):
        """Restituisce una lista di tutti i progetti NPI con stato 'Attivo'."""
        session = self.Session()
        try:
            return session.query(ProgettoNPI).filter(ProgettoNPI.StatoProgetto == 'Attivo').options(
                joinedload(ProgettoNPI.prodotto)
            ).order_by(ProgettoNPI.ProgettoID.desc()).all()
        finally:
            session.close()

    def create_progetto_npi_for_prodotto(self, prodotto_id):
        """
        Crea un progetto NPI, la sua Wave 1.0 e tutti i task associati.
        """
        session = self.Session()
        try:
            existing = session.query(ProgettoNPI).filter(ProgettoNPI.ProdottoID == prodotto_id).first()
            if existing:
                return None

            nuovo_progetto = ProgettoNPI(ProdottoID=prodotto_id, StatoProgetto='Attivo')
            session.add(nuovo_progetto)
            session.flush()

            nuova_wave = WaveNPI(ProgettoID=nuovo_progetto.ProgettoID, WaveIdentifier=1.0)
            session.add(nuova_wave)
            session.flush()

            tasks_catalogo = session.query(TaskCatalogo).all()
            for task_cat in tasks_catalogo:
                nuovo_task_prodotto = TaskProdotto(
                    WaveID=nuova_wave.WaveID,
                    TaskID=task_cat.TaskID
                )
                session.add(nuovo_task_prodotto)

            session.commit()

            progetto_completo = session.query(ProgettoNPI).options(
                joinedload(ProgettoNPI.prodotto)
            ).filter(ProgettoNPI.ProgettoID == nuovo_progetto.ProgettoID).one()

            return progetto_completo
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def debug_get_progetto(self, project_id):
        """Metodo di debug per verificare se il progetto esiste"""
        session = self.Session()
        try:
            progetto = session.query(ProgettoNPI).filter(ProgettoNPI.ProgettoID == project_id).first()
            if progetto:
                print(f"Progetto trovato: ID={progetto.ProgettoID}, ProdottoID={progetto.ProdottoID}")
                prodotto = session.query(Prodotto).filter(Prodotto.ProdottoID == progetto.ProdottoID).first()
                if prodotto:
                    print(f"Prodotto associato: {prodotto.NomeProdotto}")
                else:
                    print("Nessun prodotto associato trovato")
            else:
                print(f"Nessun progetto trovato con ID {project_id}")
            return progetto
        finally:
            session.close()

    def get_dettagli_progetto(self, project_id):
        """
        Recupera UN progetto NPI con tutte le sue wave e i suoi task.
        """
        session = self.Session()
        try:
            logger.debug(f"DEBUG: Cerco progetto con ID {project_id}")

            progetto = session.query(ProgettoNPI).options(
                joinedload(ProgettoNPI.prodotto),
                subqueryload(ProgettoNPI.waves).subqueryload(WaveNPI.tasks).options(
                    joinedload(TaskProdotto.owner),
                    joinedload(TaskProdotto.task_template).joinedload(TaskCatalogo.category)
                )
            ).filter(ProgettoNPI.ProgettoID == project_id).first()

            if progetto:
                logger.info(f"DEBUG: Progetto trovato - {progetto.prodotto.NomeProdotto}")
                logger.info(f"DEBUG: Numero di waves: {len(progetto.waves)}")
                if progetto.waves:
                    logger.debug(f"DEBUG: Numero di task nella prima wave: {len(progetto.waves[0].tasks)}")
            else:
                logger.info(f"DEBUG: Nessun progetto trovato con ID {project_id}")

            return progetto
        except Exception as e:
            logger.error(f"DEBUG: Errore durante il recupero del progetto: {e}")
            return None
        finally:
            session.close()

    def update_task_prodotto(self, task_prodotto_id, data):
        """
        Aggiorna i dettagli di un singolo TaskProdotto all'interno di un progetto NPI.
        """
        session = self.Session()
        try:
            task = session.query(TaskProdotto).get(task_prodotto_id)
            if not task:
                raise ValueError(f"Nessun TaskProdotto trovato con ID {task_prodotto_id}")

            date_fields = ['DataScadenza', 'DataInizio', 'DataCompletamento']
            for field in date_fields:
                if data.get(field) in ('', None):
                    data[field] = None
                elif isinstance(data.get(field), str):
                    try:
                        data[field] = datetime.strptime(data[field], '%d/%m/%Y').date()
                    except (ValueError, TypeError):
                        data[field] = None

            for key, value in data.items():
                setattr(task, key, value)

            session.commit()
            return task
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def invia_notifiche_task(self, task: TaskProdotto, conferma_utente: bool = True, lang: dict = None):
        """
        Invia le notifiche per un task specifico.

        Args:
            task: Il task da notificare
            conferma_utente: Se mostrare dialog di conferma
            lang: Dizionario con le traduzioni

        Returns:
            bool: True se le notifiche sono state inviate con successo
        """
        try:
            # Qui dovresti inizializzare il NotificationManager con i parametri appropriati
            # Per ora restituiamo True come placeholder
            logger.info(f"Notifiche inviate per task {task.TaskProdottoID}")
            return True
        except Exception as e:
            logger.error(f"Errore nell'invio notifiche per task {task.TaskProdottoID}: {e}")
            return False

    def get_gantt_data(self, progetto_id: int):
        """
        Recupera i dati di un progetto formattati per Plotly per il diagramma di Gantt.
        Mostra solo i task che sono stati assegnati E hanno date valide.
        """
        progetto = self.get_dettagli_progetto(progetto_id)
        if not progetto or not progetto.waves:
            return None, None

        df_data = []
        for task in progetto.waves[0].tasks:
            # Filtra solo i task che hanno un proprietario assegnato E date valide
            if task.OwnerID is not None and task.DataInizio and task.DataScadenza:
                df_data.append({
                    'Task': task.task_template.NomeTask,
                    'Start': task.DataInizio,
                    'Finish': task.DataScadenza,
                    'Owner': task.owner.NomeSoggetto if task.owner else 'Non Assegnato',
                    'Status': task.Stato,
                    'TaskProdottoID': task.TaskProdottoID
                })
            else:
                # Debug: log dei task esclusi
                if task.OwnerID is None:
                    print(f"DEBUG: Task '{task.task_template.NomeTask}' non assegnato - saltato nel Gantt")
                elif not task.DataInizio or not task.DataScadenza:
                    print(f"DEBUG: Task '{task.task_template.NomeTask}' senza date valide - saltato nel Gantt")

        print(f"DEBUG: Totale task nel progetto: {len(progetto.waves[0].tasks)}")
        print(f"DEBUG: Task mostrati nel Gantt: {len(df_data)}")

        if not df_data:
            print("DEBUG: Nessun task da mostrare nel Gantt - tutti i task sono non assegnati o senza date")

        return df_data, progetto.prodotto.NomeProdotto


    def aggiorna_date_task_from_gantt(self, task_prodotto_id: int, nuova_data_inizio: datetime,
                                      nuova_data_scadenza: datetime, user: str):
        """
        Aggiorna le date di un task specifico dal Gantt.
        """
        session = self.Session()
        try:
            task = session.query(TaskProdotto).get(task_prodotto_id)
            if not task:
                raise ValueError(f"Task non trovato con ID {task_prodotto_id}")

            task.DataInizio = nuova_data_inizio.date()
            task.DataScadenza = nuova_data_scadenza.date()

            current_note = task.Note or ''
            log_note = f"\nDate aggiornate da {user} il {datetime.now().strftime('%d/%m/%Y')}."
            task.Note = current_note.strip() + log_note

            session.commit()
            logger.info(f"Date del TaskProdotto {task_prodotto_id} aggiornate da {user}.")
            return True
        except Exception as e:
            session.rollback()
            logger.error(f"Errore nell'aggiornamento del task {task_prodotto_id}: {e}")
            raise
        finally:
            session.close()