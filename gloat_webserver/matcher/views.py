from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Skill, Candidate, Job
from .utils import get_candidate_skills, find_common_skills


class FindCandidateApiView(APIView):

    def post(self, request, *args, **kwargs):
        res = {'skills': [], 'common_skills': 0}
        try:
            job_details = Job.get_job_details(request)
            candidate = Candidate.objects.all().filter(title=request.data.get('title'))
            if candidate.exists():
                for q in candidate.values("title", "id"):
                    candidate_skills = get_candidate_skills(candidate.get(id=q['id']).skills.all().values())
                    common_skills = find_common_skills(job_details['job_skills'], candidate_skills)
                    if common_skills > res['common_skills']:
                        res['title'] = q['title']
                        res['id'] = q['id']
                        res['skills'] = candidate_skills
                        res['common_skills'] = common_skills
                if not 'id' in res.keys():
                    for c in candidate.values("title", "id")[:1]:
                        candidate_skills = get_candidate_skills(candidate.get(id=c['id']).skills.all().values())
                        res['title'] = c['title']
                        res['id'] = c['id']
                        res['skills'] = candidate_skills
                        res['common_skills'] = 0
                res.pop('common_skills', None)
                return Response(res, status=status.HTTP_200_OK)
            else:
                return Response("there is no matching candidate", status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(e, status=status.HTTP_400_BAD_REQUEST)


class AddCandidateApiView(APIView):

    def post(self, request, *args, **kwargs):
        data = {
            'title': request.data.get('title'),
            'skills': request.data.get('skills'),
        }
        try:
            candidate = Candidate(title=data['title'])
            candidate.save()
            for skill in data['skills']:
                s = Skill.objects.filter(name=skill)[:1].get()
                candidate.skills.add(s)

            return Response('success', status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            candidate.delete()
            return Response(e, status=status.HTTP_400_BAD_REQUEST)


class AddSkillApiView(APIView):
    def post(self, request, *args, **kwargs):
        data = {
            'name': request.data.get('name'),
        }
        try:
            skill = Skill(name=data['name'])
            skill.save()
            return Response('success', status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            skill.delete()
            return Response(e, status=status.HTTP_400_BAD_REQUEST)


class AddJobApiView(APIView):
    def post(self, request, *args, **kwargs):
        data = {
            'title': request.data.get('title'),
            'skills': request.data.get('skills'),
        }
        try:
            job = Job(title=data['title'])
            job.save()
            for skill in data['skills']:
                s = Skill.objects.filter(name=skill)[:1].get()
                job.skills.add(s)
            return Response('success', status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            job.delete()
            return Response(e, status=status.HTTP_400_BAD_REQUEST)
