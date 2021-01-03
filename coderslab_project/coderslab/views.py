from django.shortcuts import render, HttpResponse
from django.views import View
import math
from django.views.generic import ListView, TemplateView
from .models import Branch, PipeOrder
from .forms import PipeOrderForm, BranchFormSet, CreateUserForm
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

pipe_diameters = {'DN100': 101.6, 'DN80': 76.2, 'DN50': 50.8, 'DN25': 25.4}

class OrderListView(LoginRequiredMixin, TemplateView):
    template_name = 'coderslab/order_list.html'

    def get(self, *args, **kwargs):
        print(self.request.user.id)
        pipe_order = PipeOrder.objects.all().filter(customer=self.request.user.id)
        return self.render_to_response({'pipe_order' : pipe_order})

class OrderDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'coderslab/order_details.html'

    def get(self, request, order_id):
        order_customer_id = PipeOrder.objects.get(pk=order_id).customer.id
        logged_user_id = self.request.user.id
        if order_customer_id == logged_user_id:
            pipe_order = PipeOrder.objects.get(pk=order_id)
            branches = Branch.objects.all().filter(pipe_order=order_id)
            return self.render_to_response({'pipe_order' : pipe_order,'branches': branches})
        return redirect('coderslab-home')

# home page view
class HomeView(View):
    def get(self, request):
        return render(request, "coderslab/home.html")


# register view
class RegisterView(View):

    def get(self, request):
        form = CreateUserForm()
        context = {'form': form}
        return render(request, "coderslab/register.html", context)

    def post(self, request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + username)
            form.save()
            return redirect('login')
        context = {'form': form}
        return render(request, "coderslab/register.html", context)


class PipeConfiguratorView(LoginRequiredMixin, TemplateView):
    template_name = "coderslab/pipe_form.html"

    # def form_valid(self, form):
    #     form.instance.customer = self.request.user
    #     return super().form_valid(form)

    def get(self, *args, **kwargs):
        pipeform = PipeOrderForm()
        branch_formset = BranchFormSet(queryset=Branch.objects.none())
        return self.render_to_response({'branch_formset': branch_formset, 'pipeform': pipeform})

    # Define method to handle POST request
    def post(self, request):

        pipeform = PipeOrderForm(request.POST)
        branch_formset = BranchFormSet(data=request.POST)
        # Check if submitted forms are valid

        if branch_formset.is_valid() and pipeform.is_valid():

            # >>>>>>>>>>>>>>>>>>>>>

            section_type = request.POST.get('section_type')
            size = request.POST.get('size')
            wall_thk = request.POST.get('wall_thk')
            length = float(request.POST.get('length'))
            quantity = request.POST.get('quantity')
            material = request.POST.get('material')
            positions = []
            branch_sizes = []
            angles = []
            for form in branch_formset:
                positions.append(form.cleaned_data.get('position'))
                branch_sizes.append(form.cleaned_data.get('size'))
                angles.append(form.cleaned_data.get('angle'))
            print(positions)

            branch_id = []
            for i in range(1, len(positions) + 1):
                branch_id.append(i)

            # create branches list
            list_of_branches = list(zip(branch_id, positions, angles, branch_sizes))

            print(list_of_branches)

            # get pipe OD
            pipe_diameter = float(size)

            list_of_errors = []

            # branch size check

            for branch in list_of_branches:
                if branch[3] > pipe_diameter:
                    error = f'Branch {branch[0]} is bigger than pipe diameter'
                    list_of_errors.append({'error': error})
                    list_of_branches.remove(branch)

            # branch position check

            for branch in list_of_branches:
                if length - (branch[3] / 2 + 90) < branch[1]:
                    error = f'Branch {branch[0]} position is bigger than pipe lenght or its to close to edge.'
                    list_of_errors.append({'error': error})
                    list_of_branches.remove(branch)
            for branch in list_of_branches:
                if (branch[3] / 2 + 90) > branch[1]:
                    error = f'Branch {branch[0]} position is to close to edge.'
                    list_of_errors.append({'error': error})
                    list_of_branches.remove(branch)

            list_of_branches = tuple(list_of_branches)

            print(list_of_branches)

            # check branches and create list of errors

            for i in range(0, len(list_of_branches)):
                for k in range(i + 1, len(list_of_branches)):
                    if check_branch_pair(list_of_branches[i], list_of_branches[k], pipe_diameter):
                        name = str(i) + str(k)
                        list_of_errors.append(
                            {'error': check_branch_pair(list_of_branches[i], list_of_branches[k], pipe_diameter)})
            print(list_of_errors)
            if len(list_of_errors) > 0:
                return self.render_to_response(
                    {'branch_formset': branch_formset, 'pipeform': pipeform, 'list_of_errors': list_of_errors})

            # >>>>>>>>>>>>>>>>>>>>>
            pipe_order = pipeform.save(commit=False)
            pipe_order.customer = self.request.user
            pipe_order.save()
            for form in branch_formset:
                # extract name from each form and save
                angle = form.cleaned_data.get('angle')
                size = form.cleaned_data.get('size')
                position = form.cleaned_data.get('position')
                # save book instance
                Branch(pipe_order=pipe_order, size=size, position=position, angle=angle).save()
            # once all books are saved, redirect to book list view

            # pipe_order(customer=self.request.user).save()
            return redirect('order-list')


        return self.render_to_response({'branch_formset': branch_formset, 'pipeform': pipeform})


def check_branch_pair(branch_a, branch_b, pipe_diameter):
    # pipe radius
    pipe_radius = float(pipe_diameter) / 2
    # margin along pipe surface
    margin = 10

    # branch a parameters
    branch_a_radius = float(branch_a[3]) / 2
    branch_a_angle = math.radians(float(branch_a[2]))
    branch_a_position = float(branch_a[1])
    branch_a_alfa = math.asin(branch_a_radius / pipe_radius)
    branch_a_beta = (margin / pipe_radius) + branch_a_alfa
    branch_a_elipse_radius_1 = branch_a_radius + margin
    branch_a_elipse_radius_2 = pipe_radius * math.sin(branch_a_beta)
    branch_a_x_range = (branch_a_position - branch_a_elipse_radius_1, branch_a_position + branch_a_elipse_radius_1)

    # branch b parameters
    branch_b_radius = float(branch_b[3]) / 2
    branch_b_angle = math.radians(float(branch_b[2]))
    branch_b_position = float(branch_b[1])
    branch_b_alfa = math.asin(branch_b_radius / pipe_radius)
    branch_b_beta = (margin / pipe_radius) + branch_b_alfa
    branch_b_elipse_radius_1 = branch_b_radius + margin
    branch_b_elipse_radius_2 = pipe_radius * math.sin(branch_b_beta)
    branch_b_x_range = (branch_b_position - branch_b_elipse_radius_1, branch_b_position + branch_b_elipse_radius_1)
    x_overlap = (max(branch_a_x_range[0], branch_b_x_range[0]), min(branch_a_x_range[1], branch_b_x_range[1]))

    if x_overlap[1] > x_overlap[0]:

        i = x_overlap[0]

        while i < x_overlap[1]:
            # branch a intersection equation
            elipse_a_y_of_t = math.sqrt(branch_a_elipse_radius_2 ** 2 - (branch_a_elipse_radius_2 ** 2 /
                                                                         branch_a_elipse_radius_1 ** 2) * (
                                                i - branch_a_position) ** 2)
            elipse_a_z_of_t = math.sqrt(
                pipe_radius ** 2 - branch_a_elipse_radius_2 ** 2 + (branch_a_elipse_radius_2 ** 2 /
                                                                    branch_a_elipse_radius_1 ** 2) * (
                        i - branch_a_position) ** 2)

            # branch a points for t
            elipse_a_yn1 = elipse_a_z_of_t * math.sin(branch_a_angle) + elipse_a_y_of_t * math.cos(branch_a_angle)
            elipse_a_zn1 = elipse_a_z_of_t * math.cos(branch_a_angle) - elipse_a_y_of_t * math.sin(branch_a_angle)
            elipse_a_zn2 = elipse_a_z_of_t * math.cos(branch_a_angle) + elipse_a_y_of_t * math.sin(branch_a_angle)
            elipse_a_yn2 = elipse_a_z_of_t * math.sin(branch_a_angle) - elipse_a_y_of_t * math.cos(branch_a_angle)

            # branch b intersection equation
            elipse_b_y_of_t = math.sqrt(branch_b_elipse_radius_2 ** 2 - (branch_b_elipse_radius_2 ** 2 /
                                                                         branch_b_elipse_radius_1 ** 2) * (
                                                i - branch_b_position) ** 2)
            elipse_b_z_of_t = math.sqrt(
                pipe_radius ** 2 - branch_b_elipse_radius_2 ** 2 + (branch_b_elipse_radius_2 ** 2 /
                                                                    branch_b_elipse_radius_1 ** 2) * (
                        i - branch_b_position) ** 2)

            # branch b points for t
            elipse_b_yn1 = elipse_b_z_of_t * math.sin(branch_b_angle) + elipse_b_y_of_t * math.cos(branch_b_angle)
            elipse_b_zn1 = elipse_b_z_of_t * math.cos(branch_b_angle) - elipse_b_y_of_t * math.sin(branch_b_angle)
            elipse_b_zn2 = elipse_b_z_of_t * math.cos(branch_b_angle) + elipse_b_y_of_t * math.sin(branch_b_angle)
            elipse_b_yn2 = elipse_b_z_of_t * math.sin(branch_b_angle) - elipse_b_y_of_t * math.cos(branch_b_angle)

            distence_a1_b1 = math.sqrt((elipse_a_yn1 - elipse_b_yn1) ** 2 + (elipse_a_zn1 - elipse_b_zn1) ** 2)
            distence_a1_b2 = math.sqrt((elipse_a_yn1 - elipse_b_yn2) ** 2 + (elipse_a_zn1 - elipse_b_zn2) ** 2)
            distence_a2_b1 = math.sqrt((elipse_a_yn2 - elipse_b_yn1) ** 2 + (elipse_a_zn2 - elipse_b_zn1) ** 2)
            distence_a2_b2 = math.sqrt((elipse_a_yn2 - elipse_b_yn2) ** 2 + (elipse_a_zn2 - elipse_b_zn2) ** 2)

            i += 0.05
            solution_delta = 0.5
            if -solution_delta < distence_a1_b1 < solution_delta or -solution_delta < distence_a1_b2 < solution_delta \
                    or -solution_delta < distence_a2_b1 < solution_delta or -solution_delta < distence_a2_b2 < solution_delta:
                return f'Branch {branch_a[0]} and branch {branch_b[0]} overlap or are too close'
        # check in one contains another

        if elipse_b_yn1 > elipse_a_yn1 and elipse_b_yn2 < elipse_a_yn2 and math.fabs(
                branch_a_angle - branch_b_angle) > math.pi / 2:
            return f'Branch {branch_a[0]} and branch {branch_b[0]} overlap'
        return None
    return None
