from django.db import models

# Create your models here.

class LineInfo(models.Model):
    name = models.CharField(max_length = 255)
    ip = models.CharField(max_length = 255)
    port = models.CharField(max_length = 255)
    
    def __str__(self):
        return self.name

class Indicator(models.Model):
    DATA_TYPE = (
        ('BIT', 'BIT'), ('STRING', 'STRING'), ('STATUS', 'STATUS'), ('ERROR CODE', 'ERROR CODE')
    )
    DISPLAY_TYPE = (
        ('BUTTON', 'BUTTON'), ('INDICATOR', 'INDICATOR'), ('TEXT', 'TEXT'), ('NUMBER','NUMBER')
    )
    machineID = models.CharField(max_length = 255)
    # line = models.ManyToManyField(LineInfo)
    lineID = models.CharField(max_length = 255)
    name = models.CharField(max_length = 255)
    tag_id = models.CharField(max_length = 255)
    register = models.CharField(max_length = 255)
    data_type = models.CharField(max_length = 255, choices=DATA_TYPE)
    display = models.CharField(max_length = 255, choices=DISPLAY_TYPE)
    color = models.CharField(max_length = 255,blank=True)
    asg = models.BooleanField(default=False)

    def __str__(self):
        return "%s %s %s" % (self.name, self.lineID, self.machineID)

class MachineInfo(models.Model):
    line_name = models.ForeignKey(LineInfo, on_delete=models.CASCADE, null=True)
    machineID = models.CharField(max_length = 255)
    machine_no = models.CharField(max_length = 255)
    machine_name = models.CharField(max_length = 255)
    ip_camera = models.CharField(max_length = 255)

    def __str__(self):
        return self.ip_camera
    
class ErrorNotification(models.Model):
    tag_member = models.ForeignKey(Indicator, on_delete=models.CASCADE, null=True)
    error_code = models.CharField(max_length= 255)
    error_message = models.CharField(max_length= 255)

    def __str__(self):
        return self.error_message
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


    