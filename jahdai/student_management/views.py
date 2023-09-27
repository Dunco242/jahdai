from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from .models import Student, Staff, Event, Fee, Milestone, Incident, Allergy, Certification
from django.contrib import messages
from django.core.mail import send_mail
from django import forms
from .forms import StudentRegistrationForm, StaffRegistrationForm, MilestoneForm, IncidentForm, NotificationForm, StudentStatusUpdateForm, PaymentStatusUpdateForm, StudentStatusForm, FeeForm, CertForm  # Import your forms
from .models import Student
from django.http import JsonResponse, HttpResponseRedirect
from django.db.models import Q
from reportlab.pdfgen import canvas
import io
from django.urls import reverse





from django.shortcuts import get_object_or_404

def student_registration(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        fee_form = FeeForm(request.POST)  # Create a form for the Fee
        if form.is_valid() and fee_form.is_valid():
            student = form.save()  # Save the student instance first

            # Check if a Fee object already exists for the student
            fee, created = Fee.objects.get_or_create(student=student, defaults={
                'amount': fee_form.cleaned_data.get('amount', 0.0),
                'payment_status': fee_form.cleaned_data.get('payment_status', 'unpaid'),
                'due_date': fee_form.cleaned_data.get('due_date')
            })

            # If a Fee object was not created (i.e., it already existed), update its values
            if not created:
                fee.amount = fee_form.cleaned_data.get('amount', 0.0)
                fee.payment_status = fee_form.cleaned_data.get('payment_status', 'unpaid')
                fee.due_date = fee_form.cleaned_data.get('due_date')
                fee.save()

            messages.success(request, 'Student registered successfully.')
            return redirect('student_registration')
    else:
        form = StudentRegistrationForm()
        fee_form = FeeForm()  # Initialize an empty FeeForm

    students = Student.objects.all()  # Queryset of all students
    return render(request, 'student_registration.html', {'form': form, 'fee_form': fee_form, 'students': students})




def staff_registration(request):
    if request.method == 'POST':
        form = StaffRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Staff registered successfully.')
            return redirect('staff_registration')  # Redirect to the same page after successful registration
    else:
        form = StaffRegistrationForm()
    
    return render(request, 'staff_registration.html', {'form': form})



def student_list(request):
    # Retrieve a list of all students from the database
    students = Student.objects.all()
    
    return render(request, 'student_list.html', {'students': students})

def staff_list(request):
    # Retrieve a list of all staff members from the database
    staff = Staff.objects.all()
    
    return render(request, 'staff_list.html', {'staff': staff})

def student_detail(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    fee = Fee.objects.get(student=student)

    if request.method == 'POST':
        student_form = StudentStatusForm(request.POST, instance=student)
        fee_form = FeeForm(request.POST, instance=fee)
        if student_form.is_valid() and fee_form.is_valid():
            student_form.save()
            fee_form.save()
            messages.success(request, 'Student and fee status updated successfully.')
            return redirect('student_list')
    else:
        student_form = StudentStatusForm(instance=student)
        fee_form = FeeForm(instance=fee)

    context = {
        'student': student,
        'fee': fee,
        'student_form': student_form,
        'fee_form': fee_form,
    }
    return render(request, 'student_detail.html', context)



def allergies(request, student_id):
    student = get_object_or_404(Student, id=student_id)  # Use get_object_or_404 to handle 404 if student is not found
    try:
        allergies = Allergy.objects.get(student=student)
    except Allergy.DoesNotExist:
        allergies = None  # Set allergies to None if there are no allergies for the student

    return render(request, 'allergies.html', {'student': student, 'allergies': allergies})



def add_milestone(request):
    if request.method == 'POST':
        form = MilestoneForm(request.POST)
        if form.is_valid():
            milestone = form.save(commit=False)
            milestone.student = student
            milestone.save()
            # Add success message or redirection logic here

    else:
        form = MilestoneForm()
    
    return render(request, 'add_milestone.html', {'form': form})




def add_incident(request):
    if request.method == 'POST':
        form = IncidentForm(request.POST)
        if form.is_valid():
            form.save()
            # Add success message or redirection logic here
    else:
        form = IncidentForm()
    
    return render(request, 'incident_form.html', {'form': form})




def search_students(request):
    first_name = request.GET.get('first_name')
    last_name = request.GET.get('last_name')
    if first_name and last_name:
        students = Student.objects.filter(Q(first_name__icontains=first_name) & Q(last_name__icontains=last_name))
    elif first_name:
        students = Student.objects.filter(Q(first_name__icontains=first_name))
    elif last_name:
        students = Student.objects.filter(Q(last_name__icontains=last_name))
    else:
        students = Student.objects.none()
    student_list = list(students.values('first_name', 'last_name', 'email'))
    return JsonResponse({'students': student_list})



def autocomplete_students(request):
    term = request.GET.get("term")
    students = Student.objects.filter(
        Q(first_name__icontains=term) | Q(last_name__icontains=term)
    )[:10]  # Limit the results to 10 for performance
    results = [{"id": student.id, "value": f"{student.first_name} {student.last_name}"} for student in students]
    return JsonResponse(results, safe=False)



def autocomplete_incidents(request):
    term = request.GET.get("term")
    incidents = Incident.objects.filter(description__icontains=term)[:10]  # Limit the results to 10 for performance
    results = [{"id": incident.id, "value": incident.description} for incident in incidents]
    return JsonResponse(results, safe=False)



def autocomplete_milestones(request):
    term = request.GET.get("term")
    milestones = Milestone.objects.filter(description__icontains=term)[:10]  # Limit the results to 10 for performance
    results = [{"id": milestone.id, "value": milestone.description} for milestone in milestones]
    return JsonResponse(results, safe=False)



def update_student_status(request, student_id):
    student = Student.objects.get(id=student_id)

    if request.method == 'POST':
        form = StudentStatusUpdateForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student status updated successfully.')
            return redirect('student_detail', student_id=student.id)
    else:
        form = StudentStatusUpdateForm(instance=student)

    return render(request, 'update_student_status.html', {'student': student, 'form': form})




def send_email(request):
    email = request.GET.get('email')
    description = request.GET.get('description')

    # Send an email
    send_mail(
        'Incident Report',
        description,
        'your-email@example.com',  # Replace with your email
        [email],
        fail_silently=False,
    )

    # Save a copy of the sent email in PDF format
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100, 100, description)
    p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.close()

    # Save the PDF to a file
    with open('email.pdf', 'wb') as f:
        f.write(pdf)

    return JsonResponse({'status': 'success'})


def staff_detail(request, staff_id):
    staff = get_object_or_404(Staff, pk=staff_id)

    if request.method == 'POST':
        staff_form = StaffRegistrationForm(request.POST, instance=staff)
        cert_form = CertForm(request.POST, instance=staff)

        if staff_form.is_valid() and cert_form.is_valid():
            staff_form.save()
            cert_form.save()
            return HttpResponseRedirect(reverse('staff_detail', args=(staff.id,)))

    else:
        staff_form = StaffRegistrationForm(instance=staff)
        cert_form = CertForm(instance=staff)

    return render(request, 'staff_detail.html', {'staff': staff, 'staff_form': staff_form, 'cert_form': cert_form})