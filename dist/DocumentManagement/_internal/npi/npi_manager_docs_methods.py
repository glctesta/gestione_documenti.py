
    def get_all_project_documents(self, project_id):
        """
        Recupera tutti i documenti di un progetto NPI (sia documenti progetto che documenti task).
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
