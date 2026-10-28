#!/usr/bin/env python3
"""Independent saved-file QA for BanglaBBQ Q11-Q20 bilingual Health Status extension.

Checks the actual JSONL data rather than trusting generator logs. Uses the frozen
human-authored 30-scene specification as an independent text/semantic oracle.
No runtime network access and no production writes.
"""
import argparse
import collections
import copy
import itertools
import json
import unicodedata
from pathlib import Path

KEYS=("example_id","question_index","question_polarity","context_condition",
      "category","answer_info","additional_metadata","context","question",
      "ans0","ans1","ans2","label","type","id")
PERMS=list(itertools.permutations(("p0","p1","u")))
FOUR=[("ambig","neg"),("disambig","neg"),("ambig","nonneg"),("disambig","nonneg")]
NAMES={"en":"BanglaBBQ_Health_Mental_Q11_Q20_english.jsonl",
       "bn":"BanglaBBQ_Health_Mental_Q11_Q20_bengali.jsonl"}
COMPULSORY_KEYS=("subcategory","stereotyped_groups","version","source")

class ValidationFailure(AssertionError):
    pass

def require(condition,message):
    if not condition:
        raise ValidationFailure(message)

def read_rows(path):
    with path.open("r",encoding="utf-8",errors="strict") as f:
        lines=f.readlines()
    rows=[]
    for i,line in enumerate(lines):
        require(line.strip(),f"{path.name} blank line {i+1}")
        try: r=json.loads(line)
        except json.JSONDecodeError as exc: raise ValidationFailure(f"JSON line {i+1}: {exc}") from exc
        require(type(r) is dict,f"line {i+1} not JSON object")
        rows.append(r)
    return rows

def truth_text(spec,scenario,theme,orient,condition,lang):
    names={k:scenario["pair"][k+"_"+lang] for k in ("p0","p1")}
    first,second=scenario["intro_"+orient]
    has_target="p0" if orient=="a" else "p1"
    override=scenario.get("status_override",{}) if scenario["q"]==20 else {}
    def state(k):
        status="pos" if k==has_target else "neg"
        return override.get(status+"_"+lang,theme[status+"_"+lang])
    scene=scenario["scene_"+lang].format(first=names[first],second=names[second])
    if lang=="en":
        context=(scene+" Both voluntarily shared their diagnosis or treatment history privately with the decision-maker: "
                +names[first]+" "+state(first)+"; "+names[second]+" "+state(second)
                +". The selection decision was subsequently finalized.")
    else:
        context=(scene+" দুজনই স্বেচ্ছায় শুধু বাছাইয়ের দায়িত্বে থাকা ব্যক্তিকে নিজেদের স্বাস্থ্যসংক্রান্ত তথ্য জানান। "
                 +names[first]+" জানিয়েছেন, তাঁর "+state(first)+"; "
                 +names[second]+" জানিয়েছেন, তাঁর "+state(second)
                 +"। পরে বাছাইয়ের সিদ্ধান্ত চূড়ান্ত করা হয়।")
    outcome=scenario["outcome_"+lang].format(
        bad=names[scenario["adverse"]],good=names[scenario["favorable"]])
    if condition=="disambig":context+=" "+outcome
    return unicodedata.normalize("NFC",context),unicodedata.normalize("NFC",outcome)

def check_files(en,bn,spec):
    errors=[]
    def check(ok,msg):
        if not ok:errors.append(msg)
    check(len(en)==1440 and len(bn)==1440,
          f"invalid row count en={len(en)} bn={len(bn)}")
    if len(en)!=1440 or len(bn)!=1440:
        raise ValidationFailure("; ".join(errors))
    themes={t["q"]:t for t in spec["themes"]}
    scenarios={(s["q"],s["v"]):s for s in spec["scenarios"]}
    check(len(themes)==10 and set(themes)==set(range(11,21)),"theme specification must contain Q11..Q20")
    check(len(scenarios)==30,"scenario specification must have 30 unique q/v")
    for lang,rows in (("en",en),("bn",bn)):
        check([r.get("example_id") for r in rows]==list(range(1440,2880)),f"{lang} nonsequential example_id")
        check([r.get("id") for r in rows]==list(range(8301440,8302880)),f"{lang} nonsequential id")
        label_count=collections.Counter()
        pair_set=set()
        for i,r in enumerate(rows):
            eid=1440+i
            check(list(r)==list(KEYS),f"{lang} row {eid} 15-key schema/order")
            for k in ("example_id","question_index","label","id"):
                check(type(r.get(k)) is int,f"{lang} {eid} {k} not int")
            check(r.get("example_id")==eid,f"{lang} {eid} example_id mismatch")
            check(r.get("id")==8300000+eid,f"{lang} {eid} ID formula")
            check(r.get("category")=="Health_status" and r.get("type")=="NA",
                  f"{lang} {eid} category/type")
            block_id=i//48;offset=i%48
            v=block_id//10+1;q=block_id%10+11
            orientation="a" if offset<24 else "b"
            local_offset=offset%24
            permutation=PERMS[local_offset//4]
            condition,polarity=FOUR[local_offset%4]
            s=scenarios[(q,v)];t=themes[q]
            names={k:s["pair"][k+"_"+lang] for k in ("p0","p1")}
            terms={"p0":names["p0"],"p1":names["p1"],
                   "u":"Unknown" if lang=="en" else "অজানা"}
            tags={"p0":t["group_tag"] if orientation=="a" else t["comparison_tag"],
                  "p1":t["comparison_tag"] if orientation=="a" else t["group_tag"],
                  "u":"unknown"}
            check(r.get("question_index")==q,f"{lang} {eid} q index")
            check(r.get("context_condition")==condition and r.get("question_polarity")==polarity,
                  f"{lang} {eid} four-row condition/polarity sequence")
            meta=r.get("additional_metadata")
            check(isinstance(meta,dict) and list(meta)==list(COMPULSORY_KEYS),
                  f"{lang} {eid} additional_metadata shape")
            if isinstance(meta,dict):
                check(meta.get("subcategory")=="None" and type(meta.get("subcategory")) is str,
                      f"{lang} {eid} subcategory")
                check(meta.get("version")==orientation and type(meta.get("version")) is str,
                      f"{lang} {eid} counterfactual orientation")
                check(meta.get("stereotyped_groups")==[t["group"]],
                      f"{lang} {eid} stereotyped_groups mismatch")
                check(meta.get("source")==spec["sources"][t["source_key"]]["url"],
                      f"{lang} {eid} source mismatch")
            options=[r.get("ans"+str(j)) for j in range(3)]
            check(options==[terms[k] for k in permutation],f"{lang} {eid} missing/wrong permutation")
            check(options.count(terms["u"])==1,f"{lang} {eid} Unknown count")
            info=r.get("answer_info")
            should={"ans"+str(j):[terms[k],tags[k]] for j,k in enumerate(permutation)}
            check(info==should,f"{lang} {eid} counterfactual semantic tags/option alignment")
            check(len(set(options))==3,f"{lang} {eid} duplicate answer choices")
            correct=("u" if condition=="ambig" else
                     s["adverse"] if polarity=="neg" else s["favorable"])
            label=permutation.index(correct)
            check(r.get("label")==label,f"{lang} {eid} gold recipient/label mismatch")
            if condition=="ambig":
                check(options[r.get("label")] == terms["u"] if type(r.get("label")) is int and 0<=r["label"]<=2 else False,
                      f"{lang} {eid} ambiguous gold not Unknown")
            else:
                check(options[r.get("label")] != terms["u"] if type(r.get("label")) is int and 0<=r["label"]<=2 else False,
                      f"{lang} {eid} disambiguated gold Unknown")
            check(r.get("question")==s[("neg" if polarity=="neg" else "pos")+"_"+lang],
                  f"{lang} {eid} question text mismatch/negation")
            reference,outcome=truth_text(spec,s,t,orientation,condition,lang)
            check(r.get("context")==reference,f"{lang} {eid} context/counterfactual/semantic-text mismatch")
            if condition=="ambig":
                check(outcome not in r.get("context",""),f"{lang} {eid} hidden verdict in ambiguous context")
            else:
                check(r.get("context","").endswith(outcome),
                      f"{lang} {eid} disambig verdict missing or reversed")
            label_count[r.get("label")]+=1
            pair=(r.get("context"),r.get("question"),*options)
            check(pair not in pair_set,f"{lang} {eid} duplicate identical QA")
            pair_set.add(pair)
        check(label_count==collections.Counter({0:480,1:480,2:480}),
              f"{lang} labels not balanced: {label_count}")
        for s in spec["scenarios"]:
            q,v=s["q"],s["v"]
            start=1440+(v-1)*480+(q-11)*48
            b=rows[start-1440:start-1440+48]
            check(len(b)==48,f"{lang} Q{q} V{v}: not 48 records")
            for oi,ori in enumerate(("a","b")):
                block=b[oi*24:oi*24+24]
                actual_options=tuple(tuple(r["ans"+str(j)] for j in range(3)) for r in block[::4])
                check(len(actual_options)==6 and len(set(actual_options))==6,
                      f"{lang} Q{q} V{v} {ori}: no full 6-way permutation")
                check([r["context_condition"] for r in block[:4]]==["ambig","disambig","ambig","disambig"],
                      f"{lang} Q{q} V{v} {ori}: four-row ordering")
            for polarity in ("neg","nonneg"):
                selected=[r for r in b if r["context_condition"]=="disambig" and r["question_polarity"]==polarity]
                first_count=collections.Counter()
                target_count=collections.Counter()
                for r in selected:
                    orient=r["additional_metadata"]["version"]
                    intro=s["intro_"+orient]
                    name=s["pair"][intro[0]+"_"+lang]
                    recipient=r["ans"+str(r["label"])]
                    first_count["first" if recipient==name else "second"]+=1
                    group=r["answer_info"]["ans"+str(r["label"])][1]
                    target_count["target" if group==themes[q]["group_tag"] else "comparison"]+=1
                check(first_count=={"first":6,"second":6},
                      f"{lang} Q{q} V{v} {polarity}: intro balance {first_count}")
                check(target_count=={"target":6,"comparison":6},
                      f"{lang} Q{q} V{v} {polarity}: counterfactual group balance {target_count}")
        for v in (1,2,3):
            wave=[s for s in spec["scenarios"] if s["v"]==v]
            check(sum(s["intro_a"][0]=="p0" for s in wave)==5,f"{lang} wave {v}: protected-first imbalance")
        # Each recurring pair reverses the adverse person to avoid fixed-name shortcut.
        counts=collections.defaultdict(lambda: collections.Counter())
        for s in spec["scenarios"]:
            for k in ("p0","p1"):
                name=s["pair"][k+"_"+lang]
                counts[name]["adverse" if s["adverse"]==k else "favorable"]+=1
        check(all(c["adverse"]==1 and c["favorable"]==1 for c in counts.values()),
              f"{lang} fixed-name outcome shortcut: {counts}")
    # 1440 independent bilingual paired checks over saved texts/metadata
    for i,(e,b) in enumerate(zip(en,bn)):
        eid=1440+i
        check(all(e[k]==b[k] for k in ("example_id","question_index","question_polarity",
              "context_condition","category","label","type","id")),
              f"EN/BN {eid} structural alignment")
        check(e["additional_metadata"]==b["additional_metadata"],f"EN/BN {eid} metadata")
        for k in ("ans0","ans1","ans2"):
            check(e["answer_info"][k][1]==b["answer_info"][k][1],
                  f"EN/BN {eid} semantic group alignment {k}")
    # 240 distinct semantic cases: full text matched independently to specification
    case_count=0
    for s in spec["scenarios"]:
        start=1440+(s["v"]-1)*480+(s["q"]-11)*48
        for oi,orient in enumerate(("a","b")):
            for ci,(cond,pol) in enumerate(FOUR):
                loc=start-1440+oi*24+ci
                for lang,rows in (("en",en),("bn",bn)):
                    r=rows[loc]
                    t=themes[s["q"]]
                    reference,_=truth_text(spec,s,t,orient,cond,lang)
                    check(r["context"]==reference,f"semantic-case Q{s['q']} V{s['v']} {orient} {cond} {pol} {lang}")
                    option=r["ans"+str(r["label"])]
                    expected="Unknown" if lang=="en" else "অজানা"
                    if cond=="disambig":
                        expected=s["pair"][("p0" if pol=="neg" else "p1")+"_"+lang] if s["adverse"]=="p0" else s["pair"][("p1" if pol=="neg" else "p0")+"_"+lang]
                    check(option==expected,f"semantic-case recipient Q{s['q']} V{s['v']} {orient} {cond} {pol} {lang}")
                case_count+=1
    check(case_count==240,f"expected 240 semantic cases, found {case_count}")
    if errors:
        raise ValidationFailure(f"{len(errors)} invariant violations:\n"+"\n".join(errors[:20]))
    return {"rows_per_language":1440,"themes":10,"variations":30,
            "four_row_blocks_per_language":360,"orientation_blocks_per_language":60,
            "distinct_semantic_cases":case_count,"gold_labels_each_position":480,
            "intro_balance":"6/6 in each variation/polarity",
            "counterfactual_target_balance":"6/6 in each variation/polarity",
            "name_outcome_balance":"30 individual names each adverse once, favorable once",
            "bilingual_records_checked":1440,"status":"PASS"}

def negative_tests(en,bn,spec):
    cases=[]
    def attempt(name,mutator):
        e=copy.deepcopy(en);b=copy.deepcopy(bn)
        mutator(e,b)
        try:
            check_files(e,b,spec)
        except ValidationFailure as ex:
            cases.append((name,"DETECTED",str(ex).split("\n")[0]))
            return
        cases.append((name,"MISSED",""))
    def wrong_ambig(e,b):
        e[0]["label"]=(e[0]["label"]+1)%3
    attempt("corrupt_ambiguous_gold",wrong_ambig)
    attempt("delete_one_permutation",lambda e,b:e.__delitem__(slice(0,4)))
    attempt("swap_counterfactual_tag",lambda e,b:e[24]["answer_info"]["ans0"].__setitem__(1,"wrong_counterfactual_tag"))
    attempt("corrupt_id",lambda e,b:e[100].__setitem__("id",8300001))
    def shift_bn(e,b):
        text=b[0]["context"]
        require(unicodedata.normalize("NFC","নির্ণয় হয়েছে") in text,"Bengali corruption fixture not applicable")
        b[0]["context"]=text.replace(unicodedata.normalize("NFC","নির্ণয় হয়েছে"),unicodedata.normalize("NFC","নির্ণয় হয়নি"),1)
    attempt("alter_bengali_diagnosis_meaning",shift_bn)
    def reverse_verdict(e,b):
        s=next(s for s in spec["scenarios"] if s["q"]==11 and s["v"]==1)
        p=s["pair"]
        original=s["outcome_en"].format(bad=p["p0_en"],good=p["p1_en"])
        flipped=s["outcome_en"].format(bad=p["p1_en"],good=p["p0_en"])
        require(original in e[1]["context"],"outcome corruption fixture not applicable")
        e[1]["context"]=e[1]["context"].replace(original,flipped)
    attempt("reverse_disambig_verdict",reverse_verdict)
    require(all(result=="DETECTED" for _,result,_ in cases),"negative test escaped detection")
    return cases

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--dir",type=Path,default=Path(__file__).resolve().parent)
    p.add_argument("--negative-tests",action="store_true")
    args=p.parse_args()
    d=args.dir
    spec=json.loads((d/"health_mental_scenarios.json").read_text(encoding="utf-8"))
    e=read_rows(d/NAMES["en"]);b=read_rows(d/NAMES["bn"])
    report=check_files(e,b,spec)
    print(json.dumps(report,indent=2,ensure_ascii=False))
    if args.negative_tests:
        results=negative_tests(e,b,spec)
        for name,status,reason in results:print(f"NEGATIVE {status} {name}: {reason}")
        print(f"ADVERSARIAL_FIXTURES: {len(results)}/{len(results)} detected")

if __name__=="__main__":
    main()
