from collections import Counter
import re

def extract_skills(job_list):
    keywords = []
    pattern = re.compile(r'\b(Java|Python|JavaScript|Angular|React|Node|C\+\+|C#|PHP|Laravel|Spring|SQL|Docker|AWS|Azure|Kubernetes|HTML|CSS|.NET)\b', re.IGNORECASE)

    for job in job_list:
        for field in ["name", "slug", "profile", "skills", "missions"]:
            text = job.get(field, "")
            if not isinstance(text, str):
                continue
            matches = pattern.findall(text)
            keywords.extend(list(set([match.lower() for match in matches])))

    return Counter(keywords)

def analyze_skills(job_data):
    skills = extract_skills(job_data)
    return skills.most_common()