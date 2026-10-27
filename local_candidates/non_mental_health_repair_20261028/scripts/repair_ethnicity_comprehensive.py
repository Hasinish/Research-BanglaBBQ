import os
import sys
import json
import re

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
CAND_DIR = os.path.join(REPO_ROOT, "local_candidates", "final_seven_category_qa", "candidates")
OUT_CAND_DIR = os.path.join(REPO_ROOT, "local_candidates", "non_mental_health_repair_20261028", "candidates")

SRC_EN = os.path.join(CAND_DIR, "BanglaBBQ_Ethnicity_FINAL_english.jsonl")
SRC_BN = os.path.join(CAND_DIR, "BanglaBBQ_Ethnicity_FINAL_bengali.jsonl")

DST_EN = os.path.join(OUT_CAND_DIR, "BanglaBBQ_Ethnicity_repaired_english.jsonl")
DST_BN = os.path.join(OUT_CAND_DIR, "BanglaBBQ_Ethnicity_repaired_bengali.jsonl")

# Theme configuration
# theme_id -> group_en, group_bn, role_en, role_bn, names_by_var
THEME_CONFIG = {
    1: {
        "group_en": "Munda", "group_bn": "মুণ্ডা", "role_en": "student", "role_bn": "শিক্ষার্থী",
        "vars": {
            1: ("Bikash Munda", "Tanvir Ahmed", "বিকাশ মুণ্ডা", "তানভীর আহমেদ"),
            2: ("Subir Munda", "Sajid Hasan", "সুবীর মুণ্ডা", "সাজিদ হাসান"),
            3: ("Proloy Munda", "Nayeem Hossain", "প্রলয় মুণ্ডা", "নাঈম হোসেন"),
        }
    },
    2: {
        "group_en": "Chakma", "group_bn": "চাকমা", "role_en": "student", "role_bn": "শিক্ষার্থী",
        "vars": {
            1: ("Ripon Chakma", "Nafis Iqbal", "রিপন চাকমা", "নাফিস ইকবাল"),
            2: ("Shanto Chakma", "Farhan Hossain", "শান্ত চাকমা", "ফারহান হোসেন"),
            3: ("Joy Chakma", "Asif Karim", "জয় চাকমা", "আসিফ করিম"),
        }
    },
    3: {
        "group_en": "Chakma", "group_bn": "চাকমা", "role_en": "candidate", "role_bn": "প্রার্থী",
        "vars": {
            1: ("Prashanta Chakma", "Salman Mahmud", "প্রশান্ত চাকমা", "সালমান মাহমুদ"),
            2: ("Sujan Chakma", "Tahmid Hasan", "সুজন চাকমা", "তাহমিদ হাসান"),
            3: ("Dipu Chakma", "Fahim Reza", "দিপু চাকমা", "ফাহিম রেজা"),
        }
    },
    4: {
        "group_en": "Chakma", "group_bn": "চাকমা", "role_en": "prospective tenant", "role_bn": "সম্ভাব্য ভাড়াটিয়া",
        "short_role_en": "tenant", "short_role_bn": "ভাড়াটিয়া",
        "vars": {
            1: ("Debashish Chakma", "Rashed Chowdhury", "দেবাশীষ চাকমা", "রাশেদ চৌধুরী"),
            2: ("Subir Chakma", "Arifur Rahman", "সুবীর চাকমা", "আরিফুর রহমান"),
            3: ("Milan Chakma", "Tariqul Islam", "মিলন চাকমা", "তারিকুল ইসলাম"),
        }
    },
    5: {
        "group_en": "Garo (Mandi)", "group_bn": "গারো (মান্দি)", "role_en": "patient", "role_bn": "রোগী",
        "vars": {
            1: ("Promila Marak", "Sharmin Akter", "প্রমিলা মারাক", "শারমিন আক্তার"),
            2: ("Christina Sangma", "Nasrin Sultana", "ক্রিস্টিনা সাংমা", "নাসরিন সুলতানা"),
            3: ("Anjali Chisim", "Sabina Yasmin", "অঞ্জলি চিসিম", "সাবিনা ইয়াসমিন"),
        }
    },
    6: {
        "group_en": "Santal", "group_bn": "সাঁওতাল", "role_en": "applicant", "role_bn": "আবেদনকারী",
        "vars": {
            1: ("Hopna Murmu", "Rafiqul Islam", "হপনা মুর্মু", "রফিকুল ইসলাম"),
            2: ("Babulal Hembrom", "Enamul Haque", "বাবুলাল হেমব্রম", "এনামুল হক"),
            3: ("Sunil Tudu", "Mizanur Rahman", "সুনীল টুডু", "মিজানুর রহমান"),
        }
    },
    7: {
        "group_en": "Mro", "group_bn": "ম্রো", "role_en": "resident", "role_bn": "বাসিন্দা",
        "vars": {
            1: ("Menle Mro", "Kamrul Hasan", "মেনলে ম্রো", "কামরুল হাসান"),
            2: ("Rengpao Mro", "Belal Hossain", "রেংপাও ম্রো", "বেলাল হোসেন"),
            3: ("Thawai Mro", "Zakir Hossain", "থওয়াই ম্রো", "জাকির হোসেন"),
        }
    },
    8: {
        "group_en": "Santal", "group_bn": "সাঁওতাল", "role_en": "complainant", "role_bn": "অভিযোগকারী",
        "vars": {
            1: ("Suklal Soren", "Mahbubur Rahman", "সুকলাল সরেন", "মাহবুবুর রহমান"),
            2: ("Chunuram Murmu", "Shafiqul Alam", "চুনুরাম মুর্মু", "শফিকুল আলম"),
            3: ("Ratan Mardi", "Mostafa Kamal", "রতন মার্ডি", "মোস্তফা কামাল"),
        }
    },
    9: {
        "group_en": "Marma", "group_bn": "মারমা", "role_en": "student", "role_bn": "শিক্ষার্থী",
        "vars": {
            1: ("Aung Shwe Prue", "Salman Farooq", "অং শৈ প্রু", "সালমান ফারুক"),
            2: ("Mong Shwe Prue", "Shahriar Kabir", "মং শৈ প্রু", "শাহরিয়ার কবির"),
            3: ("Kya Shwe Hla", "Rayhan Ahmed", "ক্য শৈ হ্লা", "রায়হান আহমেদ"),
        }
    },
    10: {
        "group_en": "Marma", "group_bn": "মারমা", "role_en": "student", "role_bn": "শিক্ষার্থী",
        "vars": {
            1: ("U May Marma", "Shahriar Kabir", "উ মে মারমা", "শাহরিয়ার কবির"),
            2: ("Aung San Prue", "Naimur Rahman", "অং সান প্রু", "নাঈমুর রহমান"),
            3: ("Saw Hla Marma", "Ashraful Islam", "স হ্লা মারমা", "আশরাফুল ইসলাম"),
        }
    }
}

def transform_ethnicity_records():
    with open(SRC_EN, "r", encoding="utf-8") as fe, open(SRC_BN, "r", encoding="utf-8") as fb:
        recs_en = [json.loads(l) for l in fe]
        recs_bn = [json.loads(l) for l in fb]

    out_en = []
    out_bn = []

    for r_en, r_bn in zip(recs_en, recs_bn):
        eid = r_en["example_id"]
        var = (eid // 480) + 1
        q_idx = ((eid % 480) // 48) + 1
        cfg = THEME_CONFIG[q_idx]

        name_ind_en, name_beng_en, name_ind_bn, name_beng_bn = cfg["vars"][var]
        grp_en = cfg["group_en"]
        grp_bn = cfg["group_bn"]
        role_en = cfg["role_en"]
        role_bn = cfg["role_bn"]
        short_role_en = cfg.get("short_role_en", role_en)
        short_role_bn = cfg.get("short_role_bn", role_bn)

        meta = r_en.get("additional_metadata", {})
        orient = meta.get("version", "a")

        ctx_en = r_en["context"]
        ctx_bn = r_bn["context"]

        # Define full descriptive terms
        ind_full_en = f"{grp_en} {role_en} {name_ind_en}"
        beng_full_en = f"Bengali {role_en} {name_beng_en}"

        ind_full_bn = f"{grp_bn} {role_bn} {name_ind_bn}"
        beng_full_bn = f"বাঙালি {role_bn} {name_beng_bn}"

        if orient == "a":
            # Target is A, Comparison is B
            # English Context
            ctx_en = re.sub(rf"\b{re.escape(grp_en)} {re.escape(role_en)} A\b", ind_full_en, ctx_en)
            ctx_en = re.sub(rf"\bethnic Bengali {re.escape(role_en)} B\b", beng_full_en, ctx_en)
            ctx_en = re.sub(rf"\b{re.escape(role_en)} A\b", name_ind_en, ctx_en)
            ctx_en = re.sub(rf"\b{re.escape(role_en)} B\b", name_beng_en, ctx_en)
            if short_role_en != role_en:
                ctx_en = re.sub(rf"\b{re.escape(short_role_en)} A\b", name_ind_en, ctx_en)
                ctx_en = re.sub(rf"\b{re.escape(short_role_en)} B\b", name_beng_en, ctx_en)

            # Bengali Context
            ctx_bn = re.sub(rf"{re.escape(grp_bn)} জনগোষ্ঠীর {re.escape(role_bn)} ক(?=[^\u0980-\u09FF]|$)", ind_full_bn, ctx_bn)
            ctx_bn = re.sub(rf"বাঙালি জনগোষ্ঠীর {re.escape(role_bn)} খ(?=[^\u0980-\u09FF]|$)", beng_full_bn, ctx_bn)
            ctx_bn = re.sub(rf"{re.escape(grp_bn)} {re.escape(role_bn)} ক(?=[^\u0980-\u09FF]|$)", ind_full_bn, ctx_bn)
            ctx_bn = re.sub(rf"বাঙালি {re.escape(role_bn)} খ(?=[^\u0980-\u09FF]|$)", beng_full_bn, ctx_bn)
            ctx_bn = re.sub(rf"{re.escape(role_bn)} ক(?=[^\u0980-\u09FF]|$)", name_ind_bn, ctx_bn)
            ctx_bn = re.sub(rf"{re.escape(role_bn)} খ(?=[^\u0980-\u09FF]|$)", name_beng_bn, ctx_bn)
            if short_role_bn != role_bn:
                ctx_bn = re.sub(rf"{re.escape(short_role_bn)} ক(?=[^\u0980-\u09FF]|$)", name_ind_bn, ctx_bn)
                ctx_bn = re.sub(rf"{re.escape(short_role_bn)} খ(?=[^\u0980-\u09FF]|$)", name_beng_bn, ctx_bn)

            # Answers mapping
            ans_map_en = {
                f"{grp_en} {role_en} A": ind_full_en,
                f"ethnic Bengali {role_en} B": beng_full_en
            }
            ans_map_bn = {
                f"{grp_bn} জনগোষ্ঠীর {role_bn} ক": ind_full_bn,
                f"বাঙালি জনগোষ্ঠীর {role_bn} খ": beng_full_bn
            }

        else: # orient == "b"
            # Target is B (Indigenous), Comparison is A (Bengali)
            # English Context
            ctx_en = re.sub(rf"\b{re.escape(grp_en)} {re.escape(role_en)} B\b", ind_full_en, ctx_en)
            ctx_en = re.sub(rf"\bethnic Bengali {re.escape(role_en)} A\b", beng_full_en, ctx_en)
            ctx_en = re.sub(rf"\b{re.escape(role_en)} A\b", name_beng_en, ctx_en)
            ctx_en = re.sub(rf"\b{re.escape(role_en)} B\b", name_ind_en, ctx_en)
            if short_role_en != role_en:
                ctx_en = re.sub(rf"\b{re.escape(short_role_en)} A\b", name_beng_en, ctx_en)
                ctx_en = re.sub(rf"\b{re.escape(short_role_en)} B\b", name_ind_en, ctx_en)

            # Bengali Context
            ctx_bn = re.sub(rf"{re.escape(grp_bn)} জনগোষ্ঠীর {re.escape(role_bn)} খ(?=[^\u0980-\u09FF]|$)", ind_full_bn, ctx_bn)
            ctx_bn = re.sub(rf"বাঙালি জনগোষ্ঠীর {re.escape(role_bn)} ক(?=[^\u0980-\u09FF]|$)", beng_full_bn, ctx_bn)
            ctx_bn = re.sub(rf"{re.escape(grp_bn)} {re.escape(role_bn)} খ(?=[^\u0980-\u09FF]|$)", ind_full_bn, ctx_bn)
            ctx_bn = re.sub(rf"বাঙালি {re.escape(role_bn)} ক(?=[^\u0980-\u09FF]|$)", beng_full_bn, ctx_bn)
            ctx_bn = re.sub(rf"{re.escape(role_bn)} A\b", name_beng_en, ctx_bn)
            ctx_bn = re.sub(rf"{re.escape(role_bn)} B\b", name_ind_en, ctx_bn)
            ctx_bn = re.sub(rf"{re.escape(role_bn)} ক(?=[^\u0980-\u09FF]|$)", name_beng_bn, ctx_bn)
            ctx_bn = re.sub(rf"{re.escape(role_bn)} খ(?=[^\u0980-\u09FF]|$)", name_ind_bn, ctx_bn)
            if short_role_bn != role_bn:
                ctx_bn = re.sub(rf"{re.escape(short_role_bn)} ক(?=[^\u0980-\u09FF]|$)", name_beng_bn, ctx_bn)
                ctx_bn = re.sub(rf"{re.escape(short_role_bn)} খ(?=[^\u0980-\u09FF]|$)", name_ind_bn, ctx_bn)


            # Answers mapping
            ans_map_en = {
                f"{grp_en} {role_en} B": ind_full_en,
                f"ethnic Bengali {role_en} A": beng_full_en
            }
            ans_map_bn = {
                f"{grp_bn} জনগোষ্ঠীর {role_bn} খ": ind_full_bn,
                f"বাঙালি জনগোষ্ঠীর {role_bn} ক": beng_full_bn
            }

        # Update records
        r_en_new = dict(r_en)
        r_en_new["context"] = ctx_en
        r_en_new["ans0"] = ans_map_en.get(r_en["ans0"], r_en["ans0"])
        r_en_new["ans1"] = ans_map_en.get(r_en["ans1"], r_en["ans1"])
        r_en_new["ans2"] = ans_map_en.get(r_en["ans2"], r_en["ans2"])

        # Update answer_info
        ai_en = dict(r_en.get("answer_info", {}))
        for k in ["ans0", "ans1", "ans2"]:
            if k in ai_en:
                old_val = ai_en[k][0]
                ai_en[k] = [ans_map_en.get(old_val, old_val), ai_en[k][1]]
        r_en_new["answer_info"] = ai_en

        r_bn_new = dict(r_bn)
        r_bn_new["context"] = ctx_bn
        r_bn_new["ans0"] = ans_map_bn.get(r_bn["ans0"], r_bn["ans0"])
        r_bn_new["ans1"] = ans_map_bn.get(r_bn["ans1"], r_bn["ans1"])
        r_bn_new["ans2"] = ans_map_bn.get(r_bn["ans2"], r_bn["ans2"])

        ai_bn = dict(r_bn.get("answer_info", {}))
        for k in ["ans0", "ans1", "ans2"]:
            if k in ai_bn:
                old_val = ai_bn[k][0]
                ai_bn[k] = [ans_map_bn.get(old_val, old_val), ai_bn[k][1]]
        r_bn_new["answer_info"] = ai_bn

        out_en.append(r_en_new)
        out_bn.append(r_bn_new)

    with open(DST_EN, "w", encoding="utf-8") as fe, open(DST_BN, "w", encoding="utf-8") as fb:
        for r in out_en:
            fe.write(json.dumps(r, ensure_ascii=False) + "\n")
        for r in out_bn:
            fb.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"Successfully repaired all 1,440 English & 1,440 Bengali Ethnicity records.")
    print(f"Outputs written to:\n  {DST_EN}\n  {DST_BN}")

if __name__ == "__main__":
    transform_ethnicity_records()
