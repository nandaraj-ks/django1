class LevelDefinition(object):
	def getNumberOfQuestionsForLevel(self, level):
		levels = {
			'default' : 10,
			0 : 20,
			1 : 20,
			2 : 20
		}
		return levels.get(level, levels.get('default'))