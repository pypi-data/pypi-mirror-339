"""
PyPI'daki neuradoc paketinin sürümünü ve durumunu kontrol etmek için script.
Bu script doğrudan PyPI'ya sorgu yapar.
"""

import requests
import logging
import json
import tempfile
import os
from pathlib import Path
import sys

# Ana dizini import yoluna ekle
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Loglama ayarları
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_pypi_package():
    """PyPI'daki neuradoc paketini kontrol et"""
    logger.info("PyPI'daki neuradoc paketini kontrol ediyorum...")
    
    try:
        response = requests.get("https://pypi.org/pypi/neuradoc/json")
        response.raise_for_status()
        
        data = response.json()
        latest_version = data.get("info", {}).get("version", "bulunamadı")
        
        logger.info(f"neuradoc paketi PyPI'da bulundu!")
        logger.info(f"En son sürüm: {latest_version}")
        
        # Detaylı bilgiler
        pypi_info = data.get("info", {})
        
        logger.info(f"Paket adı: {pypi_info.get('name')}")
        logger.info(f"Özet: {pypi_info.get('summary')}")
        logger.info(f"Yazar: {pypi_info.get('author')}")
        logger.info(f"Email: {pypi_info.get('author_email')}")
        logger.info(f"Proje URL: {pypi_info.get('project_url')}")
        logger.info(f"Lisans: {pypi_info.get('license')}")
        
        # Sürümleri listele
        releases = data.get("releases", {})
        for version, release_info in releases.items():
            logger.info(f"Sürüm {version} yayınlanma tarihi: {release_info[0].get('upload_time') if release_info else 'bilinmiyor'}")
        
        # Yerel sürümü kullanarak test et
        logger.info("\nYerel kütüphaneyi kullanarak temel işlevselliği test ediyorum...")
        test_local_functionality()
        
        return True
    
    except requests.exceptions.RequestException as e:
        logger.error(f"PyPI sorgu hatası: {e}")
        return False
    
    except Exception as e:
        logger.error(f"Genel hata: {e}")
        return False

def test_local_functionality():
    """Yerel kütüphaneyi kullanarak temel işlevselliği test et"""
    try:
        import neuradoc
        from neuradoc.models.element import ElementType
        
        # Test belge içeriği
        test_content = """
        # Test Belgesi
        
        Bu, neuradoc kütüphanesinin işlevselliğini test etmek için oluşturulmuş basit bir belgedir.
        
        ## İkinci Seviye Başlık
        
        - Liste öğesi 1
        - Liste öğesi 2
        - Liste öğesi 3
        
        ### Kod Bloğu
        
        ```python
        def test_function():
            return "Hello, world!"
        ```
        
        Bu test belgesinin sonu.
        """
        
        # Geçici dosya oluştur
        fd, temp_path = tempfile.mkstemp(suffix='.md')
        try:
            with os.fdopen(fd, 'w') as temp_file:
                temp_file.write(test_content)
            
            logger.info(f"Geçici test dosyası oluşturuldu: {temp_path}")
            
            # Belgeyi yükle
            doc = neuradoc.load_document(temp_path)
            logger.info(f"Belge yüklendi: {doc}")
            
            # Metin çıkar
            text = doc.get_text_content()
            logger.info(f"Toplam metin uzunluğu: {len(text)} karakter")
            logger.info(f"İlk 50 karakter: {text[:50]}...")
            
            # Dönüştürücüyü test et
            from neuradoc.transformers.llm_transformer import LLMTransformer
            transformer = LLMTransformer()
            
            md_result = transformer.to_markdown(doc)
            logger.info(f"Markdown dönüşümü başarılı, uzunluk: {len(md_result)} karakter")
            
            json_result = transformer.to_json(doc)
            logger.info(f"JSON dönüşümü başarılı, uzunluk: {len(str(json_result))} karakter")
            
            logger.info("Temel işlevsellik testi BAŞARILI!")
            
        finally:
            # Geçici dosyayı temizle
            if os.path.exists(temp_path):
                os.remove(temp_path)
                logger.info(f"Geçici dosya silindi: {temp_path}")
    
    except Exception as e:
        logger.error(f"Yerel test hatası: {e}")

if __name__ == "__main__":
    check_pypi_package()