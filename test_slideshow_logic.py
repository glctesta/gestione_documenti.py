import os
import sys
from datetime import datetime, date

# Mock environment
class MockLang:
    def __init__(self): self.current_language = 'it'

class MockDB:
    def __init__(self):
        self.settings = {
            'SlideshowFolderPath': 'T:\\Traceability_RESET_Services\\Pict\\SlideShows\\',
            'SlideshowIntervalMinutes': '1',
            'Sys_natale': 'natale1.jpg;natale2.jpg',
            'Sys_natale_prealler': '7',
            'Sys_natale_postallert': '2',
            'Sys_HappyNewYear': 'HappyNewYear2026.jpg',
            'Sys_HappyNewYear_Preallert': '3',
            'Sys_HappyNewYear_PostAllert': '10',
            'Sys_pasqua': 'pasqua1.jpg',
            'Sys_HappyEastern': 'BuonaPasqua.jpg',
            'Sys_HappyEastern_Preallert': '3',
            'Sys_HappyEasterh_PostAllert': '5',
            'Sys_eastern_data': 'SELECT SarbatoareDate FROM Sarbatorilor WHERE Religion=? AND TipSarbatoare=?'
        }
    def fetch_setting(self, key): return self.settings.get(key)
    class MockCursor:
        def execute(self, q, p): pass
        def fetchone(self): return [date(2025, 4, 20)] # Catholic Easter 2025
    @property
    def cursor(self): return self.MockCursor()

# Simulate the logic
def test_slideshow_logic():
    db = MockDB()
    lang = MockLang()
    current_date = date(2025, 12, 18) # Simulation of TODAY
    
    def get_int(key):
        val = db.fetch_setting(key)
        try: return int(val)
        except: return 0
    def get_list(key):
        val = db.fetch_setting(key)
        if not val: return []
        return [x.strip() for x in val.split(';') if x.strip()]

    special_images_to_add = []
    special_images_set = set()
    all_images = ['natale1.jpg', 'natale2.jpg', 'happy.jpg', 'normal1.jpg', 'normal2.jpg', 'pasqua1.jpg', 'BuonaPasqua.jpg', 'HappyNewYear2026.jpg', 'nuovoanno1.jpg']

    # 1. Christmas
    christmas_imgs = get_list('Sys_natale')
    if christmas_imgs:
        for img in christmas_imgs: special_images_set.add(img)
        christmas_pre = get_int('Sys_natale_preallert') or get_int('Sys_natale_prealler')
        christmas_post = get_int('Sys_natale_postallert')
        c_date = date(current_date.year, 12, 25)
        delta = (current_date - c_date).days
        print(f"Christmas Delta: {delta}, Pre: {christmas_pre}")
        if -christmas_pre <= delta <= christmas_post: 
            print("Christmas ACTIVE")
            special_images_to_add.extend(christmas_imgs)

    # 2. New Year
    ny_imgs = get_list('Sys_HappyNewYear')
    if ny_imgs:
        for img in ny_imgs: special_images_set.add(img)
        for extra_ny in get_list('Sys_nuovoanno'): special_images_set.add(extra_ny)
        ny_pre = get_int('Sys_HappyNewYear_Preallert')
        ny_post = get_int('Sys_HappyNewYear_PostAllert')
        ny_date_curr = date(current_date.year, 1, 1)
        delta_curr = (current_date - ny_date_curr).days
        ny_date_next = date(current_date.year + 1, 1, 1)
        delta_next = (current_date - ny_date_next).days
        if (-ny_pre <= delta_curr <= ny_post) or (-ny_pre <= delta_next <= ny_post):
            print("New Year ACTIVE")
            special_images_to_add.extend(ny_imgs)

    # 3. Easter
    easter_imgs = get_list('Sys_pasqua') + get_list('Sys_HappyEastern')
    if easter_imgs:
        for img in easter_imgs: special_images_set.add(img)
        easter_date = date(2025, 4, 20) # Mocked from DB
        easter_pre = get_int('Sys_HappyEastern_Preallert')
        easter_post = get_int('Sys_HappyEasterh_PostAllert')
        delta = (current_date - easter_date).days
        print(f"Easter Delta: {delta}")
        if -easter_pre <= delta <= easter_post:
            print("Easter ACTIVE")
            special_images_to_add.extend(easter_imgs)

    # Construct final list
    image_files = []
    if special_images_to_add:
        print(f"Showing ONLY special images ({len(special_images_to_add)} types)")
        for _ in range(1): # simplified for print
            for img in special_images_to_add:
                if img in all_images:
                    image_files.append(img)
    else:
        print("Showing normal images")
        for img in all_images:
            if img not in special_images_set:
                image_files.append(img)
    
    print(f"Final SlideShow List: {image_files}")

if __name__ == "__main__":
    test_slideshow_logic()
