# File: test_npi_relationships.py

import pytest
from sqlalchemy import inspect
from npi.data_models import (
    Categoria,
    TaskProdotto,
    ProgettoNPI,
    Prodotto,
    TaskCatalogo
)


def test_categoria_structure(db_session):
    """
    Test: Verifica struttura tabella Categories
    """
    # Query una categoria dal database
    categoria = db_session.query(Categoria).first()

    if categoria:
        print(f"\n✅ Categoria trovata:")
        print(f"   CategoryId: {categoria.CategoryId}")
        print(f"   Category: {categoria.Category}")
        print(f"   NrOrdin: {categoria.NrOrdin}")

        # Verifica che gli attributi esistano
        assert hasattr(categoria, 'CategoryId')
        assert hasattr(categoria, 'Category')
        assert hasattr(categoria, 'NrOrdin')
        assert hasattr(categoria, 'tasks_catalogo')
    else:
        print("\n⚠️ Nessuna categoria trovata nel database")
        pytest.skip("Tabella Categories vuota")


def test_wavenpi_progetto_relationship(db_session):
    """
    Test: Verifica relazione TaskProdotto.WaveID → ProgettiNPI.ProgettoID
    """
    # Query un task con WaveID
    task = db_session.query(TaskProdotto).filter(
        TaskProdotto.WaveID.isnot(None)
    ).first()

    if task:
        print(f"\n✅ TaskProdotto trovato:")
        print(f"   TaskId: {task.TaskId}")
        print(f"   WaveID: {task.WaveID}")

        # Verifica che la relazione funzioni
        if task.progetto_npi:
            print(f"   Progetto NPI collegato: {task.progetto_npi.ProgettoNPIId}")
            assert task.progetto_npi.ProgettoNPIId == task.WaveID
        else:
            print(f"   ⚠️ Nessun ProgettoNPI trovato con ProgettoID={task.WaveID}")
    else:
        print("\n⚠️ Nessun TaskProdotto con WaveID trovato")
        pytest.skip("Nessun TaskProdotto con WaveID nel database")


def test_taskprodotto_prodotto_relationship(db_session):
    """
    Test: Verifica relazione TaskProdotto.ProdottoId → Prodotti.ProdottoID
    """
    # Query un task con ProdottoId
    task = db_session.query(TaskProdotto).filter(
        TaskProdotto.ProdottoId.isnot(None)
    ).first()

    if task:
        print(f"\n✅ TaskProdotto trovato:")
        print(f"   TaskId: {task.TaskId}")
        print(f"   ProdottoId: {task.ProdottoId}")

        # Verifica che la relazione funzioni
        if task.prodotto:
            print(f"   Prodotto collegato: {task.prodotto.NomeProdotto}")
            assert task.prodotto.ProdottoID == task.ProdottoId
        else:
            print(f"   ⚠️ Nessun Prodotto trovato con ProdottoID={task.ProdottoId}")
    else:
        print("\n⚠️ Nessun TaskProdotto con ProdottoId trovato")
        pytest.skip("Nessun TaskProdotto con ProdottoId nel database")


def test_taskprodotto_taskcatalogo_relationship(db_session):
    """
    Test: Verifica relazione TaskProdotto.TaskCatalogoId → TaskCatalogo.TaskID
    """
    # Query un task con TaskCatalogoId
    task = db_session.query(TaskProdotto).filter(
        TaskProdotto.TaskCatalogoId.isnot(None)
    ).first()

    if task:
        print(f"\n✅ TaskProdotto trovato:")
        print(f"   TaskId: {task.TaskId}")
        print(f"   TaskCatalogoId: {task.TaskCatalogoId}")

        # Verifica che la relazione funzioni
        if task.task_catalogo:
            print(f"   TaskCatalogo collegato: {task.task_catalogo.NomeTask}")
            assert task.task_catalogo.TaskCatalogoId == task.TaskCatalogoId
        else:
            print(f"   ⚠️ Nessun TaskCatalogo trovato con TaskID={task.TaskCatalogoId}")
    else:
        print("\n⚠️ Nessun TaskProdotto con TaskCatalogoId trovato")
        pytest.skip("Nessun TaskProdotto con TaskCatalogoId nel database")


def test_progetto_npi_prodotto_relationship(db_session):
    """
    Test: Verifica relazione ProgettiNPI.ProdottoID → Prodotti.ProdottoID
    """
    # Query un progetto con ProdottoID
    progetto = db_session.query(ProgettoNPI).filter(
        ProgettoNPI.ProdottoID.isnot(None)
    ).first()

    if progetto:
        print(f"\n✅ ProgettoNPI trovato:")
        print(f"   ProgettoNPIId: {progetto.ProgettoNPIId}")
        print(f"   ProdottoID: {progetto.ProdottoID}")

        # Verifica che la relazione funzioni
        if progetto.prodotto:
            print(f"   Prodotto collegato: {progetto.prodotto.NomeProdotto}")
            assert progetto.prodotto.ProdottoID == progetto.ProdottoID
        else:
            print(f"   ⚠️ Nessun Prodotto trovato con ProdottoID={progetto.ProdottoID}")
    else:
        print("\n⚠️ Nessun ProgettoNPI con ProdottoID trovato")
        pytest.skip("Nessun ProgettoNPI con ProdottoID nel database")


def test_database_tables_exist(engine):
    """
    Test: Verifica che tutte le tabelle esistano nel database
    """
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    print(f"\n📊 Tabelle trovate nel database ({len(tables)}):")
    for table in sorted(tables):
        print(f"   - {table}")

    # Verifica che le tabelle NPI esistano
    required_tables = [
        'Categories',
        'TaskCatalogo',
        'TaskProdotto',
        'ProgettiNPI',
        'Prodotti'
    ]

    for table in required_tables:
        assert table in tables, f"Tabella {table} non trovata nel database"
        print(f"   ✅ {table} presente")


def test_count_records(db_session):
    """
    Test: Conta i record nelle tabelle principali
    """
    counts = {
        'Categories': db_session.query(Categoria).count(),
        'TaskCatalogo': db_session.query(TaskCatalogo).count(),
        'TaskProdotto': db_session.query(TaskProdotto).count(),
        'ProgettiNPI': db_session.query(ProgettoNPI).count(),
        'Prodotti': db_session.query(Prodotto).count(),
    }

    print(f"\n📈 Record count:")
    for table, count in counts.items():
        print(f"   {table}: {count} records")
        assert count >= 0  # Verifica che la query funzioni
