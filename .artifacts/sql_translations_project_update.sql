-- Traduzioni per aggiornamento progetto esistente

-- Messaggio: Progetto esiste, vuoi aggiornare?
IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'it' AND translationkey = 'msg_project_exists_update')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('it', 'msg_project_exists_update', 'Il progetto esiste già. Vuoi aggiornare i dati (owner, descrizione) e aggiungere documenti?');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'en' AND translationkey = 'msg_project_exists_update')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('en', 'msg_project_exists_update', 'Project already exists. Do you want to update data (owner, description) and add documents?');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'ro' AND translationkey = 'msg_project_exists_update')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('ro', 'msg_project_exists_update', N'Proiectul există deja. Doriți să actualizați datele (proprietar, descriere) și să adăugați documente?');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'de' AND translationkey = 'msg_project_exists_update')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('de', 'msg_project_exists_update', 'Projekt existiert bereits. Möchten Sie Daten (Eigentümer, Beschreibung) aktualisieren und Dokumente hinzufügen?');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'sv' AND translationkey = 'msg_project_exists_update')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('sv', 'msg_project_exists_update', 'Projektet finns redan. Vill du uppdatera data (ägare, beskrivning) och lägga till dokument?');

-- Messaggio: Progetto aggiornato
IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'it' AND translationkey = 'msg_project_updated')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('it', 'msg_project_updated', 'Progetto aggiornato con successo');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'en' AND translationkey = 'msg_project_updated')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('en', 'msg_project_updated', 'Project updated successfully');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'ro' AND translationkey = 'msg_project_updated')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('ro', 'msg_project_updated', N'Proiect actualizat cu succes');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'de' AND translationkey = 'msg_project_updated')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('de', 'msg_project_updated', 'Projekt erfolgreich aktualisiert');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'sv' AND translationkey = 'msg_project_updated')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('sv', 'msg_project_updated', 'Projekt uppdaterat');
