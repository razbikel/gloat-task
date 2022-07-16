from django.db import models


class Skill(models.Model):
    name = models.CharField(max_length=180, primary_key=True)

    def __str__(self):
        return self.name


class Candidate(models.Model):
    title = models.CharField(max_length=180)
    skills = models.ManyToManyField(Skill)

    def __str__(self):
        return self.title


class Job(models.Model):
    title = models.CharField(max_length=180)
    skills = models.ManyToManyField(Skill)

    @staticmethod
    def get_job_details(request):
        res = {'job_skills': []}
        job = Job.objects.filter(title=request.data.get('title'))[:1]
        for q in job.values():
            res['job_id'] = q["id"]
            res['job_title'] = q["title"]
        for q in job.get().skills.all().values():
            res['job_skills'].append(q['name'])
        return res


