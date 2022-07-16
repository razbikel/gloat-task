
def get_candidate_skills(query_set):
    res = []
    for q in query_set:
        res.append(q['name'])
    return res


def find_common_skills(job_skills, candidate_skills):
    return len(list(set(job_skills).intersection(candidate_skills)))
