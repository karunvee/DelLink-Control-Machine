from django.db import models

# Create your models here.

class LineInfo(models.Model):
    name = models.CharField(max_length = 255)
    ip = models.CharField(max_length = 255)
    post = models.CharField(max_length = 255)
    
    def __str__(self):
        return self.name

class Indicator(models.Model):
    DATA_TYPE = (
        ('BIT', 'BIT'), ('INT', 'INT'), ('FLOAT', 'FLOAT'),('ASCII', 'ASCII')
    )
    DISPLAY_TYPE = (
        ('BIT', 'BIT'), ('ASCII', 'ASCII')
    )
    name = models.CharField(max_length = 255)
    tag_id = models.CharField(max_length = 255)
    register = models.CharField(max_length = 255)
    data_type = models.CharField(max_length = 255, choices=DATA_TYPE)
    display = models.CharField(max_length = 255, choices=DATA_TYPE)
    asg = models.BooleanField(default=False)

    def __str__(self):
        return self.name

# class Lines(models.Model):
#     name = models.CharField(max_length = 255, null=True)

#     def __str__(self):
#         return self.name

# class Indicator(models.Model):
#     DATA = (
#         ('Bit' , 'Bit' ),('Word', 'Word')
#     )
#     OUTPUT = (
#         ('Indicator' , 'Indicator' ),('Data Display', 'Data Display'),('Data Graph', 'Data Graph')
#     )
#     machine_id = models.CharField(max_length = 255)
#     address = models.CharField(max_length = 255)
#     name = models.CharField(max_length = 255)
#     description = models.CharField(max_length = 255)
#     data_type = models.CharField(max_length = 255, null=True, choices=DATA)
#     output_type = models.CharField(max_length = 255, null=True, choices=OUTPUT)
#     flag = models.BooleanField(default=False)

#     def __str__(self):
#         return self.name

# class PLCmembers(models.Model):
#     line = models.ManyToManyField(Lines)
#     indicator_members = models.ForeignKey(Indicator, null=True, on_delete=models.SET_NULL, blank=True)
#     ip = models.CharField(max_length = 255)
#     port = models.CharField(max_length = 255)
#     name = models.CharField(max_length = 255)
#     plc_model = models.CharField(max_length = 255)
#     owner = models.CharField(max_length = 255, blank=True)
#     pic_path = models.CharField(max_length = 255, blank=True)

#     def __str__(self):
#         return self.name


    