import pyodbc
from config_manager import ConfigManager

creds = ConfigManager(key_file='encryption_key.key', config_file='db_config.enc').load_config()
cs = (f"DRIVER={creds['driver']};SERVER={creds['server']};DATABASE={creds['database']};"
      f"UID={creds['username']};PWD={creds['password']};TrustServerCertificate=Yes")
cn = pyodbc.connect(cs, autocommit=True)
cur = cn.cursor()
print('Famiglia di 99900393:', end=' ')
cur.execute("""SELECT m.CodiceMateriale, fm.Famiglia FROM Traceability_RS.ind.Materiali m
  LEFT JOIN Traceability_RS.ind.FamigliaMateriali fm ON fm.FamigliaMaterialiId = m.FamigliaMaterialiId
  WHERE m.CodiceMateriale = '99900393'""")
print(cur.fetchone())

print('Famiglie presenti:')
cur.execute("""SELECT Famiglia, COUNT(*) FROM Traceability_RS.ind.FamigliaMateriali GROUP BY Famiglia""")
for r in cur.fetchall():
    print(' ', r)

print('Etichette reali (famiglia Labels):')
cur.execute("""SELECT TOP 5 m.CodiceMateriale FROM Traceability_RS.ind.Materiali m
  JOIN Traceability_RS.ind.FamigliaMateriali fm ON fm.FamigliaMaterialiId = m.FamigliaMaterialiId
  WHERE fm.Famiglia = 'Labels'""")
for r in cur.fetchall():
    print(' ', r[0])

print('Prodotti con associazioni attive:')
cur.execute("""SELECT TOP 3 b.idProduct, p.ProductCode, COUNT(*) FROM Traceability_RS.ind.BomIndirectMaterials b
  JOIN Traceability_RS.dbo.Products p ON p.IDProduct = b.idProduct
  WHERE b.DateOut IS NULL GROUP BY b.idProduct, p.ProductCode""")
for r in cur.fetchall():
    print(' ', r)
cur.close()
cn.close()
