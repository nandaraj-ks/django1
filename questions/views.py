from django.shortcuts import render, redirect

# Create your views here.
def viewQuestion(request):
	import random
	from models import Question, QuestionLog
	from forms import ChoiceForm
	from subscriber.models import Subscriber
	from sample.utils.appConfig import LevelDefinition

	subscriber = Subscriber.objects.get(user=request.user)
	askedQuestionsForUser = QuestionLog.objects.values_list('question', flat=True).filter(
		subsciber__exact=subscriber.id, 
		question__level=subscriber.level,
		isComplete__exact=True
	)
	numberOfQnForLevel = LevelDefinition().getNumberOfQuestionsForLevel(subscriber.level)
	if request.POST:
		question = Question.objects.get(pk=int(request.POST.get('questionHidden')))
		form = ChoiceForm(question, data=request.POST)
		if form.is_valid():
			isComplete = (question.correctChoice == form.cleaned_data['choiceSelect'])
			if isComplete:
				subscriber.mooblePoint += 1

			dictToSave = {
				'question' : question,
				'subsciber' : subscriber,
				'reply' : form.cleaned_data['choiceSelect'],
				'isComplete' : isComplete
			}
			questionLog = QuestionLog(**dictToSave)
			print len(askedQuestionsForUser)
			questionLog.save()
			print len(askedQuestionsForUser)
			print numberOfQnForLevel
			if isComplete:
				# if he has done it right check if the no of qns for the level is met
				# if yes then upgrade his level
				if (len(askedQuestionsForUser) + 1) == numberOfQnForLevel:
					subscriber.level += 1
			subscriber.save()
			return redirect('/')

	questionForUser = Question.objects.filter(
		level__exact=subscriber.level
	).exclude(
		id__in=askedQuestionsForUser
	)
	question = random.choice(questionForUser) if questionForUser else None
	template_values = {
		'question' : question,
		'form' : ChoiceForm(
			question,
			initial={
				'questionHidden' : question.id
			}
		) if questionForUser else None,
		'subscriber' : subscriber,
		'questionNumber' : len(askedQuestionsForUser) + 1,
		'questionsPending' : (numberOfQnForLevel - len(askedQuestionsForUser))
	}
	return render(request, 'questions/question.html', template_values)


SHEET_PATH = '/home/dev5/Downloads/mooble_sms.xlsx'
QUESTION_HEADER = 'WebQuestion'
CHOICES_HEADER = 'WebChoice[0-9]+'
CORRECT_CHOICE_HEADER = 'WebAnswer'
LEVEL_HEADER = 'Level'

def createQuestion(request, level, sheetIndex):
	import re
	import datetime
	import xlrd
	from django import http
	from models import Question

	if not request.user.is_superuser:
		print 'User %s does not have the permission to create question.' % request.user.username
		return http.HttpResponse(
			'User <b>%s</b> does not have the permission to create question. <a href="/logout?next=%s">Logout</a>' \
			% (request.user.username, request.path)
		)
	toPut = []
	level = level or 0
	sheetIndex = sheetIndex or 0
	book = xlrd.open_workbook(SHEET_PATH)

	print "The number of worksheets is", book.nsheets

	sh = book.sheet_by_index(int(sheetIndex))
	print sh.name, sh.nrows, sh.ncols
	for rx in range(sh.nrows):
		dictToSave = {
			'answerChoices' : [],
			'level' : level
		}
		print 'Processing Row %s.' % (rx + 1)
		for cx in range(sh.ncols):

			cellHeaderValue = sh.cell_value(0, cx)
			cellValue = str(sh.cell_value(rx, cx)).strip()
			cellName = xlrd.cellname(rx, cx)

			if re.match(QUESTION_HEADER, cellHeaderValue):
				print 'Found question %s at cell %s.' % (cellValue, cellName)
				dictToSave['question'] = cellValue
			elif re.match(CHOICES_HEADER, cellHeaderValue):
				print 'Found choice %s at cell %s.' % (cellValue, cellName)
				if cellValue:
					dictToSave['answerChoices'].append(cellValue)
			elif re.match(CORRECT_CHOICE_HEADER, cellHeaderValue):
				print 'Found correct choice as %s at cell %s.' %(cellValue, cellName)
				dictToSave['correctChoice'] = cellValue
			elif re.match(LEVEL_HEADER, cellHeaderValue):
				print 'Found level as %s at cell %s.' %(cellValue, cellName)
				dictToSave['level'] = cellValue
		dictToSave['answerChoices'] = ','.join(dictToSave['answerChoices'])
		dictToSave['pub_date'] = datetime.datetime.now()
		print 'Creating Question %d' % (rx + 1)
		toPut.append(Question(**dictToSave))
	if len(toPut) > 0:
		print 'Successfully created all questions. Number of Qns created are %d.' % sh.nrows
		Question.objects.bulk_create(toPut)
	return http.HttpResponse('Successfully created all questions. Number of Qns created are %d.' % sh.nrows)


