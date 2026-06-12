from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ── KNOWLEDGE BASE ──────────────────────────────────────────

SYMPTOMS = {
    "G001": {
        "code": "G001",
        "label": "Kendali Kekuatan Luar",
        "description": "Merasa pikiran/tubuh dikendalikan kekuatan luar",
        "detail": "Sensasi bahwa pikiran atau gerakan tubuh berasal dari entitas atau kekuatan di luar diri sendiri."
    },
    "G002": {
        "code": "G002",
        "label": "Kehilangan Kontrol Motorik",
        "description": "Kehilangan kontrol motorik secara mendadak (tubuh bergerak otomatis)",
        "detail": "Tubuh melakukan gerakan tanpa instruksi sadar — tangan gemetar, kaki bergerak sendiri, atau postur berubah tanpa kehendak."
    },
    "G003": {
        "code": "G003",
        "label": "Amnesia Sesaat",
        "description": "Mengalami amnesia sesaat / lupa kejadian yang baru berlangsung",
        "detail": "Tidak dapat mengingat sebagian atau seluruh kejadian dalam rentang waktu tertentu yang baru saja berlangsung."
    },
    "G004": {
        "code": "G004",
        "label": "Perubahan Nada Suara",
        "description": "Perubahan nada suara atau gaya bicara yang bukan dirinya",
        "detail": "Suara terdengar berbeda — lebih berat, lebih tinggi, atau dengan logat/aksen yang tidak biasa digunakan."
    },
    "G005": {
        "code": "G005",
        "label": "Gerakan Repetitif Otomatis",
        "description": "Melakukan gerakan otomatis yang repetitif (meniru gerakan silat/tarian)",
        "detail": "Gerakan berulang yang terstruktur seperti pola tarian, gerakan bela diri, atau ritual tertentu tanpa kesadaran penuh."
    },
    "G006": {
        "code": "G006",
        "label": "Derealisasi",
        "description": "Merasa lingkungan sekitar menjadi tidak nyata (Derealization)",
        "detail": "Persepsi bahwa dunia di sekitar terasa seperti mimpi, kabur, jauh, atau tidak nyata secara visual dan emosional."
    },
    "G007": {
        "code": "G007",
        "label": "Depersonalisasi",
        "description": "Merasa terasing dari tubuh sendiri (Depersonalization)",
        "detail": "Perasaan mengamati diri sendiri dari luar, seolah menjadi penonton bagi tubuh dan pikiran sendiri."
    },
    "G008": {
        "code": "G008",
        "label": "Bahasa Tak Dikenal",
        "description": "Meracau atau berbicara dalam bahasa yang tidak dipahami dalam kondisi normal",
        "detail": "Mengeluarkan ucapan, bahasa, atau suara yang tidak dikenali atau tidak dapat dipahami saat kondisi sadar normal."
    },
}

RULES = [
    {
        "id": "R001",
        "conditions": ["G001", "G002", "G003", "G004", "G005"],
        "diagnosis": "Dissociative Trance Disorder",
        "subtitle": "Kondisi Trans Disosiasi",
        "category": "Gangguan Disosiasi Berbasis Budaya (Culture-Bound)",
        "severity": "danger",
        "explanation": (
            "Terjadi konflik temporer di otak antara pusat emosi (sistem limbik) dan sirkuit memori (hipokampus). "
            "Otak mengalami banjir hormon dopamin dan oksitosin yang memicu relaksasi ekstrem dan perilaku otomatis, "
            "sementara korteks prefrontal mengalami penekanan aktivitas sementara. Kondisi ini dikenal sebagai "
            "'ego dissolution state' akibat gangguan integrasi jaringan default-mode network (DMN)."
        ),
        "recommendation": (
            "Segera konsultasikan dengan psikiater atau psikolog klinis, terutama jika episode berulang lebih dari "
            "2 kali dalam sebulan. Catat jurnal harian setelah episode dan hindari lingkungan pemicu tanpa pendampingan profesional."
        ),
        "triggers": [
            "Stres psikososial akut",
            "Ritual keagamaan/budaya yang intens",
            "Kelelahan ekstrem",
            "Sugesti kelompok (mass suggestion)",
            "Trauma psikologis yang belum terproses"
        ],
        "trigger_explanation": (
            "Episode trans disosiasi umumnya dipicu oleh kombinasi faktor biologis dan sosiokultural. "
            "Otak dalam kondisi stres tinggi atau sugesti kolektif dapat memasuki mode altered state of consciousness secara involunter."
        ),
        "trigger_mechanism": [
            "Stresor akut / ritual intens memicu lonjakan kortisol",
            "↓",
            "Amigdala teraktivasi → sistem limbik mendominasi korteks prefrontal",
            "↓",
            "Default Mode Network (DMN) terganggu → hilang kontrol diri",
            "↓",
            "Muncul gerakan otomatis, perubahan suara, dan amnesia sesaat"
        ],
    },
    {
        "id": "R002",
        "conditions": ["G006", "G007", "G003"],
        "diagnosis": "Depersonalization / Derealization Disorder",
        "subtitle": "Episode Depersonalisasi / Derealisasi",
        "category": "Gangguan Disosiasi Persepsi",
        "severity": "warning",
        "explanation": (
            "Mekanisme pertahanan ego di otak memutus integrasi persepsi sensorik akibat stres atau kecemasan ekstrem. "
            "Terjadi penurunan aktivitas di insula dan korteks somatosensoris, membuat individu merasa terpisah dari diri "
            "atau realitasnya — respons adaptif otak untuk 'mematikan' input emosional yang berlebihan."
        ),
        "recommendation": (
            "Konsultasikan dengan psikolog klinis untuk penilaian lebih lanjut. Teknik grounding (5-4-3-2-1 sensory technique) "
            "dapat membantu saat episode berlangsung. Evaluasi komorbiditas kecemasan atau depresi oleh profesional kesehatan mental."
        ),
        "triggers": [
            "Serangan panik / kecemasan tinggi",
            "Penggunaan zat psikoaktif",
            "Kurang tidur kronis",
            "Trauma masa kecil (childhood trauma)",
            "Gangguan disosiatif yang sudah ada sebelumnya"
        ],
        "trigger_explanation": (
            "Depersonalisasi sering muncul sebagai respons otomatis otak terhadap ancaman emosional yang overwhelming — "
            "otak 'memutus' koneksi sensorik untuk melindungi diri dari overload."
        ),
        "trigger_mechanism": [
            "Kecemasan / panik mendadak memicu hiperventilasi",
            "↓",
            "Aktivitas insula & korteks somatosensoris menurun drastis",
            "↓",
            "Integrasi persepsi diri-tubuh dan diri-lingkungan terputus",
            "↓",
            "Muncul perasaan 'mengamati diri dari luar' dan dunia terasa tidak nyata"
        ],
    },
    {
        "id": "R003",
        "conditions": ["G008", "G003", "G001"],
        "diagnosis": "Hyper-Recalling Trance State",
        "subtitle": "Kondisi Trans Hiper-Rekognisi Memori",
        "category": "Gangguan Disosiasi Memori Implisit",
        "severity": "warning",
        "explanation": (
            "Sirkuit memori mengalami pembukaan akses berlebihan (hyper-recalling) dalam kondisi trans. "
            "Amigdala yang teraktivasi penuh berinteraksi dengan hipokampus dalam mode 'replay spontan', sehingga "
            "memori implisit — suara, bahasa, melodi masa lalu — dipanggil kembali secara otomatis di luar kendali "
            "kesadaran, analogis dengan 'memory intrusion' pada PTSD."
        ),
        "recommendation": (
            "Konsultasi dengan neuropsikolog atau psikolog klinis untuk memetakan pola memori implisit sebagai pemicu. "
            "Terapi berbasis trauma seperti EMDR (Eye Movement Desensitization and Reprocessing) dapat dipertimbangkan."
        ),
        "triggers": [
            "Paparan suara/musik yang pernah didengar masa lalu",
            "Aroma atau sensori terhubung memori lama",
            "Stres pasca-trauma (PTSD sub-klinis)",
            "Hipnosis atau kondisi trance yang diinduksi",
            "Meditasi mendalam tanpa bimbingan"
        ],
        "trigger_explanation": (
            "Kondisi ini terkait erat dengan memori implisit di struktur limbik. Stimulus tertentu membuka 'pintu' "
            "akses ke memori terpendam, memunculkannya kembali sebagai vokalisasi atau bahasa yang tidak dikenal."
        ),
        "trigger_mechanism": [
            "Stimulus sensorik spesifik mengaktifkan memori implisit lama",
            "↓",
            "Amigdala + hipokampus masuk mode 'spontaneous replay'",
            "↓",
            "Korteks prefrontal kehilangan kendali atas output verbal",
            "↓",
            "Muncul vokalisasi bahasa asing / meracau di luar kesadaran"
        ],
    },
]

# ── WORKING MEMORY ──────────────────────────────────────────

def create_working_memory(selected_symptoms):
    return {
        "facts":       set(selected_symptoms),
        "fired_rules": [],
        "rule_scores": {},
        "trace":       [],
    }

def wm_evaluate_rule(wm, rule):
    conditions = set(rule["conditions"])
    matched    = wm["facts"].intersection(conditions)
    score      = round(len(matched) / len(conditions) * 100, 1)
    wm["rule_scores"][rule["id"]] = {
        "confidence":    score,
        "match_count":   len(matched),
        "total":         len(conditions),
        "matched_codes": list(matched),
    }
    wm["trace"].append({
        "rule_id":    rule["id"],
        "confidence": score,
        "matched":    list(matched),
    })
    wm["fired_rules"].append(rule["id"])
    return score

# ── INFERENCE ENGINE ────────────────────────────────────────

def run_inference(selected_symptoms):
    wm = create_working_memory(selected_symptoms)

    for rule in RULES:
        wm_evaluate_rule(wm, rule)

    all_results = sorted([
        {
            "rule_id":          rule["id"],
            "diagnosis":        rule["diagnosis"],
            "severity":         rule["severity"],
            "confidence":       wm["rule_scores"][rule["id"]]["confidence"],
            "match_count":      wm["rule_scores"][rule["id"]]["match_count"],
            "total_conditions": wm["rule_scores"][rule["id"]]["total"],
        }
        for rule in RULES
    ], key=lambda x: x["confidence"], reverse=True)

    top = all_results[0]

    if top["confidence"] == 0:
        return {
            "status":            "normal",
            "diagnosis":         "Kondisi Normal / Tidak Terdeteksi Gangguan Disosiasi",
            "subtitle":          "Tidak ada pola gejala yang signifikan",
            "category":          "—",
            "severity":          "normal",
            "confidence":        0,
            "match_count":       0,
            "total_conditions":  0,
            "explanation":       (
                "Berdasarkan gejala yang dipilih, sistem tidak mendeteksi pola yang cukup kuat untuk "
                "mengindikasikan gangguan disosiasi. Jika ada ketidaknyamanan psikologis yang persisten, "
                "konsultasi preventif tetap direkomendasikan."
            ),
            "recommendation":    "Pertahankan pola hidup sehat: tidur cukup, kelola stres, dan jaga koneksi sosial.",
            "triggers":          [],
            "trigger_explanation": "",
            "trigger_mechanism": [],
            "matched_labels":    [],
            "selected_symptoms": selected_symptoms,
            "all_results":       all_results,
            "wm_trace":          wm["trace"],
        }

    top_rule   = next(r for r in RULES if r["id"] == top["rule_id"])
    score_data = wm["rule_scores"][top["rule_id"]]

    return {
        "status":              "detected",
        "diagnosis":           top_rule["diagnosis"],
        "subtitle":            top_rule["subtitle"],
        "category":            top_rule["category"],
        "severity":            top_rule["severity"],
        "confidence":          score_data["confidence"],
        "match_count":         score_data["match_count"],
        "total_conditions":    score_data["total"],
        "explanation":         top_rule["explanation"],
        "recommendation":      top_rule["recommendation"],
        "triggers":            top_rule["triggers"],
        "trigger_explanation": top_rule["trigger_explanation"],
        "trigger_mechanism":   top_rule["trigger_mechanism"],
        "matched_labels":      [
            SYMPTOMS[c]["description"]
            for c in score_data["matched_codes"]
            if c in SYMPTOMS
        ],
        "selected_symptoms":   selected_symptoms,
        "all_results":         all_results,
        "wm_trace":            wm["trace"],
    }

# ── USER INTERFACE / FLASK ROUTES ───────────────────────────

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", symptoms=SYMPTOMS)

@app.route("/analyze", methods=["POST"])
def analyze():
    selected = request.form.getlist("symptoms")
    result   = run_inference(selected)
    return render_template("index.html", symptoms=SYMPTOMS, result=result, show_result=True)

@app.route("/api/analyze", methods=["POST"])
def api_analyze():
    data   = request.get_json(silent=True) or {}
    result = run_inference(data.get("symptoms", []))
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)