import events
from accounts import serializers
import random
import accounts
from accounts.models import Account
from django.shortcuts import render
from events.models import Event
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from registration.models import TeamMember, TeamStatus
from registration.serializers import TeamMemberSerializer


def index(request):
    return render(request, "accounts/base.html")


class TeamRegistrationViewSet(ModelViewSet):
    serializer_class = TeamMemberSerializer
    queryset = TeamMember.objects.all()

    def create(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            account_id = serializer.data.get("account")
            event_id = serializer.data.get("event")
            team_code = serializer.data.get("team_code")

            try:
                TeamMember.objects.get(account=account_id, event=event_id)
                return Response(
                    {"Error": f"{account_id} already registered to the event"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            except TeamMember.DoesNotExist:
                account = Account.objects.get(id=account_id)
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
                            team_member.save()
                            reg_team.current_size += 1

                            if reg_team.current_size == reg_team.event.team_size:
                                reg_team.is_full = True
                            reg_team.save()
                            return Response(
                                {
                                    "Success": f"{account_id} added to team with code {team_code}"
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
                    team = TeamStatus(event=event, team_code=team_code)
                    if event.team_size == 1:
                        team.is_full = True
                    team.save()

                    team_member = TeamMember.objects.create(
                        account=account, event=event, team=team
                    )
                    team_member.save()
                return Response(
                    {"Team Code": team_code},
                    status=status.HTTP_201_CREATED,
                )
        else:
            return Response(
                {"error": "Invalid Request"}, status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, *args, **kwargs):

        try:
            team_member = TeamMember.objects.get(id = kwargs.get("pk"))
            team = team_member.team
            team.current_size -= 1
            if team.current_size == 0:
                team.delete()
            else :
                team.is_full = False
                team.save()
                team_member.delete()
            return Response(
                {"Success": "De registered from " + team.event.title}, status=status.HTTP_204_NO_CONTENT
            )
        except TeamMember.DoesNotExist:
            return Response(
                {"error": "Given user is not registered to the event"}, status=status.HTTP_400_BAD_REQUEST 
            )