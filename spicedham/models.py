from django.db import models as djmodels

class WordProbability(djmodels.Model):
    word = djmodels.CharField(max_length=255, primary_key=True)
    numSpam = djmodels.IntegerField()
    numTotal = djmodels.IntegerField()

    def __unicode__(self):
        return self.word
