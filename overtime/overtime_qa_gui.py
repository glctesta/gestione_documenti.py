"""
Overtime Q&A GUI
Form per visualizzare e rispondere alle domande sulle richieste di straordinario.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def open_overtime_qa_window(parent, db_handler, lang_manager, user_name, user_id=0):
    """
    Apre la finestra per visualizzare e rispondere alle domande overtime.

    Args:
        parent: Finestra parent
        db_handler: DatabaseHandler instance
        lang_manager: LanguageManager instance
        user_name: Nome utente loggato
        user_id: ID utente (idanga da tbuserkey)
    """
    OvertimeQAWindow(parent, db_handler, lang_manager, user_name, user_id)


class OvertimeQAWindow(tk.Toplevel):
    """
    Finestra per visualizzare domande ricevute e inserire risposte.
    Filtrata per l'utente loggato (mostra solo le domande rivolte a lui).
    """

    def __init__(self, parent, db_handler, lang_manager, user_name, user_id=0):
        super().__init__(parent)

        self.db = db_handler
        self.lang = lang_manager
        self.user_name = user_name
        self.user_id = user_id  # idanga dell'utente loggato

        # Setup finestra
        self.title(self.lang.get('overtime_qa_title', 'Risposte Straordinari'))
        self.geometry("1300x650")
        self.transient(parent)
        self.grab_set()

        self._create_widgets()
        self._load_questions()

    def _create_widgets(self):
        """Crea i widget dell'interfaccia."""
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # === FILTRI ===
        filter_frame = ttk.LabelFrame(main_frame, text=self.lang.get('filters', 'Filtri'), padding="10")
        filter_frame.pack(fill=tk.X, pady=5)

        ttk.Label(filter_frame, text=self.lang.get('answer_status', 'Stato:')).grid(
            row=0, column=0, padx=5, pady=5, sticky=tk.W
        )
        self.status_var = tk.StringVar(value='Pending')
        status_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.status_var,
            values=['All', 'Pending', 'Answered'],
            state='readonly',
            width=15
        )
        status_combo.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        status_combo.bind('<<ComboboxSelected>>', lambda e: self._load_questions())

        ttk.Button(
            filter_frame,
            text=self.lang.get('refresh', 'Aggiorna'),
            command=self._load_questions
        ).grid(row=0, column=2, padx=5, pady=5)

        # === LISTA DOMANDE ===
        list_frame = ttk.LabelFrame(
            main_frame,
            text=self.lang.get('pending_questions', 'Domande in attesa'),
            padding="10"
        )
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        columns = ('qa_id', 'request_number', 'question_date', 'asked_by', 'question', 'employee', 'status')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)

        self.tree.heading('qa_id', text='ID')
        self.tree.heading('request_number', text=self.lang.get('request_number', 'Numero'))
        self.tree.heading('question_date', text=self.lang.get('question_date', 'Data domanda'))
        self.tree.heading('asked_by', text=self.lang.get('asked_by', 'Chiesto da'))
        self.tree.heading('question', text=self.lang.get('question_text', 'Domanda'))
        self.tree.heading('employee', text=self.lang.get('employee_reference', 'Dipendente'))
        self.tree.heading('status', text=self.lang.get('answer_status', 'Stato'))

        self.tree.column('qa_id', width=50)
        self.tree.column('request_number', width=130)
        self.tree.column('question_date', width=140)
        self.tree.column('asked_by', width=180)
        self.tree.column('question', width=350)
        self.tree.column('employee', width=180)
        self.tree.column('status', width=100)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # === PULSANTI AZIONE ===
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=10)

        ttk.Button(
            action_frame,
            text=self.lang.get('reply', 'Rispondi'),
            command=self._reply_to_question
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            action_frame,
            text=self.lang.get('close', 'Chiudi'),
            command=self.destroy
        ).pack(side=tk.RIGHT, padx=5)

    def _load_questions(self):
        """Carica le domande destinate all'utente loggato."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        status_filter = self.status_var.get()

        # Le domande sono destinate al richiedente (IdChief) della overtime request
        # L'utente loggato corrisponde a IdChief nella ExtraTimeApproval
        query = """
        SELECT
            q.QAId,
            ISNULL(r.NumRegistro, CAST(a.IdRegistro AS VARCHAR)) AS RequestNumber,
            q.QuestionDate,
            ISNULL(u_asker.NomeUser, 'N/A') AS AskedBy,
            q.QuestionText,
            CASE
                WHEN q.StoryExtraHourApprovalId IS NOT NULL
                THEN ISNULL(e.EmployeeSurname + ' ' + e.EmployeeName, 'N/A')
                ELSE '--'
            END AS EmployeeRef,
            CASE
                WHEN q.AnswerDate IS NOT NULL THEN 'Answered'
                ELSE 'Pending'
            END AS Status
        FROM ResetServices.dbo.ExtraTimeApprovalQA q
        INNER JOIN ResetServices.dbo.ExtraTimeApproval a
            ON q.ExtraHourApprovalId = a.ExtraHourApprovalId
        LEFT JOIN ResetServices.dbo.TbRegistro r
            ON a.IdRegistro = r.Contatore
        LEFT JOIN ResetServices.dbo.tbuserkey u_asker
            ON q.QuestionBy = u_asker.idanga
        LEFT JOIN ResetServices.dbo.ExtraTimeApprovalStory s
            ON q.StoryExtraHourApprovalId = s.StoryExtraHourApprovalId
        LEFT JOIN Employee.dbo.EmployeeHireHistory h
            ON s.IdEmployee = h.EmployeeHireHistoryId
        LEFT JOIN Employee.dbo.Employees e
            ON h.EmployeeId = e.EmployeeId
        WHERE a.IdChief = ?
        """

        params = [self.user_id]

        if status_filter == 'Pending':
            query += " AND q.AnswerDate IS NULL"
        elif status_filter == 'Answered':
            query += " AND q.AnswerDate IS NOT NULL"

        query += " ORDER BY q.QuestionDate DESC"

        try:
            cursor = self.db.conn.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()
            cursor.close()

            for row in results:
                date_str = row[2].strftime('%d/%m/%Y %H:%M') if row[2] else 'N/D'
                question_preview = (row[4][:80] + '...') if row[4] and len(row[4]) > 80 else (row[4] or '')
                status_label = self.lang.get('answered', 'Answered') if row[6] == 'Answered' \
                    else self.lang.get('pending', 'Pending')

                self.tree.insert('', tk.END, values=(
                    row[0],            # QAId
                    row[1],            # RequestNumber
                    date_str,          # QuestionDate
                    row[3],            # AskedBy
                    question_preview,  # Question (truncated)
                    row[5],            # Employee ref
                    status_label       # Status
                ))

        except Exception as e:
            logger.error(f"Errore caricamento domande: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Errore caricamento domande:\n{str(e)}",
                parent=self
            )

    def _reply_to_question(self):
        """Apre il dialogo per rispondere a una domanda selezionata."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('select_question', 'Selezionare una domanda.'),
                parent=self
            )
            return

        qa_id = self.tree.item(selected[0])['values'][0]
        status_text = self.tree.item(selected[0])['values'][6]

        # Controlla se già risposta
        if status_text == self.lang.get('answered', 'Answered'):
            messagebox.showinfo(
                self.lang.get('info', 'Informazione'),
                self.lang.get('already_answered', 'Questa domanda ha già una risposta.'),
                parent=self
            )
            return

        # Apri dialogo risposta
        dialog = ReplyQuestionDialog(self, self.db, self.lang, qa_id, self.user_id, self.user_name)
        self.wait_window(dialog)

        if dialog.answer_sent:
            self._load_questions()


class ReplyQuestionDialog(tk.Toplevel):
    """Dialogo per rispondere a una domanda overtime."""

    def __init__(self, parent, db_handler, lang_manager, qa_id, user_id, user_name):
        super().__init__(parent)

        self.db = db_handler
        self.lang = lang_manager
        self.qa_id = qa_id
        self.user_id = user_id
        self.user_name = user_name
        self.answer_sent = False

        self.title(self.lang.get('reply_title', 'Rispondi alla domanda'))
        self.geometry("700x550")
        self.transient(parent)
        self.grab_set()

        self._create_widgets()
        self._load_question_details()

    def _create_widgets(self):
        """Crea i widget del dialogo."""
        main_frame = ttk.Frame(self, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # === Info richiesta ===
        info_frame = ttk.LabelFrame(
            main_frame,
            text=self.lang.get('request_reference', 'Riferimento richiesta'),
            padding="10"
        )
        info_frame.pack(fill=tk.X, pady=5)

        ttk.Label(info_frame, text=f"{self.lang.get('request_number', 'Numero')}:",
                  font=('', 9, 'bold')).grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.request_number_label = ttk.Label(info_frame, text='')
        self.request_number_label.grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)

        ttk.Label(info_frame, text=f"{self.lang.get('asked_by', 'Chiesto da')}:",
                  font=('', 9, 'bold')).grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.asker_label = ttk.Label(info_frame, text='')
        self.asker_label.grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)

        # Dipendente (se presente)
        ttk.Label(info_frame, text=f"{self.lang.get('regarding_employee', 'Riguardo al dipendente')}:",
                  font=('', 9, 'bold')).grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        self.employee_label = ttk.Label(info_frame, text='--')
        self.employee_label.grid(row=2, column=1, sticky=tk.W, padx=5, pady=2)

        # === Domanda originale ===
        question_frame = ttk.LabelFrame(
            main_frame,
            text=self.lang.get('original_question', 'Domanda originale'),
            padding="10"
        )
        question_frame.pack(fill=tk.X, pady=5)

        self.question_text = tk.Text(question_frame, height=5, wrap=tk.WORD, state=tk.DISABLED)
        self.question_text.pack(fill=tk.X)

        # === Risposta ===
        answer_frame = ttk.LabelFrame(
            main_frame,
            text=self.lang.get('your_answer', 'La tua risposta'),
            padding="10"
        )
        answer_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.answer_text = tk.Text(answer_frame, height=8, wrap=tk.WORD)
        self.answer_text.pack(fill=tk.BOTH, expand=True)

        # === Pulsanti ===
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)

        ttk.Button(
            btn_frame,
            text=self.lang.get('send_answer', 'Invia risposta'),
            command=self._send_answer
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            btn_frame,
            text=self.lang.get('cancel', 'Annulla'),
            command=self.destroy
        ).pack(side=tk.RIGHT, padx=5)

    def _load_question_details(self):
        """Carica i dettagli della domanda."""
        query = """
        SELECT
            q.QuestionText,
            ISNULL(r.NumRegistro, CAST(a.IdRegistro AS VARCHAR)) AS RequestNumber,
            ISNULL(u_asker.NomeUser, 'N/A') AS AskedBy,
            q.QuestionBy,
            CASE
                WHEN q.StoryExtraHourApprovalId IS NOT NULL
                THEN ISNULL(e.EmployeeSurname + ' ' + e.EmployeeName, 'N/A')
                ELSE NULL
            END AS EmployeeRef,
            q.ExtraHourApprovalId
        FROM ResetServices.dbo.ExtraTimeApprovalQA q
        INNER JOIN ResetServices.dbo.ExtraTimeApproval a
            ON q.ExtraHourApprovalId = a.ExtraHourApprovalId
        LEFT JOIN ResetServices.dbo.TbRegistro r
            ON a.IdRegistro = r.Contatore
        LEFT JOIN ResetServices.dbo.tbuserkey u_asker
            ON q.QuestionBy = u_asker.idanga
        LEFT JOIN ResetServices.dbo.ExtraTimeApprovalStory s
            ON q.StoryExtraHourApprovalId = s.ExtraTimeApprovalStoryId
        LEFT JOIN Employee.dbo.EmployeeHireHistory h
            ON s.IdEmployee = h.EmployeeHireHistoryId
        LEFT JOIN Employee.dbo.Employees e
            ON h.EmployeeId = e.EmployeeId
        WHERE q.QAId = ?
        """

        try:
            result = self.db.fetch_one(query, (self.qa_id,))
            if result:
                self.question_text.config(state=tk.NORMAL)
                self.question_text.insert('1.0', result[0] or '')
                self.question_text.config(state=tk.DISABLED)

                self.request_number_label.config(text=result[1] or 'N/D')
                self.asker_label.config(text=result[2] or 'N/D')
                self._asker_id = result[3]  # Salva per invio email risposta
                self._request_number = result[1] or 'N/D'
                self._request_id = result[5]

                if result[4]:
                    self.employee_label.config(text=result[4])
                else:
                    self.employee_label.config(text='--')

        except Exception as e:
            logger.error(f"Errore caricamento dettagli domanda: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Errore caricamento dettagli:\n{str(e)}",
                parent=self
            )

    def _send_answer(self):
        """Salva la risposta e invia email al mittente della domanda."""
        answer = self.answer_text.get('1.0', tk.END).strip()

        if not answer:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('answer_empty', 'Inserire il testo della risposta.'),
                parent=self
            )
            return

        try:
            # Aggiorna il record QA nel database
            update_query = """
            UPDATE ResetServices.dbo.ExtraTimeApprovalQA
            SET AnswerBy = ?,
                AnswerDate = GETDATE(),
                AnswerText = ?
            WHERE QAId = ?
            """
            cursor = self.db.conn.cursor()
            cursor.execute(update_query, (self.user_id, answer, self.qa_id))
            self.db.conn.commit()
            cursor.close()

            # Invia email di notifica al mittente della domanda
            try:
                from .overtime_manager import OvertimeManager
                manager = OvertimeManager(self.db)
                manager.send_answer_email(
                    qa_id=self.qa_id,
                    asker_id=self._asker_id,
                    answer_text=answer,
                    responder_name=self.user_name,
                    request_number=self._request_number
                )
            except Exception as email_err:
                logger.error(f"Errore invio email risposta: {email_err}", exc_info=True)
                # Non bloccare se l'email fallisce

            messagebox.showinfo(
                self.lang.get('success', 'Successo'),
                self.lang.get('answer_sent_ok', 'Risposta inviata con successo.'),
                parent=self
            )
            self.answer_sent = True
            self.destroy()

        except Exception as e:
            self.db.conn.rollback()
            logger.error(f"Errore salvataggio risposta: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"{self.lang.get('answer_send_error', 'Errore durante invio risposta.')}:\n{str(e)}",
                parent=self
            )
