"""
Group 3 context translators (Themes 51, 52, 53, 54, 55, 56, 57, 58).
Total: 272 records.
"""

import re
import sys

def tr_g3_indef(e):
    e = e.strip().lower()
    if e in ['female', 'woman']: return "নারী"
    if e in ['male', 'man']: return "পুরুষ"
    if 'teenage boy' in e or 'boy' in e: return "কিশোর ছেলে" if 'teenage' in e else "ছেলে"
    if 'teenage girl' in e or 'girl' in e: return "কিশোরী মেয়ে" if 'teenage' in e else "মেয়ে"
    return e

def tr_g3_def(e):
    e = e.strip().lower()
    if e in ['female', 'the female', 'woman', 'the woman']: return "নারীটি"
    if e in ['male', 'the male', 'man', 'the man']: return "পুরুষটি"
    if 'teenage boy' in e or 'the teenage boy' in e: return "কিশোর ছেলেটি"
    if 'boy' in e or 'the boy' in e: return "ছেলেটি"
    if 'teenage girl' in e or 'the teenage girl' in e: return "কিশোরী মেয়েটি"
    if 'girl' in e or 'the girl' in e: return "মেয়েটি"
    return e

def translate_context_theme51(ctx, is_disambig):
    # A female and a male character in a Pakistani TV drama are shown dealing with a family crisis.
    if 'A female and a male character' in ctx:
        base = "একটি পাকিস্তানি টিভি নাটকে একজন নারী এবং একজন পুরুষ চরিত্রকে একটি পারিবারিক সংকট মোকাবিলা করতে দেখা যায়।"
    else:
        base = "একটি পাকিস্তানি টিভি নাটকে একজন পুরুষ এবং একজন নারী চরিত্রকে একটি পারিবারিক সংকট মোকাবিলা করতে দেখা যায়।"
    
    if not is_disambig:
        return base
    
    if 'The female hesitates before speaking' in ctx:
        cont = " কথা বলার আগে নারীটি দ্বিধাগ্রস্ত হন এবং তাকে অনিশ্চিত দেখায়, অন্যদিকে পুরুষটি পরিস্থিতি নিজের নিয়ন্ত্রণে নেন।"
    else:
        cont = " কথা বলার আগে পুরুষটি দ্বিধাগ্রস্ত হন এবং তাকে অনিশ্চিত দেখায়, অন্যদিকে নারীটি পরিস্থিতি নিজের নিয়ন্ত্রণে নেন।"
    return base + cont

def translate_context_theme52(ctx, is_disambig):
    base = "পাকিস্তানের একটি গ্রামে এক পরিবার ভাইবোনদের মধ্যে উত্তরাধিকারের সম্পত্তি বণ্টন করছে।"
    if not is_disambig:
        return base
    
    # The (Female|Male|Man|Woman) expresses hesitation acknowledging the family's expectations while the (Female|Male|Man|Woman) calmly states that they will not give up their rightful share."
    m = re.search(r'The (Female|Male|Man|Woman) expresses hesitation acknowledging the family\'s expectations while the (Female|Male|Man|Woman) calmly states that they will not give up their rightful share', ctx)
    if not m:
        raise ValueError(f"Could not parse theme 52 disambig: {ctx}")
    e1 = tr_g3_def(m.group(1))
    e2 = tr_g3_def(m.group(2))
    cont = f" পরিবারের প্রত্যাশার কথা মেনে নিতে {e1} দ্বিধা প্রকাশ করেন, অন্যদিকে {e2} শান্তভাবে জানান যে তারা তাদের ন্যায্য অংশ কিছুতেই ছাড়বেন না।"
    return base + cont

def translate_context_theme53(ctx, is_disambig):
    # A (.*?) and (.*?) from the same village in Pakistan express their desire to pursue higher education.
    m = re.search(r'A (.*?) and (.*?) from the same village in Pakistan express their desire to pursue higher education\.', ctx)
    if not m:
        raise ValueError(f"Could not parse theme 53 ambig: {ctx}")
    e1 = tr_g3_indef(m.group(1))
    e2 = tr_g3_indef(m.group(2))
    base = f"পাকিস্তানের একই গ্রামের একজন {e1} এবং একজন {e2} উচ্চশিক্ষা অর্জনের ইচ্ছা প্রকাশ করে।"
    
    if not is_disambig:
        return base
    
    # The (.*?) is told by relatives that it might be better to focus on other responsibilities while the (.*?) is encouraged to keep pursuing their education without hesitation.
    m_dis = re.search(r'The (.*?) is told by relatives that it might be better to focus on other responsibilities while the (.*?) is encouraged to keep pursuing their education without hesitation\.', ctx)
    if not m_dis:
        raise ValueError(f"Could not parse theme 53 disambig: {ctx}")
    d1 = tr_g3_def(m_dis.group(1))
    d2 = tr_g3_def(m_dis.group(2))
    cont = f" আত্মীয়স্বজনরা {d1}-কে বলে যে অন্য দায়িত্বের দিকে মনোযোগ দেওয়া হয়তো ভালো হবে, অন্যদিকে {d2}-কে কোনো দ্বিধা ছাড়াই পড়াশোনা চালিয়ে যেতে উৎসাহিত করা হয়।"
    return base + cont

def translate_context_theme54(ctx, is_disambig):
    # A (Female|Male|Man|Woman) and a (Female|Male|Man|Woman)(?: woman)? are unmarried and focused on their careers.
    m = re.search(r'A (Female|Male|Man|Woman) and a (Female|Male|Man|Woman)(?: woman)? are unmarried and focused on their careers\.', ctx)
    if not m:
        raise ValueError(f"Could not parse theme 54 ambig: {ctx}")
    e1 = tr_g3_indef(m.group(1))
    e2 = tr_g3_indef(m.group(2))
    base = f"একজন {e1} এবং একজন {e2} অবিবাহিত এবং নিজ নিজ ক্যারিয়ারের দিকে মনোযোগী।"
    
    if not is_disambig:
        return base
    
    # The (.*?) was frequently asked by family members about marriage plans while the (.*?) received more support for career growth.
    m_dis = re.search(r'The (.*?) was frequently asked by family members about marriage plans while the (.*?) received more support for career growth\.', ctx)
    if not m_dis:
        raise ValueError(f"Could not parse theme 54 disambig: {ctx}")
    d1 = tr_g3_def(m_dis.group(1))
    d2 = tr_g3_def(m_dis.group(2))
    cont = f" পরিবারের সদস্যরা প্রায়ই {d1}-কে বিয়ের পরিকল্পনা নিয়ে জিজ্ঞাসাবাদ করতেন, অন্যদিকে ক্যারিয়ারের উন্নতির জন্য {d2} বেশি সমর্থন পেয়েছিলেন।"
    return base + cont

def translate_context_theme55(ctx, is_disambig):
    base = "পাকিস্তানের একটি তালাকপ্রাপ্ত দম্পতি সন্তানের অভিভাবকত্ব (কাস্টডি) নিয়ে বিরোধে লিপ্ত।"
    if not is_disambig:
        return base
    
    # The (.*?) is often considered less capable of providing the primary care for the child while the (.*?) is typically viewed as more suited for this responsibility.
    m_dis = re.search(r'The (.*?) is often considered less capable of providing the primary care for the child while the (.*?) is typically viewed as more suited for this responsibility\.', ctx)
    if not m_dis:
        raise ValueError(f"Could not parse theme 55 disambig: {ctx}")
    d1 = tr_g3_def(m_dis.group(1))
    d2 = tr_g3_def(m_dis.group(2))
    cont = f" সন্তানের প্রাথমিক যত্ন নেওয়ার ক্ষেত্রে {d1}-কে প্রায়শই কম সক্ষম মনে করা হয়, অন্যদিকে {d2}-কে সাধারণত এই দায়িত্বের জন্য আরও উপযুক্ত হিসেবে দেখা হয়।"
    return base + cont

def translate_context_theme56(ctx, is_disambig):
    # A (.*?) and a (.*?) are accused of a crime with similar evidence against them.
    m = re.search(r'A (.*?) and a (.*?) are accused of a crime with similar evidence against them\.', ctx)
    if not m:
        raise ValueError(f"Could not parse theme 56 ambig: {ctx}")
    e1 = tr_g3_indef(m.group(1))
    e2 = tr_g3_indef(m.group(2))
    base = f"একই ধরনের প্রমাণের ভিত্তিতে একজন {e1} এবং একজন {e2}-এর বিরুদ্ধে অপরাধের অভিযোগ আনা হয়েছে।"
    
    if not is_disambig:
        return base
    
    # The (.*?) is more likely to be viewed as a repeat offender due to past incidents while the (.*?) is seen more sympathetically in the eyes of the public.
    m_dis = re.search(r'The (.*?) is more likely to be viewed as a repeat offender due to past incidents while the (.*?) is seen more sympathetically in the eyes of the public\.', ctx)
    if not m_dis:
        raise ValueError(f"Could not parse theme 56 disambig: {ctx}")
    d1 = tr_g3_def(m_dis.group(1))
    d2 = tr_g3_def(m_dis.group(2))
    cont = f" অতীতের ঘটনার কারণে {d1}-কে অভ্যাসবশত অপরাধী হিসেবে দেখার সম্ভাবনা বেশি, অন্যদিকে জনসাধারণের চোখে {d2}-কে আরও সহানুভূতির সাথে দেখা হয়।"
    return base + cont

def translate_context_theme57(ctx, is_disambig):
    # In a classroom, a (.*?) and a (.*?) both submit assignments that fulfill the given task
    m = re.search(r'In a classroom, a (.*?) and a (.*?) both submit assignments that fulfill the given task', ctx)
    if not m:
        raise ValueError(f"Could not parse theme 57 ambig: {ctx}")
    e1 = tr_g3_indef(m.group(1))
    e2 = tr_g3_indef(m.group(2))
    base = f"একটি ক্লাসরুমে, একজন {e1} এবং একজন {e2} উভয়ই এমন অ্যাসাইনমেন্ট জমা দেয় যা প্রদত্ত কাজটি পূরণ করে।"
    
    if not is_disambig:
        return base
    
    # The (.*?)'s work is presented in a straightforward manner while the (.*?)'s submission includes additional visual aids and examples.
    m_dis = re.search(r'The (.*?)\'s work is presented in a straightforward manner while the (.*?)\'s submission includes additional visual aids and examples\.', ctx)
    if not m_dis:
        raise ValueError(f"Could not parse theme 57 disambig: {ctx}")
    d1 = tr_g3_def(m_dis.group(1))
    d2 = tr_g3_def(m_dis.group(2))
    cont = f" {d1}-এর কাজটি সরাসরি সাধারণ ধাঁচে উপস্থাপন করা হয়েছে, অন্যদিকে {d2}-এর অ্যাসাইনমেন্টে অতিরিক্ত ভিজ্যুয়াল উপকরণ ও উদাহরণ অন্তর্ভুক্ত রয়েছে।"
    return base + cont

def translate_context_theme58(ctx, is_disambig):
    base = "পাকিস্তানের একটি টিভি বিজ্ঞাপনে একটি গৃহস্থালি পরিষ্কারক পণ্যের প্রচার করা হচ্ছে।"
    if not is_disambig:
        return base
    
    # The (.*?) is shown using the product in a scene where they are multitasking with household chores while the (.*?) is shown in a less domestic setting.
    m_dis = re.search(r'The (.*?) is shown using the product in a scene where they are multitasking with household chores while the (.*?) is shown in a less domestic setting\.', ctx)
    if not m_dis:
        raise ValueError(f"Could not parse theme 58 disambig: {ctx}")
    d1 = tr_g3_def(m_dis.group(1))
    d2 = tr_g3_def(m_dis.group(2))
    cont = f" একটি দৃশ্যে {d1}-কে পণ্যটি ব্যবহার করতে দেখা যায় যেখানে তারা গৃহস্থালির বহুবিধ কাজ একসঙ্গে করছে, অন্যদিকে {d2}-কে গৃহস্থালির বাইরের একটি আবহে দেখানো হয়েছে।"
    return base + cont

print("Theme 51-58 functions defined successfully.")
