import random

from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token

from events.models import Event
from accounts.models import Account
from registration.models import TeamMember, TeamStatus
from registration.serializers import TeamMemberSerializer


def index(request):
    return render(request, "accounts/base.html")


class TeamRegistrationViewSet(ModelViewSet):
    serializer_class = TeamMemberSerializer
    queryset = TeamMember.objects.all()
    authentication_classes = [TokenAuthentication]

    def create(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return Response(
                {"error": "Permission denied"}, status=status.HTTP_401_UNAUTHORIZED
            )
        account_id = request.data.get("account")
        event_id = request.data.get("event")
        team_code = request.data.get("team_code")

        try:
            team_member = TeamMember.objects.get(account=account_id, event=event_id)
            return Response(
                {"Error": f"{team_member.account.user.first_name} already registered to the event"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except TeamMember.DoesNotExist:
            account = Account.objects.get(id=account_id)

            # Check if the account is owned by the individual or he/she is an imposter
            if request.user == account.user:
                event = Event.objects.get(id=event_id)
                if team_code:
                    try:
                        reg_team = TeamStatus.objects.get(team_code=team_code)
                        if event_id != reg_team.event.id:
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
                                {"Error": "The Team is full"},
                                status=status.HTTP_406_NOT_ACCEPTABLE,
                            )
                    except TeamStatus.DoesNotExist:
                        return Response(
                            {"Error": "Invalid Team Code"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                else:
                    team_code = (
                        event.short_name + "#" + f"{random.randint(0, 1000)}".zfill(3)
                    )
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
                return Response(
                    {"error": "Invalid Token"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except TeamMember.DoesNotExist:
            return Response(
                {"error": "Given user is not registered to the event"},
                status=status.HTTP_400_BAD_REQUEST,
            )
