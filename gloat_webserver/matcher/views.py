from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Skill, Candidate, Job
from .serializers import SkillSerializer, CandidateSerializer


def get_job_details(request):
    res = {'job_skills': []}
    job = Job.objects.filter(title=request.data.get('title'))[:1]
    for q in job.values():
        res['job_id'] = q["id"]
        res['job_title'] = q["title"]
    for q in job.get().skills.all().values():
        res['job_skills'].append(q['name'])
    return res


def get_candidate_skills(query_set):
    res = []
    for q in query_set:
        res.append(q['name'])
    return res


def find_common_skills(job_skills, candidate_skills):
    return len(list(set(job_skills).intersection(candidate_skills)))


class FindCandidateApiView(APIView):

    def post(self, request, *args, **kwargs):
        res = {'skills': [], 'common_skills': 0}
        job_details = get_job_details(request)
        print(job_details)

        candidate = Candidate.objects.all().filter(title=request.data.get('title'))

        for q in candidate.values("title", "id"):
            candidate_skills = get_candidate_skills(candidate.get(id=q['id']).skills.all().values())
            common_skills = find_common_skills(job_details['job_skills'], candidate_skills)
            if common_skills > res['common_skills']:
                res['title'] = q['title']
                res['id'] = q['id']
                res['skills'] = candidate_skills
                res['common_skills'] = common_skills
        res.pop('common_skills', None)
        print(res)
        return Response(res, status=status.HTTP_200_OK)


class AddCandidateApiView(APIView):
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        # skills = Skill.objects;
        # print(skills)
        # serializer = SkillSerializer(skills, many=True)
        # print(serializer.data);
        # return Response(serializer.data, status=status.HTTP_200_OK)
        # for c in Candidate.objects.raw('SELECT * FROM gloat.matcher_candidate where skills'):
        #     print(c)
        return Response("success", status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        data = {
            'title': request.data.get('title'),
            'skills': request.data.get('skills'),
        }
        candidate = Candidate(title=data['title'])
        candidate.save()
        for skill in data['skills']:
            print(skill)
            s = Skill.objects.filter(name=skill)[:1].get()
            print(s)
            candidate.skills.add(s)
        # for skill in skills:
        #     candidate.skills.set(skill)
        return Response('success', status=status.HTTP_201_CREATED)

        # try:
        #     candidate.save()
        #     return Response('success', status=status.HTTP_201_CREATED)
        # except BaseException as err:
        #     print("An exception occurred")
        #     return Response(err, status=status.HTTP_400_BAD_REQUEST)

        # serializer = CandidateSerializer(data=data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        #
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddSkillApiView(APIView):
    def post(self, request, *args, **kwargs):
        data = {
            'name': request.data.get('name'),
        }
        print(data['name'])
        skill = Skill(name=data['name'])
        try:
            skill.save()
            return Response('success', status=status.HTTP_201_CREATED)
        except BaseException as err:
            print("An exception occurred")
            return Response(err.__str__(), status=status.HTTP_400_BAD_REQUEST)


class AddJobApiView(APIView):
    def post(self, request, *args, **kwargs):
        data = {
            'title': request.data.get('title'),
            'skills': request.data.get('skills'),
        }
        job = Job(title=data['title'])
        job.save()
        for skill in data['skills']:
            s = Skill.objects.filter(name=skill)[:1].get()
            job.skills.add(s)
        return Response('success', status=status.HTTP_201_CREATED)
