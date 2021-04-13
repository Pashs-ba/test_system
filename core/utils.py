from django.core.files.uploadedfile import InMemoryUploadedFile


def upload_file(file: InMemoryUploadedFile):
    with open('users/{}'.format(file.name), 'wb') as f:
        for i in file.chunks():
            f.write(i)