from decimal import Decimal, ROUND_HALF_UP

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db.models import Count, Sum, Case, When, Value, CharField
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse

from books.forms import BookForm
from books.models import Book


def custom_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "You need to log in first to access this page.")
            return redirect('login')
        return view_func(request, *args, **kwargs)

    return wrapper


class CustomLoginView(LoginView):
    template_name = 'login.html'


# Create your views here.
@custom_login_required
def base(request):
    return render(request, 'base.html')


@custom_login_required
def books_list(request):
    books = Book.objects.all()
    return render(request, 'books_list.html', {'books': books})


@custom_login_required
def dashboard(request):
    # Annotate each book with 'category_display', replacing empty or NULL categories with 'Uncategorized'
    category_stats = Book.objects.annotate(
        category_display=Case(
            When(category__isnull=True, then=Value('Uncategorized')),
            When(category='', then=Value('Uncategorized')),
            default='category',
            output_field=CharField(),
        )
    ).values('category_display').annotate(
        book_count=Count('id'),
        total_expense=Sum('distribution_expense')
    ).order_by('category_display')

    # Round the total_expense for each category
    for stat in category_stats:
        if stat['total_expense'] is not None:
            stat['total_expense'] = stat['total_expense'].quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        else:
            stat['total_expense'] = Decimal('0.00')

    # Calculate overall totals
    overall_total_books = Book.objects.count()
    overall_total_expense = Book.objects.aggregate(total=Sum('distribution_expense'))['total'] or Decimal('0.00')
    overall_total_expense = overall_total_expense.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    context = {
        'category_stats': category_stats,
        'overall_total_books': overall_total_books,
        'overall_total_expense': overall_total_expense,
    }
    return render(request, 'dashboard.html', context)


@custom_login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book added successfully!')
            return redirect('books_list')
    else:
        form = BookForm()
    return render(request, 'add_book.html', {'form': form})


@custom_login_required
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully!')
            return redirect('books_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'edit_book.html', {'form': form, 'book': book})


@custom_login_required
def delete_book(request, pk):
    if request.method == 'POST':  # Use POST instead of DELETE
        book = get_object_or_404(Book, pk=pk)
        book.delete()
        return JsonResponse({'message': 'Book deleted successfully!'})
    return JsonResponse({'error': 'Invalid request method.'}, status=400)


# Privacy Policy View
def privacy_policy(request):
    return render(request, 'privacy-policy.html')


# Terms of Service View
def terms_of_service(request):
    return render(request, 'terms-of-service.html')
