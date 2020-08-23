from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import render,redirect


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('<h2>Welcome to the Hypercar Service!</h2>')


class TicketView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/tickets.html')


service_line = {
    'change_oil': [],
    'inflate_tires': [],
    'diagnostic': [],
}

ticket_number = 0


def check_time(request, service):
    if service == 'change_oil':
        global wait_time
        wait_time = len(service_line['change_oil']) * 2
    elif service == 'inflate_tires':
        wait_time = len(service_line['change_oil']) * 2 + len(service_line['inflate_tires']) * 5
    elif service == 'diagnostic':
        wait_time = len(service_line['change_oil']) * 2 + len(service_line['inflate_tires']) * 5 + len(
            service_line['diagnostic']) * 30
    global ticket_number
    ticket_number += 1
    service_line[service].append(ticket_number)
    context = {'ticket': ticket_number, 'time': wait_time}
    return render(request, 'tickets/service.html', context)


class ProcessView(View):
    def get(self, request, *args, **kwargs):
        service_queue = {
            'change_oil': len(service_line['change_oil']),
            'inflate_tires': len(service_line['inflate_tires']),
            'diagnostic': len(service_line['diagnostic']),
        }
        return render(request, 'tickets/processing.html', service_queue)

    def post(self, request, *args, **kwargs):
        if len(service_line['change_oil']) > 0:
            del service_line['change_oil'][0]

        elif len(service_line['inflate_tires']) > 0:
            del service_line['inflate_tires'][0]

        elif len(service_line['diagnostic']) > 0:
            del service_line['diagnostic'][0]
        return redirect(next)


def next(request):
    if all(len(service_line[i]) == 0 for i in service_line):
        ticket = 'Waiting for the next client'

    if len(service_line['change_oil']) >= 1:
        ticket = f"Next ticket #{service_line['change_oil'][0]}"
    elif len(service_line['inflate_tires']) >= 1:
        ticket = f"Next ticket #{service_line['inflate_tires'][0]}"
    elif len(service_line['diagnostic']) >= 1:
        ticket = f"Next ticket #{service_line['diagnostic'][0]}"

    context = {'ticket': ticket}
    return render(request, 'tickets/next.html', context)
