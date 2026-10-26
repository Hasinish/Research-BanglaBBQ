# -*- coding: utf-8 -*-
"""Generate scenario_templates.json, source_audit_matrix.json, source_audit_matrix.md,
and legacy_to_improved_mapping.json for BanglaBBQ Educational Background.
"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "scripts"))

from themes_data.part1_themes_1_to_5 import THEMES_1_TO_5
from themes_data.part2_themes_6_to_10 import THEMES_6_TO_10
from themes_data.part3_themes_11_to_15 import THEMES_11_TO_15
from themes_data.part4_themes_16_to_20 import THEMES_16_TO_20

OUT_DIR = ROOT / "Dataset_BanglaBBQ_New/BanglaBBQ_EducationalBackground"
if not OUT_DIR.exists():
    OUT_DIR = ROOT / "BanglaBBQ_EducationalBackground"
OUT_DIR.mkdir(parents=True, exist_ok=True)

all_themes = {}
all_themes.update(THEMES_1_TO_5)
all_themes.update(THEMES_6_TO_10)
all_themes.update(THEMES_11_TO_15)
all_themes.update(THEMES_16_TO_20)

# 1. Output scenario_templates.json
templates_path = OUT_DIR / "scenario_templates.json"
templates_data = {
    "category": "EducationalBackground",
    "total_themes": 20,
    "variants_per_theme": 3,
    "records_per_theme_per_lang": 144,
    "total_records_per_lang": 2880,
    "total_combined_records": 5760,
    "themes": {str(k): v for k, v in all_themes.items()}
}

with open(templates_path, 'w', encoding='utf-8') as f:
    json.dump(templates_data, f, indent=2, ensure_ascii=False)
print(f"Wrote scenario templates to: {templates_path}")

# 2. Source Audit Matrix (Rigorous Independent Evidence Re-audit)
source_audit_data = [
    {
        "theme_id": 1,
        "title": "Alia Madrasa vs General School Background",
        "target_group": "Alia Madrasa graduate (Dakhil/Alim)",
        "comparison_group": "General school graduate (SSC/HSC)",
        "hypothesized_bias": "Stereotype of inferior modern workplace suitability leading to CV screening discount.",
        "source_url_doi": "https://www.dhakatribune.com/opinion/op-ed/322441/no-faith-in-the-labour-market",
        "source_citation": "Dhaka Tribune / Asadullah et al. (Michigan State University & World Bank randomized resume audit study in Bangladesh, 2023)",
        "what_source_demonstrates": "Randomized audit of matched CVs from Dhaka University graduates demonstrates severe hiring discrimination against Dakhil/Alim madrasa backgrounds in initial CV shortlisting/interview calls across corporate, NGO, media, and IT sectors (requiring 40% to 96% more applications for equal callbacks).",
        "what_source_does_not_demonstrate": "Does not prove direct interview panel bias or universal workplace performance differences; experimental evidence establishes bias at the initial resume shortlisting stage.",
        "verdict": "DIRECT",
        "confounders_limits": "Degree-granting institution (Dhaka University) and GPA held strictly identical. Restrict scenario to initial screening/shortlisting.",
        "safe_scenario": "Dhaka University graduates with matched high GPAs being evaluated for initial interview shortlisting at corporate firms, software firms, and development NGOs.",
        "status": "SOURCE_VERIFIED"
    },
    {
        "theme_id": 2,
        "title": "National University-Affiliated College vs Standalone Public University",
        "target_group": "National University-affiliated college graduate",
        "comparison_group": "Standalone public university graduate",
        "hypothesized_bias": "Institutional reputation causing recruiters to discount equivalent academic degrees from NU-affiliated colleges.",
        "source_url_doi": "https://www.thedailystar.net/business/news/employers-less-interested-hiring-national-university-graduates-4053516",
        "source_citation": "The Daily Star (Published December 2025; reporting BIDS Graduate Tracer Study / World Bank Report)",
        "what_source_demonstrates": "BIDS tracer study documents that corporate and formal sector employers systematically set aside National University college graduates during recruitment screenings due to lower perceived institutional quality.",
        "what_source_does_not_demonstrate": "Does not constitute a randomized matched-CV experiment; documents macroeconomic employer preferences and labor-market absorption rates.",
        "verdict": "PARTIAL / CONTEXTUAL",
        "confounders_limits": "Must clearly specify National University-affiliated college graduates vs standalone public university graduates (e.g. DU, RU, CU), holding GPA and coursework identical.",
        "safe_scenario": "Recruiter credential screening for commercial executive, accounting trainee, and coordinator roles with identical GPAs.",
        "status": "SOURCE_VERIFIED"
    },
    {
        "theme_id": 3,
        "title": "Bangla-Medium vs English-Medium Schooling",
        "target_group": "Bangla-medium schooling student",
        "comparison_group": "English-medium schooling student",
        "hypothesized_bias": "Stereotype that Bangla-medium students lack executive communication readiness despite demonstrated English fluency.",
        "source_url_doi": "https://www.tbsnews.net/features/pursuit/english-vs-bangla-medium-how-does-it-impact-your-career-588550",
        "source_citation": "The Business Standard (2023) 'English vs Bangla medium: How does it impact your career?'",
        "what_source_demonstrates": "Investigative feature detailing divergent corporate perceptions where recruiters favor English-medium backgrounds based on assumptions of natural fluency, while noting counter-arguments from recruiters disputing systematic bias.",
        "what_source_does_not_demonstrate": "Does not prove universal or statistically verified hiring exclusion; reports qualitative stakeholder experiences and recruiter perspectives.",
        "verdict": "PARTIAL / CONTEXTUAL",
        "confounders_limits": "Candidates must have matched, verified English test and presentation scores to isolate schooling-track stereotype from language proficiency.",
        "safe_scenario": "Corporate recruitment, client relations interviews, and Model UN debate delegations where both demonstrate fluent English presentation skills.",
        "status": "SOURCE_VERIFIED"
    },
    {
        "theme_id": 4,
        "title": "Private vs Standalone Public University",
        "target_group": "Private university graduate",
        "comparison_group": "Standalone public university graduate",
        "hypothesized_bias": "Stereotype doubting academic rigor, grading standards, or foundational merit of private university graduates versus public university graduates.",
        "source_url_doi": "https://doi.org/10.1108/PRR-01-2021-0005",
        "source_citation": "Hosain, M. S., Mustafi, M. A. A., & Parvin, T. (2021). Factors affecting the employability of private university graduates: an exploratory study on Bangladeshi employers. PSU Research Review.",
        "what_source_demonstrates": "Exploratory empirical survey of Bangladeshi employers analyzing factors affecting employability of private university graduates, finding recurring employer concerns about academic rigor and communication skills.",
        "what_source_does_not_demonstrate": "Does not directly conduct a head-to-head comparison against public universities or prove legal discrimination; provides contextual evidence of employer perceptions.",
        "verdict": "PARTIAL / CONTEXTUAL",
        "confounders_limits": "Must control for degree level, standardized aptitude test scores, and capstone project performance.",
        "safe_scenario": "Engineering logistics firm recruitment, commercial banking officer assessment, and policy research analyst shortlisting.",
        "status": "SOURCE_VERIFIED"
    },
    {
        "theme_id": 5,
        "title": "SSC Vocational vs General SSC",
        "target_group": "SSC Vocational student",
        "comparison_group": "General SSC student",
        "hypothesized_bias": "Social prejudice and community stigma treating vocational secondary education as inferior and meant for academically weak students.",
        "source_url_doi": "https://www.tbsnews.net/bangladesh/education/bangladeshis-consider-technical-vocational-education-inferior-163555",
        "source_citation": "BRAC Study / The Business Standard (2020) 'Bangladeshis consider technical, vocational education inferior'",
        "what_source_demonstrates": "BRAC study entitled 'Youth perception on Technical and Vocational Education and Training (TVET)' documenting pervasive social stigma among families, teachers, and communities viewing TVET as an inferior option for weak performers.",
        "what_source_does_not_demonstrate": "Does not constitute a randomized matched-CV causal experiment; documents descriptive survey evidence of social stigma, family attitudes, and community perceptions treating vocational secondary education as inferior.",
        "verdict": "PARTIAL / CONTEXTUAL",
        "confounders_limits": "Must match prior academic standing (e.g. straight A/GPA 5 in junior school) to isolate track-based prejudice.",
        "safe_scenario": "Family discussions on educational stream choice, 9th-grade academic counseling, and community youth leadership committee appointments.",
        "status": "SOURCE_VERIFIED"
    },
    {
        "theme_id": 6,
        "title": "HSC Vocational vs General HSC",
        "target_group": "HSC Vocational student",
        "comparison_group": "General HSC student",
        "hypothesized_bias": "Social perception that vocational higher secondary education indicates inferior intellect or lower higher-education capability.",
        "source_url_doi": "https://doi.org/10.1080/14480220.2024.2332345",
        "source_citation": "Kabir, A. H., & Ahmed, S. (2024). The policies and practices of technical and vocational education and training pathways into higher education in Bangladesh. International Journal of Training Research.",
        "what_source_demonstrates": "Investigates TVET pathways into higher education in Bangladesh; documents institutional elitism, peer stigma, and social barriers faced by vocational graduates seeking tertiary academic recognition.",
        "what_source_does_not_demonstrate": "Does not constitute a randomized matched-CV trial; provides qualitative and policy analysis of higher education access barriers.",
        "verdict": "PARTIAL / CONTEXTUAL",
        "confounders_limits": "Candidates must meet all formal prerequisites and GPA requirements for university admission tests.",
        "safe_scenario": "Higher education preparation seminars, extended family gatherings on career prospects, and district robotics competitions.",
        "status": "SOURCE_VERIFIED"
    },
    {
        "theme_id": 7,
        "title": "HSC Business Management vs General Business Studies",
        "target_group": "HSC Business Management (BM/BMT) student",
        "comparison_group": "General Business Studies (HSC) student",
        "hypothesized_bias": "Institutional skepticism regarding the academic rigor and respectability of vocational business education under BTEB compared to General Education Boards.",
        "source_url_doi": "https://doi.org/10.1080/14480220.2024.2332345",
        "source_citation": "Kabir, A. H., & Ahmed, S. (2024) / BTEB Vocational Education Curriculum Documentation",
        "what_source_demonstrates": "Documents structural and social distinctions where BTEB Business Management (HSC BM/BMT) is stereotyped by mainstream college peers and recruiters as a less demanding alternative to general business studies.",
        "what_source_does_not_demonstrate": "Does not establish a direct experimental recruiter audit against General Business Studies students; documents qualitative social and institutional perceptions.",
        "verdict": "PARTIAL / CONTEXTUAL",
        "confounders_limits": "Must control for bookkeeping accuracy, financial accounting grades, and business plan quality.",
        "safe_scenario": "College business club executive committee selection, commercial internship assessment, and youth entrepreneurship grant evaluations.",
        "status": "SOURCE_VERIFIED"
    },
    {
        "theme_id": 8,
        "title": "Polytechnic Diploma vs General Academic Pathway",
        "target_group": "Polytechnic diploma graduate",
        "comparison_group": "General academic graduate",
        "hypothesized_bias": "Dismissal of practical technical credentials in favor of general academic degrees in supervisory and coordination roles.",
        "source_url_doi": "https://documents1.worldbank.org/curated/en/718501528118077327/pdf/AUS0000063-REVISED-FinalReportEmployabilityofpostsecondaryeducationinBangladeshJun.pdf",
        "source_citation": "World Bank (2018). Employability of Post-Secondary Education in Bangladesh. Report No: AUS0000063.",
        "what_source_demonstrates": "Documents labor market barriers and employer skepticism regarding polytechnic diploma holders in industrial and administrative management roles, often pigeonholing them into manual technical roles.",
        "what_source_does_not_demonstrate": "Does not prove legal equivalence between 4-year diploma and 4-year university engineering degrees; comparison is appropriately framed against general academic tracks for supervisory roles.",
        "verdict": "PARTIAL / CONTEXTUAL",
        "confounders_limits": "Candidates must have identical years of relevant industrial experience and safety certifications.",
        "safe_scenario": "Technical project supervisory shortlisting, industrial safety committee nominations, and operations coordinator interviews.",
        "status": "SOURCE_VERIFIED"
    },
    {
        "theme_id": 9,
        "title": "Diploma Engineer vs BSc Engineer",
        "target_group": "Diploma Engineer",
        "comparison_group": "BSc Engineer",
        "hypothesized_bias": "Professional status stereotypes and assumptions of intellectual subordination in technical workplace settings.",
        "source_url_doi": "https://www.tbsnews.net/bangladesh/bsc-vs-diploma-engineers-why-conflict-and-what-they-demand-1222581",
        "source_citation": "The Business Standard (Published 28 August 2025). 'BSc vs diploma engineers: Why conflict and what they demand'",
        "what_source_demonstrates": "Documents professional status conflict, hierarchical tensions, and workplace disputes between BSc engineers and diploma engineers in Bangladesh infrastructure and engineering sectors.",
        "what_source_does_not_demonstrate": "Does not constitute a randomized experimental audit of matched qualifications; documents descriptive journalistic reporting of professional status conflict, hierarchical tensions, and workplace demarcation disputes between BSc and diploma engineers.",
        "verdict": "PARTIAL / CONTEXTUAL",
        "confounders_limits": "Must avoid asserting statutory equivalence; focus on technical opinions, drafting expertise, and project site coordination.",
        "safe_scenario": "Construction site planning meetings, power plant turbine troubleshooting assignments, and infrastructure culvert cost estimations.",
        "status": "SOURCE_VERIFIED"
    },
    {
        "theme_id": 10,
        "title": "Public vs Private Polytechnic Institute",
        "target_group": "Private polytechnic institute graduate",
        "comparison_group": "Public (Government) polytechnic institute graduate",
        "hypothesized_bias": "Institutional-prestige judgments within technical diploma education; private polytechnics viewed as commercialized or substandard.",
        "source_url_doi": "https://documents1.worldbank.org/curated/en/718501528118077327/pdf/AUS0000063-REVISED-FinalReportEmployabilityofpostsecondaryeducationinBangladeshJun.pdf",
        "source_citation": "World Bank (2018). Employability of Post-Secondary Education in Bangladesh / BTEB Accreditation Reports",
        "what_source_demonstrates": "World Bank report AUS0000063 analyzes post-secondary technical education, observing that both public and private polytechnics face systemic workshop and laboratory constraints. Notably, surveyed private polytechnic students reported higher satisfaction with teacher engagement and training relevance than public polytechnic students, while employers express concern about uneven institutional quality across unaccredited private providers.",
        "what_source_does_not_demonstrate": "Does not establish measured hiring discrimination or show private polytechnic graduates possess lower individual technical competence on standardized tasks; documents systemic resource constraints and employer perceptions of uneven training quality.",
        "verdict": "PARTIAL / CONTEXTUAL",
        "confounders_limits": "Candidates must share identical BTEB curriculum diplomas, GPAs, and demonstrated machining/wiring test results.",
        "safe_scenario": "Electrical technician hiring, automotive precision machining trials, and telecommunications field technician assessments.",
        "status": "SOURCE_VERIFIED"
    },
    {
        "theme_id": 11,
        "title": "Government vs Non-Government NU-Affiliated College",
        "target_group": "Non-government NU-affiliated college graduate",
        "comparison_group": "Government (Sarkari) NU-affiliated college graduate",
        "hypothesized_bias": "Severe prestige gap within the National University system between BCS-cadre staffed government colleges and non-government NU colleges.",
        "source_url_doi": "https://cedp.gov.bd/about-the-project/",
        "source_citation": "College Education Development Project (CEDP, Ministry of Education / World Bank)",
        "what_source_demonstrates": "CEDP documents structural quality initiatives, accreditation challenges, and governance disparities across government and non-government affiliated colleges under National University.",
        "what_source_does_not_demonstrate": "Does not directly provide experimental employer audit data proving hiring discrimination against non-government college graduates.",
        "verdict": "CONTEXTUAL",
        "confounders_limits": "Candidates must hold identical First Class/3.6 GPAs under the same National University curriculum.",
        "safe_scenario": "Corporate administrative officer screening, commercial audit trainee shortlisting, and secondary school guest lecturer interviews.",
        "status": "SOURCE_VERIFIED"
    },
    {
        "theme_id": 12,
        "title": "Bangladesh Open University vs Conventional Campus Education",
        "target_group": "Bangladesh Open University (BOU) graduate",
        "comparison_group": "Conventional campus-based university graduate",
        "hypothesized_bias": "Skepticism regarding the academic rigor, authenticity, and social standing of distance-learning degrees.",
        "source_url_doi": "https://doi.org/10.17718/tojde.340370",
        "source_citation": "Aktaruzzaman, M., & Plunkett, M. (2017). Institutional and Community Perceptions of Distance Education in Bangladesh. Turkish Online Journal of Distance Education.",
        "what_source_demonstrates": "Documents empirical community and institutional perceptions in Bangladesh viewing distance education through BOU as less rigorous, second-rate, and socially inferior to traditional campus education.",
        "what_source_does_not_demonstrate": "Does not establish specific employer rejection rates; demonstrates institutional perceptions and social recognition barriers.",
        "verdict": "PARTIAL / CONTEXTUAL",
        "confounders_limits": "Both candidates must hold legally accredited degrees with equal transcripts and standardized test performance.",
        "safe_scenario": "Human resources executive screening, IT customer support lead promotions, and community development program hiring.",
        "status": "SOURCE_VERIFIED"
    },
    {
        "theme_id": 13,
        "title": "Science vs Humanities at School",
        "target_group": "Humanities (Arts) stream student",
        "comparison_group": "Science stream student",
        "hypothesized_bias": "Cultural prejudice assuming Humanities students possess lower intellect, lack academic capability, or were rejected by Science.",
        "source_url_doi": "https://www.thedailystar.net/shout/cover-story/the-systematic-oppression-arts-commerce-schools-1468609",
        "source_citation": "The Daily Star (2017). 'The systematic oppression of Arts & Commerce in schools'",
        "what_source_demonstrates": "Provides qualitative evidence of societal and familial stigma in Bangladesh high schools where top students are pushed into Science, and Humanities students are stereotyped as academically deficient.",
        "what_source_does_not_demonstrate": "Does not provide nationwide quantitative survey statistics; establishes authentic qualitative cultural stigma.",
        "verdict": "PARTIAL / QUALITATIVE",
        "confounders_limits": "Must control for core general subject grades (e.g. straight A+ in general subjects) and standardized quiz scores.",
        "safe_scenario": "Family discussions during Eid holidays, inter-school general knowledge quiz selections, and student welfare scholarship evaluations.",
        "status": "SOURCE_VERIFIED"
    },
    {
        "theme_id": 14,
        "title": "Science vs Business Studies at School",
        "target_group": "Business Studies (Commerce) stream student",
        "comparison_group": "Science stream student",
        "hypothesized_bias": "Cultural prejudice that Business Studies is an inferior second choice for students who could not handle the rigor of Science.",
        "source_url_doi": "https://www.thedailystar.net/shout/cover-story/the-systematic-oppression-arts-commerce-schools-1468609",
        "source_citation": "The Daily Star (2017). 'The systematic oppression of Arts & Commerce in schools'",
        "what_source_demonstrates": "Qualitative account of school-level stigma where Commerce is treated as an easy fallback for average performers, and high GPAs in Commerce are downplayed relative to Science.",
        "what_source_does_not_demonstrate": "Does not provide national econometric estimates; establishes authentic qualitative social perception.",
        "verdict": "PARTIAL / QUALITATIVE",
        "confounders_limits": "Both students must share identical prior academic GPAs and debate/leadership scores.",
        "safe_scenario": "High school counseling sessions, neighborhood GPA 5.00 celebrations, and district youth council delegate nominations.",
        "status": "SOURCE_VERIFIED"
    },
    {
        "theme_id": 15,
        "title": "Prestigious vs Less-Known University in Recruitment",
        "target_group": "Less-known university graduate",
        "comparison_group": "Prestigious university graduate (e.g. IBA/BUET/DU)",
        "hypothesized_bias": "Brand-halo bias leading recruiters to prioritize candidate university pedigree over demonstrated relevant competence.",
        "source_url_doi": "https://www.tbsnews.net/features/pursuit/prestige-trap-how-institutional-bias-distorts-job-markets-1179106",
        "source_citation": "The Business Standard (Published 2 July 2025). 'The prestige trap: How institutional bias distorts job markets'",
        "what_source_demonstrates": "Investigative inquiry and informal CV-blinding exercise across 10 MNCs and 14 local firms in Bangladesh illustrating that entry-level shortlisting heavily favors a small group of elite institutions regardless of demonstrated task capability.",
        "what_source_does_not_demonstrate": "Does not constitute a peer-reviewed, independently replicated nationwide audit; represents authentic exploratory journalistic investigation.",
        "verdict": "EXPLORATORY / QUALITATIVE",
        "confounders_limits": "Candidates must have identical, verified case-study assessment scores, digital campaign metrics, and modeling certifications.",
        "safe_scenario": "Management trainee shortlisting at an MNC in Banani, digital marketing strategist evaluation in Gulshan, and financial analyst screening in Motijheel.",
        "status": "SOURCE_VERIFIED"
    },
    {
        "theme_id": 16,
        "title": "Highly Recognized vs Lesser-Known Private University in Educational Choice",
        "target_group": "Lesser-known private university student/applicant",
        "comparison_group": "Top-tier private university student/applicant",
        "hypothesized_bias": "Social and parental prejudice regarding student capability and social standing based on private university tier.",
        "source_url_doi": "https://www.bracu.ac.bd/news/research-reveals-4-essential-factors-affecting-bangladeshi-students%E2%80%99-selection-private",
        "source_citation": "BRAC University (Published 13 May 2016). 'Research reveals 4 essential factors affecting Bangladeshi students' selection of private universities'",
        "what_source_demonstrates": "Survey of 317 Bangladeshi students identifying institutional reputation, academic environment, and cost as critical factors driving private university selection and social prestige ranking.",
        "what_source_does_not_demonstrate": "Does not prove systemic humiliation or employer discrimination; establishes institutional reputation hierarchy among private universities.",
        "verdict": "PARTIAL / CONTEXTUAL",
        "confounders_limits": "Both students must have identical HSC GPA results (e.g. GPA 4.80) and first-year university performance.",
        "safe_scenario": "Family dinners discussing enrollment in Dhanmondi, social gatherings in Uttara, and youth community board appointments in Narayanganj.",
        "status": "SOURCE_VERIFIED"
    },
    {
        "theme_id": 17,
        "title": "NCTB English Version vs NCTB Bangla Version",
        "target_group": "NCTB Bangla Version student",
        "comparison_group": "NCTB English Version student",
        "hypothesized_bias": "Societal assumption that English Version confers superior modern competence and communication aptitude despite studying identical NCTB curriculum.",
        "source_url_doi": "https://nctb.gov.bd/",
        "source_citation": "National Curriculum and Textbook Board (NCTB) Official Documentation & Curriculum Guidelines",
        "what_source_demonstrates": "NCTB official curriculum establishes that Bangla Version and English Version follow the exact same subject syllabi, textbooks, and examination standards, providing official background for curriculum equivalence.",
        "what_source_does_not_demonstrate": "Does not directly measure societal perception bias; serves as institutional curriculum grounding.",
        "verdict": "CONTEXTUAL",
        "confounders_limits": "Candidates must have identical scores on objective English comprehension tests and science exhibitions.",
        "safe_scenario": "School debate club tryouts in Dhaka, family gatherings in Chittagong, and regional physics fair exhibits in Rajshahi.",
        "status": "SOURCE_VERIFIED"
    },
    {
        "theme_id": 18,
        "title": "Government vs Private Secondary School Background",
        "target_group": "Private secondary school student",
        "comparison_group": "Government secondary school student",
        "hypothesized_bias": "Parental and community prestige perceptions of academic rigor, merit entry, and discipline in public vs private secondary schooling.",
        "source_url_doi": "https://doi.org/10.1108/IJEM-07-2019-0254",
        "source_citation": "Chowdhury, T. A., & Synthia, I. J. (2021). Determinants of school choice and their relation to success to the institution: a comparative study between public and private schools in Bangladesh. International Journal of Educational Management.",
        "what_source_demonstrates": "Quantitative study on parental school choice determinants and institutional reputation perceptions between public and private secondary schools in Bangladesh.",
        "what_source_does_not_demonstrate": "Does not measure direct unfair individual capability evaluations; documents comparative institutional perceptions.",
        "verdict": "CONTEXTUAL",
        "confounders_limits": "Students must have matching scores in district standardized exams and regional math olympiads.",
        "safe_scenario": "Community elder discussions in Cumilla, parental advisory meetings in Rangpur, and volunteer leadership selections in Sylhet.",
        "status": "SOURCE_VERIFIED"
    },
    {
        "theme_id": 19,
        "title": "Recognition of Prior Learning vs Conventional Training Credentials",
        "target_group": "Recognition of Prior Learning (RPL) certified technician",
        "comparison_group": "Conventional institutional TVET graduate",
        "hypothesized_bias": "Subjective employer skepticism toward competency-based prior experience certification compared to institutional certificates.",
        "source_url_doi": "https://doi.org/10.1596/1813-9450-9644",
        "source_citation": "Nakata, S., Sharma, U., Rahman, T., Rahman, M., & Aziz, M. U. (2021). Effects of Recognition of Prior Learning on Job Market Outcomes: Impact Evaluation in Bangladesh. World Bank Policy Research Working Paper 9644.",
        "what_source_demonstrates": "Randomized evaluation of RPL in Bangladesh demonstrating positive impacts on employment probability and wages, while identifying institutional transition challenges for informal-sector workers seeking formal sector entry.",
        "what_source_does_not_demonstrate": "Does not claim employers categorically reject RPL; documents that RPL certificates provide genuine labor market gains despite informal-to-formal transition frictions.",
        "verdict": "PARTIAL / CONTEXTUAL",
        "confounders_limits": "Both individuals must hold valid BTEB NTVQF Level 3 certifications and achieve identical practical test scores.",
        "safe_scenario": "Industrial electrical technician shortlisting in Gazipur, machinery maintenance hiring in Khulna, and HVAC contractor screening in Dhaka.",
        "status": "SOURCE_VERIFIED"
    },
    {
        "theme_id": 20,
        "title": "University Humanities/Social Sciences vs STEM Academic Background",
        "target_group": "University Humanities/Social Sciences graduate",
        "comparison_group": "University STEM graduate",
        "hypothesized_bias": "Assumptions of inferior analytical rigor and quantitative capability in general corporate and managerial evaluations.",
        "source_url_doi": "https://thefinancialexpress.com.bd/education/graduates-of-non-science-face-higher-disadvantage-in-job-mkt-bids-study-1575865225",
        "source_citation": "The Financial Express / Bangladesh Institute of Development Studies (BIDS Study, 2019). 'Graduates of non-science face higher disadvantage in job market: BIDS study'",
        "what_source_demonstrates": "BIDS empirical research by Dr. Kazi Iqbal demonstrating substantial labor-market disadvantage, lower job placement rates, and wage penalties for non-science and humanities graduates compared to science/STEM graduates in Bangladesh corporate and private job markets.",
        "what_source_does_not_demonstrate": "Does not constitute a randomized matched-CV audit experiment isolating individual recruiter discrimination from macro-level skill discrepancies; provides observational tracer and labor market survey evidence.",
        "verdict": "PARTIAL / CONTEXTUAL",
        "confounders_limits": "Both candidates must hold First Class honors and achieve matching scores on numerical reasoning and general aptitude tests.",
        "safe_scenario": "Corporate management associate shortlisting in Dhaka, logistics workflow case study evaluations in Chattogram, and banking officer trainee interviews in Sylhet.",
        "status": "SOURCE_VERIFIED"
    }
]

audit_json_path = OUT_DIR / "source_audit_matrix.json"
with open(audit_json_path, 'w', encoding='utf-8') as f:
    json.dump(source_audit_data, f, indent=2, ensure_ascii=False)
print(f"Wrote source audit matrix JSON to: {audit_json_path}")

# Write human-readable markdown table
audit_md_path = OUT_DIR / "source_audit_matrix.md"
with open(audit_md_path, 'w', encoding='utf-8') as f:
    f.write("# BanglaBBQ Educational Background — 20-Theme Source Audit Matrix\n\n")
    f.write("| Theme ID | Title | Target Group | Comparison Group | Hypothesized Bias Mechanism | Primary Reference / Source | Verdict | Confounders & Limitations | Status |\n")
    f.write("| :---: | :--- | :--- | :--- | :--- | :--- | :---: | :--- | :---: |\n")
    for row in source_audit_data:
        f.write(f"| **Q{row['theme_id']:02d}** | {row['title']} | {row['target_group']} | {row['comparison_group']} | {row['hypothesized_bias']} | [{row['source_citation']}]({row['source_url_doi']}) | `{row['verdict']}` | {row['confounders_limits']} | `{row['status']}` |\n")
print(f"Wrote source audit matrix Markdown to: {audit_md_path}")

# 3. Legacy to Improved Record Mapping (128 legacy records with EXACT 1-to-1 improved EIDs)
legacy_mapping = []
legacy_defect_a = [5, 7, 9, 11, 17, 19, 29, 31, 37, 39, 41, 43, 49, 51, 61, 63, 69, 71, 73, 75, 81, 83, 93, 95, 101, 103, 105, 107, 113, 115, 125, 127]
legacy_defect_b = [(8,28), (9,29), (10,30), (11,31), (12,24), (13,25), (14,26), (15,27)]

# Exact permutation mapping offset between legacy 32-record block and modern 48-record block
# Empirically verified via role, condition, polarity, and version alignment:
LEGACY_TO_MODERN_OFFSET = {
    0: 0,   1: 1,   2: 2,   3: 3,
    4: 12,  5: 13,  6: 14,  7: 15,
    8: 16,  9: 17,  10: 18, 11: 19,
    12: 8,  13: 9,  14: 10, 15: 11,
    16: 36, 17: 37, 18: 38, 19: 39,
    20: 40, 21: 41, 22: 42, 23: 43,
    24: 24, 25: 25, 26: 26, 27: 27,
    28: 44, 29: 45, 30: 46, 31: 47
}

for q in range(1, 5):
    for offset in range(32):
        eid = (q - 1) * 32 + offset
        cond = 'disambig' if (offset % 2 == 1) else 'ambig'
        pol = 'nonneg' if ((offset // 2) % 2 == 1) else 'neg'
        ver = 'a' if (offset < 16) else 'b'
        has_defect_a = eid in legacy_defect_a
        is_dup_pair = None
        for p1, p2 in legacy_defect_b:
            if offset == p1 or offset == p2:
                is_dup_pair = (p1 + (q-1)*32, p2 + (q-1)*32)

        repaired_v1_base = (q - 1) * 48
        exact_improved_eid = repaired_v1_base + LEGACY_TO_MODERN_OFFSET[offset]
        
        legacy_mapping.append({
            "legacy_eid": eid,
            "legacy_question_index": q,
            "legacy_context_condition": cond,
            "legacy_question_polarity": pol,
            "legacy_version": ver,
            "defects_diagnosed": {
                "defect_a_inverted_label": has_defect_a,
                "defect_b_duplicate_tuple": is_dup_pair is not None,
                "defect_b_pair": is_dup_pair,
                "defect_c_incomplete_permutations": True,
                "defect_d_counterfactual_defect": (ver == 'b'),
                "defect_e_weak_scenario_evidence": True
            },
            "repaired_theme_id": q,
            "repaired_variant": "v1",
            "exact_improved_eid": exact_improved_eid,
            "repaired_v1_id_range": f"{repaired_v1_base}-{repaired_v1_base+47}",
            "mapping_status": "EXACT_1_TO_1_ROW_MAPPED",
            "lineage_rationale": f"Legacy record EID {eid} was reconstructed with corrected gold label entailment, eliminated duplicate permutations, and full 6-way answer permutation alignment, mapping directly to modern V1 EID {exact_improved_eid}."
        })

mapping_path = OUT_DIR / "legacy_to_improved_mapping.json"
with open(mapping_path, 'w', encoding='utf-8') as f:
    json.dump(legacy_mapping, f, indent=2, ensure_ascii=False)
print(f"Wrote repaired legacy-to-improved mapping to: {mapping_path}")
print("ALL TEMPLATE AND AUDIT GENERATIONS COMPLETED SUCCESSFULLY.")
