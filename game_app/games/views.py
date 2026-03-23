from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm, FizzBuzzForm, TicTacToeForm
from .models import PlayerProfile, GameScore
from . import services


def home(request):
    """
    Home page view.
    """
    return render(request, 'home.html')


def register_view(request):
    """
    User registration view.
    """
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = RegisterForm()
    
    return render(request, 'register.html', {'form': form})


def login_view(request):
    """
    User login view.
    """
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('home')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    """
    User logout view.
    """
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


@login_required
def fizzbuzz_game(request):
    """
    FizzBuzz game view.
    """
    # Initialize game if not in session
    if 'fizzbuzz_number' not in request.session:
        request.session['fizzbuzz_number'] = 1
        request.session['fizzbuzz_score'] = 0
    
    current_number = request.session['fizzbuzz_number']
    current_score = request.session['fizzbuzz_score']
    game_over_popup = request.session.pop('fizzbuzz_game_over_popup', None)
    
    if request.method == 'POST':
        form = FizzBuzzForm(request.POST)
        if form.is_valid():
            user_answer = form.cleaned_data['answer']
            
            # Validate answer
            if services.validate_fizzbuzz_answer(current_number, user_answer):
                # Correct answer
                request.session['fizzbuzz_score'] += 10
                request.session['fizzbuzz_number'] += 1
                messages.success(request, 'Correct! +10 points')
                return redirect('fizzbuzz_game')
            else:
                # Wrong answer - game over
                final_score = request.session['fizzbuzz_score']
                
                # Save score to database
                GameScore.objects.create(
                    user=request.user,
                    game_name='fizzbuzz',
                    score=final_score
                )
                
                # Update player profile
                profile = request.user.profile
                profile.total_score += final_score
                profile.games_played += 1
                profile.save()
                
                # Clear session
                del request.session['fizzbuzz_number']
                del request.session['fizzbuzz_score']

                request.session['fizzbuzz_game_over_popup'] = (
                    f'Game Over! Final score: {final_score}'
                )
                return redirect('fizzbuzz_game')
    else:
        form = FizzBuzzForm()
    
    context = {
        'form': form,
        'current_number': current_number,
        'current_score': current_score,
        'game_over_popup': game_over_popup,
    }
    return render(request, 'fizzbuzz.html', context)


@login_required
def fizzbuzz_reset(request):
    """
    Reset FizzBuzz game.
    """
    if 'fizzbuzz_number' in request.session:
        del request.session['fizzbuzz_number']
    if 'fizzbuzz_score' in request.session:
        del request.session['fizzbuzz_score']
    return redirect('fizzbuzz_game')


@login_required
def tictactoe_game(request):
    """
    TicTacToe game view.
    """
    # Initialize game if not in session
    if 'tictactoe_board' not in request.session:
        request.session['tictactoe_board'] = services.initialize_tictactoe_board()
        request.session['tictactoe_game_over'] = False
        request.session['tictactoe_winner'] = None
    
    board = request.session['tictactoe_board']
    game_over = request.session.get('tictactoe_game_over', False)
    winner = request.session.get('tictactoe_winner', None)

    def finalize_game(result):
        request.session['tictactoe_game_over'] = True
        request.session['tictactoe_winner'] = result

        score = 0
        if result == 'X':
            score = 50
            messages.success(request, 'You Win! +50 points')
        elif result == 'Draw':
            score = 10
            messages.info(request, 'Draw! +10 points')
        else:
            messages.error(request, 'You Lose!')

        GameScore.objects.create(
            user=request.user,
            game_name='tictactoe',
            score=score
        )

        profile = request.user.profile
        profile.total_score += score
        profile.games_played += 1
        profile.save()
    
    if request.method == 'POST' and not game_over:
        form = TicTacToeForm(request.POST)
        if form.is_valid():
            position = form.cleaned_data['position']
            
            # Validate and make player move
            if services.is_valid_move(board, position):
                board[position] = 'X'
                request.session['tictactoe_board'] = board
                
                # Check for winner after player move
                result = services.check_winner(board)
                if result:
                    finalize_game(result)
                else:
                    # Computer's turn (AI)
                    comp_position = services.tictactoe_move(board)
                    if comp_position is not None:
                        board[comp_position] = 'O'
                        request.session['tictactoe_board'] = board
                        
                        # Check for winner after computer move
                        result = services.check_winner(board)
                        if result:
                            finalize_game(result)
                
                return redirect('tictactoe_game')
    
    # Build indexed rows to simplify template rendering and move submission.
    board_with_index = list(enumerate(board))
    board_rows = [board_with_index[i:i+3] for i in range(0, 9, 3)]
    
    context = {
        'board_rows': board_rows,
        'game_over': game_over,
        'winner': winner
    }
    return render(request, 'tictactoe.html', context)


@login_required
def tictactoe_reset(request):
    """
    Reset TicTacToe game.
    """
    if 'tictactoe_board' in request.session:
        del request.session['tictactoe_board']
    if 'tictactoe_game_over' in request.session:
        del request.session['tictactoe_game_over']
    if 'tictactoe_winner' in request.session:
        del request.session['tictactoe_winner']
    return redirect('tictactoe_game')


def leaderboard(request):
    """
    Leaderboard view showing top players.
    """
    players = PlayerProfile.objects.select_related('user').order_by('-total_score')[:20]
    
    context = {
        'players': players
    }
    return render(request, 'leaderboard.html', context)
