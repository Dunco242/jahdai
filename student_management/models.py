from django.db import models

class Student(models.Model):
    parent1_f_name = models.CharField(max_length=50)
    parent1_l_name = models.CharField(max_length=50)
    parent2_f_name = models.CharField(max_length=50, blank=True, null=True)
    parent2_l_name = models.CharField(max_length=50, blank=True, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    allergies = models.TextField(blank=True, null=True)

    # Define choices for the status field
    STATUS_CHOICES = [
        ('current', 'Current Student'),
        ('past', 'Past Student'),
        ('sick', 'Sick Student'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    # Define a related_name for the student_fee field
    student_fee = models.OneToOneField('Fee', related_name='student_fee_relation', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        # Call the "real" save() method
        super().save(*args, **kwargs)

        # If this student doesn't have an associated fee yet, create one
        if not hasattr(self, 'student_fee'):
            Fee.objects.create(student=self)




class Certification(models.Model):
    CERT_CHOICES = [
        ('first_aid', 'First Aid'),
        ('cpr', 'CPR'),
        ('6m_criminal_record', '6m Criminal Record'),
        ('1yr_criminal_record', '1yr Criminal Record'),
    ]

    name = models.CharField(max_length=50, choices=CERT_CHOICES)

    def __str__(self):
        return self.get_name_display()



class Staff(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    certs = models.ManyToManyField(Certification, blank=True)
    role = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"



class Event(models.Model):
    event_name = models.CharField(max_length=100)
    event_date = models.DateTimeField()
    description = models.TextField()

    def __str__(self):
        return self.event_name

class Fee(models.Model):
    student = models.OneToOneField('Student', related_name='fee_relation', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField(null=True, blank=True)
    payment_status_choices = [
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('credit', 'Credit'),
        ('payment_plan', 'Payment Plan'),
    ]
    payment_status = models.CharField(max_length=20, choices=payment_status_choices)

    def __str__(self):
        return f"Fee for {self.student.first_name} {self.student.last_name}"

        

class Milestone(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    description = models.TextField()
    date = models.DateField()

    def __str__(self):
        return f"Milestone for {self.student}"

class Incident(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    description = models.TextField()
    date = models.DateField()

    def __str__(self):
        return f"Incident for {self.student}"

class Allergy(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    allergens = models.TextField()

    def __str__(self):
        return f"Allergies for {self.student}"
