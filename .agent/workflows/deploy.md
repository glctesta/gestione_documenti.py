---
description: Build, sign, deploy and version update for DocumentManagement.exe
---

# Deploy Workflow

// turbo-all

## Steps

1. **Increment version** in `main.py` (`APP_VERSION`, cerca `^APP_VERSION` — la riga
   cambia a ogni modifica del file), increment the last digit by 1.

2. **Compile main.spec** with PyInstaller:
```
pyinstaller main.spec --noconfirm
```

3. **Copy updater.exe** to `_internal`:
```
Copy-Item "dist\updater.exe" "dist\DocumentManagement\_internal\updater.exe" -Force
```

4. **Sign both executables**:
```
& "C:\Program Files (x86)\Windows Kits\10\bin\10.0.26100.0\x86\signtool.exe" sign /sha1 "a21358bd1e887cef30c0ae40c7e8b9c885b833b3" /fd SHA256 /tr 
```

5. **Delete destination** contents:
```
Remove-Item "T:\Traceability_RESET_Services\!!!!VW SoftWare\DocumentManagement\*" -Recurse -Force
```

6. **Copy to destination**:
```
Copy-Item "dist\DocumentManagement\*" "T:\Traceability_RESET_Services\!!!!VW SoftWare\DocumentManagement\" -Recurse -Force
```

7. **Generate deploy manifest ON THE DESTINATION** — OBBLIGATORIO, ultimo passo dopo la copia:
```
python generate_deploy_manifest.py "T:\Traceability_RESET_Services\!!!!VW SoftWare\DocumentManagement"
```
Poi verifica che il file esista:
```
Test-Path "T:\Traceability_RESET_Services\!!!!VW SoftWare\DocumentManagement\deploy_manifest.json"
```

> **Perche' e' l'ultimo passo e non prima della copia.** Il manifest contiene
> l'hash SHA-256 di ogni file e l'updater dei client lo usa per copiare dal
> server SOLO i file effettivamente cambiati, confrontando l'hash del file
> LOCALE. Se il manifest manca, `updater.py` ripiega sul confronto byte-a-byte
> che **rilegge dalla rete tutti i ~6000 file**: l'aggiornamento sembra copiare
> di nuovo tutto ed e' lentissimo. Generandolo prima della copia il file
> rischia di non arrivare a destinazione (o di essere cancellato dal passo 5);
> generandolo sulla destinazione come ultimo passo il manifest descrive
> esattamente cio' che i client vedranno.

8. **Update DB version** — Run SQL using `@NewVersion` = the new APP_VERSION, and `@Must` = 1 if major/new features, 0 if minor fix:
```sql
use Traceability_RS
go

BEGIN TRANSACTION;
DECLARE @NewVersion nvarchar(10) = '<NEW_VERSION>';
DECLARE @Must bit = <0_or_1>;
DECLARE @OldVersion nvarchar(10) = (select Version + ' [Obbligatoria= ' + IIF(@Must =0,'NO','SI') as Versione from traceability_rs.dbo.SWVersions where dateout is null);

BEGIN TRY
    UPDATE [Traceability_RS].[dbo].[SWVersions] 
    SET DateOut = GETDATE()
    WHERE DateOut IS NULL;

    INSERT INTO [Traceability_RS].[dbo].[SWVersions] (NameProgram, Version, Datesys, DateOut, MainPath, Must)
    SELECT 
        NameProgram, 
        @NewVersion AS Version,
        GETDATE() AS Datesys,
        NULL AS DateOut,
        MainPath, 
        @Must
    FROM 
        [Traceability_RS].[dbo].[SWVersions]
    WHERE 
        DateOut IS NOT NULL
    ORDER BY 
        Datesys DESC
    OFFSET 0 ROWS FETCH NEXT 1 ROWS ONLY;

    Print @OldVersion + ' → Nuova Versione = ' + @NewVersion + ', Obbligatoria= ' + IIF(@Must=0,'NO','SI')
    COMMIT TRANSACTION;
END TRY
BEGIN CATCH
    ROLLBACK TRANSACTION;
    DECLARE @ErrorMessage NVARCHAR(4000);
    DECLARE @ErrorSeverity INT;
    DECLARE @ErrorState INT;
    SELECT @ErrorMessage = ERROR_MESSAGE(), @ErrorSeverity = ERROR_SEVERITY(), @ErrorState = ERROR_STATE();
    RAISERROR (@ErrorMessage, @ErrorSeverity, @ErrorState);
    SELECT * FROM SWVersions WHERE DateOut IS NULL;
END CATCH;
```