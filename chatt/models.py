from django.db import models
from django.contrib.auth.models  import User 

# Create your models here.


class TwoGroup(models.Model):
    prof = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'pro_chats')
    fresher = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'fre_chat')
    channel_name = models.CharField(max_length = 20, default = '')
    created_on = models.DateTimeField(auto_now = True)

    def __str__(self):
        return "Prof {} Fresher {} Channel Name {}".format(self.prof.first_name, self.fresher.first_name, self.channel_name)


class Messages(models.Model):
    chatgroup = models.ForeignKey(TwoGroup, related_name= 'chats', on_delete = models.CASCADE)
    message   = models.CharField(max_length = 500, default = '')
    sender    = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'sent_messages')
    created_on = models.DateTimeField(auto_now =  True)


    def __str__(self):
        return "User {} chat group {}".format(self.sender.first_name, self.chatgroup.channel_name)


class OnlineStatus(models.Model):
    user            = models.OneToOneField(User, on_delete = models.CASCADE, related_name = 'user_status')
    status_count    = models.IntegerField(default = 0)
    last_seen       = models.DateTimeField(auto_now = True)

    def __str__(self):
        return "User {} status count {}".format(self.user.first_name, self.status_count)