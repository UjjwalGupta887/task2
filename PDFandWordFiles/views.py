from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views.generic.edit import FormView, CreateView
from django.template import RequestContext
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .models import WordFiles
from .models import WordFiles_Attachment
from django.conf import settings
import os




def Upload(request):
    #if request is get request
    if request.method=='GET':
        return render(request,"dynamic.html",{})
    #if request is post request
    if request.method=='POST':
        obj=WordFiles.objects.create()

        val=(request.FILES.getlist("uploadfiles[]"))
        print(len(val))
        obj.Title=request.POST["Title"]
        obj.Description=request.POST["Description"]
        obj.save();
        #Create WordFiles object and use it id as foreign key in WordFiles_Attachment
        print(obj.id)
        for i in val:
            name=i.name
            path = default_storage.save(name, ContentFile(i.read()))
            j=WordFiles_Attachment.objects.create(key=obj,file=path)
            _,extension = os.path.splitext(path)
            if(extension.lower()!='.pdf'):
                os.system("pwd")
                os.system("unoconv -f pdf "+"media/"+path)
        v=list(map(lambda x: ( "../media/"+x.file,       os.path.splitext("../../media/"+x.file)[0]+".pdf"),WordFiles_Attachment.objects.filter(key_id=obj.id)))
        #return data for visualization
        return render(request,'word.html',{'Title':obj.Title,'Description':obj.Description,"path_ori":v})
