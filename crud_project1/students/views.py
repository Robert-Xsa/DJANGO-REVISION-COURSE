from django.shortcuts import render, redirect, get_object_or_404
from .forms import StudentForm
from .models import Student

# Create your views here.

#Create students
def create_student(request):
    form = StudentForm()

    if request.method == 'POST':
        form = StudentForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('student_list')

    return render(request,'create.html',{'form':form})

#Display view
def student_list(request):
    students = Student.objects.all()

    return render(request, 'students.html',{'students':students})

#Edit exist record
def update_student(request, id):
    student = get_object_or_404(Student, id)
    form = StudentForm(instance=student)

    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)

        if form.is_valid():
            form.save()
            return redirect('student_list')

    return render(request, 'update.html', {'form': form})

#Delete/ Remove records
def delete_student(request, id):
    student = get_object_or_404(Student, id =id)

    if request.method == 'POST':
        student.delete()
        return redirect('student_list')

    return render(request, 'delete.html',{'student':student})




        



        

