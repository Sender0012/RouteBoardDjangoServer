from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Route, RoutePoint, BackgroundImage, GameBoard, Path
from .forms import RegisterForm, RouteForm, RoutePointForm, GameBoardForm
import json

# --- Rejestracja ---
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

# --- Dashboard z listą tras użytkownika ---
@login_required
def dashboard(request):
    routes = Route.objects.filter(user=request.user)
    return render(request, 'routes/dashboard.html', {'routes': routes})

# --- Tworzenie nowej trasy ---
@login_required
def create_route(request):
    if request.method == 'POST':
        form = RouteForm(request.POST)

        if form.is_valid() and form.data['name'] != '':
            route = form.save(commit=False)
            route.user = request.user
            route.save()
            return redirect('route_detail', route_id=route.id)
    else:
        form = RouteForm()
    return render(request, 'routes/create_route.html', {'form': form})

# --- Szczegóły trasy + punkty ---
@login_required
def route_detail(request, route_id):
    route = get_object_or_404(Route, id=route_id, user=request.user)
    points = route.points.all()
    background = route.background
    return render(request, 'routes/route_detail.html', {
        'route': route,
        'points': points,
        'background': background,
    })

# --- Dodawanie punktów do trasy ---
@login_required
def add_point(request, route_id):
    route = get_object_or_404(Route, id=route_id, user=request.user)
    if request.method == 'POST':
        form = RoutePointForm(request.POST)
        if form.is_valid():
            point = form.save(commit=False)
            point.route = route
            point.order = route.points.count() + 1
            point.save()
            return redirect('route_detail', route_id=route.id)
    else:
        form = RoutePointForm()
    return render(request, 'routes/add_point.html', {'form': form, 'route': route})

# --- Usuwanie punktów ---
@login_required
def delete_point(request, route_id, point_id):
    route = get_object_or_404(Route, id=route_id, user=request.user)
    point = get_object_or_404(RoutePoint, id=point_id, route=route)
    if request.method == 'POST':
        point.delete()
        return redirect('route_detail', route_id=route.id)
    return render(request, 'routes/confirm_delete_point.html', {'point': point, 'route': route})
## --- BOARD GAME --- ##

@login_required
def gameboard_list(request):
    boards = GameBoard.objects.all()
    return render(request, 'game/gameboard_list.html', {'boards': boards})

@login_required
def gameboard_create(request):
    if request.method == 'POST':
        form = GameBoardForm(request.POST)
        if form.is_valid():
            board = form.save(commit=False)
            board.user = request.user
            board.dots = json.loads(request.POST.get('dots', '[]'))
            board.save()
            boards = GameBoard.objects.all()
            return render(request, 'game/gameboard_list.html', {'boards': boards})
        return JsonResponse({'success': False, 'error': form.errors.as_json()})
    else:
        form = GameBoardForm()
    return render(request, 'game/create_board.html', {'form': form})

@login_required
def gameboard_update(request, board_id):
    board = get_object_or_404(GameBoard, pk=board_id)
    user = request.user

    path, created = Path.objects.get_or_create(user=user, board=board)

    # handles the paths sent by the post request
    if request.method == "POST":
        path.lines = json.loads(request.POST.get("lines", "[]"))
        path.save()
        return redirect('gameboard_update', board_id=board.id)

    return render(request, 'game/edit_path.html', {
        'board': board,
        'path': path,
        'initial_lines': json.dumps(path.lines),
    })


@login_required
def gameboard_delete(request, pk):
    board = get_object_or_404(GameBoard, pk=pk, user=request.user)
    if request.method == 'POST':
        board.delete()
        return redirect('gameboard_list')
    return render(request, 'game/gameboard_confirm_delete.html', {'board': board})
# def create_board_view(request):
#     return render(request, 'game/create_board.html')

# @require_POST
# @login_required()
# def save_board_view(request):
#     data = json.loads(request.body)
#     board = GameBoard.objects.create(
#         user=request.user,
#         title=data['title'],
#         rows=data['rows'],
#         cols=data['cols']
#     )
#     dots = [Dot(board=board, row=dot['row'], col=dot['col'], color=dot['color']) for dot in data['dots']]
#     Dot.objects.bulk_create(dots)
#     return JsonResponse({'status': 'ok'})