from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.management import call_command
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.core import serializers
from django.db.models import Prefetch
from django.db import transaction
from datetime import datetime
import logging
import git
import csv
import os

logger = logging.getLogger(__name__)

# Create your views here.
@csrf_exempt
def github_webhook(request):
    if request.method == "POST":
        try:
            logger.info("Webhook fired. Attempting to pull new code from GitHub...")
            repo = git.Repo('/home/neoncamouflage/Tanja')
            origin = repo.remotes.origin
            origin.pull()
            logger.info("Code pulled successfully, now running collectstatic...")
            call_command('collectstatic', '--noinput')
            logger.info("collectstatic completed successfully.")

            logger.info("Reloading the web application...")
            os.system('touch /var/www/neoncamouflage_pythonanywhere_com_wsgi.py')
            logger.info("Application reloaded successfully.")

            return HttpResponse("Update successful, static files collected and app reloaded.")
        except Exception as e:
            logger.error(f"Failed to update: {e}", exc_info=True)
            return HttpResponse(str(e), status=500)
    else:
        logger.warning("Received a non-POST request to the webhook.")
        return HttpResponse("Only POST requests allowed", status=405)