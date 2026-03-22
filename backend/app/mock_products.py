# Mock product data mapped to real product IDs from our dataset
MOCK_PRODUCTS = {
    "B005LJQPE0": {
        "name": "Sony WH-1000XM4 Wireless Headphones",
        "brand": "Sony",
        "category": "Headphones",
        "price": 299.99,
        "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400",
        "description": "Industry leading noise cancellation with 30hr battery life.",
        "rating": 4.95
    },
    "B0033PRWSW": {
        "name": "Logitech MX Master 3 Wireless Mouse",
        "brand": "Logitech",
        "category": "Computer Accessories",
        "price": 99.99,
        "image": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400",
        "description": "Advanced wireless mouse with ultra-fast scrolling.",
        "rating": 4.91
    },
    "B007SZ0E1K": {
        "name": "Apple AirPods Pro (2nd Generation)",
        "brand": "Apple",
        "category": "Earbuds",
        "price": 249.99,
        "image": "https://images.unsplash.com/photo-1600294037681-c80b4cb5b434?w=400",
        "description": "Active noise cancellation with adaptive transparency.",
        "rating": 4.88
    },
    "B003FVVMS0": {
        "name": "Samsung 970 EVO 1TB NVMe SSD",
        "brand": "Samsung",
        "category": "Storage",
        "price": 89.99,
        "image": "https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?w=400",
        "description": "High performance NVMe SSD with speeds up to 3500MB/s.",
        "rating": 4.87
    },
    "B00006I53W": {
        "name": "Anker 65W USB-C Charger",
        "brand": "Anker",
        "category": "Chargers",
        "price": 35.99,
        "image": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400",
        "description": "Fast charging for laptops, phones and tablets.",
        "rating": 4.94
    },
    "B004EBUXHQ": {
        "name": "Razer DeathAdder V2 Gaming Mouse",
        "brand": "Razer",
        "category": "Gaming",
        "price": 69.99,
        "image": "https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?w=400",
        "description": "20000 DPI optical sensor for precise gaming control.",
        "rating": 4.90
    },
    "B0029N3U8K": {
        "name": "Kingston 32GB USB 3.0 Flash Drive",
        "brand": "Kingston",
        "category": "Storage",
        "price": 12.99,
        "image": "https://images.unsplash.com/photo-1617802690992-15d93263d3a9?w=400",
        "description": "Compact and reliable USB flash drive for data transfer.",
        "rating": 4.87
    },
    "B00053HC5": {
        "name": "TP-Link WiFi 6 Router AX3000",
        "brand": "TP-Link",
        "category": "Networking",
        "price": 79.99,
        "image": "https://images.unsplash.com/photo-1606904825846-647eb07f5be2?w=400",
        "description": "Next gen WiFi 6 for faster speeds and more capacity.",
        "rating": 4.91
    },
    "B004FA8NOQ": {
        "name": "Corsair K95 RGB Mechanical Keyboard",
        "brand": "Corsair",
        "category": "Keyboards",
        "price": 159.99,
        "image": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=400",
        "description": "Cherry MX switches with per-key RGB lighting.",
        "rating": 4.90
    },
    "B001BTCSI6": {
        "name": "LG 27UK850-W 4K Monitor",
        "brand": "LG",
        "category": "Monitors",
        "price": 449.99,
        "image": "https://images.unsplash.com/photo-1527443224154-c4a573d81afd?w=400",
        "description": "27 inch 4K UHD IPS display with USB-C connectivity.",
        "rating": 4.90
    },
    "B0082E9K7U": {
        "name": "Bose QuietComfort 45 Headphones",
        "brand": "Bose",
        "category": "Headphones",
        "price": 329.99,
        "image": "https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=400",
        "description": "World class noise cancellation with premium sound.",
        "rating": 4.85
    },
    "B00HFFDDLG": {
        "name": "Elgato Stream Deck MK.2",
        "brand": "Elgato",
        "category": "Streaming",
        "price": 149.99,
        "image": "https://images.unsplash.com/photo-1593640408182-31c228b9b7b1?w=400",
        "description": "15 LCD keys to control streaming, recording and more.",
        "rating": 4.88
    },
    "B00CZDT30S": {
        "name": "WD 4TB External Hard Drive",
        "brand": "Western Digital",
        "category": "Storage",
        "price": 89.99,
        "image": "https://images.unsplash.com/photo-1531492746076-161ca9bcad58?w=400",
        "description": "Portable 4TB storage for backup and extra space.",
        "rating": 4.87
    },
    "B00G4UQ6U8": {
        "name": "Jabra Evolve2 85 Wireless Headset",
        "brand": "Jabra",
        "category": "Headsets",
        "price": 379.99,
        "image": "https://images.unsplash.com/photo-1484704849700-f032a568e944?w=400",
        "description": "Professional headset with advanced ANC for office use.",
        "rating": 4.86
    },
    "B00GMTN96U": {
        "name": "Crucial 16GB DDR4 RAM",
        "brand": "Crucial",
        "category": "Memory",
        "price": 44.99,
        "image": "https://images.unsplash.com/photo-1562976540-1502c2145851?w=400",
        "description": "High performance DDR4 memory for desktop computers.",
        "rating": 4.85
    },
    "B00E3FHXYO": {
        "name": "Belkin 12-Outlet Power Strip",
        "brand": "Belkin",
        "category": "Power",
        "price": 29.99,
        "image": "https://images.unsplash.com/photo-1586953208448-b95a79798f07?w=400",
        "description": "Surge protected 12-outlet power strip with 8ft cord.",
        "rating": 4.92
    },
    "B00FSA8VQ2": {
        "name": "Rode NT-USB Microphone",
        "brand": "Rode",
        "category": "Microphones",
        "price": 169.99,
        "image": "https://images.unsplash.com/photo-1598550880863-4e8aa3d0edb4?w=400",
        "description": "Studio quality USB microphone for recording and streaming.",
        "rating": 4.89
    },
    "B0088CJT4U": {
        "name": "Secretlab TITAN Evo Gaming Chair",
        "brand": "Secretlab",
        "category": "Furniture",
        "price": 519.99,
        "image": "https://images.unsplash.com/photo-1598300042247-d088f8ab3a91?w=400",
        "description": "Premium gaming chair with lumbar support and 4D armrests.",
        "rating": 4.91
    },
    "B00D4MFPLA": {
        "name": "Philips Hue Smart Bulb Starter Kit",
        "brand": "Philips",
        "category": "Smart Home",
        "price": 79.99,
        "image": "https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=400",
        "description": "Smart LED bulbs with 16 million colors and voice control.",
        "rating": 4.88
    },
    "B004CLYEE6": {
        "name": "GoPro HERO12 Black Action Camera",
        "brand": "GoPro",
        "category": "Cameras",
        "price": 399.99,
        "image": "https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=400",
        "description": "5.3K video with HyperSmooth 6.0 stabilization.",
        "rating": 4.87
    }
}

GENERIC_TEMPLATES = [
    {"name": "Wireless Bluetooth Speaker", "category": "Audio", "brand": "JBL",
     "image": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=400",
     "description": "Portable waterproof speaker with 12hr battery life."},
    {"name": "USB-C Hub 7-in-1", "category": "Accessories", "brand": "Anker",
     "image": "https://images.unsplash.com/photo-1625842268584-8f3296236761?w=400",
     "description": "Multiport hub with HDMI, USB 3.0 and SD card slots."},
    {"name": "Mechanical Gaming Keyboard", "category": "Keyboards", "brand": "HyperX",
     "image": "https://images.unsplash.com/photo-1541140532154-b024d705b90a?w=400",
     "description": "Compact TKL mechanical keyboard with RGB backlighting."},
    {"name": "4K Webcam Pro", "category": "Cameras", "brand": "Logitech",
     "image": "https://images.unsplash.com/photo-1587826080692-f439cd0b70da?w=400",
     "description": "Ultra HD webcam with built-in noise cancelling mic."},
    {"name": "Portable Power Bank 20000mAh", "category": "Power", "brand": "Anker",
     "image": "https://images.unsplash.com/photo-1609592424858-a685f3aa2c67?w=400",
     "description": "High capacity power bank with fast charging support."},
    {"name": "Smart LED Desk Lamp", "category": "Lighting", "brand": "BenQ",
     "image": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=400",
     "description": "Eye-care LED lamp with adjustable color temperature."},
    {"name": "Noise Cancelling Earbuds", "category": "Audio", "brand": "Samsung",
     "image": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=400",
     "description": "Premium earbuds with active noise cancellation."},
    {"name": "Laptop Stand Adjustable", "category": "Accessories", "brand": "Nexstand",
     "image": "https://images.unsplash.com/photo-1593642632559-0c6d3fc62b89?w=400",
     "description": "Portable aluminum laptop stand with 6 height levels."},
    {"name": "27inch Curved Gaming Monitor", "category": "Monitors", "brand": "Samsung",
     "image": "https://images.unsplash.com/photo-1527443224154-c4a573d81afd?w=400",
     "description": "165Hz curved display with 1ms response time."},
    {"name": "Smart Security Camera", "category": "Smart Home", "brand": "Arlo",
     "image": "https://images.unsplash.com/photo-1558002038-1055907df827?w=400",
     "description": "1080p indoor security camera with night vision."},
]

def get_product_details(product_id: str):
    """Get mock product details for a product ID"""
    if product_id in MOCK_PRODUCTS:
        return {"product_id": product_id, **MOCK_PRODUCTS[product_id]}
    # Use hash to consistently pick different template per product
    template = GENERIC_TEMPLATES[abs(hash(product_id)) % len(GENERIC_TEMPLATES)].copy()
    template['price']  = round(19.99 + (abs(hash(product_id)) % 300), 2)
    template['rating'] = round(3.5 + (abs(hash(product_id)) % 15) / 10, 1)
    return {"product_id": product_id, **template}

def enrich_recommendations(recommendations: list):
    """Add product details to recommendation results"""
    enriched = []
    for rec in recommendations:
        product = get_product_details(rec['product_id'])
        enriched.append({**rec, **product})
    return enriched