-- ============================================================
-- FAQ Module Translations
-- Table: [Traceability_RS].[dbo].[AppTranslations]
-- Lingue: it, en, ro, de, sv
-- ============================================================

-- ── Menu voci ────────────────────────────────────────────────

-- submenu_faq
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'submenu_faq' AND LanguageCode = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'submenu_faq', N'FAQ');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'submenu_faq' AND LanguageCode = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'submenu_faq', N'FAQ');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'submenu_faq' AND LanguageCode = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'submenu_faq', N'FAQ');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'submenu_faq' AND LanguageCode = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'submenu_faq', N'FAQ');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'submenu_faq' AND LanguageCode = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'submenu_faq', N'FAQ');

-- submenu_faq_viewer
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'submenu_faq_viewer' AND LanguageCode = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'submenu_faq_viewer', N'Domande frequenti');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'submenu_faq_viewer' AND LanguageCode = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'submenu_faq_viewer', N'Frequently Asked Questions');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'submenu_faq_viewer' AND LanguageCode = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'submenu_faq_viewer', N'Întrebări frecvente');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'submenu_faq_viewer' AND LanguageCode = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'submenu_faq_viewer', N'Häufige Fragen');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'submenu_faq_viewer' AND LanguageCode = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'submenu_faq_viewer', N'Vanliga frågor');

-- submenu_faq_management
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'submenu_faq_management' AND LanguageCode = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'submenu_faq_management', N'Gestione FAQ');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'submenu_faq_management' AND LanguageCode = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'submenu_faq_management', N'FAQ Management');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'submenu_faq_management' AND LanguageCode = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'submenu_faq_management', N'Gestionare FAQ');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'submenu_faq_management' AND LanguageCode = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'submenu_faq_management', N'FAQ-Verwaltung');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'submenu_faq_management' AND LanguageCode = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'submenu_faq_management', N'FAQ-hantering');

-- gestione_faq (autorizzazione)
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'gestione_faq' AND LanguageCode = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'gestione_faq', N'Gestione FAQ');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'gestione_faq' AND LanguageCode = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'gestione_faq', N'FAQ Management');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'gestione_faq' AND LanguageCode = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'gestione_faq', N'Gestionare FAQ');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'gestione_faq' AND LanguageCode = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'gestione_faq', N'FAQ-Verwaltung');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'gestione_faq' AND LanguageCode = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'gestione_faq', N'FAQ-hantering');

-- ── FaqViewerWindow ──────────────────────────────────────────

-- faq_viewer_title
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_viewer_title' AND LanguageCode = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'faq_viewer_title', N'Domande Frequenti — FAQ');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_viewer_title' AND LanguageCode = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'faq_viewer_title', N'Frequently Asked Questions — FAQ');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_viewer_title' AND LanguageCode = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'faq_viewer_title', N'Întrebări frecvente — FAQ');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_viewer_title' AND LanguageCode = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'faq_viewer_title', N'Häufig gestellte Fragen — FAQ');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_viewer_title' AND LanguageCode = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'faq_viewer_title', N'Vanliga frågor — FAQ');

-- faq_chapters
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_chapters' AND LanguageCode = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'faq_chapters', N'Capitoli');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_chapters' AND LanguageCode = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'faq_chapters', N'Chapters');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_chapters' AND LanguageCode = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'faq_chapters', N'Capitole');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_chapters' AND LanguageCode = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'faq_chapters', N'Kapitel');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_chapters' AND LanguageCode = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'faq_chapters', N'Kapitel');

-- faq_no_answers
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_no_answers' AND LanguageCode = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'faq_no_answers', N'Nessuna risposta disponibile.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_no_answers' AND LanguageCode = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'faq_no_answers', N'No answers available.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_no_answers' AND LanguageCode = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'faq_no_answers', N'Niciun răspuns disponibil.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_no_answers' AND LanguageCode = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'faq_no_answers', N'Keine Antworten verfügbar.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_no_answers' AND LanguageCode = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'faq_no_answers', N'Inga svar tillgängliga.');

-- ── FaqManagementWindow — titolo e tab ───────────────────────

-- faq_mgmt_title
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_mgmt_title' AND LanguageCode = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'faq_mgmt_title', N'Gestione FAQ');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_mgmt_title' AND LanguageCode = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'faq_mgmt_title', N'FAQ Management');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_mgmt_title' AND LanguageCode = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'faq_mgmt_title', N'Gestionare FAQ');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_mgmt_title' AND LanguageCode = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'faq_mgmt_title', N'FAQ-Verwaltung');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_mgmt_title' AND LanguageCode = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'faq_mgmt_title', N'FAQ-hantering');

-- faq_tab_chapters
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_tab_chapters' AND LanguageCode = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'faq_tab_chapters', N'Capitoli');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_tab_chapters' AND LanguageCode = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'faq_tab_chapters', N'Chapters');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_tab_chapters' AND LanguageCode = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'faq_tab_chapters', N'Capitole');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_tab_chapters' AND LanguageCode = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'faq_tab_chapters', N'Kapitel');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_tab_chapters' AND LanguageCode = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'faq_tab_chapters', N'Kapitel');

-- faq_tab_subtitles
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_tab_subtitles' AND LanguageCode = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'faq_tab_subtitles', N'Domande');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_tab_subtitles' AND LanguageCode = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'faq_tab_subtitles', N'Questions');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_tab_subtitles' AND LanguageCode = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'faq_tab_subtitles', N'Întrebări');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_tab_subtitles' AND LanguageCode = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'faq_tab_subtitles', N'Fragen');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_tab_subtitles' AND LanguageCode = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'faq_tab_subtitles', N'Frågor');

-- faq_tab_answers
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_tab_answers' AND LanguageCode = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'faq_tab_answers', N'Risposte');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_tab_answers' AND LanguageCode = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'faq_tab_answers', N'Answers');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_tab_answers' AND LanguageCode = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'faq_tab_answers', N'Răspunsuri');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_tab_answers' AND LanguageCode = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'faq_tab_answers', N'Antworten');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_tab_answers' AND LanguageCode = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'faq_tab_answers', N'Svar');

-- ── Capitoli CRUD ────────────────────────────────────────────

-- faq_add_chapter
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_add_chapter' AND LanguageCode = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'faq_add_chapter', N'Nuovo Capitolo');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_add_chapter' AND LanguageCode = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'faq_add_chapter', N'New Chapter');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_add_chapter' AND LanguageCode = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'faq_add_chapter', N'Capitol nou');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_add_chapter' AND LanguageCode = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'faq_add_chapter', N'Neues Kapitel');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_add_chapter' AND LanguageCode = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'faq_add_chapter', N'Nytt kapitel');

-- faq_edit_chapter
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_edit_chapter' AND LanguageCode = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'faq_edit_chapter', N'Modifica Capitolo');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_edit_chapter' AND LanguageCode = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'faq_edit_chapter', N'Edit Chapter');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_edit_chapter' AND LanguageCode = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'faq_edit_chapter', N'Modifică Capitol');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_edit_chapter' AND LanguageCode = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'faq_edit_chapter', N'Kapitel bearbeiten');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_edit_chapter' AND LanguageCode = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'faq_edit_chapter', N'Redigera kapitel');

-- faq_chapter_title_prompt
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_chapter_title_prompt' AND LanguageCode = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'faq_chapter_title_prompt', N'Titolo del capitolo:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_chapter_title_prompt' AND LanguageCode = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'faq_chapter_title_prompt', N'Chapter title:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_chapter_title_prompt' AND LanguageCode = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'faq_chapter_title_prompt', N'Titlul capitolului:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_chapter_title_prompt' AND LanguageCode = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'faq_chapter_title_prompt', N'Kapiteltitel:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_chapter_title_prompt' AND LanguageCode = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'faq_chapter_title_prompt', N'Kapiteltitel:');

-- faq_select_chapter
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_select_chapter' AND LanguageCode = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'faq_select_chapter', N'Seleziona un capitolo');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_select_chapter' AND LanguageCode = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'faq_select_chapter', N'Select a chapter');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_select_chapter' AND LanguageCode = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'faq_select_chapter', N'Selectați un capitol');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_select_chapter' AND LanguageCode = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'faq_select_chapter', N'Bitte ein Kapitel auswählen');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_select_chapter' AND LanguageCode = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'faq_select_chapter', N'Välj ett kapitel');

-- faq_archive_confirm
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_archive_confirm' AND LanguageCode = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'faq_archive_confirm', N'Archiviare il capitolo e tutto il suo contenuto (domande e risposte)?');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_archive_confirm' AND LanguageCode = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'faq_archive_confirm', N'Archive this chapter and all its content (questions and answers)?');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_archive_confirm' AND LanguageCode = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'faq_archive_confirm', N'Arhivați capitolul și tot conținutul său (întrebări și răspunsuri)?');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_archive_confirm' AND LanguageCode = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'faq_archive_confirm', N'Dieses Kapitel und seinen gesamten Inhalt (Fragen und Antworten) archivieren?');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_archive_confirm' AND LanguageCode = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'faq_archive_confirm', N'Arkivera detta kapitel och allt innehåll (frågor och svar)?');

-- ── Domande CRUD ─────────────────────────────────────────────

-- faq_filter_chapter
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_filter_chapter' AND LanguageCode = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'faq_filter_chapter', N'Capitolo:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_filter_chapter' AND LanguageCode = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'faq_filter_chapter', N'Chapter:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_filter_chapter' AND LanguageCode = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'faq_filter_chapter', N'Capitol:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_filter_chapter' AND LanguageCode = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'faq_filter_chapter', N'Kapitel:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_filter_chapter' AND LanguageCode = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'faq_filter_chapter', N'Kapitel:');

-- faq_add_subtitle
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_add_subtitle' AND LanguageCode = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'faq_add_subtitle', N'Nuova Domanda');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_add_subtitle' AND LanguageCode = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'faq_add_subtitle', N'New Question');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_add_subtitle' AND LanguageCode = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'faq_add_subtitle', N'Întrebare nouă');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_add_subtitle' AND LanguageCode = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'faq_add_subtitle', N'Neue Frage');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_add_subtitle' AND LanguageCode = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'faq_add_subtitle', N'Ny fråga');

-- faq_edit_subtitle
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_edit_subtitle' AND LanguageCode = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'faq_edit_subtitle', N'Modifica Domanda');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_edit_subtitle' AND LanguageCode = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'faq_edit_subtitle', N'Edit Question');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_edit_subtitle' AND LanguageCode = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'faq_edit_subtitle', N'Modifică Întrebare');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_edit_subtitle' AND LanguageCode = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'faq_edit_subtitle', N'Frage bearbeiten');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_edit_subtitle' AND LanguageCode = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'faq_edit_subtitle', N'Redigera fråga');

-- faq_subtitle_prompt
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_subtitle_prompt' AND LanguageCode = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'faq_subtitle_prompt', N'Testo della domanda:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_subtitle_prompt' AND LanguageCode = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'faq_subtitle_prompt', N'Question text:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_subtitle_prompt' AND LanguageCode = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'faq_subtitle_prompt', N'Textul întrebării:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_subtitle_prompt' AND LanguageCode = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'faq_subtitle_prompt', N'Fragetext:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_subtitle_prompt' AND LanguageCode = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'faq_subtitle_prompt', N'Frågetext:');

-- faq_select_subtitle
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_select_subtitle' AND LanguageCode = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'faq_select_subtitle', N'Seleziona una domanda');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_select_subtitle' AND LanguageCode = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'faq_select_subtitle', N'Select a question');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_select_subtitle' AND LanguageCode = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'faq_select_subtitle', N'Selectați o întrebare');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_select_subtitle' AND LanguageCode = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'faq_select_subtitle', N'Bitte eine Frage auswählen');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_select_subtitle' AND LanguageCode = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'faq_select_subtitle', N'Välj en fråga');

-- faq_archive_subtitle_confirm
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_archive_subtitle_confirm' AND LanguageCode = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'faq_archive_subtitle_confirm', N'Archiviare questa domanda e tutte le sue risposte?');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_archive_subtitle_confirm' AND LanguageCode = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'faq_archive_subtitle_confirm', N'Archive this question and all its answers?');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_archive_subtitle_confirm' AND LanguageCode = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'faq_archive_subtitle_confirm', N'Arhivați această întrebare și toate răspunsurile sale?');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_archive_subtitle_confirm' AND LanguageCode = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'faq_archive_subtitle_confirm', N'Diese Frage und alle zugehörigen Antworten archivieren?');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_archive_subtitle_confirm' AND LanguageCode = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'faq_archive_subtitle_confirm', N'Arkivera denna fråga och alla dess svar?');

-- ── Risposte CRUD ────────────────────────────────────────────

-- faq_question_label
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_question_label' AND LanguageCode = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'faq_question_label', N'Domanda:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_question_label' AND LanguageCode = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'faq_question_label', N'Question:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_question_label' AND LanguageCode = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'faq_question_label', N'Întrebare:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_question_label' AND LanguageCode = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'faq_question_label', N'Frage:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_question_label' AND LanguageCode = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'faq_question_label', N'Fråga:');

-- faq_add_answer
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_add_answer' AND LanguageCode = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'faq_add_answer', N'Nuova Risposta');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_add_answer' AND LanguageCode = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'faq_add_answer', N'New Answer');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_add_answer' AND LanguageCode = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'faq_add_answer', N'Răspuns nou');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_add_answer' AND LanguageCode = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'faq_add_answer', N'Neue Antwort');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_add_answer' AND LanguageCode = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'faq_add_answer', N'Nytt svar');

-- faq_edit_answer
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_edit_answer' AND LanguageCode = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'faq_edit_answer', N'Modifica Risposta');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_edit_answer' AND LanguageCode = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'faq_edit_answer', N'Edit Answer');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_edit_answer' AND LanguageCode = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'faq_edit_answer', N'Modifică Răspuns');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_edit_answer' AND LanguageCode = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'faq_edit_answer', N'Antwort bearbeiten');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_edit_answer' AND LanguageCode = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'faq_edit_answer', N'Redigera svar');

-- faq_answer_prompt
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_answer_prompt' AND LanguageCode = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'faq_answer_prompt', N'Testo della risposta:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_answer_prompt' AND LanguageCode = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'faq_answer_prompt', N'Answer text:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_answer_prompt' AND LanguageCode = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'faq_answer_prompt', N'Textul răspunsului:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_answer_prompt' AND LanguageCode = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'faq_answer_prompt', N'Antworttext:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_answer_prompt' AND LanguageCode = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'faq_answer_prompt', N'Svartext:');

-- faq_select_answer
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_select_answer' AND LanguageCode = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'faq_select_answer', N'Seleziona una risposta');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_select_answer' AND LanguageCode = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'faq_select_answer', N'Select an answer');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_select_answer' AND LanguageCode = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'faq_select_answer', N'Selectați un răspuns');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_select_answer' AND LanguageCode = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'faq_select_answer', N'Bitte eine Antwort auswählen');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_select_answer' AND LanguageCode = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'faq_select_answer', N'Välj ett svar');

-- faq_archive_answer_confirm
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_archive_answer_confirm' AND LanguageCode = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'faq_archive_answer_confirm', N'Archiviare questa risposta?');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_archive_answer_confirm' AND LanguageCode = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'faq_archive_answer_confirm', N'Archive this answer?');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_archive_answer_confirm' AND LanguageCode = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'faq_archive_answer_confirm', N'Arhivați acest răspuns?');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_archive_answer_confirm' AND LanguageCode = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'faq_archive_answer_confirm', N'Diese Antwort archivieren?');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'faq_archive_answer_confirm' AND LanguageCode = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'faq_archive_answer_confirm', N'Arkivera detta svar?');
