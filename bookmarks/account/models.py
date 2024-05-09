from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)  # null=True 允许存储null
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)  # blank=True 可以为空，填写表单的时候也可以为空

    def __str__(self):
        return f'Profile for user {self.user.username}'


class Contact(models.Model):
    # user_from 发起关注的人，user_to 被关注的人
    user_from = models.ForeignKey('auth.User', related_name='rel_from_set', on_delete=models.CASCADE)  # 反向查询所有Contact实例
    user_to = models.ForeignKey('auth.User', related_name='rel_to_set', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return f'{self.user_from} follows {self.user_to}'


# Add following field to User dynamically  todo 看不懂
user_model = get_user_model()
user_model.add_to_class('following',
                        models.ManyToManyField('self',
                                               through=Contact,
                                               related_name='followers',
                                               symmetrical=False))

# class User(models.Model):
#     # other fields...
#
#     @property
#     def following(self):
#         return [contact.user_to for contact in self.rel_from_set.all()]
#
#     @property
#     def followers(self):
#         return [contact.user_from for contact in self.rel_to_set.all()]
