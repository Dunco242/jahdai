from django import forms
from .models import Student, Staff, Milestone, Incident, Fee, Certification

from django import forms
from .models import Student

class StudentRegistrationForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    due_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    amount = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Student
        fields = '__all__'
        exclude = ['student_fee']

    def save(self, commit=True):
        student = super().save(commit=False)

        # Save the student instance first
        student.save()

        # Create a related Fee object for the student with the initial fee
        due_date = self.cleaned_data.get('due_date')
        amount = self.cleaned_data.get('amount', 0.0)
        payment_status = 'unpaid'  # Default to 'unpaid'
        Fee.objects.create(student=student, amount=amount, due_date=due_date, payment_status=payment_status)

        return student




class StaffRegistrationForm(forms.ModelForm):
    certs = forms.ModelMultipleChoiceField(
        queryset=Certification.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Staff
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'role', 'certs']




class MilestoneForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Milestone
        fields = '__all__'
        

class IncidentForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Incident
        fields = '__all__'

class StudentStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['status']

class PaymentStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Fee
        fields = ['amount', 'payment_status']

class NotificationForm(forms.Form):
    custom_message = forms.CharField(widget=forms.Textarea, required=True)



class StudentStatusForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Student
        fields = ['parent1_f_name', 'parent1_l_name', 'parent2_f_name', 'parent2_l_name',
                    'first_name', 'last_name', 'date_of_birth', 'email', 'phone_number',
                    'address', 'allergies', 'status', 'allergies']




class FeeForm(forms.ModelForm):
    due_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Fee
        fields = ['payment_status', 'amount', 'due_date']



class CertForm(forms.ModelForm):
    class Meta:
        model = Certification
        fields = ['name']
        widgets = {
            'name': forms.CheckboxSelectMultiple,
        }
