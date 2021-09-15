from django.db import models
from fresher.models import ProFrehserMeeting

# Create your models here.


# Table to store uid for recording purpose
class RecordingUid(models.Model):
    meeting         = models.OneToOneField(ProFrehserMeeting, on_delete = models.CASCADE, related_name = 'uids')
    pro_uid         = models.IntegerField(default=0)
    fresh_uid       = models.IntegerField(default=0)

    def __str__(self):
        return "Meeting {} profUid {} FresherUid {}".format(self.meeting.id, self.pro_uid, self.fresh_uid)
