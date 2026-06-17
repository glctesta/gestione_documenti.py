"""
kit_essegi_parser.py
Parser dei file XLSX "lista prelievo" generati da Essegi (report Reels
traceability) salvati in T:\\KITTING.

Spec: docs/PlanRespect_KitPreparation_Spec_v1.2.md §5.1.1
Rilevazioni Sprint 0:
  - le colonne NON hanno posizione fissa: vanno ricavate dalla riga di
    intestazione 'REEL CODE' (osservato: dati da col. B nel file reale)
  - gli ordini sono nell'intestazione in formato compatto 'PR554/553/552/551'
    e vanno normalizzati a 9 caratteri totali: 'PR554' -> 'PR0000554'
"""
import hashlib
import logging
import os
import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

logger = logging.getLogger("PlanMonitor")

KITTING_DIR = r"T:\KITTING"

RE_UNIQUE_HU = re.compile(r'^HU\d{9}(_\d{2})?$')
RE_UNIQUE_SHORT = re.compile(r'^\d{6}$')
RE_ORDERS_COMPACT = re.compile(r'^PR\d+(?:/\d+)+$|^PR\d+$')

ORDER_TOTAL_LEN = 9  # 'PR' + zeri di padding + numero = 9 caratteri


@dataclass
class EssegiRow:
    """Una riga materiale della lista prelievo."""
    row_number: int            # riga nel foglio Excel (per messaggi)
    unique_number: str         # REEL CODE
    material_code: str         # ITEM CODE
    quantity: float            # QT


@dataclass
class EssegiFile:
    """Risultato del parsing di un file lista prelievo."""
    file_path: str
    file_name: str
    file_hash: str             # SHA-256 del contenuto
    file_date: datetime        # LastWriteTime
    orders_compact: str        # es. 'PR554/553/552/551'
    orders: List[str]          # normalizzati, es. ['PR0000554', ...]
    rows: List[EssegiRow] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    @property
    def distinct_materials(self) -> set:
        return {r.material_code for r in self.rows}


class EssegiParseError(Exception):
    """Errore bloccante nel parsing della lista prelievo."""


def normalize_order(num: str) -> str:
    """'554' -> 'PR0000554' (lunghezza totale 9, 'PR' incluso)."""
    return 'PR' + num.zfill(ORDER_TOTAL_LEN - 2)


def expand_orders(compact: str) -> List[str]:
    """'PR554/553/552/551' -> ['PR0000554', 'PR0000553', 'PR0000552', 'PR0000551']"""
    parts = compact.replace(' ', '').split('/')
    nums = [parts[0][2:]] + parts[1:]
    return [normalize_order(n) for n in nums if n.isdigit()]


def file_sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()


def list_kitting_files(directory: str = KITTING_DIR) -> List[dict]:
    """
    Elenca i file .xlsx in T:\\KITTING con anteprima ordini, ordinati per
    data modifica decrescente. Ogni voce: {path, name, date, orders_compact}.
    """
    if not os.path.isdir(directory):
        raise EssegiParseError(f"Directory non raggiungibile: {directory}")
    out = []
    for f in os.listdir(directory):
        if not f.lower().endswith('.xlsx') or f.startswith('~$'):
            continue
        path = os.path.join(directory, f)
        try:
            compact, _ = _find_orders_header_quick(path)
        except Exception as e:
            logger.warning("Anteprima ordini fallita per %s: %s", f, e)
            compact = None
        out.append({
            'path': path,
            'name': f,
            'date': datetime.fromtimestamp(os.path.getmtime(path)),
            'orders_compact': compact or '?',
        })
    out.sort(key=lambda d: d['date'], reverse=True)
    return out


def _find_orders_header_quick(path: str):
    from openpyxl import load_workbook
    wb = load_workbook(path, read_only=True, data_only=True)
    try:
        return _find_orders_header(wb.active)
    finally:
        wb.close()


def _find_orders_header(ws, max_rows: int = 10):
    """Cerca la riga ordini compatta nelle prime righe (qualsiasi colonna)."""
    for row in ws.iter_rows(min_row=1, max_row=max_rows):
        for cell in row:
            v = str(cell.value).strip() if cell.value is not None else ''
            if RE_ORDERS_COMPACT.match(v):
                return v, cell.row
    return None, None


def _find_data_columns(ws, max_rows: int = 20):
    """
    Individua la riga di intestazione colonne e gli indici (0-based) di
    REEL CODE / ITEM CODE / QT. Ritorna (data_start_row, col_unique, col_code, col_qty).
    """
    for row in ws.iter_rows(min_row=1, max_row=max_rows):
        headers = {str(c.value).strip().upper(): c.column - 1
                   for c in row if c.value is not None}
        if 'REEL CODE' in headers:
            col_unique = headers['REEL CODE']
            col_code = headers.get('ITEM CODE', col_unique + 1)
            col_qty = headers.get('QT', headers.get('QUANTITY', col_unique + 3))
            return row[0].row + 1, col_unique, col_code, col_qty
    return None, None, None, None


def parse_essegi_file(path: str) -> EssegiFile:
    """
    Parsa un file lista prelievo Essegi. Solleva EssegiParseError se il
    tracciato non e' riconoscibile (niente ordini o niente righe dati).
    Le anomalie non bloccanti finiscono in .warnings.
    """
    from openpyxl import load_workbook
    if not os.path.isfile(path):
        raise EssegiParseError(f"File non trovato: {path}")

    wb = load_workbook(path, read_only=True, data_only=True)
    try:
        ws = wb.active

        compact, _ = _find_orders_header(ws)
        if not compact:
            raise EssegiParseError(
                "Intestazione ordini non trovata (atteso formato 'PRnnn/nnn/...' nelle prime righe)")
        orders = expand_orders(compact)
        if not orders:
            raise EssegiParseError(f"Nessun ordine valido nell'intestazione: '{compact}'")

        data_start, col_unique, col_code, col_qty = _find_data_columns(ws)
        if data_start is None:
            raise EssegiParseError("Intestazione colonne 'REEL CODE' non trovata")

        result = EssegiFile(
            file_path=path,
            file_name=os.path.basename(path),
            file_hash=file_sha256(path),
            file_date=datetime.fromtimestamp(os.path.getmtime(path)),
            orders_compact=compact,
            orders=orders,
        )

        def cell(row, idx):
            return row[idx].value if len(row) > idx else None

        for row in ws.iter_rows(min_row=data_start):
            raw = cell(row, col_unique)
            unique = str(raw).strip() if raw is not None else ''
            if not unique:
                continue
            if not (RE_UNIQUE_HU.match(unique) or RE_UNIQUE_SHORT.match(unique)):
                # ripetizioni di testata a cambio pagina: ignora in silenzio
                if unique.upper() != 'REEL CODE' and not RE_ORDERS_COMPACT.match(unique):
                    result.warnings.append(
                        f"Riga {row[0].row}: '{unique}' non riconosciuto come unique number, riga saltata")
                continue

            raw_code = cell(row, col_code)
            code = str(raw_code).strip() if raw_code is not None else ''
            if not code:
                result.warnings.append(f"Riga {row[0].row}: MaterialCode mancante, riga saltata")
                continue

            raw_qty = cell(row, col_qty)
            try:
                qty = (float(str(raw_qty).replace('.', '').replace(',', '.'))
                       if isinstance(raw_qty, str) else float(raw_qty))
                if qty < 0:
                    raise ValueError
            except (TypeError, ValueError):
                result.warnings.append(
                    f"Riga {row[0].row}: quantita' non valida ({raw_qty!r}), riga saltata")
                continue

            result.rows.append(EssegiRow(
                row_number=row[0].row,
                unique_number=unique,
                material_code=code,
                quantity=qty,
            ))

        if not result.rows:
            raise EssegiParseError("Nessuna riga materiale valida nel file")

        logger.info("Parsed %s: ordini=%s, righe=%d, warnings=%d",
                    result.file_name, result.orders, len(result.rows), len(result.warnings))
        return result
    finally:
        wb.close()
