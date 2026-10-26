# Run once to seed the RAG index with ICAR crop advisories
ADVISORIES = [
    ("wheat_rust", "गेहूं में रस्ट रोग: पत्तियों पर नारंगी या भूरे धब्बे दिखें तो प्रोपिकोनाज़ोल 25% EC का 0.1% घोल छिड़कें। रोग फैलने से पहले उपचार करें।"),
    ("wheat_yellow", "गेहूं में पीली पत्तियां: नाइट्रोजन की कमी से होती है। यूरिया 50 किग्रा/हेक्टेयर टॉप ड्रेसिंग करें।"),
    ("rice_blast", "धान में ब्लास्ट रोग: ट्राइसाइक्लाज़ोल 75WP 0.6 ग्राम/लीटर पानी में मिलाकर छिड़काव करें।"),
    ("cotton_bollworm", "कपास में बॉलवर्म: क्लोरपाइरीफॉस 2.5 मिली/लीटर का छिड़काव करें। जैविक नियंत्रण के लिए NPV वायरस का उपयोग करें।"),
    ("soybean_aphid", "सोयाबीन में माहू कीट: इमिडाक्लोप्रिड 0.5 मिली/लीटर का छिड़काव करें। प्राकृतिक शत्रु लेडीबर्ड बीटल को नष्ट न करें।"),
    ("irrigation_wheat", "गेहूं की सिंचाई: बुवाई के 20-25 दिन बाद पहली सिंचाई करें। कुल 5-6 सिंचाई पर्याप्त हैं।"),
    ("fertilizer_rice", "धान में उर्वरक: नाइट्रोजन 120 किग्रा, फास्फोरस 60 किग्रा, पोटाश 60 किग्रा प्रति हेक्टेयर दें।"),
    ("maize_stalk_borer", "मक्का में तना छेदक: कार्बोफ्यूरान 3G दानेदार 20 किग्रा/हेक्टेयर पत्तियों के भंवर में डालें।"),
]

def seed_index():
    from server.rag import add_documents, collection
    if collection.count() > 0:
        return  # already seeded
    texts = [a[1] for a in ADVISORIES]
    ids = [a[0] for a in ADVISORIES]
    add_documents(texts, ids)
    print(f"[RAG] Seeded {len(ADVISORIES)} advisories")