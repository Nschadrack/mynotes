from multiprocessing import context
from django.shortcuts import render
from setuptools import Require
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from .models import Note
from .serializers import NoteSerializer, MyTokenObtainPairSerializer, UserSeriliazer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView



@api_view(["GET"])
def getRoutes(request):
    routes = [
        {
            'Endpoint': '/notes/',
            'method': 'GET',
            'body': None,
            'description': 'Returns an array of notes'
        },
        {
            'Endpoint': '/notes/id',
            'method': 'GET',
            'body': None,
            'description': 'Returns a single note object'
        },
        {
            'Endpoint': '/notes/create/',
            'method': 'POST',
            'body': {'body': ""},
            'description': 'Creates new note with data sent in post request'
        },
        {
            'Endpoint': '/notes/id/update/',
            'method': 'PUT',
            'body': {'body': ""},
            'description': 'Creates an existing note with data sent in post request'
        },
        {
            'Endpoint': '/notes/id/delete/',
            'method': 'DELETE',
            'body': None,
            'description': 'Deletes and exiting note'
        },
    ]

    return Response(routes)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def getOrSaveNotes(request):
    """
        List all notes or create a new note
    """

    if request.method == "GET":
        user = request.user
        notes = user.note_set.all().order_by("-created")
        seriliazer = NoteSerializer(notes, many=True)
        return Response(seriliazer.data)
    elif request.method == "POST":
        data = request.data 
        seriliazer = NoteSerializer(data=data)
        if seriliazer.is_valid():
            note = seriliazer.save()
            note.user = request.user
            note.save()
            return Response(seriliazer.data, status=201)
        else:
            return Response(seriliazer.errors, status=400)
    else:
        return HttpResponse(status=405)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def getOrUpdateOrDeleteNote(request, pk):
    """
        Get single note, update an existing note or delete an existing note
    """
    try:
        note = Note.objects.get(pk=pk)
    except Note.DoesNotExist:
        return HttpResponse(status=404)
    

    if request.method == "GET":
        seriliazer = NoteSerializer(note, many=False)
        return Response(seriliazer.data, status=200)

    elif request.method == "PUT":
        seriliazer = NoteSerializer(note, data=request.data)
        if seriliazer.is_valid():
            seriliazer.save()
            return Response(seriliazer.data, status=205)
        return HttpResponse(status=400)

    elif request.method == "DELETE":
        note.delete()
        return HttpResponse(status=204)

  
    return HttpResponse(status=405)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(["POST"])
def register_user(request):
    data = request.data 
    seriliazer = UserSeriliazer(data=data)
    if seriliazer.is_valid():
        seriliazer.save()
        return Response(seriliazer.data, status=201)

    return Response(seriliazer.errors, status=400)
    

