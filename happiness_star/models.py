from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


def one_to_five(number):

    if number < 1 or number > 5:
        raise ValidationError('Must be between 1 and 5')


class Star(models.Model):

    class Meta:
        unique_together = ('user', 'date')

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()

    spirit = models.IntegerField('energy / spirit', validators=[one_to_five])
    exercise = models.IntegerField(validators=[one_to_five])
    work = models.IntegerField(validators=[one_to_five])
    play = models.IntegerField(validators=[one_to_five])
    friends = models.IntegerField(validators=[one_to_five])
    adventure = models.IntegerField('romance / adventure', validators=[one_to_five])

    def overall(self):
        return (self.spirit + self.exercise + self.play + self.work +
                self.friends + self.adventure) / 6.0

    def __repr__(self):
        return '<Star user=%s date=%s>' % (self.user.email,
                                           self.date.isoformat())

    def __str__(self):
        return 'user: %s, date: %s, overall: %f' % (
            self.user.username,
            self.date.isoformat(),
            self.overall())

    def __iter__(self):
        return iter([('spirit', self.spirit), ('exercise', self.exercise),
                     ('play', self.play), ('work', self.work),
                     ('friends', self.friends), ('adventure', self.adventure),
                     ('tags', [tag.name for tag in self.tag_set.all()]),
                     ('date', self.date.isoformat())])


class Tag(models.Model):

    name = models.CharField(max_length=64, unique=True)
    star = models.ManyToManyField(Star)

    def __repr__(self):
        return '<Tag name=%s>' % (self.name,)

    def __str__(self):
        return '%s' % (self.name,)
