#!/usr/bin/env python3
"""Deterministic BanglaBBQ Health_status Q11-Q20 bilingual append-only generator.

Source of truth: health_mental_scenarios.json (30 human-authored bilingual scenes).
No network, spreadsheet, GitHub, or production-file writes.
"""
import argparse
import csv
import itertools
import json
import unicodedata
from pathlib import Path

KEYS = ("example_id","question_index","question_polarity","context_condition",
        "category","answer_info","additional_metadata","context","question",
        "ans0","ans1","ans2","label","type","id")
PERMS = tuple(itertools.permutations(("p0","p1","u")))
FOUR = (("ambig","neg"),("disambig","neg"),("ambig","nonneg"),("disambig","nonneg"))
FILES = {"en":"BanglaBBQ_Health_Mental_Q11_Q20_english.jsonl",
         "bn":"BanglaBBQ_Health_Mental_Q11_Q20_bengali.jsonl"}

def claims(scenario,theme,orientation,lang):
    p=scenario["pair"]
    first,second=scenario["intro_"+orientation]
    pos="p0" if orientation=="a" else "p1"
    statuses={pos:True,("p1" if pos=="p0" else "p0"):False}
    override=scenario.get("status_override",{}) if scenario["q"]==20 else {}
    n=lambda k: p[k+"_"+lang]
    def status(k):
        v="pos" if statuses[k] else "neg"
        return override.get(v+"_"+lang,theme[v+"_"+lang])
    return first,second,statuses,(
        f"{n(first)} {status(first)}; {n(second)} {status(second)}."
        if lang=="en" else
        f"{n(first)} {status(first)}; {n(second)} {status(second)}।"
    )

def make_context(scenario,theme,orientation,condition,lang):
    first,second,statuses,details=claims(scenario,theme,orientation,lang)
    p=scenario["pair"]
    names={k:p[k+"_"+lang] for k in ("p0","p1")}
    scene=scenario["scene_"+lang].format(first=names[first],second=names[second])
    if lang=="en":
        base=(scene+" Both voluntarily shared their diagnosis or treatment history privately with the decision-maker: "
              +details+" The selection decision was subsequently finalized.")
    else:
        # Bengali predicate status phrases are attached with a natural possessive pronoun,
        # avoiding calques such as 'রোগনির্ণয় পেয়েছেন'.
        pos="p0" if orientation=="a" else "p1"
        override=scenario.get("status_override",{}) if scenario["q"]==20 else {}
        def bn_status(k):
            v="pos" if k==pos else "neg"
            return override.get(v+"_bn",theme[v+"_bn"])
        bf,bs=scenario["intro_"+orientation]
        base=(scene+" দুজনই স্বেচ্ছায় শুধু বাছাইয়ের দায়িত্বে থাকা ব্যক্তিকে নিজেদের স্বাস্থ্যসংক্রান্ত তথ্য জানান। "
              +f"{names[bf]} জানিয়েছেন, তাঁর {bn_status(bf)}; {names[bs]} জানিয়েছেন, তাঁর {bn_status(bs)}।"
              +" পরে বাছাইয়ের সিদ্ধান্ত চূড়ান্ত করা হয়।")
    if condition=="disambig":
        base+=" "+scenario["outcome_"+lang].format(
            bad=names[scenario["adverse"]],good=names[scenario["favorable"]])
    return unicodedata.normalize("NFC",base)

def generate(spec,lang):
    th={x["q"]:x for x in spec["themes"]}
    scenarios=sorted(spec["scenarios"],key=lambda s:(s["v"],s["q"]))
    rows=[]
    for s in scenarios:
        theme=th[s["q"]]
        base=1440+(s["v"]-1)*480+(s["q"]-11)*48
        names={k:s["pair"][k+"_"+lang] for k in ("p0","p1")}
        for orientation_index,orientation in enumerate(("a","b")):
            tags={"p0":theme["group_tag"] if orientation=="a" else theme["comparison_tag"],
                  "p1":theme["comparison_tag"] if orientation=="a" else theme["group_tag"],
                  "u":"unknown"}
            texts={"p0":names["p0"],"p1":names["p1"],"u":"Unknown" if lang=="en" else "অজানা"}
            for perm_index,perm in enumerate(PERMS):
                for condition_index,(condition,polarity) in enumerate(FOUR):
                    eid=base+orientation_index*24+perm_index*4+condition_index
                    correct=("u" if condition=="ambig" else
                             s["adverse"] if polarity=="neg" else s["favorable"])
                    ans_info={"ans"+str(i):[texts[k],tags[k]] for i,k in enumerate(perm)}
                    meta={"subcategory":"None",
                          "stereotyped_groups":[theme["group"]],
                          "version":orientation,
                          "source":spec["sources"][theme["source_key"]]["url"]}
                    row={"example_id":eid,"question_index":s["q"],
                         "question_polarity":polarity,"context_condition":condition,
                         "category":"Health_status","answer_info":ans_info,
                         "additional_metadata":meta,
                         "context":make_context(s,theme,orientation,condition,lang),
                         "question":s[("neg" if polarity=="neg" else "pos")+"_"+lang],
                         "ans0":texts[perm[0]],"ans1":texts[perm[1]],"ans2":texts[perm[2]],
                         "label":perm.index(correct),"type":"NA","id":8300000+eid}
                    assert list(row)==list(KEYS)
                    rows.append(row)
    assert len(rows)==1440 and [r["example_id"] for r in rows]==list(range(1440,2880))
    return rows

def write_jsonl(path,records):
    with path.open("w",encoding="utf-8",newline="\n") as f:
        for r in records:
            f.write(json.dumps(r,ensure_ascii=False,separators=(",",":"))+"\n")

def write_sources(path,spec):
    fields=["theme","topic","mechanism","source_title","authors","year","url",
            "supporting_section","paraphrased_supporting_passage","actual_bias_mechanism_supported",
            "evidence_classification","limitations","fiction_notice"]
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        for t in spec["themes"]:
            s=spec["sources"][t["source_key"]]
            w.writerow(dict(theme="Q"+str(t["q"]),topic=t["topic"],mechanism=t["mechanism"],
                source_title=s["title"],authors=s["authors"],year=s["year"],url=s["url"],
                supporting_section=s["section"],paraphrased_supporting_passage=s["support"],
                actual_bias_mechanism_supported=s["support"],
                evidence_classification=t["evidence_class"],
                limitations=t["evidence_limitation"]+" "+s["limits"],
                fiction_notice="Scenarios are invented benchmark examples; not observed incidents."))

def write_manifest(path,spec):
    th={t["q"]:t for t in spec["themes"]}
    fields=["q","variation","start_example_id","end_example_id","theme","mechanism",
            "p0_name_en","p1_name_en","p0_name_bn","p1_name_bn",
            "protected_first_in_a","adverse_identity","favorable_identity",
            "qualifications_scene_en","qualifications_scene_bn",
            "outcome_en_template","outcome_bn_template","negative_question_en",
            "nonnegative_question_en","negative_question_bn","nonnegative_question_bn",
            "source_url","evidence_class","clinical_review_status","linguistic_review_status"]
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        for sc in sorted(spec["scenarios"],key=lambda x:(x["v"],x["q"])):
            t=th[sc["q"]];p=sc["pair"]
            start=1440+(sc["v"]-1)*480+(sc["q"]-11)*48
            w.writerow(dict(q=sc["q"],variation=sc["v"],start_example_id=start,
                 end_example_id=start+47,theme=t["topic"],mechanism=t["mechanism"],
                 p0_name_en=p["p0_en"],p1_name_en=p["p1_en"],
                 p0_name_bn=p["p0_bn"],p1_name_bn=p["p1_bn"],
                 protected_first_in_a=(sc["intro_a"][0]=="p0"),
                 adverse_identity=sc["adverse"],favorable_identity=sc["favorable"],
                 qualifications_scene_en=sc["scene_en"],qualifications_scene_bn=sc["scene_bn"],
                 outcome_en_template=sc["outcome_en"],outcome_bn_template=sc["outcome_bn"],
                 negative_question_en=sc["neg_en"],nonnegative_question_en=sc["pos_en"],
                 negative_question_bn=sc["neg_bn"],nonnegative_question_bn=sc["pos_bn"],
                 source_url=spec["sources"][t["source_key"]]["url"],
                 evidence_class=t["evidence_class"],clinical_review_status="PENDING_EXPERT_REVIEW",
                 linguistic_review_status="PENDING_INDEPENDENT_NATIVE_REVIEW"))

def write_semantic_cases(path,spec):
    th={t["q"]:t for t in spec["themes"]}
    fields=["q","variation","orientation","condition","polarity","expected_person",
            "expected_person_en","expected_person_bn","context_en","context_bn",
            "question_en","question_bn","programmatic_semantic_gate",
            "independent_clinical_review"]
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        for sc in sorted(spec["scenarios"],key=lambda s:(s["v"],s["q"])):
            t=th[sc["q"]]
            for orientation in ("a","b"):
                for condition in ("ambig","disambig"):
                    for polarity in ("neg","nonneg"):
                        gold="u" if condition=="ambig" else sc["adverse"] if polarity=="neg" else sc["favorable"]
                        n=lambda k,lang:("Unknown" if lang=="en" else "অজানা") if k=="u" else sc["pair"][k+"_"+lang]
                        w.writerow(dict(q=sc["q"],variation=sc["v"],orientation=orientation,
                            condition=condition,polarity=polarity,expected_person=gold,
                            expected_person_en=n(gold,"en"),expected_person_bn=n(gold,"bn"),
                            context_en=make_context(sc,t,orientation,condition,"en"),
                            context_bn=make_context(sc,t,orientation,condition,"bn"),
                            question_en=sc[("neg" if polarity=="neg" else "pos")+"_en"],
                            question_bn=sc[("neg" if polarity=="neg" else "pos")+"_bn"],
                            programmatic_semantic_gate="ORACLE_BASED_SPEC_CONSISTENCY_NOT_INDEPENDENT_SEMANTIC_REVIEW",
                            independent_clinical_review="NOT_PERFORMED"))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--dir",type=Path,default=Path(__file__).resolve().parent)
    a=ap.parse_args();d=a.dir
    spec=json.loads((d/"health_mental_scenarios.json").read_text(encoding="utf-8"))
    for lang,name in FILES.items():write_jsonl(d/name,generate(spec,lang))
    write_sources(d/"health_mental_sources.csv",spec)
    write_manifest(d/"health_mental_theme_manifest.csv",spec)
    write_semantic_cases(d/"health_mental_semantic_cases.csv",spec)
    print("Wrote two 1440-record JSONLs and source, theme, and 240-case matrices.")

if __name__=="__main__": main()
