from datetime import datetime


def year(request):
    dt = datetime.now().year
    """Добавляет переменную с текущим годом."""
    return {
        'year': dt
    }
