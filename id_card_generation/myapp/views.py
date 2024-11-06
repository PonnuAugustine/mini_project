from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError
from .models import Profile
from .models import Department
from .models import Batch
from .models import Student
from .models import Faculty
from .models import Verification

# Create your views here.
def index(request):
    return render(request, 'index.html')
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Admin login check
        admin_username = "admin"
        admin_password = "Admin@123"

        if username == admin_username and password == admin_password:
            # Set the session flag for admin
            request.session['admin_logged_in'] = True
            return redirect('adminhome')  # Redirect to admin home

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)  # Log in the user
            
            try:
                # Redirect to the appropriate homepage based on the user's role
                profile = Profile.objects.get(user=user)
                if profile.role == 'student':
                    return redirect('studenthome')  # Change to the URL name for student home
                elif profile.role == 'faculty':
                    return redirect('facultyhome')  # Change to the URL name for faculty home
            except Profile.DoesNotExist:
                messages.error(request, 'Profile does not exist.')
                return redirect('index')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('index')  # Redirect back to login page on error
    return render(request, 'login.html')
def register(request):
    print("Received a request to register.")
    departments = Department.objects.all() 
    if request.method == 'POST':
        print("Handling POST request.")
        username = request.POST['username']
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        password = request.POST['password']
        user_type = request.POST['userType']  # Assuming this comes from your form
        department_id = request.POST.get('department')  # Assuming department is part of the form for faculty

        print(f"User Type: {user_type}") 

        try:
            print("Attempting to create user.")
            user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
            user.save()

            profile = Profile.objects.create(user=user, role=user_type)
            profile.save()

            if user_type == 'faculty':
                department = Department.objects.get(id=department_id)  # Get the department for faculty
                faculty = Faculty.objects.create(user=user, department=department)  # Create a Faculty record
                faculty.save()
                print("Faculty data saved successfully.")

            messages.success(request, 'Account created successfully!')
            print("Redirecting to login")
            return redirect('login')
        except IntegrityError:
            messages.error(request, 'Username already exists!')
            print("Username already exists, redirecting back to register.")
            return redirect('register')
    print("Rendering registration form.")
    return render(request, 'register.html', {'departments': departments})  # Render the registration form

def studenthome(request):
    return render(request, 'studenthome.html')

def facultyhome(request):
    faculty = Faculty.objects.get(user=request.user)
    # Count of students in the faculty's department with "Pending" status
    pending_students_count = Student.objects.filter(
        department=faculty.department,
        approval_status='Pending'
    ).count()

    context = {
        'faculty': faculty,
        'pending_students_count': pending_students_count,
    }
    return render(request, 'facultyhome.html', context)

def studentdata(request):
    # Get the logged-in user (faculty)
    faculty = Faculty.objects.get(user=request.user)

    # Fetch the students from the same department as the faculty
    students = Student.objects.filter(department=faculty.department)

    # Pass the student data to the template
    return render(request, 'fstudentdata.html', {'students': students})

def verify_student(request, admission_no):
    if request.method == "POST":
        student = get_object_or_404(Student, admission_no=admission_no)
        student.approval_status = 'Approved'
        student.save()
        messages.success(request, 'Student has been verified successfully.')
    return redirect('studentdata')

def submit_correction(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        correction_details = request.POST.get('correction_details')
        
        # Fetch the student instance
        student = get_object_or_404(Student, admission_no=student_id)
        
        # Create a new Verification (correction) request
        Verification.objects.create(
            student=student,
            requested_by=request.user,
            details=correction_details,
            status='Pending'
        )

        # Update the student's approval status to "Sent Back"
        student.approval_status = 'Sent Back'
        student.save()
        
        messages.success(request, 'Correction request sent successfully.')
        return redirect('studentdata')
    
    return redirect('studentdata')

def view_corrections(request):
    # Fetch the student instance based on the logged-in user
    student = get_object_or_404(Student, user=request.user)  # Assuming `user` is linked to Django's User model
    
    # Fetch all verification (correction) requests related to the student
    corrections = Verification.objects.filter(student=student)

    return render(request, 'studentupdates.html', {
        'corrections': corrections
    })

def pendingupdates(request):
    return render(request, 'f_pendingupdates.html')

def studentform(request):
    user = request.user  # Get the logged-in user
    departments = Department.objects.all()
    batches = Batch.objects.all()

    if request.method == 'POST':
        # Manually fetch form data from the POST request
        admission_no = request.POST.get('admission_no')
        department_id = request.POST.get('department')
        batch_id = request.POST.get('batch')
        house = request.POST.get('house')
        street = request.POST.get('street')
        city = request.POST.get('city')
        district = request.POST.get('district')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        phone = request.POST.get('phone')
        guardian_phone = request.POST.get('guardian_phone')
        blood_group = request.POST.get('blood_group')
        date_of_birth = request.POST.get('date_of_birth')
        photo = request.FILES.get('photo')  # Handle the uploaded file

        # Get related objects for ForeignKey fields
        department = Department.objects.get(id=department_id)
        batch = Batch.objects.get(id=batch_id)

        # Check if student record already exists
        try:
            student = Student.objects.get(user=user)
        except Student.DoesNotExist:
            student = Student(user=user)

        # Update or create student details
        student.admission_no = admission_no
        student.department = department
        student.batch = batch
        student.house = house
        student.street = street
        student.city = city
        student.district = district
        student.state = state
        student.pincode = pincode
        student.phone = phone
        student.guardian_phone = guardian_phone
        student.blood_group = blood_group
        student.date_of_birth = date_of_birth
        
        if photo:
            student.photo = photo  # Only update the photo if a new one is uploaded

        student.save()  # Save the student data

        # Add a success message
        messages.success(request, "Data submitted successfully.")

        return redirect('studentform')  # Redirect to a success page or another view

    return render(request, 'student_form.html', {
        'departments': departments,
        'batches': batches,
        'user': user  # Pass the user to the template if needed
    })

def studentprofile(request):
    return render(request, 'student_profile.html')

def adminhome(request):
    return render(request, 'adminhome.html')

def adminbase(request):
    return render(request, 'adminbase.html')

def view_verified_students(request):
    verified_students = Student.objects.filter(approval_status='Approved')
    return render(request, 'view_students.html', {'verified_students': verified_students})

def batch(request):
    if request.method == 'POST':
        start_year = request.POST.get('start_year')
        end_year = request.POST.get('end_year')
    
        # Validate input
        if start_year and end_year:
            try:
                Batch.objects.create(start_year=start_year, end_year=end_year)
                messages.success(request, 'Batch created successfully!')
                return redirect('batch')  # Redirect to the batch page or another appropriate page
            except Exception as e:
                messages.error(request, f"Error creating batch: {str(e)}")
        else:
            messages.error(request, 'Please fill in all fields.')

    # Fetch all departments to display in the form
    batches = Batch.objects.all()
    return render(request, 'batch.html', {'batches': batches})

def department(request):
    if request.method == 'POST':
        department_name = request.POST.get('department')
        if department_name:
            try:
                Department.objects.create(name=department_name)
            except IntegrityError:
                # Handle error if department name already exists
                error_message = "Department with this name already exists."
                departments = Department.objects.all()
                return render(request, 'department.html', {'departments': departments, 'error_message': error_message})
    
    # Fetch all departments to display
    departments = Department.objects.all()
    return render(request, 'department.html', {'departments': departments})

def facultyverify(request):
    # Get all faculty members
    all_faculties = Faculty.objects.all()

    # If the request method is POST, update verification status
    if request.method == 'POST':
        faculty_id = request.POST.get('faculty_id')
        faculty = get_object_or_404(Faculty, id=faculty_id)
        
        # Update the verification status
        faculty.is_verified = True
        faculty.save()

        # Display a success message
        messages.success(request, f"{faculty.user.first_name} {faculty.user.last_name} has been verified.")
        return redirect('facultyverify')  # Redirect back to the verification page

    # Render the template with all faculty members
    return render(request, 'faculty_verify.html', {'all_faculties': all_faculties})

def verify_faculty(request, faculty_id):
    faculty = get_object_or_404(Faculty, id=faculty_id)
    faculty.is_verified = True
    faculty.save()
    messages.success(request, f"{faculty.user.first_name} {faculty.user.last_name} has been verified successfully.")
    return redirect('faculty_verify') 

def generateid(request):
    return render(request, 'generate_id.html')

def idcard(request, student_id):
    student = get_object_or_404(Student, admission_no=student_id)
    context = {
        'MEDIA_URL': settings.MEDIA_URL,
        'student': student
    }
    return render(request, 'idcard.html', context)

def generate_multiple_idcards(request):
    # Fetch all verified students (students whose approval status is 'Approved')
    verified_students = Student.objects.filter(approval_status='Approved')
    
    return render(request, 'multipleid.html', {'verified_students': verified_students})