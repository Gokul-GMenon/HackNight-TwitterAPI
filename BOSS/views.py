from builtins import print
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .forms import PositionForm
from .models import DataField
# Create your views here.

state = 0
acc = -1

def latest_fl(id):

    from api_calls import get_following as lt1

    import json
    dic_fol = json.loads(lt1.call(id))['data']
    
    from api_calls import get_followers as lt2
    import json
    dic_flw = json.loads(lt2.call(id))['data']
    # print("\nlatest - ",dic_flw,'\n')

    return {'follower': {'name': dic_fol[0]['name'], 'user': dic_fol[0]['username']}, 'following': {'name': dic_flw[0]['name'], 'user': dic_flw[0]['username']}}

def liked_tweets(id):
    
    from api_calls import latest_tweet as lt

    import json
    dic = json.loads(lt.call(id))['data']
    # print("\n\nliked - ",len(dic),"\n\n")

    return len(dic)
    

def latest(id):

    from api_calls import latest_tweet as lt

    import json
    dic = json.loads(lt.call(id))['data'][0]
    print("\n\n",dic,"\n\n")
    date = dic['created_at'][:10]
    time = dic['created_at'][11:-5]
    # print(time, '\n', date, '\n\n')
    return {'text':dic['text'], 'time': time,'date': date}

def liked(id):

    from api_calls import liked_tweets as lt

    import json
    dic = json.loads(lt.call(id))['data'][0]
    print("\n\n",dic,"\n\n")
    # date = dic['created_at'][:10]
    # time = dic['created_at'][11:-5]
    # print(time, '\n', date, '\n\n')
    # return {'text':dic['text'], 'time': time,'date': date}

    return dic['text']

def counter(name):

    from api_calls import tweet_counts as lt

    import json
    dic = json.loads(lt.call(name))['data']
    # print("\n\n",dic,"\n\n")

    c = 0
    lg = 0
    sum = 0
    for i in range(len(dic)):
        if lg < int(dic[i]['tweet_count']):
            lg = int(dic[i]['tweet_count'])
            c = i
        
        sum += dic[i]['tweet_count']

    return {'sum': sum, 'day': 7-c}
            


def core(request):
    
    lt = {'text': '', 'time':'', 'date':''}
    lk = ''
    n_liked = 0
    cnt = ''
    dic = {'follower': {'name': '', 'user': ''}, 'following': {'name': '', 'user': ''}}
    cnt == {'sum': '', 'day': ''}

    global acc, state
    acc+=1
    if(request.method == 'POST'):
        form = PositionForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            # print(name)
            from api_calls import id_return as id
            
            import json
            user_id = json.loads(id.call(name))['data'][0]
            
            print(user_id['id'])
            DataField.objects.all().delete()
            obj = DataField()
            obj.name = name
            obj.user_id = user_id['id']
            obj.save()
            state = 1

            return redirect('core')

    else:
        form  = PositionForm()

        if acc !=0:
            id = DataField.objects.last()
            lt = latest(id.user_id)
            lk = liked(id.user_id)
            cnt = counter(id.name)
            n_liked = liked_tweets(id.user_id)
            dic = latest_fl(id.user_id)


    return render(request, 'BOSS/index.html', {'state': state, 'form': form, 'lttx': lt['text'], 'ltt': lt['time'], 'ltd':lt['date'], 'lk': lk, 'sum': cnt['sum'], 'day': cnt['day'], 'liked': n_liked, 'nm_follower': dic['follower']['name'],'nm_following': dic['following']['name'], 'user_follower': dic['follower']['user'], 'user_following': dic['following']['user']})
