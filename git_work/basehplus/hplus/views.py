from django.shortcuts import render, render_to_response


# Create your views here.
def main(request):
    return render_to_response("base/main.html")


def index(request):
    return render_to_response("base/index.html")


def index01(request):
    return render_to_response("index/index01.html")


def index02(request):
    return render_to_response("index/index02.html")


def index03(request):
    return render_to_response("index/index03.html")


def echarts(request):
    return render_to_response("charts/echarts.html")


def flot(request):
    return render_to_response("charts/flot.html")


def morris(request):
    return render_to_response("charts/morris.html")


def metrics(request):
    return render_to_response("charts/metrics.html")


def emailbox(request):
    return render_to_response("email/emailbox.html")


def mail_detail(request):
    return render_to_response("email/mail_detail.html")


def mail_compose(request):
    return render_to_response("email/mail_compose.html")


def clients(request):
    return render_to_response("pages/clients.html")


def contacts(request):
    return render_to_response("pages/contacts.html")


def profile(request):
    return render_to_response("pages/profile.html")


def projects(request):
    return render_to_response("pages/projects.html")


def project_detail(request):
    return render_to_response("pages/project_detail.html")


def teams_board(request):
    return render_to_response("pages/teams_board.html")


def table_basic(request):
    return render_to_response("tables/table_basic.html")


def table_bootstrap(request):
    return render_to_response("tables/table_bootstrap.html")
