print("test_models")

# test bad inputs to models
# test create model
# test delete model
# test filter model
# test minimum number of fields that need to be entered
from django.test import TestCase
from gsndb.models import Note, District


class DistrictModelTest(TestCase):
    def test_create_instance_minimum_fields(self):
        newDistrict = District.objects.create(name = 'Denver Public Schools', state = 'CO', city = 'Denver', code = 'DPS')

'''    create_instance_all_fields(self):

    get_instance_all_fields(self):

    update_instance(self):

    bad_field_inputs(self):

    add_note(self):

    delete_instance(self):
''' 


'''
class District(models.Model):

    state = models.CharField(
        max_length=2,
        blank = True,
        choices = STATE_CHOICES,
    )
    city = models.CharField(max_length=50, blank=True)
    code = models.CharField(max_length=10, blank=True)
    name = models.CharField(max_length=100, blank=True)
    notes = GenericRelation(Note)'''