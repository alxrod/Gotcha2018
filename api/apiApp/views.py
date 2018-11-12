from django.http import HttpResponse
from django.template import loader

from django.utils import timezone
import datetime

from .models import Player, TargetRel
import json
from operator import attrgetter
import random

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from operator import itemgetter

from .forms import LocForm


def Logout(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required
def index(request, *args, **kwargs):
	if request.method == 'POST':
		if request.user.is_authenticated():
			form = LocForm(request.POST)
			if form.is_valid() and form.cleaned_data['position'] != "unchanged":
				print "Lat Long!"
				if form.cleaned_data['position'] != "unchanged":
					latlon = form.cleaned_data['position'].split(",")
				target = Player.objects.get(id=request.user.player.id)
				oldRel = TargetRel.objects.get(target=target, aliveStatus=True)
				tagger = Player.objects.get(id=oldRel.tagger.id)
				targetsRel = TargetRel.objects.get(tagger=target, aliveStatus=True)

				# THis needs to go into a the main method
				target.aliveStatus= False
				target.timeTagged = timezone.now()
				oldRel.aliveStatus = False
				if form.cleaned_data['position'] != "unchanged":
					oldRel.latitude = latlon[0]
					oldRel.longitude = latlon[1]
				targetsRel.aliveStatus = False
				tagger.numOfTags+=1

				tagger.save()
				target.save()
				oldRel.save()
				targetsRel.save()

				print "Tagging Complete:"
				print target.relForward.last().jsonify()
				newTarget = target.relForward.last().target
				print "Alive Status of Jumping Rel:"
				print target.relForward.last().aliveStatus
				newRel  =  TargetRel(tagger=tagger, target=newTarget)

				newRel.save()
				request.user.player = Player.objects.get(id=request.user.player.id)
				return redirect("/api")
			else:
				return redirect("/api")

	else: 
		everyone = Player.objects.filter(aliveStatus=True)
		everyoneJson = []
		for player in everyone:
			everyoneJson.append(player.dictify())
		random.shuffle(everyoneJson)
		sortedEveryone = reversed(sorted(everyoneJson, key=itemgetter('numOfTags')))

		# Trick to make it work but only really works right where we are
		onMap = TargetRel.objects.filter(longitude__lt=0)
		markedTags = []
		markerString = ""
		for tag in onMap:
			markerString += "&markers=size:mid%7Ccolor:red%7Clabel:%7C"+tag.giveLatLong()

		print markerString

		allTags = TargetRel.objects.filter(aliveStatus=False)
		totalTags = len(allTags)

		tags = TargetRel.objects.filter(tagger=request.user.player).filter(aliveStatus=False)
		yourTagBreakDown = {"c1": 0, "c2": 0, "c3": 0, "c4": 0}
		for tag in tags:
			if tag.target.hsClass == 1:
				yourTagBreakDown["c1"]+=1;
			if tag.target.hsClass == 2:
				yourTagBreakDown["c2"]+=1;
			if tag.target.hsClass == 3:
				yourTagBreakDown["c3"]+=1;
			if tag.target.hsClass == 4:
				yourTagBreakDown["c4"]+=1;

		totalTagBreakDown = {"c1": 0, "c2": 0, "c3": 0, "c4": 0}
		for tag in allTags:
			if tag.target.hsClass == 1:
				totalTagBreakDown["c1"]+=1;
			if tag.target.hsClass == 2:
				totalTagBreakDown["c2"]+=1;
			if tag.target.hsClass == 3:
				totalTagBreakDown["c3"]+=1;
			if tag.target.hsClass == 4:
				totalTagBreakDown["c4"]+=1;

		print "Breakdown:"
		print yourTagBreakDown
		if len(tags) > 0:
			recent = tags.last().target.timeTagged
		else: 
			recent = "*no tags yet*"

		if request.user.player == request.user.player.relForward.last().target:
			win = True
		else:
			win = False

		if request.user.is_authenticated():
			context = {
					  "targetName": request.user.player.relForward.last().target.giveName(),
					   "targetDirectory": "apiApp/images/pics/" + request.user.player.relForward.last().target.directoryPath,
					   "yourDirectory": "apiApp/images/pics/" + request.user.player.directoryPath,
					   "taggerId": request.user.player.id,
					   "targetClass": request.user.player.relForward.last().target.fancyClass(),
					   "aliveStatus": request.user.player.aliveStatus,
					   "everyone": sortedEveryone,
					   "markerString": markerString,
					   "yourTags": request.user.player.numOfTags,
					   "yourRecent": recent,
					   "yourBD": yourTagBreakDown,
					   "totalBD": totalTagBreakDown,
					   "totalTags": totalTags,
					   "win": win,
			}
		else:
			context = {}
		template = loader.get_template('apiApp/index.html')
		return HttpResponse(template.render(context, request))


def credentialTester(request):
	return json.dumps(user)

def getPlayer(request, player_separated_email):
	player_email = player_separated_email+"@milton.edu"
	return HttpResponse(Player.objects.get(email=player_email).jsonify())

def getTargetRel(request, rel_id):
	return HttpResponse(TargetRel.objects.get(id=rel_id).jsonify())

def tagPlayer(request, tagger_id):
	tagger = Player.objects.get(id=tagger_id)
	oldRel = TargetRel.objects.get(tagger=tagger, aliveStatus=True)
	target = Player.objects.get(id=oldRel.target.id)
	targetsRel = TargetRel.objects.get(tagger=target, aliveStatus=True)

	# THis needs to go into a the main method
	target.aliveStatus= False
	target.timeTagged = timezone.now()
	oldRel.aliveStatus = False
	targetsRel.aliveStatus = False
	tagger.numOfTags+=1

	tagger.save()
	target.save()
	oldRel.save()
	targetsRel.save()

	print "Tagging Complete:"
	print target.relForward.first().jsonify()
	newTarget = target.relForward.first().target
	newRel  =  TargetRel(tagger=tagger, target=newTarget)

	newRel.save()
	return redirect("/api")


def getRecent(request):
	allTags = TargetRel.objects.filter(aliveStatus=False)
	allTagged = [x.target for x in list(allTags) if x.target.aliveStatus==False]
	print sorted(allTagged, key=attrgetter('timeTagged'))
	jsonified = []
	for i in range(20):
		if i < len(allTagged):
			jsonified.append(allTagged[i].jsonify())
		else:
			break
	return HttpResponse(jsonified)


def getClassTags(request):
	allTags = TargetRel.objects.filter(aliveStatus=False)
	allTags = [x for x in list(allTags) if x.target.aliveStatus==False]
	print "Yup"
	print allTags
	classes = {"tags":[0,0,0,0], "outs":[0,0,0,0]}
	for tag in allTags:
		classes['tags'][tag.tagger.hsClass]+=1
		classes['outs'][tag.target.hsClass]+=1

	return HttpResponse(json.dumps(classes))


