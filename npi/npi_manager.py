# File: npi/npi_manager.py
import logging
from datetime import datetime
from sqlalchemy.orm import sessionmaker, joinedload, subqueryload, selectinload, scoped_session
from sqlalchemy.engine import Engine
from sqlalchemy import select, update, delete, func, and_, event, text
from sqlalchemy.pool import QueuePool
from npi.data_models import ProgettoNPI, Base, Prodotto, Soggetto, TaskCatalogo, Categoria, WaveNPI, TaskProdotto
import urllib

logger = logging.getLogger(__name__)

class GestoreNPI:
    """
    Classe principale che orchestra la gestione dei dati NPI tramite il DB.
    """

    def __init__(self, engine: Engine):
        if not engine:
            raise ValueError("SQLAlchemy Engine non può essere None.")

        self.engine = engine

        # Crea le tabelle se non esistono
        Base.metadata.create_all(self.engine, checkfirst=True)

        # Configura sessionmaker - NON usare scoped_session che causa problemi
        self.session_factory = sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
            autoflush=True,
            autocommit=False
        )

        logger.info("GestoreNPI pronto e tabelle NPI verificate/create.")

    def _setup_connection_events(self):
        """Setup event listeners per gestione connessioni (opzionale per debugging)."""

        @event.listens_for(self.engine, "connect")
        def receive_connect(dbapi_conn, connection_record):
            """Chiamato quando viene creata una nuova connessione."""
            logger.debug("Nuova connessione database stabilita")

        @event.listens_for(self.engine, "close")
        def receive_close(dbapi_conn, connection_record):
            """Chiamato quando una connessione viene chiusa."""
            logger.debug("Connessione database chiusa")

    # Sostituisci il metodo _get_session con questo:

    def _get_session(self):
        """Crea una nuova sessione per ogni operazione."""
        try:
            session = self.session_factory()
            # Test semplice della connessione
            session.execute(text("SELECT 1"))
            return session
        except Exception as e:
            logger.error(f"Errore nella creazione della sessione: {e}")
            raise

    def _detach_object(self, session, obj):
        """Helper per rendere un oggetto indipendente dalla sessione."""
        if obj:
            session.expunge(obj)
        return obj

    def _detach_list(self, session, obj_list):
        """Helper per rendere una lista di oggetti indipendente dalla sessione."""
        for obj in obj_list:
            session.expunge(obj)
        return obj_list

    def get_soggetti(self):
        """Recupera tutti i soggetti ordinati per nome."""
        session = self._get_session()
        try:
            soggetti = session.scalars(
                select(Soggetto).order_by(Soggetto.Nome)
            ).all()
            return self._detach_list(session, soggetti)
        except Exception as e:
            logger.error(f"Errore in get_soggetti: {e}")
            session.rollback()
            raise
        finally:
            session.close()

    def get_soggetto_by_id(self, soggetto_id):
        """Recupera un soggetto per ID."""
        session = self._get_session()
        try:
            soggetto = session.scalars(
                select(Soggetto).where(Soggetto.SoggettoId == soggetto_id)
            ).first()
            return self._detach_object(session, soggetto)
        except Exception as e:
            logger.error(f"Errore in get_soggetto_by_id: {e}")
            session.rollback()
            raise
        finally:
            session.close()

    def create_soggetto(self, data):
        """Crea un nuovo soggetto."""
        session = self._get_session()
        try:
            nuovo_soggetto = Soggetto(**data)
            session.add(nuovo_soggetto)
            session.commit()
            session.refresh(nuovo_soggetto)
            return self._detach_object(session, nuovo_soggetto)
        except Exception as e:
            logger.error(f"Errore in create_soggetto: {e}")
            session.rollback()
            raise
        finally:
            session.close()

    def update_soggetto(self, soggetto_id, data):
        """Aggiorna un soggetto esistente."""
        session = self._get_session()
        try:
            soggetto = session.get(Soggetto, soggetto_id)
            if soggetto:
                for key, value in data.items():
                    setattr(soggetto, key, value)
                session.commit()
                session.refresh(soggetto)
                return self._detach_object(session, soggetto)
            return None
        except Exception as e:
            logger.error(f"Errore in update_soggetto: {e}")
            session.rollback()
            raise
        finally:
            session.close()

    def delete_soggetto(self, soggetto_id):
        """Elimina un soggetto."""
        session = self._get_session()
        try:
            soggetto = session.get(Soggetto, soggetto_id)
            if soggetto:
                session.delete(soggetto)
                session.commit()
                return True
            return False
        except Exception as e:
            logger.error(f"Errore in delete_soggetto: {e}")
            session.rollback()
            raise
        finally:
            session.close()


            # --- METODI CRUD PER PRODOTTI ---

    def get_prodotti(self):
        """Recupera tutti i prodotti ordinati per nome."""
        session = self._get_session()
        try:
            prodotti = session.scalars(
                select(Prodotto).order_by(Prodotto.NomeProdotto)
            ).all()

            return self._detach_list(session, prodotti)
        except Exception as e:
            logger.error(f"Errore in get_prodotti: {e}")
            session.rollback()
            raise
        finally:
            session.close()

    def get_prodotto_by_id(self, prodotto_id):
        """Recupera un prodotto per ID."""
        session = self._get_session()
        try:
            prodotto = session.scalars(
                select(Prodotto).where(Prodotto.ProdottoID == prodotto_id)
            ).first()

            return self._detach_object(session, prodotto)
        except Exception as e:
            logger.error(f"Errore in get_prodotto_by_id: {e}")
            session.rollback()
            raise
        finally:
            session.close()

    def create_prodotto(self, data):
        """Crea un nuovo prodotto."""
        session = self._get_session()
        try:
            nuovo_prodotto = Prodotto(**data)
            session.add(nuovo_prodotto)
            session.commit()
            session.refresh(nuovo_prodotto)

            return self._detach_object(session, nuovo_prodotto)
        except Exception as e:
            logger.error(f"Errore in create_prodotto: {e}")
            session.rollback()
            raise
        finally:
            session.close()

    def update_prodotto(self, prodotto_id, data):
        """Aggiorna un prodotto esistente."""
        session = self._get_session()
        try:
            prodotto = session.get(Prodotto, prodotto_id)
            if prodotto:
                for key, value in data.items():
                    setattr(prodotto, key, value)
                session.commit()
                session.refresh(prodotto)
                return self._detach_object(session, prodotto)
            return None
        except Exception as e:
            logger.error(f"Errore in update_prodotto: {e}")
            session.rollback()
            raise
        finally:
            session.close()

    def delete_prodotto(self, prodotto_id):
        """Elimina un prodotto."""
        session = self._get_session()
        try:
            prodotto = session.get(Prodotto, prodotto_id)
            if prodotto:
                session.delete(prodotto)
                session.commit()
                return True
            return False
        except Exception as e:
            logger.error(f"Errore in delete_prodotto: {e}")
            session.rollback()
            raise
        finally:
            session.close()

            # --- METODI CRUD PER CATEGORIE ---

    def get_categories(self):
        """Recupera tutte le categorie ordinate per NrOrdin."""
        session = self._get_session()
        try:
            categories = session.scalars(
                select(Categoria).order_by(Categoria.NrOrdin)
            ).all()

            return self._detach_list(session, categories)
        except Exception as e:
            logger.error(f"Errore in get_categories: {e}")
            session.rollback()
            raise
        finally:
            session.close()

    def get_category_by_id(self, category_id):
        """Recupera una categoria per ID."""
        session = self._get_session()
        try:
            category = session.scalars(
                select(Categoria).where(Categoria.CategoryId == category_id)
            ).first()

            return self._detach_object(session, category)
        except Exception as e:
            logger.error(f"Errore in get_category_by_id: {e}")
            session.rollback()
            raise
        finally:
            session.close()

    def create_category(self, data):
        """Crea una nuova categoria con controllo duplicati NrOrdin."""
        session = self._get_session()
        try:
            # Controllo duplicati di NrOrdin prima di inserire
            nr_ordin_value = data.get('NrOrdin')
            if nr_ordin_value is not None:
                existing = session.scalars(
                    select(Categoria).where(Categoria.NrOrdin == nr_ordin_value)
                ).first()
                if existing:
                    raise ValueError(
                        f"Il numero d'ordine {nr_ordin_value} è già utilizzato "
                        f"dalla categoria '{existing.Category}'."
                    )

            new_category = Categoria(**data)
            session.add(new_category)
            session.commit()
            session.refresh(new_category)

            return self._detach_object(session, new_category)
        except Exception as e:
            logger.error(f"Errore in create_category: {e}")
            session.rollback()
            raise
        finally:
            session.close()

    def update_category(self, category_id, data):
        """Aggiorna una categoria con controllo duplicati NrOrdin."""
        session = self._get_session()
        try:
            # Controllo duplicati di NrOrdin, escludendo la categoria corrente
            nr_ordin_value = data.get('NrOrdin')
            if nr_ordin_value is not None:
                existing = session.scalars(
                    select(Categoria).where(
                        and_(
                            Categoria.NrOrdin == nr_ordin_value,
                            Categoria.CategoryId != category_id
                        )
                    )
                ).first()
                if existing:
                    raise ValueError(
                        f"Il numero d'ordine {nr_ordin_value} è già utilizzato "
                        f"dalla categoria '{existing.Category}'."
                    )

            category = session.get(Categoria, category_id)
            if category:
                for key, value in data.items():
                    setattr(category, key, value)
                session.commit()
                session.refresh(category)
                return self._detach_object(session, category)
            return None
        except Exception as e:
            logger.error(f"Errore in update_category: {e}")
            session.rollback()
            raise
        finally:
            session.close()

    def delete_category(self, category_id):
        """Elimina una categoria con controllo utilizzo."""
        session = self._get_session()
        try:
            # Controlla se la categoria è associata a qualche task
            num_tasks = session.scalar(
                select(func.count(TaskCatalogo.TaskID)).where(
                    TaskCatalogo.CategoryId == category_id
                )
            )
            if num_tasks > 0:
                raise Exception(
                    f"Impossibile eliminare la categoria: è associata a {num_tasks} "
                    f"task nel catalogo."
                )

            category = session.get(Categoria, category_id)
            if category:
                session.delete(category)
                session.commit()
                return True
            return False
        except Exception as e:
            logger.error(f"Errore in delete_category: {e}")
            session.rollback()
            raise
        finally:
            session.close()

    def get_catalogo_task(self):
        """Recupera tutti i task del catalogo con categoria."""
        session = self._get_session()
        try:
            stmt = select(TaskCatalogo).options(
                selectinload(TaskCatalogo.categoria)
            ).order_by(TaskCatalogo.NrOrdin)

            tasks = session.scalars(stmt).all()

            return self._detach_list(session, tasks)
        except Exception as e:
            logger.error(f"Errore in get_catalogo_task: {e}")
            session.rollback()
            raise
        finally:
            session.close()

    def get_catalogo_task_by_id(self, task_id):
        """Recupera un task del catalogo per ID."""
        session = self._get_session()
        try:
            stmt = select(TaskCatalogo).options(
                selectinload(TaskCatalogo.categoria)
            ).where(TaskCatalogo.TaskID == task_id)

            task = session.scalars(stmt).first()

            return self._detach_object(session, task)
        except Exception as e:
            logger.error(f"Errore in get_catalogo_task_by_id: {e}")
            session.rollback()
            raise
        finally:
            session.close()

    def get_catalogo_task_by_itemid(self, item_id: str):
        """Recupera un task del catalogo per ItemID."""
        session = self._get_session()
        try:
            task = session.scalars(
                select(TaskCatalogo).where(TaskCatalogo.ItemID == item_id)
            ).first()

            return self._detach_object(session, task)
        except Exception as e:
            logger.error(f"Errore in get_catalogo_task_by_itemid: {e}")
            session.rollback()
            raise
        finally:
            session.close()

    def _renumber_all_tasks(self, session):
        """Rinumera tutti i task con un passo di 10."""
        logger.info("Rinumerazione in corso per tutti i task del catalogo...")
        all_tasks = session.scalars(
            select(TaskCatalogo).order_by(TaskCatalogo.NrOrdin, TaskCatalogo.ItemID)
        ).all()

        for i, task in enumerate(all_tasks):
            task.NrOrdin = (i + 1) * 10

        session.flush()
        logger.info("Rinumerazione completata.")

    def create_catalogo_task(self, data, anchor_task_id=None):
        """Crea un nuovo task nel catalogo."""
        session = self._get_session()
        try:
            is_title = data.get('IsTitle', False)

            if is_title and data.get('CategoryId') is not None:
                min_ordin = session.scalar(
                    select(func.min(TaskCatalogo.NrOrdin)).where(
                        TaskCatalogo.CategoryId == data['CategoryId']
                    )
                )
                if min_ordin is not None:
                    data['NrOrdin'] = min_ordin - 5  # Si posiziona prima
                else:
                    cat_ordin = session.scalar(
                        select(Categoria.NrOrdin).where(
                            Categoria.CategoryId == data['CategoryId']
                        )
                    )
                    data['NrOrdin'] = (cat_ordin or 0) * 100
            else:
                if anchor_task_id:
                    anchor_task = session.get(TaskCatalogo, anchor_task_id)
                    anchor_ordin = anchor_task.NrOrdin if anchor_task else 0

                    next_ordin = session.scalar(
                        select(TaskCatalogo.NrOrdin)
                        .where(TaskCatalogo.NrOrdin > anchor_ordin)
                        .order_by(TaskCatalogo.NrOrdin.asc())
                        .limit(1)
                    )
                else:
                    anchor_ordin = session.scalar(
                        select(func.max(TaskCatalogo.NrOrdin))
                    ) or 0
                    next_ordin = None

                if next_ordin is None:
                    new_ordin = anchor_ordin + 10
                else:
                    gap = next_ordin - anchor_ordin
                    if gap < 2:
                        self._renumber_all_tasks(session)
                        # Ricalcola dopo numerazione
                        refreshed_anchor = session.get(TaskCatalogo, anchor_task_id)
                        new_anchor_ordin = refreshed_anchor.NrOrdin if refreshed_anchor else 0
                        new_ordin = new_anchor_ordin + 5
                    else:
                        new_ordin = anchor_ordin + gap // 2

                data['NrOrdin'] = new_ordin

            nuovo = TaskCatalogo(**data)
            session.add(nuovo)
            session.commit()
            session.refresh(nuovo)

            return self._detach_object(session, nuovo)
        except Exception as e:
            logger.error(f"Errore in create_catalogo_task: {e}")
            session.rollback()
            raise
        finally:
            session.close()

    def update_catalogo_task(self, task_id, data):
        """Aggiorna un task del catalogo."""
        session = self._get_session()
        try:
            task = session.get(TaskCatalogo, task_id)
            if task:
                for key, value in data.items():
                    setattr(task, key, value)
                session.commit()
                session.refresh(task)
                return self._detach_object(session, task)
            return None
        except Exception as e:
            logger.error(f"Errore in update_catalogo_task: {e}")
            session.rollback()
            raise
        finally:
            session.close()

    def delete_catalogo_task(self, task_id):
        """Elimina un task del catalogo."""
        session = self._get_session()
        try:
            task = session.get(TaskCatalogo, task_id)
            if task:
                session.delete(task)
                session.commit()
                return True
            return False
        except Exception as e:
            logger.error(f"Errore in delete_catalogo_task: {e}")
            session.rollback()
            raise
        finally:
            session.close()

    def get_progetti_attivi(self):
        """Restituisce una lista di tutti i progetti NPI con stato 'Attivo'."""
        session = self._get_session()
        try:
            progetti = session.scalars(
                select(ProgettoNPI)
                .options(joinedload(ProgettoNPI.prodotto))
                .where(ProgettoNPI.StatoProgetto == 'Attivo')
                .order_by(ProgettoNPI.ProgettoId.desc())
            ).all()
            return self._detach_list(session, progetti)
        except Exception as e:
            logger.error(f"Errore in get_progetti_attivi: {e}")
            session.rollback()
            raise
        finally:
            session.close()

    def create_progetto_npi_for_prodotto(self, prodotto_id):
        """Crea un progetto NPI, la sua Wave 1.0 e tutti i task associati."""
        session = self._get_session()
        try:
            # Verifica se esiste già un progetto per questo prodotto
            existing = session.scalars(
                select(ProgettoNPI).where(ProgettoNPI.ProdottoID == prodotto_id)
            ).first()
            if existing:
                return None

            # Crea il progetto
            nuovo_progetto = ProgettoNPI(
                ProdottoID=prodotto_id,
                StatoProgetto='Attivo',
                DataInizio=datetime.now()
            )
            session.add(nuovo_progetto)
            session.flush()

            # Crea la Wave 1.0
            nuova_wave = WaveNPI(
                ProgettoID=nuovo_progetto.ProgettoId,
                WaveIdentifier=1.0
            )
            session.add(nuova_wave)
            session.flush()

            # Crea i task prodotto da catalogo
            tasks_catalogo = session.scalars(select(TaskCatalogo)).all()
            for task_cat in tasks_catalogo:
                nuovo_task_prodotto = TaskProdotto(
                    WaveID=nuova_wave.WaveID,
                    TaskID=task_cat.TaskId
                )
                session.add(nuovo_task_prodotto)

            session.commit()

            # Recupera il progetto completo
            progetto_completo = session.scalars(
                select(ProgettoNPI)
                .options(joinedload(ProgettoNPI.prodotto))
                .where(ProgettoNPI.ProgettoId == nuovo_progetto.ProgettoId)
            ).one()

            return self._detach_object(session, progetto_completo)
        except Exception as e:
            logger.error(f"Errore in create_progetto_npi_for_prodotto: {e}")
            session.rollback()
            raise
        finally:
            session.close()

    def debug_get_progetto(self, project_id):
        """Metodo di debug per verificare se il progetto esiste."""
        session = self._get_session()
        try:
            progetto = session.scalars(
                select(ProgettoNPI).where(ProgettoNPI.ProgettoID == project_id)
            ).first()

            if progetto:
                logger.info(f"Progetto trovato: ID={progetto.ProgettoID}, ProdottoID={progetto.ProdottoID}")
                prodotto = session.get(Prodotto, progetto.ProdottoID)
                if prodotto:
                    logger.info(f"Prodotto associato: {prodotto.NomeProdotto}")
                else:
                    logger.info("Nessun prodotto associato trovato")
            else:
                logger.info(f"Nessun progetto trovato con ID {project_id}")

            return self._detach_object(session, progetto)
        except Exception as e:
            logger.error(f"Errore in debug_get_progetto: {e}")
            session.rollback()
            raise
        finally:
            session.close()

    def get_dettagli_progetto(self, project_id):
        """Recupera UN progetto NPI con tutte le sue wave e i suoi task."""
        session = self._get_session()
        try:
            logger.debug(f"Cerco progetto con ID {project_id}")

            progetto = session.scalars(
                select(ProgettoNPI)
                .options(
                    joinedload(ProgettoNPI.prodotto),
                    subqueryload(ProgettoNPI.waves).subqueryload(WaveNPI.tasks).options(
                        joinedload(TaskProdotto.owner),
                        joinedload(TaskProdotto.task_catalogo).joinedload(TaskCatalogo.categoria)
                    )
                )
                .where(ProgettoNPI.ProgettoId == project_id)
            ).first()

            if progetto:
                logger.info(f"Progetto trovato - {progetto.prodotto.NomeProdotto}")
                logger.info(f"Numero di waves: {len(progetto.waves)}")
                if progetto.waves:
                    logger.debug(f"Numero di task nella prima wave: {len(progetto.waves[0].tasks)}")
            else:
                logger.info(f"Nessun progetto trovato con ID {project_id}")

            return self._detach_object(session, progetto)
        except Exception as e:
            logger.error(f"Errore durante il recupero del progetto: {e}")
            session.rollback()
            return None
        finally:
            session.close()

    def update_project_dates(self, project_id: int, start_date: datetime, due_date: datetime, lang):
        """
        Aggiorna le date di un progetto con logica di business per il task finale (IsFinalMilestone=True).
        Restituisce una tupla (progetto_aggiornato, messaggio_informativo).
        """
        session = self._get_session()
        try:
            # 1. VALIDAZIONE INIZIALE
            if due_date and start_date and due_date < start_date:  # Aggiunto controllo su start_date not None
                raise ValueError(lang.get('validation_error_end_before_start'))
            if not start_date:
                raise ValueError(lang.get('validation_error_start_date_required'))

            override_message = None
            progetto = session.get(ProgettoNPI, project_id)
            if not progetto:
                raise ValueError(f"Progetto con ID {project_id} non trovato.")

            # 2. CERCA IL TASK SPECIALE (con IsFinalMilestone=True)
            # --- MODIFICA LOGICA QUI ---
            # Query per trovare il TaskProdotto collegato al TaskCatalogo con IsFinalMilestone=True
            final_milestone_task = session.scalars(
                select(TaskProdotto)
                .join(TaskCatalogo, TaskProdotto.TaskID == TaskCatalogo.TaskID)
                .join(WaveNPI, TaskProdotto.WaveID == WaveNPI.WaveID)
                .filter(
                    WaveNPI.ProgettoID == project_id,
                    TaskCatalogo.IsFinalMilestone == True  # Cerca per flag, non per ID
                )
            ).first()
            # --- FINE MODIFICA ---

            # 3. APPLICA LOGICA DI BUSINESS SUL TASK FINALE
            if final_milestone_task:
                # Caso A: Se il task finale è già assegnato e ha una data...
                if final_milestone_task.OwnerID is not None and final_milestone_task.DataScadenza is not None:
                    # La scadenza del progetto DEVE essere uguale a quella del task.
                    due_date = final_milestone_task.DataScadenza
                    base_msg = lang.get('info_project_due_date_aligned')
                    task_name = final_milestone_task.task_catalogo.NomeTask
                    override_message = f"{base_msg} (Task: '{task_name}')"
                # Caso B: Il task finale non è assegnato (o non ha una data)...
                else:
                    # La sua scadenza viene impostata uguale a quella del progetto.
                    final_milestone_task.DataScadenza = due_date

            # 4. AGGIORNA LE DATE DEL PROGETTO
            progetto.DataInizio = start_date
            progetto.ScadenzaProgetto = due_date

            session.commit()

            # 5. RESTITUISCI I DATI
            # Non serve fare il refresh, basta restituire l'oggetto con le date aggiornate
            return progetto, override_message

        except Exception as e:
            logger.error(f"Errore durante l'aggiornamento delle date del progetto {project_id}: {e}", exc_info=True)
            session.rollback()
            raise
        finally:
            session.close()

    def update_task_prodotto(self, task_prodotto_id, data):
        """Aggiorna i dettagli di un singolo TaskProdotto."""
        session = self._get_session()
        try:
            task = session.get(TaskProdotto, task_prodotto_id)
            if not task:
                raise ValueError(f"Nessun TaskProdotto trovato con ID {task_prodotto_id}")

            # Gestione campi data
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
            session.refresh(task)

            return self._detach_object(session, task)
        except Exception as e:
            logger.error(f"Errore in update_task_prodotto: {e}")
            session.rollback()
            raise
        finally:
            session.close()

    def invia_notifiche_task(self, task: TaskProdotto, conferma_utente: bool = True, lang: dict = None):
        """Invia le notifiche per un task specifico."""
        try:
            logger.info(f"Notifiche inviate per task {task.TaskProdottoID}")
            return True
        except Exception as e:
            logger.error(f"Errore nell'invio notifiche per task {task.TaskProdottoID}: {e}")
            return False

    def get_gantt_data(self, progetto_id: int):
        """Recupera i dati di un progetto formattati per Plotly per il diagramma di Gantt."""
        session = self._get_session()
        try:
            progetto = session.scalars(
                select(ProgettoNPI)
                .options(
                    joinedload(ProgettoNPI.prodotto),
                    subqueryload(ProgettoNPI.waves).subqueryload(WaveNPI.tasks).options(
                        joinedload(TaskProdotto.owner),
                        joinedload(TaskProdotto.task_catalogo)
                    )
                )
                .where(ProgettoNPI.ProgettoId == progetto_id)
            ).first()

            if not progetto or not progetto.waves:
                return None, None

            df_data = []
            for task in progetto.waves[0].tasks:
                # Filtra solo i task che hanno un proprietario assegnato E date valide
                if (task.OwnerID is not None and
                        task.DataInizio and
                        task.DataScadenza):

                    # Assicurati che la data di fine sia >= alla data di inizio
                    if task.DataInizio > task.DataScadenza:
                        data_inizio = task.DataScadenza
                        data_fine = task.DataInizio
                    else:
                        data_inizio = task.DataInizio
                        data_fine = task.DataScadenza

                    df_data.append({
                        'Task': task.task_catalogo.NomeTask if task.task_catalogo else "Task non definito",
                        'Start': data_inizio,
                        'Finish': data_fine,
                        'Owner': task.owner.Nome if task.owner else 'Non Assegnato',
                        'Status': task.Stato,
                        'TaskProdottoID': task.TaskProdottoID
                    })

            logger.debug(f"Totale task nel progetto: {len(progetto.waves[0].tasks)}")
            logger.debug(f"Task mostrati nel Gantt: {len(df_data)}")

            return df_data, progetto.prodotto.NomeProdotto

        except Exception as e:
            logger.error(f"Errore in get_gantt_data: {e}")
            raise
        finally:
            session.close()

    def aggiorna_date_task_from_gantt(self, task_prodotto_id: int, nuova_data_inizio: datetime,
                                      nuova_data_scadenza: datetime, user: str):
        """Aggiorna le date di un task specifico dal Gantt."""
        session = self._get_session()
        try:
            task = session.get(TaskProdotto, task_prodotto_id)
            if not task:
                raise ValueError(f"Task non trovato con ID {task_prodotto_id}")

            task.DataInizio = nuova_data_inizio.date()
            task.DataScadenza = nuova_data_scadenza.date()

            current_note = task.Note or ''
            log_note = f"\nDate aggiornate da {user} il {datetime.now().strftime('%d/%m/%Y')}."
            task.Note = current_note.strip() + log_note

            session.commit()
            session.refresh(task)

            logger.info(f"Date del TaskProdotto {task_prodotto_id} aggiornate da {user}.")

            return self._detach_object(session, task)
        except Exception as e:
            logger.error(f"Errore nell'aggiornamento del task {task_prodotto_id}: {e}")
            session.rollback()
            raise
        finally:
            session.close()

    def get_dashboard_projects(self):
        """
        Recupera i dati dei progetti per la dashboard principale, basandosi sulla milestone finale.
        """
        session = self._get_session()
        try:
            # Replica della query richiesta con SQLAlchemy
            stmt = select(
                ProgettoNPI.ProgettoId,
                func.coalesce(ProgettoNPI.NomeProgetto, Prodotto.NomeProdotto).label("NomeProgetto"),
                Prodotto.CodiceProdotto,
                Prodotto.Cliente,
                TaskProdotto.DataScadenza.label("ScadenzaMilestoneFinale")
            ).join(
                Prodotto, ProgettoNPI.ProdottoID == Prodotto.ProdottoID
            ).join(
                WaveNPI, ProgettoNPI.ProgettoId == WaveNPI.ProgettoID
            ).join(
                TaskProdotto, WaveNPI.WaveID == TaskProdotto.WaveID
            ).join(
                TaskCatalogo, TaskProdotto.TaskID == TaskCatalogo.TaskID
            ).where(
                TaskCatalogo.IsFinalMilestone == True
            ).order_by(
                ProgettoNPI.DataInizio.desc()
            )

            result = session.execute(stmt).all()
            return result
        finally:
            session.close()

    def get_project_analysis(self, project_id: int):
        """
        Analizza un progetto per trovare i task in ritardo per ogni owner.
        """
        session = self._get_session()
        try:
            from collections import defaultdict
            today = datetime.now().date()

            # Carica tutti i task del progetto con owner e catalogo
            tasks = session.scalars(
                select(TaskProdotto)
                .join(WaveNPI)
                .options(
                    joinedload(TaskProdotto.owner),
                    joinedload(TaskProdotto.task_catalogo)
                )
                .where(WaveNPI.ProgettoID == project_id)
            ).all()

            late_tasks_by_owner = defaultdict(list)
            final_milestone_task = None

            for task in tasks:
                # Trova la milestone finale per il reminder
                if task.task_catalogo and task.task_catalogo.IsFinalMilestone:
                    final_milestone_task = task

                # Controlla se il task è in ritardo
                if (task.owner and task.DataScadenza and
                        task.DataScadenza.date() < today and
                        task.Stato not in ['Completato']):
                    late_tasks_by_owner[task.owner].append(task)

            return late_tasks_by_owner, final_milestone_task
        finally:
            session.close()

    def send_project_reminders(self, late_tasks_by_owner, final_milestone_task):
        """
        Invia email di sollecito (in inglese) agli owner con task in ritardo.
        """
        from email_connector import EmailSender  # Import locale
        total_sent = 0
        total_failed = 0

        # Prepara il corpo base del reminder sulla milestone finale
        final_milestone_info = "No final milestone date set for this project."
        if final_milestone_task and final_milestone_task.DataScadenza:
            final_milestone_info = (f"Please remember the final project milestone is on: "
                                    f"<strong>{final_milestone_task.DataScadenza.strftime('%Y-%m-%d')}</strong>.")

        # Inizializza il sender
        try:
            email_sender = EmailSender()
            # Le credenziali sono caricate da file dentro EmailSender
        except Exception as e:
            logger.error(f"Failed to initialize EmailSender: {e}")
            raise Exception(f"Failed to initialize EmailSender: {e}")

        for owner, tasks in late_tasks_by_owner.items():
            if not owner.Email:
                logger.warning(f"Owner {owner.Nome} has no email address. Skipping reminder.")
                total_failed += 1
                continue

            # Costruisci l'elenco dei task in ritardo
            tasks_html_list = "<ul>"
            for task in tasks:
                tasks_html_list += (f"<li><strong>{task.task_catalogo.NomeTask}</strong> "
                                    f"(Due Date: {task.DataScadenza.strftime('%Y-%m-%d')})</li>")
            tasks_html_list += "</ul>"

            # Corpo e oggetto dell'email
            subject = "NPI Project - Overdue Task Reminder"
            body = f"""
            <html>
            <body>
                <p>Dear {owner.Nome},</p>
                <p>This is an automatic reminder. The following tasks assigned to you for the NPI project are overdue:</p>
                {tasks_html_list}
                <p>Please update their status or complete them as soon as possible.</p>
                <br>
                <p><em>{final_milestone_info}</em></p>
                <br>
                <p>Thank you,</p>
                <p>NPI Management System</p>
            </body>
            </html>
            """

            # Invia email
            try:
                email_sender.send_email(
                    to_email=owner.Email,
                    subject=subject,
                    body=body,
                    is_html=True
                )
                logger.info(f"Reminder sent successfully to {owner.Email}")
                total_sent += 1
            except Exception as e:
                logger.error(f"Failed to send reminder to {owner.Email}: {e}")
                total_failed += 1

        return total_sent, total_failed

    def get_full_projects_report_data(self):
        """
        Prepara i dati completi per il report PDF, includendo l'analisi dei ritardi
        per ogni progetto attivo. Restituisce una lista di dizionari.
        """
        report_data = []

        # 1. Recupera la lista dei progetti attivi dalla dashboard
        active_projects = self.get_dashboard_projects()
        if not active_projects:
            return []

        for proj_summary in active_projects:
            project_id = proj_summary.ProgettoId

            # 2. Per ogni progetto, esegui l'analisi dei ritardi
            late_tasks_by_owner, _ = self.get_project_analysis(project_id)

            # 3. Formatta l'analisi dei ritardi
            analysis_summary = []
            if late_tasks_by_owner:
                for owner, tasks in late_tasks_by_owner.items():
                    analysis_summary.append({'owner_name': owner.Nome, 'late_count': len(tasks)})

            # 4. Aggrega tutti i dati per questo progetto
            report_data.append({
                'info': proj_summary,
                'analysis': analysis_summary
            })

        return report_data

    def get_all_npi_projects(self):
        """Recupera tutti i progetti NPI con le informazioni del prodotto associato."""
        session = self._get_session()
        try:
            progetti = session.scalars(
                select(ProgettoNPI)
                .options(joinedload(ProgettoNPI.prodotto))
                .order_by(ProgettoNPI.DataInizio.desc())
            ).all()
            return progetti
        finally:
            session.close()

    def copy_tasks_from_project(self, source_project_id: int, target_project_id: int):
        """
        Copia gli assegnamenti Owner dai task di un progetto sorgente a uno di destinazione.
        Per i task copiati, imposta lo Stato a 'Da Fare' e la DataScadenza a NULL.
        """
        if source_project_id == target_project_id:
            raise ValueError("Il progetto sorgente e quello di destinazione non possono essere gli stessi.")

        session = self._get_session()
        try:
            # 1. Recupera i task di origine (Source) e mettili in una mappa per un accesso rapido
            source_tasks_query = (
                select(TaskProdotto)
                .join(WaveNPI)
                .where(WaveNPI.ProgettoID == source_project_id)
            )
            source_tasks = session.scalars(source_tasks_query).all()
            source_task_map = {task.TaskID: task for task in source_tasks}  # Mappa TaskCatalogoID -> TaskProdotto

            # 2. Recupera i task di destinazione (Target)
            target_tasks_query = (
                select(TaskProdotto)
                .join(WaveNPI)
                .where(WaveNPI.ProgettoID == target_project_id)
            )
            target_tasks = session.scalars(target_tasks_query).all()

            if not target_tasks:
                raise ValueError("Il progetto di destinazione non ha task da aggiornare.")

            # 3. Itera sui task di destinazione e aggiornali
            updated_count = 0
            for target_task in target_tasks:
                source_task = source_task_map.get(target_task.TaskID)

                # Se esiste un task corrispondente nell'origine e ha un owner...
                if source_task and source_task.OwnerID is not None:
                    target_task.OwnerID = source_task.OwnerID
                    target_task.Stato = 'Da Fare'  # Reset dello stato
                    target_task.DataScadenza = None  # Reset della data
                    target_task.DataInizio = None
                    target_task.DataCompletamento = None
                    updated_count += 1

            session.commit()
            logger.info(
                f"Copiati {updated_count} assegnamenti dal progetto {source_project_id} al {target_project_id}.")
            return updated_count

        except Exception as e:
            logger.error(f"Errore durante la copia dei task: {e}", exc_info=True)
            session.rollback()
            raise
        finally:
            session.close()
