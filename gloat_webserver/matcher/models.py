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

# class CandidateSkill(models.Model):
#     candidateId = models.ForeignKey(Candidate, on_delete=models.CASCADE)
#     skillId = models.ForeignKey(Skill, on_delete=models.CASCADE)
#
#
# class JobSkill(models.Model):
#     jobId = models.ForeignKey(Job, on_delete=models.CASCADE)
#     skillId = models.ForeignKey(Skill, on_delete=models.CASCADE)
