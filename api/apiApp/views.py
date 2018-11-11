from django.http import HttpResponse
from django.template import loader

from django.utils import timezone
import datetime

from .models import Player, TargetRel
import json
from operator import attrgetter

def index(request):
    template = loader.get_template('apiApp/index.html')
    context = {}
    return HttpResponse(template.render(context, request))

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
	return HttpResponse(json.dumps("Valid Tag"))


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


