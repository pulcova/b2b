from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, User
from users.models import Owner, Dealer, Retailer, Employee

class Command(BaseCommand):
    help = 'Create initial data for the app'

    def handle(self, *args, **options):
        # Create groups
        groups = ['dealer', 'owner', 'retailer', 'employee']
        for group_name in groups:
            Group.objects.get_or_create(name=group_name)

        # Create users and assign them to groups
        users = [
            {'username': 'user1', 'password': 'password1', 'group': 'dealer'},
            {'username': 'user2', 'password': 'password2', 'group': 'owner'},
            {'username': 'user3', 'password': 'password3', 'group': 'retailer'},
            {'username': 'user4', 'password': 'password4', 'group': 'employee'},
        ]
        for user_data in users:
            user = User.objects.create_user(user_data['username'], password=user_data['password'])
            group = Group.objects.get(name=user_data['group'])
            user.groups.add(group)

        # Create an Employee and a Dealer and assign them to users
        employee_user = User.objects.get(username='user4')
        Employee.objects.create(user=employee_user, first_name='Employee', last_name='User')

        dealer_user = User.objects.get(username='user1')
        Dealer.objects.create(user=dealer_user, first_name='Dealer', last_name='User')

        # Create an Owner and a Retailer and assign them to users
        owner_user = User.objects.get(username='user2')
        Owner.objects.create(user=owner_user, first_name='Owner', last_name='User')

        retailer_user = User.objects.get(username='user3')
        Retailer.objects.create(user=retailer_user, first_name='Retailer', last_name='User')