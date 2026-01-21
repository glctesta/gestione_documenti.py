# File: npi/npi_manager.py
import logging
from datetime import datetime
from sqlalchemy.orm import sessionmaker, joinedload, subqueryload, selectinload, scoped_session
from sqlalchemy.engine import Engine
from sqlalchemy import select, update, delete, func, and_, event, text
from sqlalchemy.pool import QueuePool
from npi.data_models import (ProgettoNPI, Base, Prodotto, Soggetto, TaskCatalogo,
                             Categoria, WaveNPI, TaskProdotto, NpiDocument, NpiDocumentType, TaskDependency)
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

    def get_tasks_by_category(self, category_id):
        """
        Recupera tutti i task del catalogo per una specifica categoria.
        
        Args:
            category_id: ID della categoria
            
        Returns:
            Lista di TaskCatalogo ordinati per NrOrdin
        """
        from sqlalchemy.orm import selectinload
        
        session = self._get_session()
        try:
            tasks = session.scalars(
                select(TaskCatalogo).options(
                    selectinload(TaskCatalogo.categoria)
                ).where(
                    TaskCatalogo.CategoryId == category_id
                ).order_by(TaskCatalogo.NrOrdin)
            ).all()
            
            return self._detach_list(session, tasks)
        except Exception as e:
            logger.error(f"Errore in get_tasks_by_category: {e}")
            session.rollback()
            raise
        finally:
            session.close()

    def is_category_used_in_projects(self, category_id):
        """
        Verifica se una categoria è stata utilizzata in almeno un progetto.
        
        Args:
            category_id: ID della categoria
            
        Returns:
            True se la categoria è usata, False altrimenti
        """
        session = self._get_session()
        try:
            # Query per verificare se esistono TaskProdotto con task di questa categoria
            count = session.scalar(
                select(func.count(TaskProdotto.TaskProdottoID)).join(
                    TaskCatalogo, TaskProdotto.TaskID == TaskCatalogo.TaskID
                ).where(
                    TaskCatalogo.CategoryId == category_id
                )
            )
            
            return count > 0
        except Exception as e:
            logger.error(f"Errore in is_category_used_in_projects: {e}")
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
        """
        Crea un nuovo task nel catalogo con numerazione gerarchica.
        
        La numerazione segue il pattern: (NrOrdin_Categoria * 100) + numero_task
        I task nella stessa categoria avanzano di 5 in 5.
        
        Esempio:
        - Categoria con NrOrdin=10: task avranno 1005, 1010, 1015, ...
        - Categoria con NrOrdin=20: task avranno 2005, 2010, 2015, ...
        """
        session = self._get_session()
        try:
            category_id = data.get('CategoryId')
            if not category_id:
                raise ValueError("CategoryId è obbligatorio per creare un task")
            
            # Ottieni il NrOrdin della categoria
            cat_ordin = session.scalar(
                select(Categoria.NrOrdin).where(
                    Categoria.CategoryId == category_id
                )
            )
            if cat_ordin is None:
                raise ValueError(f"Categoria con ID {category_id} non trovata")
            
            # Calcola la base per questa categoria (es: 10 -> 1000, 20 -> 2000)
            category_base = cat_ordin * 100
            
            # Trova il massimo NrOrdin esistente per questa categoria
            max_ordin_in_category = session.scalar(
                select(func.max(TaskCatalogo.NrOrdin)).where(
                    TaskCatalogo.CategoryId == category_id
                )
            )
            
            # Calcola il nuovo NrOrdin
            if max_ordin_in_category is None:
                # Primo task di questa categoria
                new_ordin = category_base + 5
            else:
                # Incrementa di 5 rispetto all'ultimo task della categoria
                new_ordin = max_ordin_in_category + 5
            
            data['NrOrdin'] = new_ordin
            
            logger.info(f"Creazione task in categoria {category_id} (NrOrdin cat: {cat_ordin}): nuovo NrOrdin = {new_ordin}")

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
        """
        Aggiorna un task del catalogo.
        
        Se viene modificato il NrOrdin, verifica che non esista già 
        un altro task con lo stesso NrOrdin nella stessa categoria.
        """
        session = self._get_session()
        try:
            task = session.get(TaskCatalogo, task_id)
            if not task:
                return None
            
            # Se viene modificato il NrOrdin, verifica duplicati nella categoria
            if 'NrOrdin' in data and data['NrOrdin'] != task.NrOrdin:
                new_ordin = data['NrOrdin']
                category_id = data.get('CategoryId', task.CategoryId)
                
                # Verifica se esiste già un task con questo NrOrdin nella stessa categoria
                existing_task = session.scalar(
                    select(TaskCatalogo).where(
                        and_(
                            TaskCatalogo.CategoryId == category_id,
                            TaskCatalogo.NrOrdin == new_ordin,
                            TaskCatalogo.TaskID != task_id
                        )
                    )
                )
                
                if existing_task:
                    raise ValueError(
                        f"Il numero d'ordine {new_ordin} è già utilizzato "
                        f"dal task '{existing_task.NomeTask}' nella stessa categoria."
                    )
            
            # Applica le modifiche
            for key, value in data.items():
                setattr(task, key, value)
            
            session.commit()
            session.refresh(task)
            return self._detach_object(session, task)
            
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
        """
        Restituisce una lista di tutti i progetti NPI con stato 'Attivo'.
        Utilizza una query SQL custom per formattare i dati nel formato richiesto:
        Cliente -> CodiceProdotto (Version: X) NomeProdotto [Status]
        Include il conteggio dei task assegnati.
        """
        session = self._get_session()
        try:
            # Query SQL personalizzata con conteggio task
            sql_query = """
                SELECT n.[ProgettoID],
                       p.Cliente + ' -> ' + p.CodiceProdotto + ' (Version: ' + ISNULL(n.[version],'#N/D') + ') ' + p.NomeProdotto
                       + ' [' + IIF(COUNT(t.[TaskProdottoID])=0, 'Not Started', 'Assigned task #' + CAST(COUNT(t.[TaskProdottoID]) AS NVARCHAR)) + ']' AS ActiveNpi,
                       p.Cliente,
                       p.CodiceProdotto,
                       p.NomeProdotto,
                       n.[Version],
                       n.ProdottoID
                FROM [Traceability_RS].[dbo].[ProgettiNPI] n 
                INNER JOIN Prodotti p ON p.ProdottoID = n.ProdottoID
                INNER JOIN WaveNPI w ON w.ProgettoID = n.ProgettoID
                LEFT JOIN [Traceability_RS].[dbo].[TaskProdotto] t ON w.WaveID = t.WaveID AND t.[stato] IS NOT NULL
                WHERE StatoProgetto = 'Attivo'
                GROUP BY n.[ProgettoID], 
                         p.Cliente + ' -> ' + p.CodiceProdotto + ' (Version: ' + ISNULL(n.[version],'#N/D') + ') ' + p.NomeProdotto,
                         p.Cliente,
                         p.CodiceProdotto,
                         p.NomeProdotto,
                         n.[Version],
                         n.ProdottoID
                ORDER BY p.Cliente + ' -> ' + p.CodiceProdotto + ' (Version: ' + ISNULL(n.[version],'#N/D') + ') ' + p.NomeProdotto, n.[Version]
            """
            
            # Esegui la query raw
            result = session.execute(text(sql_query))
            
            # Converti i risultati in una lista di dizionari
            progetti = []
            for row in result:
                progetti.append({
                    'ProgettoId': row[0],
                    'ActiveNpi': row[1],
                    'Cliente': row[2],
                    'CodiceProdotto': row[3],
                    'NomeProdotto': row[4],
                    'Version': row[5],
                    'ProdottoID': row[6]
                })
            
            return progetti
        except Exception as e:
            logger.error(f"Errore in get_progetti_attivi: {e}")
            session.rollback()
            raise
        finally:
            session.close()

    def create_progetto_npi_for_prodotto(self, prodotto_id, version=None, owner_id=None, descrizione=None):
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
                DataInizio=datetime.now(),
                Version=version,
                OwnerID=owner_id,
                Descrizione=descrizione
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
                    TaskID=task_cat.TaskID  # Corretto: TaskID non TaskId
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

    def get_progetto_by_prodotto(self, prodotto_id):
        """Recupera il progetto NPI associato a un prodotto."""
        session = self._get_session()
        try:
            progetto = session.scalars(
                select(ProgettoNPI)
                .options(joinedload(ProgettoNPI.prodotto))
                .where(ProgettoNPI.ProdottoID == prodotto_id)
            ).first()
            return self._detach_object(session, progetto) if progetto else None
        finally:
            session.close()

    def update_progetto_npi(self, progetto_id, data):
        """Aggiorna i dati di un progetto NPI."""
        session = self._get_session()
        try:
            progetto = session.get(ProgettoNPI, progetto_id)
            if not progetto:
                raise ValueError(f"Progetto {progetto_id} non trovato")
            
            # Aggiorna i campi
            for key, value in data.items():
                if hasattr(progetto, key):
                    setattr(progetto, key, value)
            
            session.commit()
            logger.info(f"Progetto {progetto_id} aggiornato")
            return self._detach_object(session, progetto)
        except Exception as e:
            logger.error(f"Errore aggiornamento progetto: {e}")
            session.rollback()
            raise
        finally:
            session.close()

    def validate_final_milestone_completion(self, task_prodotto_id: int) -> tuple:
        """
        Valida che il task finale (IsFinalMilestone=True) possa essere marcato come 'Completato'.

        REGOLA: Un task finale può essere completato SOLO se TUTTI i task con NrOrdin inferiore
        sono già stati marcati come 'Completato'.

        Args:
            task_prodotto_id: ID del task da validare

        Returns:
            tuple: (is_valid: bool, message: str)
                - (True, "") se la validazione passa
                - (False, messaggio_errore) se la validazione fallisce
        """
        session = self._get_session()
        try:
            # Recupera il task
            task = session.get(TaskProdotto, task_prodotto_id)
            if not task:
                return False, "Task non trovato."

            # Verifica se è il task finale
            if not task.IsPostFinalMilestone:
                # Non è un task finale, niente da validare
                return True, ""

            logger.info(
                f"Validazione task finale {task_prodotto_id} "
                f"({task.task_catalogo.NomeTask if task.task_catalogo else 'Unknown'})"
            )
            wave_tasks = session.scalars(
                select(TaskProdotto)
                .join(TaskCatalogo, TaskProdotto.TaskID == TaskCatalogo.TaskID)
                .where(TaskProdotto.WaveID == task.WaveID)
                .order_by(TaskCatalogo.NrOrdin.asc())
            ).all()

            # Trova il task finale nella lista
            final_task_index = None
            for idx, t in enumerate(wave_tasks):
                if t.TaskProdottoID == task_prodotto_id:
                    final_task_index = idx
                    break

            if final_task_index is None:
                return False, "Task finale non trovato nella wave."

            # Recupera TUTTI i task PRECEDENTI (NrOrdin inferiore)
            preceding_tasks = wave_tasks[:final_task_index]

            if not preceding_tasks:
                # Non ci sono task precedenti, il finale può essere completato
                logger.info("Nessun task precedente trovato. Task finale può essere completato.")
                return True, ""

            # Controlla che TUTTI i task precedenti siano 'Completato'
            incomplete_tasks = [
                t for t in preceding_tasks
                if t.Stato != 'Completato'
            ]

            if incomplete_tasks:
                # Costruisci il messaggio con i task incompleti
                incomplete_names = []
                for t in incomplete_tasks:
                    name = (t.task_catalogo.NomeTask
                            if t.task_catalogo
                            else f"Task {t.TaskProdottoID}")
                    stato = t.Stato or "Non assegnato"
                    incomplete_names.append(f"  • {name} (Stato: {stato})")

                error_message = (
                        "Non è possibile completare il task finale.\n\n"
                        "I seguenti task precedenti devono essere completati prima:\n\n" +
                        "\n".join(incomplete_names)
                )

                logger.warning(
                    f"Validazione fallita: {len(incomplete_tasks)} task precedenti non completati"
                )
                return False, error_message

            logger.info("Validazione superata: tutti i task precedenti sono completati.")
            return True, ""

        except Exception as e:
            logger.error(
                f"Errore durante la validazione del task finale {task_prodotto_id}: {e}",
                exc_info=True
            )
            return False, f"Errore durante la validazione: {str(e)}"
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

            stmt = (
                select(ProgettoNPI)
                .options(
                    # Caricamento delle relazioni esistenti...
                    joinedload(ProgettoNPI.prodotto),
                    subqueryload(ProgettoNPI.waves).subqueryload(WaveNPI.tasks).options(
                        joinedload(TaskProdotto.owner),
                        joinedload(TaskProdotto.task_catalogo).joinedload(TaskCatalogo.categoria),

                        # --- CORREZIONE QUI ---
                        # Aggiungiamo questa riga per dire a SQLAlchemy:
                        # "Quando carichi i task, carica subito anche la lista dei loro documenti".
                        selectinload(TaskProdotto.documents).joinedload(NpiDocument.document_type)
                    )
                )
                .where(ProgettoNPI.ProgettoId == project_id)
            )

            progetto = session.scalars(stmt).first()

            if progetto:
                logger.info(f"Progetto trovato - {progetto.prodotto.NomeProdotto}")
                if progetto.waves:
                    # Questo log ora funzionerà senza errori
                    for task in progetto.waves[0].tasks:
                        logger.debug(f"Task '{task.task_catalogo.NomeTask}' ha {len(task.documents)} documenti.")
            else:
                logger.info(f"Nessun progetto trovato con ID {project_id}")

            # Quando l'oggetto viene scollegato, ora avrà già la lista .documents popolata!
            return self._detach_object(session, progetto)
        except Exception as e:
            logger.error(f"Errore durante il recupero del progetto: {e}")
            session.rollback()
            return None
        finally:
            session.close()

    def update_project_dates(self, project_id: int, start_date: datetime, due_date: datetime, lang):
        """
        Aggiorna le date di un progetto con logica di business per il task finale (IsPostFinalMilestone=True).
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

            # 1.1 VALIDAZIONE: Data fine progetto >= ultima data task
            if due_date:
                # Trova l'ultima data di scadenza tra tutti i task del progetto
                max_task_due_date = session.scalar(
                    select(func.max(TaskProdotto.DataScadenza))
                    .join(WaveNPI, TaskProdotto.WaveID == WaveNPI.WaveID)
                    .where(
                        and_(
                            WaveNPI.ProgettoID == project_id,
                            TaskProdotto.DataScadenza.isnot(None)
                        )
                    )
                )
                
                if max_task_due_date:
                    # Converti in date se necessario
                    max_date = max_task_due_date.date() if hasattr(max_task_due_date, 'date') else max_task_due_date
                    due_date_check = due_date.date() if hasattr(due_date, 'date') else due_date
                    
                    if due_date_check < max_date:
                        error_msg = lang.get(
                            'error_project_end_before_tasks',
                            f'La data fine progetto ({due_date_check.strftime("%d/%m/%Y")}) non può essere precedente '
                            f'all\'ultima data di scadenza dei task ({max_date.strftime("%d/%m/%Y")}).'
                        )
                        raise ValueError(error_msg)

            # 2. CERCA IL TASK SPECIALE (con IsFinalMilestone=True)
            # --- MODIFICA LOGICA QUI ---
            # Query per trovare il TaskProdotto con IsPostFinalMilestone=True
            final_milestone_task = session.scalars(
                select(TaskProdotto)
                .join(WaveNPI, TaskProdotto.WaveID == WaveNPI.WaveID)
                .filter(
                    WaveNPI.ProgettoID == project_id,
                    TaskProdotto.IsPostFinalMilestone == True
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

    def update_progetto_npi(self, project_id: int, data: dict):
        """Aggiorna i campi di un progetto NPI."""
        session = self._get_session()
        try:
            progetto = session.get(ProgettoNPI, project_id)
            if not progetto:
                raise ValueError(f"Progetto con ID {project_id} non trovato.")
            
            # Aggiorna i campi forniti
            for key, value in data.items():
                if hasattr(progetto, key):
                    setattr(progetto, key, value)
            
            session.commit()
            return self._detach_object(session, progetto)
        except Exception as e:
            logger.error(f"Errore durante l'aggiornamento del progetto {project_id}: {e}", exc_info=True)
            session.rollback()
            raise
        finally:
            session.close()

    # ========================================
    # Task Dependencies Management
    # ========================================
    
    def get_task_dependencies(self, task_prodotto_id):
        """Recupera tutte le dipendenze di un task."""
        session = self._get_session()
        try:
            dependencies = session.scalars(
                select(TaskDependency)
                .options(
                    joinedload(TaskDependency.depends_on_task).joinedload(TaskProdotto.task_catalogo).joinedload(TaskCatalogo.categoria)
                )
                .where(TaskDependency.TaskProdottoID == task_prodotto_id)
            ).all()
            return self._detach_list(session, dependencies)
        except Exception as e:
            logger.error(f"Errore nel recupero dipendenze task {task_prodotto_id}: {e}", exc_info=True)
            return []
        finally:
            session.close()
    
    def get_available_predecessor_tasks(self, task_id, wave_id):
        """
        Restituisce i task disponibili come predecessori per un dato task.
        Esclude il task stesso e i task che creerebbero dipendenze circolari.
        """
        session = self._get_session()
        try:
            # Ottieni tutti i task della stessa wave
            all_tasks = session.scalars(
                select(TaskProdotto)
                .options(
                    joinedload(TaskProdotto.task_catalogo).joinedload(TaskCatalogo.categoria)
                )
                .where(TaskProdotto.WaveID == wave_id)
                .where(TaskProdotto.TaskProdottoID != task_id)
            ).all()
            
            # Filtra i task che creerebbero dipendenze circolari
            available_tasks = []
            for task in all_tasks:
                if not self._would_create_circular_dependency(session, task_id, task.TaskProdottoID):
                    available_tasks.append(task)
            
            return self._detach_list(session, available_tasks)
        except Exception as e:
            logger.error(f"Errore nel recupero predecessori disponibili: {e}", exc_info=True)
            return []
        finally:
            session.close()
    
    def add_task_dependency(self, task_id, depends_on_task_id, dependency_type='FinishToStart'):
        """
        Aggiunge una dipendenza tra task.
        Valida che non si creino dipendenze circolari.
        """
        session = self._get_session()
        try:
            # Verifica dipendenza circolare
            if self._would_create_circular_dependency(session, task_id, depends_on_task_id):
                return False, "Impossibile aggiungere: creerebbe una dipendenza circolare"
            
            # Verifica che la dipendenza non esista già
            existing = session.scalars(
                select(TaskDependency).where(
                    and_(
                        TaskDependency.TaskProdottoID == task_id,
                        TaskDependency.DependsOnTaskProdottoID == depends_on_task_id
                    )
                )
            ).first()
            
            if existing:
                return False, "Questa dipendenza esiste già"
            
            # Crea la dipendenza
            new_dependency = TaskDependency(
                TaskProdottoID=task_id,
                DependsOnTaskProdottoID=depends_on_task_id,
                DependencyType=dependency_type
            )
            session.add(new_dependency)
            session.commit()
            
            return True, "Dipendenza aggiunta con successo"
        except Exception as e:
            logger.error(f"Errore nell'aggiunta dipendenza: {e}", exc_info=True)
            session.rollback()
            return False, f"Errore: {str(e)}"
        finally:
            session.close()
    
    def remove_task_dependency(self, dependency_id):
        """Rimuove una dipendenza tra task."""
        session = self._get_session()
        try:
            dependency = session.get(TaskDependency, dependency_id)
            if dependency:
                session.delete(dependency)
                session.commit()
                return True, "Dipendenza rimossa con successo"
            return False, "Dipendenza non trovata"
        except Exception as e:
            logger.error(f"Errore nella rimozione dipendenza: {e}", exc_info=True)
            session.rollback()
            return False, f"Errore: {str(e)}"
        finally:
            session.close()
    
    def validate_task_dependencies(self, task_id, lang=None):
        """
        Valida che tutte le dipendenze di un task siano soddisfatte.
        Restituisce (is_valid, error_message).
        """
        session = self._get_session()
        try:
            dependencies = session.scalars(
                select(TaskDependency)
                .options(
                    joinedload(TaskDependency.depends_on_task).joinedload(TaskProdotto.task_catalogo)
                )
                .where(TaskDependency.TaskProdottoID == task_id)
            ).all()
            
            if not dependencies:
                return True, ""
            
            unsatisfied = []
            for dep in dependencies:
                predecessor = dep.depends_on_task
                if dep.DependencyType == 'FinishToStart':
                    if predecessor.Stato != 'Completato':
                        task_name = predecessor.task_catalogo.NomeTask if predecessor.task_catalogo else f"Task {predecessor.TaskProdottoID}"
                        unsatisfied.append(f"  • {task_name} (Stato: {predecessor.Stato or 'Non assegnato'})")
            
            if unsatisfied:
                if lang:
                    error_msg = lang.get('error_dependency_not_satisfied', 
                                        "Impossibile completare il task. Le seguenti dipendenze non sono soddisfatte:")
                else:
                    error_msg = "Impossibile completare il task. Le seguenti dipendenze non sono soddisfatte:"
                error_msg += "\n\n" + "\n".join(unsatisfied)
                return False, error_msg
            
            return True, ""
        except Exception as e:
            logger.error(f"Errore nella validazione dipendenze: {e}", exc_info=True)
            return False, f"Errore durante la validazione: {str(e)}"
        finally:
            session.close()
    
    def _would_create_circular_dependency(self, session, task_id, depends_on_task_id):
        """
        Verifica ricorsivamente se aggiungere una dipendenza creerebbe un ciclo.
        Restituisce True se si creerebbe un ciclo, False altrimenti.
        """
        # Se depends_on_task_id dipende da task_id (direttamente o indirettamente), abbiamo un ciclo
        visited = set()
        
        def has_path(from_task, to_task):
            if from_task == to_task:
                return True
            if from_task in visited:
                return False
            visited.add(from_task)
            
            # Trova tutti i task da cui from_task dipende
            dependencies = session.scalars(
                select(TaskDependency.DependsOnTaskProdottoID)
                .where(TaskDependency.TaskProdottoID == from_task)
            ).all()
            
            for dep_task_id in dependencies:
                if has_path(dep_task_id, to_task):
                    return True
            return False
        
        return has_path(depends_on_task_id, task_id)

    def set_target_npi_task(self, task_id, project_id):
        """
        Imposta un task come Target NPI (IsPostFinalMilestone=True) e rimuove il flag da tutti gli altri task del progetto.
        """
        session = self._get_session()
        try:
            # 1. Trova il task selezionato
            target_task = session.get(TaskProdotto, task_id)
            if not target_task:
                raise ValueError(f"Task {task_id} non trovato.")

            # 2. Trova tutti i task del progetto (Wave)
            # Assumiamo che il progetto abbia una sola wave attiva o che vogliamo l'unicità per progetto
            # Recuperiamo la wave del task
            wave_id = target_task.WaveID
            
            # 3. Reset di tutti i task della stessa wave
            session.query(TaskProdotto).filter(
                TaskProdotto.WaveID == wave_id
            ).update({TaskProdotto.IsPostFinalMilestone: False})

            # 4. Imposta il flag sul task selezionato
            target_task.IsPostFinalMilestone = True
            
            session.commit()
            return True
        except Exception as e:
            logger.error(f"Errore impostazione Target NPI per task {task_id}: {e}", exc_info=True)
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
                # Controlla se la chiave esiste nel dizionario 'data' prima di accedervi
                if field in data:
                    field_value = data.get(field)

                    if field_value in ('', None):
                        data[field] = None  # Imposta esplicitamente a None
                    elif isinstance(field_value, str):
                        try:
                            # Converte la stringa in un oggetto datetime completo
                            data[field] = datetime.strptime(field_value, '%d/%m/%Y')
                        except (ValueError, TypeError):
                            # Se la conversione fallisce, imposta a None
                            data[field] = None

            # Applica tutti gli aggiornamenti
            for key, value in data.items():
                setattr(task, key, value)

            session.commit()
            session.refresh(task)

            return self._detach_object(session, task)
        except Exception as e:
            logger.error(f"Errore in update_task_prodotto: {e.__class__.__name__} - {e}", exc_info=True)
            session.rollback()
            raise
        finally:
            session.close()

    def invia_notifiche_task(self, task: TaskProdotto, conferma_utente: bool = True, lang: dict = None):
        """Invia le notifiche email per un task assegnato."""
        session = self._get_session()
        try:
            # Ricarica il task con tutte le relazioni necessarie
            task_completo = session.scalars(
                select(TaskProdotto)
                .options(
                    joinedload(TaskProdotto.task_catalogo).joinedload(TaskCatalogo.categoria),
                    joinedload(TaskProdotto.wave).joinedload(WaveNPI.progetto).joinedload(ProgettoNPI.prodotto),
                    joinedload(TaskProdotto.wave).joinedload(WaveNPI.progetto).joinedload(ProgettoNPI.owner),
                    joinedload(TaskProdotto.owner),
                    joinedload(TaskProdotto.predecessors),
                    joinedload(TaskProdotto.successors)
                )
                .where(TaskProdotto.TaskProdottoID == task.TaskProdottoID)
            ).first()
            
            if not task_completo or not task_completo.owner or not task_completo.owner.Email:
                logger.warning(f"Task {task.TaskProdottoID}: owner o email non disponibili")
                return False
            
            # Ottieni il progetto e l'owner del progetto
            progetto = task_completo.wave.progetto if task_completo.wave else None
            if not progetto:
                logger.warning(f"Task {task.TaskProdottoID}: progetto non trovato")
                return False
            
            project_owner = progetto.owner if progetto.owner else None
            
            # Prepara i dati per l'email
            email_data = {
                'assignee_name': task_completo.owner.Nome,
                'assignee_email': task_completo.owner.Email,
                'project_name': progetto.prodotto.NomeProdotto if progetto.prodotto else "N/A",
                'project_code': progetto.prodotto.CodiceProdotto if progetto.prodotto else "N/A",
                'project_owner_name': project_owner.Nome if project_owner else "N/A",
                'project_owner_email': project_owner.Email if project_owner else None,
                'project_description': progetto.Descrizione or "Nessuna descrizione disponibile",
                'project_start': progetto.DataInizio.strftime('%d/%m/%Y') if progetto.DataInizio else "N/A",
                'project_due': progetto.ScadenzaProgetto.strftime('%d/%m/%Y') if progetto.ScadenzaProgetto else "N/A",
                'project_version': progetto.Version or "N/A",
                'task_item_id': task_completo.task_catalogo.ItemID if task_completo.task_catalogo else "N/A",
                'task_name': task_completo.task_catalogo.NomeTask if task_completo.task_catalogo else "N/A",
                'task_category': task_completo.task_catalogo.categoria.Category if task_completo.task_catalogo and task_completo.task_catalogo.categoria else "N/A",
                'task_description': task_completo.task_catalogo.Descrizione if task_completo.task_catalogo else "N/A",
                'task_due_date': task_completo.DataScadenza.strftime('%d/%m/%Y') if task_completo.DataScadenza else "N/A",
                'task_status': task_completo.Stato or "Non Iniziato",
                'predecessors': self._format_task_dependencies(task_completo.predecessors, session),
                'successors': self._format_task_dependencies(task_completo.successors, session, is_successor=True)
            }
            
            # Genera HTML email
            email_html = self._generate_task_assignment_email_html(email_data)
            
            # Invia email usando utils.send_email
            from utils import send_email
            
            subject = f"{email_data['project_name']} - Assegnazione Task NPI"
            
            try:
                send_email(
                    recipients=[task_completo.owner.Email],
                    subject=subject,
                    body=email_html,
                    is_html=True
                )
                success = True
                logger.info(f"Notifica inviata con successo per task {task.TaskProdottoID} a {task_completo.owner.Email}")
            except Exception as email_error:
                success = False
                logger.error(f"Invio notifica fallito per task {task.TaskProdottoID}: {email_error}")
            
            return success
            
        except Exception as e:
            logger.error(f"Errore nell'invio notifiche per task {task.TaskProdottoID}: {e}", exc_info=True)
            return False
        finally:
            session.close()
    
    def _format_task_dependencies(self, dependencies, session, is_successor=False):
        """Formatta le dipendenze del task per l'email."""
        if not dependencies:
            return []
        
        formatted = []
        for dep in dependencies:
            # Ottieni l'ID del task dipendente
            # Se is_successor=True, questo task è il "depends_on" e vogliamo il task principale
            # Se is_successor=False, questo task è il principale e vogliamo il "depends_on"
            dep_task_id = dep.TaskProdottoID if is_successor else dep.DependsOnTaskProdottoID
            
            # Carica il task dipendente
            dep_task = session.get(TaskProdotto, dep_task_id)
            if dep_task:
                # Carica le relazioni necessarie
                session.refresh(dep_task, ['task_catalogo', 'owner'])
                
                formatted.append({
                    'item_id': dep_task.task_catalogo.ItemID if dep_task.task_catalogo else "N/A",
                    'name': dep_task.task_catalogo.NomeTask if dep_task.task_catalogo else "N/A",
                    'owner': dep_task.owner.Nome if dep_task.owner else "Non Assegnato",
                    'due_date': dep_task.DataScadenza.strftime('%d/%m/%Y') if dep_task.DataScadenza else "N/A"
                })
        return formatted
    
    def _generate_task_assignment_email_html(self, data):
        """Genera HTML professionale multilingua (IT, EN, RO) per email assegnazione task."""
        
        # Traduzioni
        translations = {
            'it': {
                'title': 'Assegnazione Task NPI',
                'subtitle': 'Sistema di Gestione Progetti NPI',
                'greeting': f"Gentile <strong>{data['assignee_name']}</strong>,",
                'intro': 'Ti è stato assegnato il seguente task per il progetto NPI:',
                'project_details': 'DETTAGLI PROGETTO',
                'project_name': 'Nome Progetto:',
                'product_code': 'Codice Prodotto:',
                'project_owner': 'Responsabile Progetto:',
                'start_date': 'Data Inizio:',
                'due_date': 'Scadenza Progetto:',
                'version': 'Versione:',
                'description': 'Descrizione:',
                'your_task': 'IL TUO TASK ASSEGNATO',
                'category': 'Categoria:',
                'task_due': 'Scadenza Task:',
                'status': 'Stato Attuale:',
                'predecessors': '⚠ Questo task dipende da:',
                'successors': 'ℹ Altri task dipendono da questo:',
                'assigned_to': 'Assegnato a:',
                'important_notes': '⚠ NOTE IMPORTANTI',
                'note1': 'Rivedi attentamente le dipendenze del task',
                'note2': 'Coordina con i membri del team per i task dipendenti',
                'note3': 'Aggiorna regolarmente lo stato del task nel sistema',
                'note4': 'Contatta il responsabile del progetto per qualsiasi domanda',
                'regards': 'Cordiali saluti,',
                'project_manager': 'Responsabile Progetto',
                'disclaimer': 'Questa è una notifica automatica dal Sistema di Gestione Progetti NPI.<br>Si prega di non rispondere a questa email.'
            },
            'en': {
                'title': 'NPI Task Assignment',
                'subtitle': 'NPI Project Management System',
                'greeting': f"Dear <strong>{data['assignee_name']}</strong>,",
                'intro': 'You have been assigned the following task for the NPI project:',
                'project_details': 'PROJECT DETAILS',
                'project_name': 'Project Name:',
                'product_code': 'Product Code:',
                'project_owner': 'Project Manager:',
                'start_date': 'Start Date:',
                'due_date': 'Project Deadline:',
                'version': 'Version:',
                'description': 'Description:',
                'your_task': 'YOUR ASSIGNED TASK',
                'category': 'Category:',
                'task_due': 'Task Deadline:',
                'status': 'Current Status:',
                'predecessors': '⚠ This task depends on:',
                'successors': 'ℹ Other tasks depend on this:',
                'assigned_to': 'Assigned to:',
                'important_notes': '⚠ IMPORTANT NOTES',
                'note1': 'Carefully review task dependencies',
                'note2': 'Coordinate with team members for dependent tasks',
                'note3': 'Regularly update task status in the system',
                'note4': 'Contact the project manager for any questions',
                'regards': 'Best regards,',
                'project_manager': 'Project Manager',
                'disclaimer': 'This is an automatic notification from the NPI Project Management System.<br>Please do not reply to this email.'
            },
            'ro': {
                'title': 'Atribuire Task NPI',
                'subtitle': 'Sistem de Management Proiecte NPI',
                'greeting': f"Stimate <strong>{data['assignee_name']}</strong>,",
                'intro': 'Ți-a fost atribuit următorul task pentru proiectul NPI:',
                'project_details': 'DETALII PROIECT',
                'project_name': 'Nume Proiect:',
                'product_code': 'Cod Produs:',
                'project_owner': 'Responsabil Proiect:',
                'start_date': 'Data Început:',
                'due_date': 'Termen Limită Proiect:',
                'version': 'Versiune:',
                'description': 'Descriere:',
                'your_task': 'TASK-UL TĂU ATRIBUIT',
                'category': 'Categorie:',
                'task_due': 'Termen Limită Task:',
                'status': 'Status Curent:',
                'predecessors': '⚠ Acest task depinde de:',
                'successors': 'ℹ Alte task-uri depind de acesta:',
                'assigned_to': 'Atribuit către:',
                'important_notes': '⚠ NOTE IMPORTANTE',
                'note1': 'Revizuiește cu atenție dependențele task-ului',
                'note2': 'Coordonează-te cu membrii echipei pentru task-urile dependente',
                'note3': 'Actualizează regulat statusul task-ului în sistem',
                'note4': 'Contactează responsabilul de proiect pentru orice întrebare',
                'regards': 'Cu stimă,',
                'project_manager': 'Responsabil Proiect',
                'disclaimer': 'Aceasta este o notificare automată de la Sistemul de Management Proiecte NPI.<br>Vă rugăm să nu răspundeți la acest email.'
            }
        }
        
        # Genera sezioni per ogni lingua
        sections_html = ""
        for lang_code in ['it', 'en', 'ro']:
            t = translations[lang_code]
            
            # Formatta predecessori
            predecessors_html = ""
            if data['predecessors']:
                predecessors_html = f"<h4 style='color: #d9534f; margin-top: 15px;'>{t['predecessors']}</h4><ul style='margin: 5px 0;'>"
                for pred in data['predecessors']:
                    predecessors_html += f"<li><strong>{pred['item_id']}</strong> - {pred['name']} - {t['assigned_to']} {pred['owner']} - {t['task_due']} {pred['due_date']}</li>"
                predecessors_html += "</ul>"
            
            # Formatta successori
            successors_html = ""
            if data['successors']:
                successors_html = f"<h4 style='color: #5bc0de; margin-top: 15px;'>{t['successors']}</h4><ul style='margin: 5px 0;'>"
                for succ in data['successors']:
                    successors_html += f"<li><strong>{succ['item_id']}</strong> - {succ['name']} - {t['assigned_to']} {succ['owner']} - {t['task_due']} {succ['due_date']}</li>"
                successors_html += "</ul>"
            
            # Aggiungi sezione lingua
            lang_flag = {'it': '🇮🇹', 'en': '🇬🇧', 'ro': '🇷🇴'}[lang_code]
            sections_html += f"""
            <div class="lang-section" style="margin: 30px 0; padding: 20px; background: #f8f9fa; border-radius: 8px;">
                <div style="text-align: center; margin-bottom: 20px;">
                    <span style="font-size: 24px;">{lang_flag}</span>
                    <h2 style="color: #0078d4; margin: 10px 0;">{t['title']}</h2>
                </div>
                
                <p style="font-size: 16px; margin-bottom: 20px;">{t['greeting']}</p>
                <p>{t['intro']}</p>
                
                <div class="section">
                    <h2>📊 {t['project_details']}</h2>
                    <div class="info-row"><span class="label">{t['project_name']}</span> <span class="value">{data['project_name']}</span></div>
                    <div class="info-row"><span class="label">{t['product_code']}</span> <span class="value">{data['project_code']}</span></div>
                    <div class="info-row"><span class="label">{t['project_owner']}</span> <span class="value">{data['project_owner_name']}</span></div>
                    <div class="info-row"><span class="label">{t['start_date']}</span> <span class="value">{data['project_start']}</span></div>
                    <div class="info-row"><span class="label">{t['due_date']}</span> <span class="value">{data['project_due']}</span></div>
                    <div class="info-row"><span class="label">{t['version']}</span> <span class="value">{data['project_version']}</span></div>
                    <div class="info-row" style="margin-top: 15px;">
                        <span class="label">{t['description']}</span><br>
                        <span class="value" style="display: block; margin-top: 5px; padding: 10px; background: white; border-radius: 4px;">{data['project_description']}</span>
                    </div>
                </div>
                
                <div class="section">
                    <h2>✅ {t['your_task']}</h2>
                    <div class="task-box">
                        <h3>{data['task_item_id']} - {data['task_name']}</h3>
                        <div class="info-row"><span class="label">{t['category']}</span> <span class="value">{data['task_category']}</span></div>
                        <div class="info-row"><span class="label">{t['description']}</span> <span class="value">{data['task_description']}</span></div>
                        <div class="info-row"><span class="label">{t['task_due']}</span> <span class="value" style="color: #d9534f; font-weight: bold;">{data['task_due_date']}</span></div>
                        <div class="info-row"><span class="label">{t['status']}</span> <span class="value">{data['task_status']}</span></div>
                        
                        {predecessors_html}
                        {successors_html}
                    </div>
                </div>
                
                <div class="important-notes">
                    <h3>{t['important_notes']}</h3>
                    <ul>
                        <li>{t['note1']}</li>
                        <li>{t['note2']}</li>
                        <li>{t['note3']}</li>
                        <li>{t['note4']}</li>
                    </ul>
                </div>
                
                <div class="footer">
                    <p><strong>{t['regards']}</strong></p>
                    <p><strong>{data['project_owner_name']}</strong><br>{t['project_manager']}</p>
                    <hr style="border: none; border-top: 1px solid #ddd; margin: 15px 0;">
                    <p style="font-size: 11px; color: #999;">{t['disclaimer']}</p>
                </div>
            </div>
            {"<hr style='border: none; border-top: 3px solid #0078d4; margin: 40px 0;'>" if lang_code != 'ro' else ""}
            """
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; }}
                .container {{ max-width: 800px; margin: 0 auto; padding: 20px; background-color: #f9f9f9; }}
                .header {{ background: linear-gradient(135deg, #0078d4 0%, #005a9e 100%); color: #1a3a52; padding: 30px 20px; border-radius: 8px 8px 0 0; text-align: center; }}
                .header h1 {{ margin: 0; font-size: 28px; color: #1a3a52; }}
                .header p {{ margin: 5px 0 0 0; font-size: 14px; opacity: 0.9; color: #1a3a52; }}
                .content {{ background: white; padding: 30px; border-radius: 0 0 8px 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .section {{ margin: 25px 0; padding: 20px; background: white; border-left: 4px solid #0078d4; border-radius: 4px; }}
                .section h2 {{ color: #0078d4; margin: 0 0 15px 0; font-size: 20px; border-bottom: 2px solid #0078d4; padding-bottom: 10px; }}
                .task-box {{ background: white; padding: 20px; margin: 15px 0; border: 2px solid #0078d4; border-radius: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }}
                .task-box h3 {{ color: #0078d4; margin: 0 0 15px 0; font-size: 18px; }}
                .label {{ font-weight: bold; color: #555; display: inline-block; min-width: 150px; }}
                .value {{ color: #333; }}
                .info-row {{ margin: 8px 0; }}
                .footer {{ background: white; padding: 20px; margin-top: 20px; border-top: 3px solid #0078d4; border-radius: 4px; text-align: center; }}
                .footer p {{ margin: 5px 0; color: #666; font-size: 13px; }}
                .important-notes {{ background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0; border-radius: 4px; }}
                .important-notes h3 {{ color: #856404; margin: 0 0 10px 0; font-size: 16px; }}
                .important-notes ul {{ margin: 10px 0; padding-left: 20px; color: #856404; }}
                ul {{ line-height: 1.8; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📋 NPI Task Assignment / Assegnazione Task NPI / Atribuire Task NPI</h1>
                    <p>🇮🇹 Italiano | 🇬🇧 English | 🇷🇴 Română</p>
                </div>
                
                <div class="content">
                    {sections_html}
                </div>
            </div>
        </body>
        </html>
        """
        
        return html

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
                        joinedload(TaskProdotto.task_catalogo).joinedload(TaskCatalogo.categoria),
                        subqueryload(TaskProdotto.dependencies)
                    )
                )
                .where(ProgettoNPI.ProgettoId == progetto_id)
            ).first()

            if not progetto or not progetto.waves:
                return None, None

            # Filtra i task validi (con owner e date)
            valid_tasks = []
            for task in progetto.waves[0].tasks:
                if (task.OwnerID is not None and
                        task.DataInizio and
                        task.DataScadenza):
                    valid_tasks.append(task)
            
            # Applica ordinamento topologico
            sorted_tasks = self._topological_sort_tasks(valid_tasks)
            
            # Crea i dati per il Gantt usando i task ordinati
            df_data = []
            for task in sorted_tasks:
                # Assicurati che la data di fine sia >= alla data di inizio
                data_inizio = min(task.DataInizio, task.DataScadenza)
                data_fine = max(task.DataInizio, task.DataScadenza)

                # Recupera le dipendenze
                deps = [d.DependsOnTaskProdottoID for d in task.dependencies]

                # 🆕 Calcolo dinamico percentuale di completamento
                completion_percentage = 0
                
                # Normalizza lo stato per il confronto (rimuove spazi e rende case-insensitive)
                stato_normalized = task.Stato.strip() if task.Stato else ""
                logger.info(f"🔍 Task {task.TaskProdottoID} ({task.task_catalogo.NomeTask if task.task_catalogo else 'N/A'}): Stato raw='{task.Stato}', normalized='{stato_normalized}'")
                
                if stato_normalized == 'Completato':
                    # Task completato = 100%
                    completion_percentage = 100
                    logger.info(f"✅ Task {task.TaskProdottoID}: Completato -> 100%")
                elif stato_normalized == 'In Lavorazione':
                    # Task in lavorazione = calcola in base alle date
                    try:
                        today = datetime.now().date()
                        start_date = data_inizio.date() if hasattr(data_inizio, 'date') else data_inizio
                        end_date = data_fine.date() if hasattr(data_fine, 'date') else data_fine
                        
                        logger.info(f"📅 Task {task.TaskProdottoID}: Oggi={today}, Inizio={start_date}, Fine={end_date}")
                        
                        if today < start_date:
                            # Non ancora iniziato (data futura)
                            completion_percentage = 0
                            logger.info(f"⏸️ Task {task.TaskProdottoID}: In Lavorazione ma non iniziato (futuro) -> 0%")
                        elif today > end_date:
                            # Scadenza superata
                            completion_percentage = 100
                            logger.info(f"⏰ Task {task.TaskProdottoID}: In Lavorazione scaduto -> 100%")
                        else:
                            # Task in corso: oggi è tra start_date e end_date (inclusi)
                            total_duration = (end_date - start_date).days
                            
                            if total_duration == 0:
                                # Task con durata 0 giorni (inizio == fine == oggi)
                                completion_percentage = 50
                                logger.info(f"⚡ Task {task.TaskProdottoID}: In Lavorazione stesso giorno (inizio=fine=oggi) -> 50%")
                            else:
                                # Calcola percentuale in base al progresso temporale
                                elapsed_duration = (today - start_date).days
                                completion_percentage = int((elapsed_duration / total_duration) * 100)
                                # Assicura che sia almeno 1% se è iniziato
                                completion_percentage = max(1, completion_percentage)
                                logger.info(f"📊 Task {task.TaskProdottoID}: In Lavorazione {elapsed_duration}/{total_duration} giorni -> {completion_percentage}%")
                    except Exception as e:
                        logger.warning(f"❌ Errore calcolo percentuale per task {task.TaskProdottoID}: {e}")
                        completion_percentage = 0
                else:
                    # Task in altri stati (Da Fare, Bloccato, ecc.) = 0%
                    completion_percentage = 0
                    logger.info(f"🔴 Task {task.TaskProdottoID}: Stato '{stato_normalized}' -> 0%")

                df_data.append({
                    'Task': task.task_catalogo.NomeTask if task.task_catalogo else "Task non definito",
                    'Category': task.task_catalogo.categoria.Category if (task.task_catalogo and task.task_catalogo.categoria) else "Nessuna Categoria",
                    'Start': data_inizio,
                    'Finish': data_fine,
                    'Owner': task.owner.Nome if task.owner else 'Non Assegnato',
                    'Status': task.Stato,
                    'TaskProdottoID': task.TaskProdottoID,
                    'Dependencies': deps,
                    'Completion': completion_percentage,  # 🆕 Percentuale calcolata dinamicamente
                    'IsTargetNPI': task.IsPostFinalMilestone if task.IsPostFinalMilestone is not None else False  # 🆕 Flag Target NPI
                })

            logger.debug(f"Totale task nel progetto: {len(progetto.waves[0].tasks)}")
            logger.debug(f"Task mostrati nel Gantt: {len(df_data)}")

            return df_data, progetto.prodotto.NomeProdotto

        except Exception as e:
            logger.error(f"Errore in get_gantt_data: {e}")
            raise
        finally:
            session.close()
    
    def _topological_sort_tasks(self, tasks):
        """Ordina i task rispettando le dipendenze con ordinamento topologico.
        
        I task senza dipendenze sono ordinati per data di inizio.
        I task con dipendenze appaiono sempre dopo i loro predecessori.
        Metodo condiviso tra project_window e generazione Gantt.
        """
        from collections import defaultdict, deque
        from datetime import datetime
        
        # Crea una mappa task_id -> task per accesso rapido
        task_map = {t.TaskProdottoID: t for t in tasks}
        task_ids = set(task_map.keys())
        
        # Costruisci il grafo delle dipendenze
        # graph[task_id] = lista di task che dipendono da task_id
        graph = defaultdict(list)
        # in_degree[task_id] = numero di dipendenze (predecessori)
        in_degree = defaultdict(int)
        
        # Inizializza tutti i task con in_degree 0
        for task_id in task_ids:
            in_degree[task_id] = 0
        
        # Popola il grafo e calcola gli in_degree
        for task in tasks:
            # Usa get_task_dependencies se disponibile, altrimenti usa dependencies
            if hasattr(task, 'dependencies'):
                dependencies = task.dependencies
            else:
                dependencies = self.get_task_dependencies(task.TaskProdottoID)
            
            for dep in dependencies:
                # L'attributo corretto è sempre DependsOnTaskProdottoID
                predecessor_id = dep.DependsOnTaskProdottoID
                # Considera solo dipendenze tra task nel set corrente
                if predecessor_id in task_ids:
                    graph[predecessor_id].append(task.TaskProdottoID)
                    in_degree[task.TaskProdottoID] += 1
        
        # Ottieni tutti i task senza dipendenze (in_degree == 0)
        # e ordinali per data di inizio
        queue = []
        for task_id in task_ids:
            if in_degree[task_id] == 0:
                task = task_map[task_id]
                # Usa la data di inizio per l'ordinamento, o una data molto lontana se None
                start_date = task.DataInizio if task.DataInizio else datetime(2099, 12, 31)
                queue.append((start_date, task_id))
        
        # Ordina i task iniziali per data di inizio
        queue.sort(key=lambda x: x[0])
        queue = deque([task_id for _, task_id in queue])
        
        # Algoritmo di Kahn per ordinamento topologico
        result = []
        
        while queue:
            # Prendi il prossimo task dalla coda
            current_id = queue.popleft()
            result.append(task_map[current_id])
            
            # Per ogni task che dipende dal task corrente
            successors_to_add = []
            for successor_id in graph[current_id]:
                in_degree[successor_id] -= 1
                
                # Se tutte le dipendenze del successor sono state soddisfatte
                if in_degree[successor_id] == 0:
                    task = task_map[successor_id]
                    start_date = task.DataInizio if task.DataInizio else datetime(2099, 12, 31)
                    successors_to_add.append((start_date, successor_id))
            
            # Ordina i successori per data di inizio prima di aggiungerli alla coda
            successors_to_add.sort(key=lambda x: x[0])
            for _, successor_id in successors_to_add:
                queue.append(successor_id)
        
        # Verifica che tutti i task siano stati processati (no cicli)
        if len(result) != len(tasks):
            logger.warning("Rilevato ciclo nelle dipendenze dei task. Alcuni task potrebbero non essere visualizzati correttamente.")
            # Aggiungi i task rimanenti alla fine (fallback)
            processed_ids = {t.TaskProdottoID for t in result}
            remaining = [t for t in tasks if t.TaskProdottoID not in processed_ids]
            result.extend(remaining)
        
        return result

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
        Recupera i dati dei progetti per la dashboard principale.
        Mostra TUTTI i progetti con la data fine progetto.
        """
        session = self._get_session()
        try:
            # Query modificata per restituire la ScadenzaProgetto
            stmt = select(
                ProgettoNPI.ProgettoId,
                func.coalesce(ProgettoNPI.NomeProgetto, Prodotto.NomeProdotto).label("NomeProgetto"),
                Prodotto.CodiceProdotto,
                Prodotto.Cliente,
                ProgettoNPI.ScadenzaProgetto.label("ScadenzaProgetto")
            ).join(
                Prodotto, ProgettoNPI.ProdottoID == Prodotto.ProdottoID
            ).order_by(
                ProgettoNPI.DataInizio.desc()
            )

            result = session.execute(stmt).all()
            return result
        finally:
            session.close()

    def get_npi_statistics(self):
        """
        Calcola le statistiche per la dashboard:
        - Totale progetti NPI
        - Progetti completati (Stato = 'Chiuso')
        - Progetti in ritardo (Stato != 'Chiuso' e ScadenzaProgetto < Oggi)
        - Statistiche per cliente
        """
        session = self._get_session()
        try:
            stats = {
                'total_projects': 0,
                'completed_projects': 0,
                'delayed_projects': 0,
                'customer_stats': []
            }

            # 1. Totale Progetti
            stats['total_projects'] = session.scalar(
                select(func.count(ProgettoNPI.ProgettoId))
            )

            # 2. Progetti Completati
            stats['completed_projects'] = session.scalar(
                select(func.count(ProgettoNPI.ProgettoId))
                .where(ProgettoNPI.StatoProgetto == 'Chiuso')
            )

            # 3. Progetti in Ritardo
            stats['delayed_projects'] = session.scalar(
                select(func.count(ProgettoNPI.ProgettoId))
                .where(
                    and_(
                        ProgettoNPI.StatoProgetto != 'Chiuso',
                        ProgettoNPI.ScadenzaProgetto < datetime.now()
                    )
                )
            )

            # 4. Statistiche per Cliente
            customer_query = (
                select(
                    Prodotto.Cliente,
                    func.count(ProgettoNPI.ProgettoId).label('count')
                )
                .join(Prodotto, ProgettoNPI.ProdottoID == Prodotto.ProdottoID)
                .group_by(Prodotto.Cliente)
                .order_by(func.count(ProgettoNPI.ProgettoId).desc())
            )
            
            customer_results = session.execute(customer_query).all()
            
            total = stats['total_projects'] or 1
            
            for client, count in customer_results:
                client_name = client or "N/A"
                percentage = (count / total) * 100
                stats['customer_stats'].append({
                    'client': client_name,
                    'count': count,
                    'percentage': round(percentage, 1)
                })

            return stats
        except Exception as e:
            logger.error(f"Errore nel calcolo statistiche NPI: {e}", exc_info=True)
            return None
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
                if task.IsPostFinalMilestone:
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


    def get_npi_document_types(self):
        """Recupera tutti i tipi di documenti NPI."""
        session = self._get_session()
        try:
            doc_types = session.scalars(
                select(NpiDocumentType).order_by(NpiDocumentType.NpiDocumentDescription)
            ).all()
            return self._detach_list(session, doc_types)
        finally:
            session.close()


    def get_documents_for_task(self, task_prodotto_id: int):
        """Recupera tutti i documenti per un dato task, ordinati per data decrescente."""
        session = self._get_session()
        try:
            documents = session.scalars(
                select(NpiDocument)
                .options(joinedload(NpiDocument.document_type))
                .where(NpiDocument.TaskProdottoId == task_prodotto_id)
                .order_by(NpiDocument.DateIn.desc())
            ).all()
            return self._detach_list(session, documents)
        finally:
            session.close()


    def get_document_body(self, document_id: int):
        """Recupera solo il corpo binario di un documento per l'apertura."""
        session = self._get_session()
        try:
            # Seleziona solo la colonna DocumentBody per efficienza
            body = session.scalar(
                select(NpiDocument.DocumentBody).where(NpiDocument.NpiDocumentId == document_id)
            )
            return body
        finally:
            session.close()

    def add_npi_document(self, task_prodotto_id, doc_type_id, title, body, user,
                         note=None, replaces_doc_id=None, doc_value=None,
                         due_date=None, IDSite=None):  # ← Aggiungi questo parametro
        """
        Aggiunge un nuovo documento NPI al database.
        """
        try:
            with self._get_session() as session:
                # Gestisci la sostituzione del documento precedente
                if replaces_doc_id:
                    old_doc = session.query(NpiDocument).filter_by(
                        NpiDocumentId=replaces_doc_id
                    ).first()
                    if old_doc:
                        old_doc.DateOut = datetime.now()
                        version_number = old_doc.VersionNumber + 1
                    else:
                        version_number = 0
                else:
                    version_number = 0

                # Crea il nuovo documento
                new_doc = NpiDocument(
                    TaskProdottoId=task_prodotto_id,
                    NpiDocumentTypeId=doc_type_id,
                    DocumentTitle=title,
                    DocumentBody=body,
                    DateIn=datetime.now(),
                    User=user,
                    NewVersionOf=replaces_doc_id,
                    ValueInEur=doc_value,
                    DateOut=due_date,
                    VersionNumber=version_number,
                    Note=note,
                    IDSite=IDSite
                )

                session.add(new_doc)
                session.commit()

                logger.info(f"Documento '{title}' aggiunto con successo per task {task_prodotto_id}")
                return new_doc

        except Exception as e:
            logger.error(f"Errore durante l'aggiunta del documento: {e}", exc_info=True)
            raise

    def check_and_notify_document_deadlines(self):
        """
        Controlla tutti i documenti con una DueDate e invia notifiche se sono scaduti.
        """
        session = self._get_session()
        try:
            today = datetime.utcnow().date()

            # Seleziona documenti non obsoleti, con una DueDate passata e associati a un task con un owner
            overdue_docs = session.scalars(
                select(NpiDocument)
                .join(NpiDocument.task_prodotto)
                .options(
                    joinedload(NpiDocument.task_prodotto).joinedload(TaskProdotto.owner),
                    joinedload(NpiDocument.task_prodotto).joinedload(TaskProdotto.task_catalogo)
                )
                .where(
                    NpiDocument.DateOut == None,  # Documento attivo
                    NpiDocument.DueDate != None,  # Ha una data di scadenza
                    NpiDocument.DueDate < today,  # La data è passata
                    TaskProdotto.OwnerID != None  # Il task ha un owner
                )
            ).all()

            if not overdue_docs:
                logger.info("Nessuna scadenza documento da notificare.")
                return 0

            # Qui dovresti implementare la logica di invio email/notifica Teams.
            # Per semplicità, logghiamo solo i documenti trovati.
            # Puoi raggrupparli per owner e inviare una singola notifica riepilogativa.

            logger.warning(f"Trovati {len(overdue_docs)} documenti con scadenza superata.")
            for doc in overdue_docs:
                owner = doc.task_prodotto.owner
                task = doc.task_prodotto
                logger.info(f"  -> Documento '{doc.DocumentTitle}' (ID: {doc.NpiDocumentId}) "
                            f"del task '{task.task_catalogo.NomeTask}' "
                            f"assegnato a '{owner.Nome}' è SCADUTO il {doc.DueDate.strftime('%Y-%m-%d')}.")

            # TODO: Implementare qui la logica di invio notifiche raggruppate per owner
            # Esempio: email_sender.send_overdue_document_summary(owner, lista_documenti_scaduti)

            return len(overdue_docs)

        finally:
            session.close()


    def authorize_document(self, document_id: int, authorizer_name: str):
        """Autorizza un documento, impostando nome e data."""
        session = self._get_session()
        try:
            doc = session.get(NpiDocument, document_id)
            if not doc:
                raise ValueError(f"Documento con ID {document_id} non trovato.")

            doc.AutorizedBy = authorizer_name
            doc.AuthorizedOn = datetime.utcnow()

            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def get_all_catalog_tasks(self):
        """Ottiene tutti i task del catalogo."""
        session = self._get_session()
        try:
            tasks = session.scalars(
                select(TaskCatalogo)
                .options(joinedload(TaskCatalogo.categoria))
                .order_by(TaskCatalogo.NrOrdin)
            ).all()
            return [self._detach_object(session, t) for t in tasks]
        finally:
            session.close()

    def add_catalog_tasks_to_project(self, wave_id, catalog_tasks):
        """Aggiunge i task del catalogo mancanti a una wave del progetto."""
        session = self._get_session()
        try:
            added_count = 0
            for catalog_task in catalog_tasks:
                # Crea un nuovo TaskProdotto per ogni task del catalogo
                new_task = TaskProdotto(
                    WaveID=wave_id,
                    TaskID=catalog_task.TaskID
                )
                session.add(new_task)
                added_count += 1
            
            session.commit()
            logger.info(f"Aggiunti {added_count} task alla wave {wave_id}")
            return added_count
        except Exception as e:
            logger.error(f"Errore aggiunta task al progetto: {e}")
            session.rollback()
            raise
        finally:
            session.close()

    # ========================================
    # GESTIONE DOCUMENTI PROGETTO
    # ========================================

    def add_progetto_documento(self, progetto_id, nome_file, tipo_file, dimensione, 
                               contenuto, descrizione=None, caricato_da=None):
        """Aggiunge un documento al progetto."""
        session = self._get_session()
        try:
            from .data_models import ProgettoDocumento
            
            documento = ProgettoDocumento(
                ProgettoID=progetto_id,
                NomeFile=nome_file,
                TipoFile=tipo_file,
                Dimensione=dimensione,
                Contenuto=contenuto,
                Descrizione=descrizione,
                CaricatoDa=caricato_da
            )
            session.add(documento)
            session.commit()
            logger.info(f"Documento {nome_file} aggiunto al progetto {progetto_id}")
            return True
        except Exception as e:
            logger.error(f"Errore aggiunta documento: {e}")
            session.rollback()
            raise
        finally:
            session.close()

    def get_progetto_documenti(self, progetto_id):
        """Recupera tutti i documenti di un progetto."""
        session = self._get_session()
        try:
            from .data_models import ProgettoDocumento
            
            documenti = session.scalars(
                select(ProgettoDocumento)
                .where(ProgettoDocumento.ProgettoID == progetto_id)
                .order_by(ProgettoDocumento.DataCaricamento.desc())
            ).all()
            return [self._detach_object(session, d) for d in documenti]
        finally:
            session.close()

    def get_progetto_documento(self, documento_id):
        """Recupera un singolo documento."""
        session = self._get_session()
        try:
            from .data_models import ProgettoDocumento
            
            documento = session.get(ProgettoDocumento, documento_id)
            return self._detach_object(session, documento) if documento else None
        finally:
            session.close()

    def delete_progetto_documento(self, documento_id):
        """Elimina un documento."""
        session = self._get_session()
        try:
            from .data_models import ProgettoDocumento
            
            documento = session.get(ProgettoDocumento, documento_id)
            if documento:
                session.delete(documento)
                session.commit()
                logger.info(f"Documento {documento_id} eliminato")
                return True
            return False
        except Exception as e:
            logger.error(f"Errore eliminazione documento: {e}")
            session.rollback()
            raise
        finally:
            session.close()
    
    def get_all_project_documents(self, project_id):
        """
        Recupera tutti i documenti di un progetto NPI (documenti task).
        Restituisce una lista di dizionari con informazioni complete.
        """
        session = self._get_session()
        try:
            from .data_models import NpiDocument, TaskProdotto, WaveNPI, TaskCatalogo, NpiDocumentType
            
            # Query per ottenere tutti i documenti dei task del progetto
            task_documents = session.scalars(
                select(NpiDocument)
                .join(TaskProdotto, NpiDocument.TaskProdottoId == TaskProdotto.TaskProdottoID)
                .join(WaveNPI, TaskProdotto.WaveID == WaveNPI.WaveID)
                .where(WaveNPI.ProgettoID == project_id)
                .options(
                    joinedload(NpiDocument.task_prodotto).joinedload(TaskProdotto.task_catalogo),
                    joinedload(NpiDocument.document_type)
                )
                .order_by(NpiDocument.DateIn.desc())
            ).all()
            
            # Formatta i risultati
            documents = []
            for doc in task_documents:
                task_name = doc.task_prodotto.task_catalogo.NomeTask if doc.task_prodotto and doc.task_prodotto.task_catalogo else "N/A"
                doc_type = doc.document_type.NpiDocumentDescription if doc.document_type else "N/A"
                
                documents.append({
                    'doc_id': doc.NpiDocumentId,
                    'task_name': task_name,
                    'doc_type': doc_type,
                    'doc_title': doc.DocumentTitle or "",
                    'date_in': doc.DateIn,
                    'date_in_formatted': doc.DateIn.strftime('%d/%m/%Y %H:%M') if doc.DateIn else "N/A",
                    'user': doc.User or "N/A",
                    'version': doc.VersionNumber or 0,
                    'value': doc.ValueInEur,
                    'note': doc.Note
                })
            
            return documents
            
        except Exception as e:
            logger.error(f"Errore recupero documenti progetto {project_id}: {e}", exc_info=True)
            raise
        finally:
            session.close()
    
    def get_npi_document(self, document_id):
        """Recupera un singolo documento NPI con il suo contenuto."""
        session = self._get_session()
        try:
            from .data_models import NpiDocument
            
            documento = session.get(NpiDocument, document_id)
            return documento
            
        except Exception as e:
            logger.error(f"Errore recupero documento {document_id}: {e}", exc_info=True)
            raise
        finally:
            session.close()
