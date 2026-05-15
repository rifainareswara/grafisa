from .database import SessionLocal
from .models import Product


def seed_products():
    db = SessionLocal()
    if db.query(Product).count() > 0:
        db.close()
        return

    products = [
        Product(
            name="Starter Kit Jualan IG",
            description="Capek bikin desain tiap hari tapi hasil jualan belum maksimal? Starter Kit Jualan IG hadir template siap edit di Canva yang dirancang khusus untuk meningkatkan engagement dan penjualan. Cukup ganti teks, foto produk, dan harga—konten langsung siap posting dalam hitungan menit.",
            target="UMKM pemula, online shop Instagram, reseller & dropshipper",
            price=39000,
            canva_link="https://link.tiroe.io/canva-product",
            category="Template Produk",
            image_url=None,
        ),
        Product(
            name="Template Promo & Diskon",
            description="Template ini dirancang khusus untuk meningkatkan daya tarik promo seperti flash sale, diskon, dan bundling. Dengan struktur desain yang fokus pada urgency dan call-to-action, konten kamu akan lebih menarik dan mendorong pembeli untuk segera transaksi.",
            target="Online shop aktif, UMKM, affiliate seller",
            price=29000,
            canva_link="https://link.tiroe.io/canva-promo",
            category="Template Diskon",
            image_url=None,
        ),
        Product(
            name="Template Katalog & Menu Digital",
            description="Template ini memudahkan kamu menampilkan produk, harga, dan informasi penting dalam satu tampilan yang menarik dan profesional.",
            target="Bisnis kuliner, fashion, jasa, dan UMKM",
            price=35000,
            canva_link="https://link.tiroe.io/canva-menu",
            category="Template Katalog",
            image_url=None,
        ),
        Product(
            name="Template Slide Edukasi",
            description="Template carousel ini membantu kamu membuat konten edukatif yang tetap mengarah ke penjualan dengan alur yang jelas dan estetik.",
            target="Personal branding, edukator, UMKM, content creator",
            price=45000,
            canva_link="https://link.tiroe.io/canva-edukasi",
            category="Template Edukasi",
            image_url=None,
        ),
    ]

    db.add_all(products)
    db.commit()
    db.close()
    print("✅ Seed data berhasil ditambahkan")
