import random
import csv
from django.db.models.deletion import DO_NOTHING
import pandas as pd

from rest_framework.views import APIView

from accounts.authentication import MultipleTokenAuthentication
from accounts.models import Account
from django.shortcuts import render
from events.models import Event
from rest_framework import permissions, status
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from registration.models import TeamMember, TeamStatus
from registration.serializers import TeamMemberSerializer


def index(request):
    return render(request, "accounts/base.html")


class TeamRegistrationViewSet(ModelViewSet):
    serializer_class = TeamMemberSerializer
    queryset = TeamMember.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [MultipleTokenAuthentication, TokenAuthentication]
    http_method_names = ["post", "delete"]

    def list(self, request):
        raise MethodNotAllowed("GET", detail="Method 'GET' not allowed without lookup")

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(
                {"error": "Permission denied"}, status=status.HTTP_401_UNAUTHORIZED
            )
        account_id = request.data.get("account")
        event_id = request.data.get("event")
        team_code = request.data.get("team_code")

        try:
            account = Account.objects.get(id=account_id)
            if request.user == account.user:
                team_member = TeamMember.objects.get(account=account_id, event=event_id)
                print("Already registered")
                return Response(
                    {
                        "Error": f"{team_member.account.user.first_name}, you have already registered to the event!"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                print("Invalid token, user and token's user don't match")
                return Response(
                    {"error": "Invalid Token"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except TeamMember.DoesNotExist:
            account = Account.objects.get(id=account_id)

            # Check if the account is owned by the individual or he/she is an imposter
            if request.user == account.user:
                event = Event.objects.get(id=event_id)
                if team_code:
                    team_code = team_code.upper()
                    try:
                        reg_team = TeamStatus.objects.get(team_code=team_code)
                        if event_id != reg_team.event.id:
                            print("event id and dosen't match provided team code")
                            print(event_id)
                            print(reg_team.event.id)
                            return Response(
                                {"Error": "Invalid Team Code"},
                                status=status.HTTP_400_BAD_REQUEST,
                            )
                        if reg_team.current_size < event.team_size:
                            team_member = TeamMember.objects.create(
                                account=account, event=event, team=reg_team
                            )
                            reg_team.current_size += 1

                            # Check if the team is full or not
                            if reg_team.current_size == reg_team.event.team_size:
                                reg_team.is_full = True
                            reg_team.save()
                            return Response(
                                {
                                    "Success": f"{account.user.first_name} added to team with code {team_code}"
                                },
                                status=status.HTTP_201_CREATED,
                            )
                        else:
                            return Response(
                                {"Error": "The Team is full!"},
                                status=status.HTTP_406_NOT_ACCEPTABLE,
                            )
                    except TeamStatus.DoesNotExist:
                        print("\n")
                        print("No such team found")
                        print(team_code)
                        print("\n")
                        return Response(
                            {"Error": "Invalid Team Code"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                else:
                    while(True):
                        team_code = (
                            event.short_name + "#" + f"{random.randint(0, 100000)}".zfill(5)
                        )
                        if not TeamStatus.objects.filter(team_code=team_code).exists():
                            break
                    
                    team = TeamStatus.objects.create(event=event, team_code=team_code)
                    if event.team_size == 1:
                        team.is_full = True
                    team.save()

                    team_member = TeamMember.objects.create(
                        account=account, event=event, team=team
                    )
                    team_member.save()
                    return Response(
                        {"team_code": team_code},
                        status=status.HTTP_201_CREATED,
                    )

            else:
                print("Invalid token, user and token's user don't match")
                return Response(
                    {"error": "Invalid Token"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

    def destroy(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return Response(
                {"error": "Permission denied"}, status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            team_member = TeamMember.objects.get(id=kwargs.get("pk"))

            # Verify token with the team member token
            if request.user == team_member.account.user:
                team = team_member.team
                team.current_size -= 1
                if team.current_size == 0:
                    team.delete()
                else:
                    team.is_full = False
                    team.save()
                    team_member.delete()
                return Response(
                    {"Success": "Registration removed from " + team.event.title},
                    status=status.HTTP_204_NO_CONTENT,
                )

            else:
                print("Invalid token, user and token's user don't match")
                return Response(
                    {"error": "Invalid Token"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except TeamMember.DoesNotExist:
            print("User not registered to the event")
            return Response(
                {"error": "Given user is not registered to the event"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class CsvGenerate(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [MultipleTokenAuthentication, TokenAuthentication]
    
    def get(self, request, *args, **kwargs):

        if(request.user.is_superuser):
            pk = kwargs.get("pk")
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="btq.csv"'
            writer = csv.writer(response)

            try:
                event = Event.objects.get(pk=pk)
                teams = TeamStatus.objects.filter(event=event, is_full=True)
                writer.writerow(["Email Id", "First Name", "Last Name", "Mobile Number", "Institute", "Team Code", "Event"])
                for team in teams:
                    teammembers = TeamMember.objects.filter(team=team)
                    for teammember in teammembers:
                        writer.writerow(
                            [teammember.account.user.email, teammember.account.user.first_name, teammember.account.user.last_name,
                            teammember.account.mobile_number, teammember.account.institute, team.team_code, event.title])
                return response
            except Event.DoesNotExist:
                return Response(
                    {"Error": "No such event"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {"Error": "Access denied"},
                    status=status.HTTP_400_BAD_REQUEST
                )


class TeamData(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [BasicAuthentication]
  
    def get(self, request, *args, **kwargs):

        try:
            short_name = request.user.username
            event = Event.objects.get(short_name=short_name)
            teams = TeamStatus.objects.filter(event=event)
            data = []
            
            for team in teams:
                teammembers = TeamMember.objects.filter(team=team)
                for teammember in teammembers:
                    teammember_dict = {
                        "Email Id": teammember.account.user.email,
                        "First Name": teammember.account.user.first_name,
                        "Last Name": teammember.account.user.last_name,
                        "Mobile Number": teammember.account.mobile_number,
                        "Institute": teammember.account.institute,
                        "Team Code": team.team_code,    
                    }
                    data.append(teammember_dict)
            
            if len(data) == 0:
                df = pd.DataFrame(
                    data, 
                    columns=(["Email Id", "First Name", "Last Name", "Mobile Number", "Institute", "Team Code"]
                ))
            else:
                df = pd.DataFrame(data)
            
            response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response["Content-Disposition"] = "attachment; filename=participants.xlsx"
            df.to_excel(response)    
            return response
        
        except Event.DoesNotExist:
            return Response(
                {"Error": f"Access denied for {request.user.username}"},
                status=status.HTTP_400_BAD_REQUEST
            )
