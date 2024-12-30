from django.shortcuts import render
from django.http import JsonResponse, FileResponse
from .models import MediaFile
import os


def handle_media(request):
    if request.method == 'POST':
        files = request.FILES.getlist('files')
        if len(files) > 10:
            return JsonResponse({'error': 'Cannot upload more than 10 files'}, status=400)

        for file in files:
            if not validate_file(file):
                return JsonResponse({'error': f'File size must be between 100KB to 10MB'}, status=400)

            category = get_file_category(file.name)
            MediaFile.objects.create(
                file=file,
                name=file.name,
                size=file.size,
                file_type=file.name.split('.')[-1],
                category=category
            )
        return JsonResponse({'message': 'Upload successful'})

    elif request.method == 'DELETE':
        file_id = request.GET.get('id')
        try:
            file = MediaFile.objects.get(id=file_id)
            file.delete()
            return JsonResponse({'message': 'File deleted'})
        except MediaFile.DoesNotExist:
            return JsonResponse({'error': 'File not found'}, status=404)

    elif request.method == 'GET' and 'download' in request.GET:
        try:
            file = MediaFile.objects.get(id=request.GET['download'])
            return FileResponse(file.file, as_attachment=True)
        except MediaFile.DoesNotExist:
            return JsonResponse({'error': 'File not found'}, status=404)

    files = MediaFile.objects.all().order_by('-uploaded_at')
    return render(request, 'media/index.html', {'files': files})


def validate_file(file):
    # Size validation (100KB - 10MB)
    min_size = 100 * 1024
    max_size = 10 * 1024 * 1024
    if not (min_size <= file.size <= max_size):
        return False

    # Extension validation
    valid_extensions = ['mp3', 'mp4', 'jpeg', 'png', 'gif']
    extension = file.name.split('.')[-1].lower()
    return extension in valid_extensions


def get_file_category(filename):
    ext = filename.split('.')[-1].lower()
    if ext == 'mp3':
        return 'AUDIO'
    elif ext == 'mp4':
        return 'VIDEO'
    return 'IMAGE'
