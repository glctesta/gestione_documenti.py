# Manual de utilizare — Modulul Oaspeți
## TraceabilityRS — Secțiunea „Operații → Personal → Oaspeți"

---

## Cuprins
1. [Accesul la secțiunea Oaspeți](#1-accesul)
2. [Înregistrare Oaspeți](#2-înregistrare)
3. [Booking — Zbor, Navetă, Hotel](#3-booking)
4. [Gestionare Oaspeți](#4-gestionare)
5. [Settings — Hoteluri](#5-hoteluri)
6. [Settings — Navetă (Shuttle)](#6-navetă)
7. [Settings — Companii Aeriene](#7-companii-aeriene)

---

## 1. Accesul la secțiunea Oaspeți {#1-accesul}

Din meniul principal al aplicației: **Operații → Personal → Oaspeți**

Toate funcționalitățile necesită **autentificare**. La prima accesare vi se va solicita cheia de acces. Odată autentificat, accesul rămâne activ pe parcursul sesiunii.

Sub-meniuri disponibile:
- **Înregistrare Oaspeți** — înregistrarea vizitatorilor
- **Settings → Hoteluri** — gestiunea hotelurilor partenere
- **Settings → Companii Aeriene** — gestiunea companiilor aeriene
- **Settings → Navetă** — gestiunea serviciilor de transport
- **Settings → Gestionare Oaspeți** — monitorizarea rezervărilor și editarea datelor oaspeților

---

## 2. Înregistrare Oaspeți {#2-înregistrare}

![Formularul de înregistrare oaspeți](C:/Users/gtesta/.gemini/antigravity/brain/e202379d-e0d8-4324-91a2-a077cb0caec6/guest_registration_form_1772901651186.png)

### Descriere
Această fereastră permite înregistrarea vizitatorilor care urmează să vină la fabrică.

### Câmpuri
| Câmp | Descriere |
|------|-----------|
| **Societate** | Selectați sau introduceți firma oaspetelui. Dacă firma nu există, va fi creată automat. |
| **Oaspete** | Selectați sau introduceți numele oaspetelui. |
| **Email** | Adresa de email a oaspetelui (opțional, dar necesară pentru confirmări). |
| **Sponsor** | Persoana din fabrică responsabilă de vizită. |
| **Data început** | Data sosirii oaspetelui. |
| **Data sfârșit** | Data plecării oaspetelui. |

### Pași de utilizare
1. Selectați sau introduceți **societatea** și **oaspetele**
2. Completați **email-ul** (important pentru primirea confirmărilor de booking)
3. Selectați **datele de vizită**
4. Apăsați **„Adaugă"** pentru a adăuga oaspetele în lista sesiunii
5. Repetați pentru alți oaspeți
6. La **închiderea ferestrei**, se va deschide automat formularul de Booking

> **⚠ Important:** Email-ul oaspetelui este folosit pentru a-i trimite o confirmare de rezervare în limba engleză. Asigurați-vă că adresa este corectă.

---

## 3. Booking — Zbor, Navetă, Hotel {#3-booking}

![Formularul de booking](C:/Users/gtesta/.gemini/antigravity/brain/e202379d-e0d8-4324-91a2-a077cb0caec6/guest_booking_form_1772901667793.png)

### Descriere
Această fereastră se deschide automat după înregistrarea oaspeților și permite configurarea serviciilor de transport și cazare.

### Tab-ul ✈ Zbor
| Câmp | Descriere |
|------|-----------|
| **Companie aeriană** | Selectați din lista existentă sau adăugați una nouă |
| **Număr zbor** | Numărul zborului (ex: LH1234) |
| **Data sosire** | Data aterizării |
| **Ora sosire** | Ora estimată de sosire (format HH:MM) |
| **Data plecare** | Data de plecare |

### Tab-ul 🚐 Navetă
- Selectați serviciul de **navetă/transport** din lista disponibilă
- Bifați **„Nu solicita serviciul de navetă"** dacă nu este necesar transportul

### Tab-ul 🏨 Hotel
- Selectați **hotelul** din lista disponibilă
- Bifați **„Nu solicita serviciul de hotel"** dacă nu este necesară cazarea

### Ce se întâmplă la apăsarea „Trimite Booking"
1. Se creează o înregistrare în baza de date cu detaliile sosirii
2. Se trimite **email de rezervare la navetă** (în limba română) cu:
   - Datele oaspeților, zborul, ora de sosire
   - Regula de ora 16:00 (dacă aplicabil)
   - Logo-ul companiei
3. Se trimite **email de rezervare la hotel** (în limba română) cu:
   - Datele oaspeților, datele de cazare
   - Datele companiei gazdă
   - Logo-ul companiei
4. Se trimite **email de confirmare fiecărui oaspete** (în limba engleză) cu:
   - Detalii despre serviciul rezervat
   - Datele de sosire/plecare
   - Contact-ul persoanei responsabile (CC)
5. Toate emailurile sunt **salvate în baza de date** cu status „Neconfirmat"

> **⚠ Important:** Emailul de confirmare este trimis doar oaspeților care au o adresă de email înregistrată.

---

## 4. Gestionare Oaspeți {#4-gestionare}

![Formularul de gestionare oaspeți](C:/Users/gtesta/.gemini/antigravity/brain/e202379d-e0d8-4324-91a2-a077cb0caec6/guest_management_form_1772901683961.png)

### Descriere
Această fereastră permite monitorizarea rezervărilor și editarea datelor de contact ale oaspeților.

### Tab-ul 📋 Rezervări

Afișează toate rezervările trimise, cu următoarele coloane:

| Coloană | Descriere |
|---------|-----------|
| **ID** | Identificatorul unic al rezervării |
| **Zbor** | Compania aeriană și numărul zborului |
| **Data Sosire** | Data și ora sosirii |
| **Data Plecare** | Data plecării |
| **Email Serviciu** | Adresa email la care a fost trimisă rezervarea |
| **Trimis** | Data și ora trimiterii emailului |
| **Confirmat** | ✅ = confirmat, ❌ = neconfirmat |

#### Funcționalități
- **📧 Retrimite email** — retrimite emailul de rezervare cu un mesaj de reiterare (RO + EN). Actualizează data trimiterii.
- **✅ Marchează confirmat** — setează rezervarea ca confirmată în baza de date
- **Arată și confirmate** — bifați pentru a vedea și rezervările deja confirmate
- **🔄 Aggiorna** — reîncarcă lista din baza de date

### Tab-ul 👤 Date Oaspeți

Permite editarea datelor de contact ale oaspeților:

| Câmp | Descriere |
|------|-----------|
| **Filtrare după companie** | Selectați o companie pentru a filtra lista |
| **Mostra Tutti** | Afișează toți oaspeții fără filtrare |
| **Email** | Editați adresa de email a oaspetelui |
| **Telefon** | Editați numărul de telefon al oaspetelui |
| **💾 Salva** | Salvează modificările în baza de date |

---

## 5. Settings — Hoteluri {#5-hoteluri}

![Formularul de gestiune hoteluri](C:/Users/gtesta/.gemini/antigravity/brain/e202379d-e0d8-4324-91a2-a077cb0caec6/hotel_settings_form_1772901699572.png)

### Descriere
Gestionarea hotelurilor partenere utilizate pentru cazarea oaspeților.

### Câmpuri
| Câmp | Descriere |
|------|-----------|
| **Nume** | Numele hotelului |
| **Email** | Adresa de email pentru rezervări |
| **Oraș** | Orașul în care se află hotelul (selectat din lista disponibilă) |

### Acțiuni disponibile
- **➕ Nou** — pregătește formularul pentru adăugarea unui hotel nou
- **💾 Salvează** — salvează hotelul (creare nouă sau actualizare)
- **🚫 Dezactivează** — dezactivează hotelul (nu va mai apărea în liste, dar rămâne în istoric)
- **Închide** — închide fereastra

> **Notă:** Dezactivarea unui hotel nu îl șterge din baza de date, ci setează o dată de ieșire. Astfel, istoricul rezervărilor rămâne intact.

---

## 6. Settings — Navetă (Shuttle) {#6-navetă}

### Descriere
Gestionarea serviciilor de transport/navetă. Interfața este **identică** cu cea de la Hoteluri.

### Câmpuri
| Câmp | Descriere |
|------|-----------|
| **Nume** | Numele serviciului de transport |
| **Email** | Adresa de email pentru solicitarea transportului |
| **Oraș** | Orașul de operare |

### Acțiuni
- **➕ Nou** — adaugă un nou serviciu de transport
- **💾 Salvează** — salvează modificările
- **🚫 Dezactivează** — dezactivează serviciul
- **Închide** — închide fereastra

---

## 7. Settings — Companii Aeriene {#7-companii-aeriene}

### Descriere
Gestionarea companiilor aeriene disponibile pentru selecție în formularul de booking.

### Câmpuri
| Câmp | Descriere |
|------|-----------|
| **Companie** | Numele complet al companiei aeriene (ex: Lufthansa) |
| **Cod IATA** | Codul IATA al companiei (ex: LH) — utilizat pentru căutarea zborurilor |

### Acțiuni
- **➕ Nou** — adaugă o companie nouă
- **💾 Salvează** — salvează modificările
- **🗑 Șterge** — elimină compania din bază de date
- **Închide** — închide fereastra

> **⚠ Atenție:** Ștergerea unei companii aeriene este permanentă. Asigurați-vă că nu există rezervări active asociate înainte de ștergere.

---

## Fluxul complet de lucru

```
1. Înregistrare Oaspeți
   ↓ (la închidere)
2. Booking — selectare zbor, navetă, hotel
   ↓ (la trimitere)
3. Email automat → furnizor navetă (RO)
   Email automat → hotel (RO)
   Email confirmare → oaspete (EN)
   ↓
4. Salvare în baza de date (status: Neconfirmat)
   ↓
5. Gestionare Oaspeți → monitorizare confirmare
   → retrimite dacă neconfirmat
   → marchează confirmat la primirea confirmării
```

---

*Manual generat de TraceabilityRS — Versiunea 2.3.2.35*
