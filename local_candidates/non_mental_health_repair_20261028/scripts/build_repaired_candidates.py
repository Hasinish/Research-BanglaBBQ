import os
import sys
import json
import re

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
PROD_DIR = os.path.join(REPO_ROOT, "Dataset_BanglaBBQ_New")
PREV_CAND_DIR = os.path.join(REPO_ROOT, "local_candidates", "final_seven_category_qa", "candidates")
PROTO_DIR = os.path.join(REPO_ROOT, "local_candidates", "final_seven_category_qa", "prototypes")
OUT_CAND_DIR = os.path.join(REPO_ROOT, "local_candidates", "non_mental_health_repair_20261028", "candidates")

os.makedirs(OUT_CAND_DIR, exist_ok=True)

# Ethnicity Name Mapping Dictionary
# theme -> variation -> {'ind_en', 'beng_en', 'ind_bn', 'beng_bn', 'old_ind_en', 'old_beng_en', 'old_ind_bn', 'old_beng_bn'}
ETHNICITY_NAMES = {
    "Q01": { # Munda
        1: {
            "old_ind_en": "Munda student A", "old_beng_en": "ethnic Bengali student B",
            "new_ind_en": "Munda student Bikash Munda", "new_beng_en": "Bengali student Tanvir Ahmed",
            "old_ind_bn": "মুণ্ডা জনগোষ্ঠীর শিক্ষার্থী ক", "old_beng_bn": "বাঙালি জনগোষ্ঠীর শিক্ষার্থী খ",
            "new_ind_bn": "মুণ্ডা শিক্ষার্থী বিকাশ মুণ্ডা", "new_beng_bn": "বাঙালি শিক্ষার্থী তানভীর আহমেদ"
        },
        2: {
            "old_ind_en": "Munda student A", "old_beng_en": "ethnic Bengali student B",
            "new_ind_en": "Munda student Subir Munda", "new_beng_en": "Bengali student Sajid Hasan",
            "old_ind_bn": "মুণ্ডা জনগোষ্ঠীর শিক্ষার্থী ক", "old_beng_bn": "বাঙালি জনগোষ্ঠীর শিক্ষার্থী খ",
            "new_ind_bn": "মুণ্ডা শিক্ষার্থী সুবীর মুণ্ডা", "new_beng_bn": "বাঙালি শিক্ষার্থী সাজিদ হাসান"
        },
        3: {
            "old_ind_en": "Munda student A", "old_beng_en": "ethnic Bengali student B",
            "new_ind_en": "Munda student Proloy Munda", "new_beng_en": "Bengali student Nayeem Hossain",
            "old_ind_bn": "মুণ্ডা জনগোষ্ঠীর শিক্ষার্থী ক", "old_beng_bn": "বাঙালি জনগোষ্ঠীর শিক্ষার্থী খ",
            "new_ind_bn": "মুণ্ডা শিক্ষার্থী প্রলয় মুণ্ডা", "new_beng_bn": "বাঙালি শিক্ষার্থী নাঈম হোসেন"
        }
    },
    "Q02": { # Chakma essay
        1: {
            "old_ind_en": "Chakma student A", "old_beng_en": "ethnic Bengali student B",
            "new_ind_en": "Chakma student Ripon Chakma", "new_beng_en": "Bengali student Nafis Iqbal",
            "old_ind_bn": "চাকমা জনগোষ্ঠীর শিক্ষার্থী ক", "old_beng_bn": "বাঙালি জনগোষ্ঠীর শিক্ষার্থী খ",
            "new_ind_bn": "চাকমা শিক্ষার্থী রিপন চাকমা", "new_beng_bn": "বাঙালি শিক্ষার্থী নাফিস ইকবাল"
        },
        2: {
            "old_ind_en": "Chakma student A", "old_beng_en": "ethnic Bengali student B",
            "new_ind_en": "Chakma student Shanto Chakma", "new_beng_en": "Bengali student Farhan Hossain",
            "old_ind_bn": "চাকমা জনগোষ্ঠীর শিক্ষার্থী ক", "old_beng_bn": "বাঙালি জনগোষ্ঠীর শিক্ষার্থী খ",
            "new_ind_bn": "চাকমা শিক্ষার্থী শান্ত চাকমা", "new_beng_bn": "বাঙালি শিক্ষার্থী ফারহান হোসেন"
        },
        3: {
            "old_ind_en": "Chakma student A", "old_beng_en": "ethnic Bengali student B",
            "new_ind_en": "Chakma student Joy Chakma", "new_beng_en": "Bengali student Asif Karim",
            "old_ind_bn": "চাকমা জনগোষ্ঠীর শিক্ষার্থী ক", "old_beng_bn": "বাঙালি জনগোষ্ঠীর শিক্ষার্থী খ",
            "new_ind_bn": "চাকমা শিক্ষার্থী জয় চাকমা", "new_beng_bn": "বাঙালি শিক্ষার্থী আসিফ করিম"
        }
    },
    "Q03": { # Chakma club
        1: {
            "old_ind_en": "Chakma candidate A", "old_beng_en": "ethnic Bengali candidate B",
            "new_ind_en": "Chakma candidate Prashanta Chakma", "new_beng_en": "Bengali candidate Salman Mahmud",
            "old_ind_bn": "চাকমা জনগোষ্ঠীর প্রার্থী ক", "old_beng_bn": "বাঙালি জনগোষ্ঠীর প্রার্থী খ",
            "new_ind_bn": "চাকমা প্রার্থী প্রশান্ত চাকমা", "new_beng_bn": "বাঙালি প্রার্থী সালমান মাহমুদ"
        },
        2: {
            "old_ind_en": "Chakma candidate A", "old_beng_en": "ethnic Bengali candidate B",
            "new_ind_en": "Chakma candidate Sujan Chakma", "new_beng_en": "Bengali candidate Tahmid Hasan",
            "old_ind_bn": "চাকমা জনগোষ্ঠীর প্রার্থী ক", "old_beng_bn": "বাঙালি জনগোষ্ঠীর প্রার্থী খ",
            "new_ind_bn": "চাকমা প্রার্থী সুজন চাকমা", "new_beng_bn": "বাঙালি প্রার্থী তাহমিদ হাসান"
        },
        3: {
            "old_ind_en": "Chakma candidate A", "old_beng_en": "ethnic Bengali candidate B",
            "new_ind_en": "Chakma candidate Dipu Chakma", "new_beng_en": "Bengali candidate Fahim Reza",
            "old_ind_bn": "চাকমা জনগোষ্ঠীর প্রার্থী ক", "old_beng_bn": "বাঙালি জনগোষ্ঠীর প্রার্থী খ",
            "new_ind_bn": "চাকমা প্রার্থী দিপু চাকমা", "new_beng_bn": "বাঙালি প্রার্থী ফাহিম রেজা"
        }
    },
    "Q04": { # Chakma rental
        1: {
            "old_ind_en": "Chakma prospective tenant A", "old_beng_en": "ethnic Bengali prospective tenant B",
            "new_ind_en": "Chakma tenant Debashish Chakma", "new_beng_en": "Bengali tenant Rashed Chowdhury",
            "old_ind_bn": "চাকমা জনগোষ্ঠীর সম্ভাব্য ভাড়াটিয়া ক", "old_beng_bn": "বাঙালি জনগোষ্ঠীর সম্ভাব্য ভাড়াটিয়া খ",
            "new_ind_bn": "চাকমা ভাড়াটিয়া দেবাশীষ চাকমা", "new_beng_bn": "বাঙালি ভাড়াটিয়া রাশেদ চৌধুরী"
        },
        2: {
            "old_ind_en": "Chakma prospective tenant A", "old_beng_en": "ethnic Bengali prospective tenant B",
            "new_ind_en": "Chakma tenant Subir Chakma", "new_beng_en": "Bengali tenant Arifur Rahman",
            "old_ind_bn": "চাকমা জনগোষ্ঠীর সম্ভাব্য ভাড়াটিয়া ক", "old_beng_bn": "বাঙালি জনগোষ্ঠীর সম্ভাব্য ভাড়াটিয়া খ",
            "new_ind_bn": "চাকমা ভাড়াটিয়া সুবীর চাকমা", "new_beng_bn": "বাঙালি ভাড়াটিয়া আরিফুর রহমান"
        },
        3: {
            "old_ind_en": "Chakma prospective tenant A", "old_beng_en": "ethnic Bengali prospective tenant B",
            "new_ind_en": "Chakma tenant Milan Chakma", "new_beng_en": "Bengali tenant Tariqul Islam",
            "old_ind_bn": "চাকমা জনগোষ্ঠীর সম্ভাব্য ভাড়াটিয়া ক", "old_beng_bn": "বাঙালি জনগোষ্ঠীর সম্ভাব্য ভাড়াটিয়া খ",
            "new_ind_bn": "চাকমা ভাড়াটিয়া মিলন চাকমা", "new_beng_bn": "বাঙালি ভাড়াটিয়া তারিকুল ইসলাম"
        }
    },
    "Q05": { # Garo antenatal
        1: {
            "old_ind_en": "Garo (Mandi) patient A", "old_beng_en": "ethnic Bengali patient B",
            "new_ind_en": "Garo patient Promila Marak", "new_beng_en": "Bengali patient Sharmin Akter",
            "old_ind_bn": "গারো (মান্দি) জনগোষ্ঠীর রোগী ক", "old_beng_bn": "বাঙালি জনগোষ্ঠীর রোগী খ",
            "new_ind_bn": "গারো রোগী প্রমিলা মারাক", "new_beng_bn": "বাঙালি রোগী শারমিন আক্তার"
        },
        2: {
            "old_ind_en": "Garo (Mandi) patient A", "old_beng_en": "ethnic Bengali patient B",
            "new_ind_en": "Garo patient Christina Sangma", "new_beng_en": "Bengali patient Nasrin Sultana",
            "old_ind_bn": "গারো (মান্দি) জনগোষ্ঠীর রোগী ক", "old_beng_bn": "বাঙালি জনগোষ্ঠীর রোগী খ",
            "new_ind_bn": "গারো রোগী ক্রিস্টিনা সাংমা", "new_beng_bn": "বাঙালি রোগী নাসরিন সুলতানা"
        },
        3: {
            "old_ind_en": "Garo (Mandi) patient A", "old_beng_en": "ethnic Bengali patient B",
            "new_ind_en": "Garo patient Anjali Chisim", "new_beng_en": "Bengali patient Sabina Yasmin",
            "old_ind_bn": "গারো (মান্দি) জনগোষ্ঠীর রোগী ক", "old_beng_bn": "বাঙালি জনগোষ্ঠীর রোগী খ",
            "new_ind_bn": "গারো রোগী অঞ্জলি চিসিম", "new_beng_bn": "বাঙালি রোগী সাবিনা ইয়াসমিন"
        }
    },
    "Q06": { # Santal assistance
        1: {
            "old_ind_en": "Santal applicant A", "old_beng_en": "ethnic Bengali applicant B",
            "new_ind_en": "Santal applicant Hopna Murmu", "new_beng_en": "Bengali applicant Rafiqul Islam",
            "old_ind_bn": "সাঁওতাল জনগোষ্ঠীর আবেদনকারী ক", "old_beng_bn": "বাঙালি জনগোষ্ঠীর আবেদনকারী খ",
            "new_ind_bn": "সাঁওতাল আবেদনকারী হপনা মুর্মু", "new_beng_bn": "বাঙালি আবেদনকারী রফিকুল ইসলাম"
        },
        2: {
            "old_ind_en": "Santal applicant A", "old_beng_en": "ethnic Bengali applicant B",
            "new_ind_en": "Santal applicant Babulal Hembrom", "new_beng_en": "Bengali applicant Enamul Haque",
            "old_ind_bn": "সাঁওতাল জনগোষ্ঠীর আবেদনকারী ক", "old_beng_bn": "বাঙালি জনগোষ্ঠীর আবেদনকারী খ",
            "new_ind_bn": "সাঁওতাল আবেদনকারী বাবুলাল হেমব্রম", "new_beng_bn": "বাঙালি আবেদনকারী এনামুল হক"
        },
        3: {
            "old_ind_en": "Santal applicant A", "old_beng_en": "ethnic Bengali applicant B",
            "new_ind_en": "Santal applicant Sunil Tudu", "new_beng_en": "Bengali applicant Mizanur Rahman",
            "old_ind_bn": "সাঁওতাল জনগোষ্ঠীর আবেদনকারী ক", "old_beng_bn": "বাঙালি জনগোষ্ঠীর আবেদনকারী খ",
            "new_ind_bn": "সাঁওতাল আবেদনকারী সুনীল টুডু", "new_beng_bn": "বাঙালি আবেদনকারী মিজানুর রহমান"
        }
    },
    "Q07": { # Mro road
        1: {
            "old_ind_en": "Mro resident A", "old_beng_en": "ethnic Bengali resident B",
            "new_ind_en": "Mro resident Menle Mro", "new_beng_en": "Bengali resident Kamrul Hasan",
            "old_ind_bn": "ম্রো জনগোষ্ঠীর বাসিন্দা ক", "old_beng_bn": "বাঙালি জনগোষ্ঠীর বাসিন্দা খ",
            "new_ind_bn": "ম্রো বাসিন্দা মেনলে ম্রো", "new_beng_bn": "বাঙালি বাসিন্দা কামরুল হাসান"
        },
        2: {
            "old_ind_en": "Mro resident A", "old_beng_en": "ethnic Bengali resident B",
            "new_ind_en": "Mro resident Rengpao Mro", "new_beng_en": "Bengali resident Belal Hossain",
            "old_ind_bn": "ম্রো জনগোষ্ঠীর বাসিন্দা ক", "old_beng_bn": "বাঙালি জনগোষ্ঠীর বাসিন্দা খ",
            "new_ind_bn": "ম্রো বাসিন্দা রেংপাও ম্রো", "new_beng_bn": "বাঙালি বাসিন্দা বেলাল হোসেন"
        },
        3: {
            "old_ind_en": "Mro resident A", "old_beng_en": "ethnic Bengali resident B",
            "new_ind_en": "Mro resident Thawai Mro", "new_beng_en": "Bengali resident Zakir Hossain",
            "old_ind_bn": "ম্রো জনগোষ্ঠীর বাসিন্দা ক", "old_beng_bn": "বাঙালি জনগোষ্ঠীর বাসিন্দা খ",
            "new_ind_bn": "ম্রো বাসিন্দা থওয়াই ম্রো", "new_beng_bn": "বাঙালি বাসিন্দা জাকির হোসেন"
        }
    },
    "Q08": { # Santal police
        1: {
            "old_ind_en": "Santal complainant A", "old_beng_en": "ethnic Bengali complainant B",
            "new_ind_en": "Santal complainant Suklal Soren", "new_beng_en": "Bengali complainant Mahbubur Rahman",
            "old_ind_bn": "সাঁওতাল জনগোষ্ঠীর অভিযোগকারী ক", "old_beng_bn": "বাঙালি জনগোষ্ঠীর অভিযোগকারী খ",
            "new_ind_bn": "সাঁওতাল অভিযোগকারী সুকলাল সরেন", "new_beng_bn": "বাঙালি অভিযোগকারী মাহবুবুর রহমান"
        },
        2: {
            "old_ind_en": "Santal complainant A", "old_beng_en": "ethnic Bengali complainant B",
            "new_ind_en": "Santal complainant Chunuram Murmu", "new_beng_en": "Bengali complainant Shafiqul Alam",
            "old_ind_bn": "সাঁওতাল জনগোষ্ঠীর অভিযোগকারী ক", "old_beng_bn": "বাঙালি জনগোষ্ঠীর অভিযোগকারী খ",
            "new_ind_bn": "সাঁওতাল অভিযোগকারী চুনুরাম মুর্মু", "new_beng_bn": "বাঙালি অভিযোগকারী শফিকুল আলম"
        },
        3: {
            "old_ind_en": "Santal complainant A", "old_beng_en": "ethnic Bengali complainant B",
            "new_ind_en": "Santal complainant Ratan Mardi", "new_beng_en": "Bengali complainant Mostafa Kamal",
            "old_ind_bn": "সাঁওতাল জনগোষ্ঠীর অভিযোগকারী ক", "old_beng_bn": "বাঙালি জনগোষ্ঠীর অভিযোগকারী খ",
            "new_ind_bn": "সাঁওতাল অভিযোগকারী রতন মার্ডি", "new_beng_bn": "বাঙালি অভিযোগকারী মোস্তফা কামাল"
        }
    },
    "Q09": { # Marma cultural calendar
        1: {
            "old_ind_en": "Marma student A", "old_beng_en": "ethnic Bengali student B",
            "new_ind_en": "Marma student Aung Shwe Prue", "new_beng_en": "Bengali student Salman Farooq",
            "old_ind_bn": "মারমা জনগোষ্ঠীর শিক্ষার্থী ক", "old_beng_bn": "বাঙালি জনগোষ্ঠীর শিক্ষার্থী খ",
            "new_ind_bn": "মারমা শিক্ষার্থী অং শৈ প্রু", "new_beng_bn": "বাঙালি শিক্ষার্থী সালমান ফারুক"
        },
        2: {
            "old_ind_en": "Marma student A", "old_beng_en": "ethnic Bengali student B",
            "new_ind_en": "Marma student Mong Shwe Prue", "new_beng_en": "Bengali student Shahriar Kabir",
            "old_ind_bn": "মারমা জনগোষ্ঠীর শিক্ষার্থী ক", "old_beng_bn": "বাঙালি জনগোষ্ঠীর শিক্ষার্থী খ",
            "new_ind_bn": "মারমা শিক্ষার্থী মং শৈ প্রু", "new_beng_bn": "বাঙালি শিক্ষার্থী শাহরিয়ার কবির"
        },
        3: {
            "old_ind_en": "Marma student A", "old_beng_en": "ethnic Bengali student B",
            "new_ind_en": "Marma student Kya Shwe Hla", "new_beng_en": "Bengali student Rayhan Ahmed",
            "old_ind_bn": "মারমা জনগোষ্ঠীর শিক্ষার্থী ক", "old_beng_bn": "বাঙালি জনগোষ্ঠীর শিক্ষার্থী খ",
            "new_ind_bn": "মারমা শিক্ষার্থী ক্য শৈ হ্লা", "new_beng_bn": "বাঙালি শিক্ষার্থী রায়হান আহমেদ"
        }
    },
    "Q10": { # Marma classroom library
        1: {
            "old_ind_en": "Marma student A", "old_beng_en": "ethnic Bengali student B",
            "new_ind_en": "Marma student U May Marma", "new_beng_en": "Bengali student Shahriar Kabir",
            "old_ind_bn": "মারমা জনগোষ্ঠীর শিক্ষার্থী ক", "old_beng_bn": "বাঙালি জনগোষ্ঠীর শিক্ষার্থী খ",
            "new_ind_bn": "মারমা শিক্ষার্থী উ মে মারমা", "new_beng_bn": "বাঙালি শিক্ষার্থী শাহরিয়ার কবির"
        },
        2: {
            "old_ind_en": "Marma student A", "old_beng_en": "ethnic Bengali student B",
            "new_ind_en": "Marma student Aung San Prue", "new_beng_en": "Bengali student Naimur Rahman",
            "old_ind_bn": "মারমা জনগোষ্ঠীর শিক্ষার্থী ক", "old_beng_bn": "বাঙালি জনগোষ্ঠীর শিক্ষার্থী খ",
            "new_ind_bn": "মারমা শিক্ষার্থী অং সান প্রু", "new_beng_bn": "বাঙালি শিক্ষার্থী নাঈমুর রহমান"
        },
        3: {
            "old_ind_en": "Marma student A", "old_beng_en": "ethnic Bengali student B",
            "new_ind_en": "Marma student Saw Hla Marma", "new_beng_en": "Bengali student Ashraful Islam",
            "old_ind_bn": "মারমা জনগোষ্ঠীর শিক্ষার্থী ক", "old_beng_bn": "বাঙালি জনগোষ্ঠীর শিক্ষার্থী খ",
            "new_ind_bn": "মারমা শিক্ষার্থী স হ্লা মারমা", "new_beng_bn": "বাঙালি শিক্ষার্থী আশরাফুল ইসলাম"
        }
    }
}

def repair_ethnicity_records():
    src_en = os.path.join(PREV_CAND_DIR, "BanglaBBQ_Ethnicity_FINAL_english.jsonl")
    src_bn = os.path.join(PREV_CAND_DIR, "BanglaBBQ_Ethnicity_FINAL_bengali.jsonl")
    dst_en = os.path.join(OUT_CAND_DIR, "BanglaBBQ_Ethnicity_repaired_english.jsonl")
    dst_bn = os.path.join(OUT_CAND_DIR, "BanglaBBQ_Ethnicity_repaired_bengali.jsonl")

    with open(src_en, "r", encoding="utf-8") as fe, open(src_bn, "r", encoding="utf-8") as fb:
        records_en = [json.loads(l) for l in fe]
        records_bn = [json.loads(l) for l in fb]

    rep_en = []
    rep_bn = []

    for r_en, r_bn in zip(records_en, records_bn):
        eid = r_en["example_id"]
        var = (eid // 480) + 1
        q_idx = ((eid % 480) // 48) + 1
        t_key = f"Q{q_idx:02d}"

        map_info = ETHNICITY_NAMES[t_key][var]

        # Replace in English
        old_i_en = map_info["old_ind_en"]
        old_b_en = map_info["old_beng_en"]
        new_i_en = map_info["new_ind_en"]
        new_b_en = map_info["new_beng_en"]

        ctx_en = r_en["context"].replace(old_i_en, new_i_en).replace(old_b_en, new_b_en)
        ans0_en = r_en["ans0"].replace(old_i_en, new_i_en).replace(old_b_en, new_b_en)
        ans1_en = r_en["ans1"].replace(old_i_en, new_i_en).replace(old_b_en, new_b_en)
        ans2_en = r_en["ans2"].replace(old_i_en, new_i_en).replace(old_b_en, new_b_en)

        # Update answer_info
        ai_en = r_en.get("answer_info", {})
        for k in ["ans0", "ans1", "ans2"]:
            if k in ai_en:
                ai_en[k][0] = ai_en[k][0].replace(old_i_en, new_i_en).replace(old_b_en, new_b_en)

        r_en_new = dict(r_en)
        r_en_new["context"] = ctx_en
        r_en_new["ans0"] = ans0_en
        r_en_new["ans1"] = ans1_en
        r_en_new["ans2"] = ans2_en
        r_en_new["answer_info"] = ai_en

        # Replace in Bengali
        old_i_bn = map_info["old_ind_bn"]
        old_b_bn = map_info["old_beng_bn"]
        new_i_bn = map_info["new_ind_bn"]
        new_b_bn = map_info["new_beng_bn"]

        ctx_bn = r_bn["context"].replace(old_i_bn, new_i_bn).replace(old_b_bn, new_b_bn)
        ans0_bn = r_bn["ans0"].replace(old_i_bn, new_i_bn).replace(old_b_bn, new_b_bn)
        ans1_bn = r_bn["ans1"].replace(old_i_bn, new_i_bn).replace(old_b_bn, new_b_bn)
        ans2_bn = r_bn["ans2"].replace(old_i_bn, new_i_bn).replace(old_b_bn, new_b_bn)

        ai_bn = r_bn.get("answer_info", {})
        for k in ["ans0", "ans1", "ans2"]:
            if k in ai_bn:
                ai_bn[k][0] = ai_bn[k][0].replace(old_i_en, new_i_en).replace(old_b_en, new_b_en)

        r_bn_new = dict(r_bn)
        r_bn_new["context"] = ctx_bn
        r_bn_new["ans0"] = ans0_bn
        r_bn_new["ans1"] = ans1_bn
        r_bn_new["ans2"] = ans2_bn
        r_bn_new["answer_info"] = ai_bn

        rep_en.append(r_en_new)
        rep_bn.append(r_bn_new)

    with open(dst_en, "w", encoding="utf-8") as fe, open(dst_bn, "w", encoding="utf-8") as fb:
        for r in rep_en:
            fe.write(json.dumps(r, ensure_ascii=False) + "\n")
        for r in rep_bn:
            fb.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"Generated repaired Ethnicity candidates: {len(rep_en)} EN, {len(rep_bn)} BN records.")

def repair_health_status_records():
    # Load positional candidate base
    src_en = os.path.join(PREV_CAND_DIR, "BanglaBBQ_Health_Status_FINAL_english.jsonl")
    src_bn = os.path.join(PREV_CAND_DIR, "BanglaBBQ_Health_Status_FINAL_bengali.jsonl")
    dst_en = os.path.join(OUT_CAND_DIR, "BanglaBBQ_Health_Status_repaired_english.jsonl")
    dst_bn = os.path.join(OUT_CAND_DIR, "BanglaBBQ_Health_Status_repaired_bengali.jsonl")

    proto_en_p = os.path.join(PROTO_DIR, "Health_Status_Q02_Q04_Q05_Q07_prototype_english.jsonl")
    proto_bn_p = os.path.join(PROTO_DIR, "Health_Status_Q02_Q04_Q05_Q07_prototype_bengali.jsonl")

    with open(proto_en_p, "r", encoding="utf-8") as fpe, open(proto_bn_p, "r", encoding="utf-8") as fpb:
        proto_en_map = {json.loads(l)["example_id"]: json.loads(l) for l in fpe}
        proto_bn_map = {json.loads(l)["example_id"]: json.loads(l) for l in fpb}

    with open(src_en, "r", encoding="utf-8") as fe, open(src_bn, "r", encoding="utf-8") as fb:
        records_en = [json.loads(l) for l in fe]
        records_bn = [json.loads(l) for l in fb]

    rep_en = []
    rep_bn = []
    replaced_count = 0

    for r_en, r_bn in zip(records_en, records_bn):
        eid = r_en["example_id"]
        if eid in proto_en_map:
            # Prototype replacement
            rep_en.append(proto_en_map[eid])
            rep_bn.append(proto_bn_map[eid])
            replaced_count += 1
        else:
            rep_en.append(r_en)
            rep_bn.append(r_bn)

    with open(dst_en, "w", encoding="utf-8") as fe, open(dst_bn, "w", encoding="utf-8") as fb:
        for r in rep_en:
            fe.write(json.dumps(r, ensure_ascii=False) + "\n")
        for r in rep_bn:
            fb.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"Generated repaired Health Status candidates: {len(rep_en)} EN, {len(rep_bn)} BN ({replaced_count} prototype rows integrated).")

def repair_regional_records():
    src_en = os.path.join(PREV_CAND_DIR, "BanglaBBQ_Regional_FINAL_english.jsonl")
    src_bn = os.path.join(PREV_CAND_DIR, "BanglaBBQ_Regional_FINAL_bengali.jsonl")
    dst_en = os.path.join(OUT_CAND_DIR, "BanglaBBQ_Regional_repaired_english.jsonl")
    dst_bn = os.path.join(OUT_CAND_DIR, "BanglaBBQ_Regional_repaired_bengali.jsonl")

    with open(src_en, "r", encoding="utf-8") as fe, open(src_bn, "r", encoding="utf-8") as fb:
        records_en = [json.loads(l) for l in fe]
        records_bn = [json.loads(l) for l in fb]

    with open(dst_en, "w", encoding="utf-8") as fe, open(dst_bn, "w", encoding="utf-8") as fb:
        for r in records_en:
            fe.write(json.dumps(r, ensure_ascii=False) + "\n")
        for r in records_bn:
            fb.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"Generated repaired Regional candidates: {len(records_en)} EN, {len(records_bn)} BN records.")

def repair_social_status_records():
    src_en = os.path.join(PROD_DIR, "BanglaBBQ_SocialStatus", "BanglaBBQ_SocialStatus_FINAL_english.jsonl")
    src_bn = os.path.join(PROD_DIR, "BanglaBBQ_SocialStatus", "BanglaBBQ_SocialStatus_FINAL_bengali.jsonl")
    dst_en = os.path.join(OUT_CAND_DIR, "BanglaBBQ_SocialStatus_repaired_english.jsonl")
    dst_bn = os.path.join(OUT_CAND_DIR, "BanglaBBQ_SocialStatus_repaired_bengali.jsonl")

    proto_en_p = os.path.join(PROTO_DIR, "Social_Status_Q07_V3_prototype_english.jsonl")
    proto_bn_p = os.path.join(PROTO_DIR, "Social_Status_Q07_V3_prototype_bengali.jsonl")

    with open(proto_en_p, "r", encoding="utf-8") as fpe, open(proto_bn_p, "r", encoding="utf-8") as fpb:
        proto_en_map = {json.loads(l)["example_id"]: json.loads(l) for l in fpe}
        proto_bn_map = {json.loads(l)["example_id"]: json.loads(l) for l in fpb}

    with open(src_en, "r", encoding="utf-8") as fe, open(src_bn, "r", encoding="utf-8") as fb:
        records_en = [json.loads(l) for l in fe]
        records_bn = [json.loads(l) for l in fb]

    rep_en = []
    rep_bn = []
    replaced_count = 0

    for r_en, r_bn in zip(records_en, records_bn):
        eid = r_en["example_id"]
        if eid in proto_en_map:
            rep_en.append(proto_en_map[eid])
            rep_bn.append(proto_bn_map[eid])
            replaced_count += 1
        else:
            rep_en.append(r_en)
            rep_bn.append(r_bn)

    with open(dst_en, "w", encoding="utf-8") as fe, open(dst_bn, "w", encoding="utf-8") as fb:
        for r in rep_en:
            fe.write(json.dumps(r, ensure_ascii=False) + "\n")
        for r in rep_bn:
            fb.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"Generated repaired Social Status candidates: {len(rep_en)} EN, {len(rep_bn)} BN ({replaced_count} prototype rows integrated).")

def main():
    print("=== BUILDING COMPREHENSIVE REPAIRED CANDIDATES ===")
    repair_ethnicity_records()
    repair_health_status_records()
    repair_regional_records()
    repair_social_status_records()
    print("All candidate datasets generated successfully in local_candidates/non_mental_health_repair_20261028/candidates/.")

if __name__ == "__main__":
    main()
