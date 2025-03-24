import requests  # GitHub sayfalarını çekmek için
from bs4 import BeautifulSoup  # HTML parsing için
import pandas as pd  # Veri işleme
import time  # İstekler arasında gecikme
import os  # Dosya işlemleri


def get_followers_following(username):
    """
    GitHub kullanıcı takipçileri ve takip edilenleri web sayfalarından çeker

    Args:
        username (str): GitHub kullanıcı adı

    Returns:
        tuple: (takipçiler listesi, takip edilenler listesi)
    """
    followers = []
    following = []

    # Headers eklenerek browser gibi davranıyoruz
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Takipçileri çek
    print(f"{username} için takipçiler çekiliyor...")
    page = 1
    while True:
        followers_url = f"https://github.com/{username}?tab=followers&page={page}"
        response = requests.get(followers_url, headers=headers)

        if response.status_code != 200:
            print(f"Hata: Takipçiler sayfası alınamadı. Durum kodu: {response.status_code}")
            break

        soup = BeautifulSoup(response.text, 'html.parser')

        # Kullanıcı element listesini bul
        user_elements = soup.select(
            'turbo-frame[id^="user-profile-frame"] div.position-relative div.d-table div.d-table-cell span.Link--secondary')

        # Eğer hiç kullanıcı bulunamazsa bir sonraki sayfaya geç
        if not user_elements:
            # Sayfa sonuna ulaşıldı mı kontrol et
            pagination = soup.select('.pagination')
            if not pagination or 'disabled' in pagination[0].select('a')[-1].get('class', []):
                break

        # Kullanıcı adlarını listeye ekle
        for element in user_elements:
            username_text = element.text.strip()
            if username_text:
                followers.append(username_text)

        # Next page
        page += 1
        print(f"Takipçiler: Sayfa {page - 1} tamamlandı. Şu ana kadar {len(followers)} takipçi bulundu.")

        # Rate limiting (GitHub'un sizi engellemesini önlemek için)
        time.sleep(1)

    # Takip edilenleri çek
    print(f"\n{username} için takip edilenler çekiliyor...")
    page = 1
    while True:
        following_url = f"https://github.com/{username}?tab=following&page={page}"
        response = requests.get(following_url, headers=headers)

        if response.status_code != 200:
            print(f"Hata: Takip edilenler sayfası alınamadı. Durum kodu: {response.status_code}")
            break

        soup = BeautifulSoup(response.text, 'html.parser')

        # Kullanıcı element listesini bul
        user_elements = soup.select(
            'turbo-frame[id^="user-profile-frame"] div.position-relative div.d-table div.d-table-cell span.Link--secondary')

        # Eğer hiç kullanıcı bulunamazsa bir sonraki sayfaya geç
        if not user_elements:
            # Sayfa sonuna ulaşıldı mı kontrol et
            pagination = soup.select('.pagination')
            if not pagination or 'disabled' in pagination[0].select('a')[-1].get('class', []):
                break

        # Kullanıcı adlarını listeye ekle
        for element in user_elements:
            username_text = element.text.strip()
            if username_text:
                following.append(username_text)

        # Next page
        page += 1
        print(f"Takip edilenler: Sayfa {page - 1} tamamlandı. Şu ana kadar {len(following)} takip edilen bulundu.")

        # Rate limiting
        time.sleep(1)

    return followers, following


def analyze_relationships(followers, following):
    """
    Takipçiler ve takip edilenler arasındaki ilişkileri analiz eder

    Args:
        followers (list): Takipçiler listesi
        following (list): Takip edilenler listesi

    Returns:
        tuple: (karşılıklı takipleşenler, takip etmeyenler, takip etmedikleriniz)
    """
    # Karşılıklı takipleşenler
    mutual = [user for user in followers if user in following]

    # Sizi takip etmeyenler (takip ettiğiniz ama sizi takip etmeyenler)
    not_following_back = [user for user in following if user not in followers]

    # Sizin takip etmedikleriniz (sizi takip eden ama sizin takip etmediğiniz)
    not_following = [user for user in followers if user not in following]

    return mutual, not_following_back, not_following


def display_results(username, followers, following, mutual, not_following_back, not_following):
    """
    Sonuçları konsola yazdırır

    Args:
        username (str): GitHub kullanıcı adı
        followers (list): Takipçiler listesi
        following (list): Takip edilenler listesi
        mutual (list): Karşılıklı takipleşenler listesi
        not_following_back (list): Takip etmeyenler listesi
        not_following (list): Takip etmedikleriniz listesi
    """
    # Listeleri alfabetik olarak sırala
    followers.sort()
    following.sort()
    mutual.sort()
    not_following_back.sort()
    not_following.sort()

    print("\n" + "=" * 50)
    print(f"GitHub Kullanıcı Analizi: {username}")
    print("=" * 50)

    print(f"\nÖZET:")
    print(f"- Takipçi sayısı: {len(followers)}")
    print(f"- Takip edilen sayısı: {len(following)}")
    print(f"- Karşılıklı takipleşme sayısı: {len(mutual)}")
    print(f"- Sizi takip etmeyen sayısı: {len(not_following_back)}")
    print(f"- Sizin takip etmediğiniz sayısı: {len(not_following)}")

    # Kullanıcı tercihine göre liste göster
    lists_to_show = {
        "Takipçileriniz": followers,
        "Takip ettikleriniz": following,
        "Karşılıklı takipleşenler": mutual,
        "Sizi takip etmeyenler (takip ettiğiniz ama sizi takip etmeyenler)": not_following_back,
        "Sizin takip etmedikleriniz (sizi takip eden ama sizin takip etmediğiniz)": not_following
    }

    for title, user_list in lists_to_show.items():
        if user_list:
            show_list = input(f"\n{title} listesini görmek istiyor musunuz? ({len(user_list)} kişi) (e/h): ")
            if show_list.lower() == 'e':
                print(f"\n{title} ({len(user_list)} kişi):")
                for i, user in enumerate(user_list, 1):
                    print(f"{i}. {user}")


def save_to_csv(username, followers, following, mutual, not_following_back, not_following):
    """
    Sonuçları CSV dosyalarına kaydeder

    Args:
        username (str): GitHub kullanıcı adı
        followers (list): Takipçiler listesi
        following (list): Takip edilenler listesi
        mutual (list): Karşılıklı takipleşenler listesi
        not_following_back (list): Takip etmeyenler listesi
        not_following (list): Takip etmedikleriniz listesi
    """
    data = {
        "takipciler": followers,
        "takip_edilenler": following,
        "karsilikli": mutual,
        "takip_etmeyenler": not_following_back,
        "takip_etmedikleriniz": not_following
    }

    output_dir = f"{username}_github_analizi"

    # Klasör oluştur
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Her listeyi CSV olarak kaydet
    for name, user_list in data.items():
        if user_list:
            df = pd.DataFrame(user_list, columns=["username"])
            filepath = os.path.join(output_dir, f"{name}.csv")
            df.to_csv(filepath, index=False)
            print(f"{filepath} dosyasına kaydedildi.")

    # Tüm verileri tek bir Excel dosyasında sakla
    excel_path = os.path.join(output_dir, f"{username}_tum_veriler.xlsx")
    with pd.ExcelWriter(excel_path) as writer:
        for name, user_list in data.items():
            if user_list:
                df = pd.DataFrame(user_list, columns=["username"])
                df.to_excel(writer, sheet_name=name, index=False)

    print(f"\nTüm veriler {excel_path} dosyasına kaydedildi.")


def main():
    print("GitHub Follower Analyzer")
    print("=" * 50)
    print("Takipçi ve takip ilişkilerini analiz edelim")

    username = input("GitHub kullanıcı adınızı girin: ")

    # Web scraping ile verileri al
    followers, following = get_followers_following(username)

    if not followers and not following:
        print("Hiç veri alınamadı. Lütfen kullanıcı adınızı kontrol edin.")
        return

    # İlişkileri analiz et
    mutual, not_following_back, not_following = analyze_relationships(followers, following)

    # Sonuçları göster
    display_results(username, followers, following, mutual, not_following_back, not_following)

    # CSV olarak kaydet
    save_option = input("\nSonuçları CSV dosyalarına kaydetmek istiyor musunuz? (e/h): ")
    if save_option.lower() == 'e':
        save_to_csv(username, followers, following, mutual, not_following_back, not_following)

    print("\nAnaliz tamamlandı! Sonuçlar başarıyla gösterildi.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram kullanıcı tarafından durduruldu.")
    except Exception as e:
        print(f"\n\nHata oluştu: {e}")
        print("GitHub sayfasının yapısı değişmiş olabilir veya bağlantı sorunu yaşanıyor olabilir.")