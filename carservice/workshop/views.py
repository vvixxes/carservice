from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Service, Mechanic, Box, CarRepairBooking, Client


def book_repair(request):
    """Запись клиента на услугу ремонта с учётом занятости боксов и мастеров."""
    services = Service.objects.all()
    mechanics = Mechanic.objects.all()
    boxes = Box.objects.all()
    clients = Client.objects.all()

    if request.method == 'POST':
        client_id = request.POST.get('client_id')
        if not client_id or not Client.objects.filter(id=client_id).exists():
            messages.error(request, 'Неверный идентификатор клиента.')
            return redirect('book_repair')

        service_id = request.POST.get('service_id')
        if not service_id or not Service.objects.filter(id=service_id).exists():
            messages.error(request, 'Неверный идентификатор услуги.')
            return redirect('book_repair')

        mechanic_id = request.POST.get('mechanic_id')
        if not mechanic_id or not Mechanic.objects.filter(id=mechanic_id).exists():
            messages.error(request, 'Неверный идентификатор мастера.')
            return redirect('book_repair')

        box_id = request.POST.get('box_id')
        if not box_id or not Box.objects.filter(id=box_id).exists():
            messages.error(request, 'Неверный идентификатор бокса.')
            return redirect('book_repair')

        booking_time = timezone.datetime.fromisoformat(request.POST['booking_time'])

        service = get_object_or_404(Service, id=service_id)
        duration = timedelta(minutes=service.duration)
        end_time = booking_time + duration

        box = get_object_or_404(Box, id=box_id)
        if CarRepairBooking.objects.filter(
            box=box,
            booking_time__lt=end_time,
            booking_time__gte=booking_time
        ).count() >= box.available_spots:
            messages.error(request, 'Все места в боксе заняты на выбранное время.')
            return render(request, 'repair/book_repair.html', {
                'services': services,
                'mechanics': mechanics,
                'boxes': boxes,
                'clients': clients,
                'current_time': timezone.now().isoformat(),
            })

        if CarRepairBooking.objects.filter(
            mechanic_id=mechanic_id,
            booking_time__lt=end_time,
            booking_time__gte=booking_time
        ).exists():
            messages.error(request, 'Этот мастер уже занят в выбранное время.')
            return render(request, 'workshop/book_repair.html', {
                'services': services,
                'mechanics': mechanics,
                'boxes': boxes,
                'clients': clients,
                'current_time': timezone.now().isoformat(),
            })

        client = get_object_or_404(Client, id=client_id)
        mechanic = get_object_or_404(Mechanic, id=mechanic_id)
        CarRepairBooking.objects.create(
            client=client,
            service=service,
            mechanic=mechanic,
            box=box,
            booking_time=booking_time
        )

        messages.success(request, 'Клиент успешно записан!')
        return render(request, 'workshop/book_repair.html', {
            'services': services,
            'mechanics': mechanics,
            'boxes': boxes,
            'clients': clients,
            'current_time': timezone.now().isoformat(),
        })

    return render(request, 'workshop/book_repair.html', {
        'services': services,
        'mechanics': mechanics,
        'boxes': boxes,
        'clients': clients,
        'current_time': timezone.now().isoformat(),
    })


def schedule(request):
    """Просмотр расписания ремонтных работ."""
    bookings = CarRepairBooking.objects.select_related('client', 'service', 'mechanic', 'box').order_by('booking_time')
    return render(request, 'workshop/schedule.html', {'bookings': bookings})
