from django.shortcuts import render
from django.http import JsonResponse
from .models import Job
from django_celery_results import models
import json
from django.views.decorators.csrf import csrf_exempt


def home_page(request):
    context_dict = {}
    return render(request, 'circumat/homepage.html', context_dict)


def edu_page(request):
    context_dict = {}
    return render(request, 'circumat/educational-materials.html', context_dict)


def matchmaking_page(request):
    context_dict = {}
    return render(request, 'circumat/matchmaking-tool.html', context_dict)


def online_tools(request):
    context_dict = {}
    return render(request, 'circumat/online-tools.html', context_dict)


def online_databases(request):
    context_dict = {}
    return render(request, 'circumat/online-databases.html', context_dict)


def project_summary(request):
    context_dict = {}
    return render(request, 'circumat/project-summary.html', context_dict)


def circular_economy(request):
    context_dict = {}
    return render(request, 'circumat/circular-economy.html', context_dict)


def academic_papers(request):
    context_dict = {}
    return render(request, 'circumat/academic-papers.html', context_dict)


def home(request):
    """
    Home page off app.
    """
    return render(request, 'circumat/home.html')


@csrf_exempt
def ajaxHandling(request):
    """AJAX handler.

    Checks if the request is a post. Uses from the request the task/job id to fetch the Celery unique identifier.
    In turn it retrieves by using the Celery unique identifier the actual results

    Args:
        object: request
    Returns:
        JSON response of result calculation

    """
    if request.method == 'POST':
        try:

            # start retrieving taskID/JobID
            jobId = request.POST.get('TaskID')

            # The model Job has a primary key that is exactly the matching jobID from the front-end
            celery_id = Job.objects.values_list('celery_id', flat=True).get(pk=jobId)
            if not (celery_id is None):
                # the model Task Results contains the results, so search via celery_id to get the results
                result = models.TaskResult.objects.values_list('result', flat=True).get(task_id=celery_id)
                cleaned_result = json.loads(result)

                data = {
                    'rawResultData': cleaned_result,
                }
                return JsonResponse(data)
            else:
                data = {
                    'status': "job failed (celery_id not found)",
                }
                return JsonResponse(data)
        except Exception as e:
            data = {
                'status': "job failed (Cannot fetch database jobID:" + str(jobId) + ")******" + str(
                    e) + "*********" + "celeryID:" + str(celery_id),
            }
            return JsonResponse(data)
    else:
        return render(request, 'circumat/error.html')
