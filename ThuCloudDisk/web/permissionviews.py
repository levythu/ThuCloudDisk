# This Python file uses the following encoding: utf-8from django.shortcuts import render_to_responsefrom django.http import HttpResponsefrom django import templatefrom django.views.decorators.csrf import csrf_protectfrom web.models import *@csrf_protectdef changePermission(request):    return render_to_response('permission.html', locals())# bucket permission settings@csrf_protect    def publicBucketDo(request):    if 'bucket' in request.GET:        bucket = request.GET['bucket']        ownerMail = 'chengls10@163.com'                if not bucket:            resultInfo = '请填写bucket'            return render_to_response('permission.html', locals())        else:            vbar = publicBucket.objects.filter(bucket = bucket)             if not vbar:                publicBucket.objects.create(ownerMail = ownerMail, bucket = bucket)                resultInfo = '设置公开成功'            else:                resultInfo = '该bucket已经设为公开'            return render_to_response('permission.html', locals())    else:        return render_to_response('permission.html', locals())        @csrf_protect          def publicBucketUndo(request):    if 'bucket' in request.GET:        bucket = request.GET['bucket']                if not bucket:            resultInfo = '请填写bucket'            return render_to_response('permission.html', locals())        else:            vbar = publicBucket.objects.filter(bucket = bucket)             if not vbar:                resultInfo = '该bucket未被公开'            else:                vbar.delete()                resultInfo = '取消公开成功'            return render_to_response('permission.html', locals())    else:        return render_to_response('permission.html', locals())# object permission settings@csrf_protect    def publicObjectDo(request):    if 'object' in request.GET:        object = request.GET['object']        ownerMail = 'chengls10@163.com'                if not object:            resultInfo = '请填写object'            return render_to_response('permission.html', locals())        else:            vbar = publicObject.objects.filter(object = object)             if not vbar:                publicObject.objects.create(ownerMail = ownerMail, object = object)                resultInfo = '设置公开成功'            else:                resultInfo = '该object已经设为公开'            return render_to_response('permission.html', locals())    else:        return render_to_response('permission.html', locals())@csrf_protect          def publicObjectUndo(request):    if 'object' in request.GET:        object = request.GET['object']                if not object:            resultInfo = '请填写object'            return render_to_response('permission.html', locals())        else:            vbar = publicObject.objects.filter(object = object)             if not vbar:                resultInfo = '该object未被公开'            else:                vbar.delete()                resultInfo = '取消公开成功'            return render_to_response('permission.html', locals())    else:        return render_to_response('permission.html', locals())@csrf_protect def shareObjectDo(request):    if 'object' in request.GET and 'sharerMail' in request.GET:        object = request.GET['object']        sharerMail = request.GET['sharerMail']        ownerMail = 'chengls10@163.com'                if not object or not sharerMail:            resultInfo = '请填写object和用户邮箱'            return render_to_response('permission.html', locals())        else:            mailTell = MyUser.objects.filter(email = sharerMail)            if not mailTell:                resultInfo = '该用户邮箱不存在'                return render_to_response('permission.html', locals())                    vbar = shareObject.objects.filter(object = object, sharerMail = sharerMail)            if not vbar:                shareObject.objects.create(object = object, sharerMail = sharerMail, ownerMail = ownerMail)                resultInfo = '设置该object对该用户公开成功'            else:                resultInfo = '该object已经对该用户公开'            return render_to_response('permission.html', locals())    else:        return render_to_response('permission.html', locals())@csrf_protect        def shareObjectUndo(request):    if 'object' in request.GET and 'sharerMail' in request.GET:        object = request.GET['object']        sharerMail = request.GET['sharerMail']                if not object or not sharerMail:            resultInfo = '请填写object和用户邮箱'            return render_to_response('permission.html', locals())        else:            mailTell = MyUser.objects.filter(email = sharerMail)            if not mailTell:                resultInfo = '该用户邮箱不存在'                return render_to_response('permission.html', locals())                        vbar = shareObject.objects.filter(object = object, sharerMail = sharerMail)            if not vbar:                resultInfo = '该object未对该用户公开'            else:                vbar.delete()                resultInfo = '取消该object对该用户的公开成功'            return render_to_response('permission.html', locals())    else:        return render_to_response('permission.html', locals())