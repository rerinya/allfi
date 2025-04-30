from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from allfi.models import Video
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import loader
from tmdbv3api import TMDb
from tmdbv3api import Movie

#request tiene la info de sesion de usuario
#comprueba POST si tiene permiso o no
#templates puede crear plantillas
#codigos largos, puede crear funciones y llamarlo
user = None
operation = False
login_e = False


def index(request):
    template = loader.get_template("allfi/index.html")
    return HttpResponse(template.render())


# ------------------------------------------------------------------------------------


def do_login(request):
    global user
    global login_e
    if request.method == "GET":
        context = {"incorrecto": ""}
        return render(request, "allfi/login.html", context)
    elif request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            login_e = True
            return redirect("login_error")

    return HttpResponse("nothing")


# ------------------------------------------------------------------------------------

@login_required(login_url="login")
def do_logout(request):
    global user
    logout(request)
    user = None
    return redirect("index")


# ------------------------------------------------------------------------------------


def login_error(request):
    global login_e
    if login_e:
        login_e = False
        template = loader.get_template("allfi/login_error.html")
        return HttpResponse(template.render())
    else:
        return redirect("login")


# ------------------------------------------------------------------------------------


@login_required(login_url="login")
def home(request):
    if request.method == "GET":
        all_video = Video.objects.all()
        list_all = list(all_video)
        nuevos = []
        i = len(list_all) - 1
        while len(nuevos) < 6:
            nuevos.append(list_all[i])
            i = i - 1
        context = {
            "nuevo1_id": nuevos[0].id,
            "nuevo1_img": nuevos[0].urlposter,
            "nuevo1_name": nuevos[0].name,
            "nuevo2_id": nuevos[1].id,
            "nuevo2_img": nuevos[1].urlposter,
            "nuevo2_name": nuevos[1].name,
            "nuevo3_id": nuevos[2].id,
            "nuevo3_img": nuevos[2].urlposter,
            "nuevo3_name": nuevos[2].name,
            "nuevo4_id": nuevos[3].id,
            "nuevo4_img": nuevos[3].urlposter,
            "nuevo4_name": nuevos[3].name,
            "nuevo5_id": nuevos[4].id,
            "nuevo5_img": nuevos[4].urlposter,
            "nuevo5_name": nuevos[4].name,
            "nuevo6_id": nuevos[5].id,
            "nuevo6_img": nuevos[5].urlposter,
            "nuevo6_name": nuevos[5].name,
            "ciencia": "Ciencia Ficción",
            "misterio": "Misterio",
            "crimen": "Crimen",
            "suspense": "Suspense",
            "terror": "Terror",
            "aventura": "Aventura",
            "fantasia": "Fantasía",
            "romance": "Romance",
            "animacion": "Animación",
            "drama": "Drama",
            "comedia": "Comedia",
            "accion": "Acción"
        }
        return render(request, "allfi/home.html", context)
    elif request.method == "POST" and 'searchbutton' in request.POST and request.POST["searchtext"]:
        searchtext = request.POST["searchtext"]
        return redirect("search/" + searchtext)
    return redirect("home")


# ------------------------------------------------------------------------------------


@login_required(login_url="login")
def movie(request, id):
    try:
        video_found = Video.objects.get(id=id)

        actor_list = []
        actor = ""
        for m in video_found.actor:
            if m == ';':
                actor_list.append(actor)
                actor = ""
            else:
                actor = actor + m
        if actor != "":
            actor_list.append(actor)

        gen = ""
        for g in video_found.genres:
            if g == '/':
                break
            gen = gen + g
        filtered_video = Video.objects.filter(genres__icontains=gen)
        recommend_list = list(filtered_video)
        for m in recommend_list:
            if id == m.id:
                recommend_list.remove(video_found)
                break
        all_video = Video.objects.all()
        list_all = list(all_video)
        i = 0
        while len(recommend_list) < 6:
            index_re = 0
            for m in recommend_list:
                if list_all[i].id == m.id:
                    i = i + 1
                    break
                index_re = index_re + 1
            if index_re == len(recommend_list) and id != list_all[i].id:
                recommend_list.append(Video.objects.get(id=list_all[i].id))
            i = i + 1

        context = {
            "title": video_found.name,
            "valoración": video_found.score,
            "descripción": video_found.description,
            "tipo": video_found.genres,
            "año": video_found.year,
            "director": video_found.director,
            "actor_list": actor_list,
            "poster": video_found.urlposter,
            "urlbackdrop": video_found.urlbackdrop,
            "playid": id,
            "recomendato1_id": recommend_list[0].id,
            "recomendado1_img": recommend_list[0].urlposter,
            "recomendado1_name": recommend_list[0].name,
            "recomendato2_id": recommend_list[1].id,
            "recomendado2_img": recommend_list[1].urlposter,
            "recomendado2_name": recommend_list[1].name,
            "recomendato3_id": recommend_list[2].id,
            "recomendado3_img": recommend_list[2].urlposter,
            "recomendado3_name": recommend_list[2].name,
            "recomendato4_id": recommend_list[3].id,
            "recomendado4_img": recommend_list[3].urlposter,
            "recomendado4_name": recommend_list[3].name,
            "recomendato5_id": recommend_list[4].id,
            "recomendado5_img": recommend_list[4].urlposter,
            "recomendado5_name": recommend_list[4].name,
            "recomendato6_id": recommend_list[5].id,
            "recomendado6_img": recommend_list[5].urlposter,
            "recomendado6_name": recommend_list[5].name
        }
        return render(request, "allfi/movie_intro.html", context)
    except Video.DoesNotExist:
        context = {"sol": "Video no existe"}
        return render(request, "allfi/sol_operation.html", context)


# ------------------------------------------------------------------------------------


@login_required(login_url="login")
def play(request, id):
    try:
        video_found = Video.objects.get(id=id)
        context = {
            "title": video_found.name,
            "urlvideo": video_found.url,
            "urlbackdrop": video_found.urlbackdrop
        }
        return render(request, "allfi/movie.html", context)
    except Video.DoesNotExist:
        context = {"sol": "Video no existe"}
        return render(request, "allfi/sol_operation.html", context)


# ------------------------------------------------------------------------------------


@login_required(login_url="login")
# noinspection PyBroadException
def info_user(request):
    global operation
    if request.method == "GET":
        if user.has_perm('allfi.add_video'):
            user_list = User.objects.filter(groups__name="USER")
            context = {"username": user.username, "email": user.email, "user_list": user_list}
            return render(request, "allfi/admin.html", context)
        else:
            context = {"username": user.username, "email": user.email}
        return render(request, "allfi/user.html", context)
    elif request.method == "POST":
        operation = True
        if 'Submit_altauser' in request.POST:
            try:
                u = User.objects.create_user(request.POST["username"],
                                             request.POST["email"],
                                             request.POST["password"])
                us = User.objects.get(username=request.POST["username"])
                group = Group.objects.get(name="USER")
                us.groups.add(group)
                group.save()
                return redirect("sol_operation/6")
            except Exception as e:
                return redirect("sol_operation/7")

        elif 'Submit_moduser' in request.POST:
            username = request.POST["username"]
            cambiado = False
            try:
                u = User.objects.get(username=username)
                if request.POST["email"]:
                    cambiado = True
                    u.email = request.POST["email"]
                if request.POST["password"]:
                    cambiado = True
                    u.set_password(request.POST["password"])
                u.save()
                if cambiado:
                    return redirect("sol_operation/4")
                else:
                    return redirect("sol_operation/15")
            except User.DoesNotExist:
                return redirect("sol_operation/2")
            except Exception as e:
                return redirect("sol_operation/5")

        elif 'Submit_bajauser' in request.POST:
            username = request.POST["username"]
            try:
                u = User.objects.get(username=username)
                if u.has_perm('allfi.add_video'):
                    return redirect("sol_operation/18")
                else:
                    u.delete()
                    return redirect("sol_operation/1")
            except User.DoesNotExist:
                return redirect("sol_operation/2")
            except Exception as e:
                return redirect("sol_operation/3")

        elif 'Submit_subirpeli' in request.POST:
            v = Video(url=request.POST["url"])
            tmdb = TMDb()
            tmdb.api_key = '3d259872105fab96d72770a252b81ea0'
            tmdb.language = 'es'
            movie = Movie()
            search = movie.search(request.POST["name"])
            if len(search) == 0:
                return redirect("sol_operation/11")
            id = search[0].id
            d = movie.details(id)
            try:
                Video.objects.get(name=d.title)  # comprobar si el video ya existe en la bd
                return redirect("sol_operation/10")
            except Video.DoesNotExist:
                v.name = d.title
                c = movie.credits(id)
                if request.POST["description"]:
                    v.description = request.POST["description"]
                else:
                    v.description = d.overview
                if request.POST["year"]:
                    v.year = request.POST["year"]
                else:
                    v.year = search[0].release_date
                if request.POST["director"]:
                    v.director = request.POST["director"]
                else:
                    director = ""
                    for res in c.crew:
                        if res['job'] == "Director":
                            director = res['name']
                    v.director = director
                if request.POST["actor"]:
                    v.actor = request.POST["actor"]
                else:
                    try:
                        i = 0
                        pos = 0
                        while i < 3:
                            if c.cast[pos]['character'] != "" and c.cast[pos]['name'] != "":
                                v.actor = v.actor + c.cast[pos]['character'] + ": " + c.cast[pos]['name'] + ";"
                                i = i + 1
                            pos = pos + 1
                    # v.actor = c.cast[0]['character'] + ": " + c.cast[0]['name'] + ";" + c.cast[1]['character'] + ": " + \
                    #        c.cast[1]['name'] + ";" + c.cast[2]['character'] + ": " + c.cast[2]['name']
                    except IndexError:
                        return redirect("sol_operation/12")
                if request.POST["urlposter"]:
                    v.urlposter = request.POST["urlposter"]
                else:
                    if search[0].poster_path is None:
                        return redirect("sol_operation/12")
                    else:
                        v.urlposter = "https://image.tmdb.org/t/p/w500/" + search[0].poster_path
                if request.POST["urlbackdrop"]:
                    v.urlbackdrop = request.POST["urlbackdrop"]
                else:
                    if search[0].backdrop_path is None:
                        return redirect("sol_operation/12")
                    else:
                        v.urlbackdrop = "https://image.tmdb.org/t/p/w500/" + search[0].backdrop_path
                if request.POST["genres"]:
                    v.genres = request.POST["genres"]
                else:
                    genres = ''
                    i = 0
                    for res in d.genres:
                        if len(d.genres) == i + 1:
                            genres = genres + res['name']
                        else:
                            genres = genres + res['name'] + '/'
                        i = i + 1
                    v.genres = genres
                if request.POST["score"]:
                    v.score = request.POST["score"]
                else:
                    v.score = search[0].vote_average
                try:
                    v.save()
                    return redirect("sol_operation/8")
                except Exception as e:
                    return redirect("sol_operation/9")
        elif 'Submit_modpeli' in request.POST:
            cambiado = False
            try:
                video = Video.objects.get(name=request.POST["name"])  # comprobar si el video ya existe en la bd
                if request.POST["description"]:
                    cambiado = True
                    video.description=request.POST["description"]
                if request.POST["url"]:
                    cambiado = True
                    video.url=request.POST["url"]
                if request.POST["year"]:
                    cambiado = True
                    video.year=request.POST["year"]
                if request.POST["director"]:
                    cambiado = True
                    video.director=request.POST["director"]
                if request.POST["actor"]:
                    cambiado = True
                    video.actor=request.POST["actor"]
                if request.POST["urlposter"]:
                    cambiado = True
                    video.urlposter=request.POST["urlposter"]
                if request.POST["urlbackdrop"]:
                    cambiado = True
                    video.urlbackdrop=request.POST["urlbackdrop"]
                if request.POST["genres"]:
                    cambiado = True
                    video.genres=request.POST["genres"]
                if request.POST["score"]:
                    cambiado = True
                    video.score=request.POST["score"]
            except Video.DoesNotExist:
                return redirect("sol_operation/14")
            if cambiado:
                video.save()
                return redirect("sol_operation/16")
            else:
                return redirect("sol_operation/17")
        elif 'Submit_elimpeli' in request.POST:
            try:
                video = Video.objects.get(name=request.POST["name"])  # comprobar si el video ya existe en la bd
                video.delete()
                return redirect("sol_operation/13")
            except Video.DoesNotExist:
                return redirect("sol_operation/14")

    return redirect("home")


# ------------------------------------------------------------------------------------


@login_required(login_url="login")
def sol_operation(request, num):
    global operation
    if operation:
        res = {
            1: "Usuario eliminado",
            2: "Usuario no existe",
            3: "No ha conseguido eliminar el usuario",
            4: "Usuario modificado",
            5: "No ha conseguido modificar el usuario",
            6: "Usuario creado",
            7: "No ha conseguido crear el usuario, usuario ya existe",
            8: "Película subido",
            9: "No ha conseguido subir la película",
            10: "Película ya existe en la base de datos",
            11: "Película no encontrado en la API TMDb",
            12: "En la API no contiene información suficiente para subir la película",
            13: "Película eliminada",
            14: "Película no existe en la base de datos",
            15: "No se ha modificado nada respecto a los datos anteriores del usuario",
            16: "Película modificado",
            17: "No se ha modificado nada respecto a los datos anteriores de la película",
            18: "No se puede eliminar el superusuario o el administrador",
        }
        context = {"sol": res.get(num, None)}
        operation = False
        return render(request, "allfi/sol_operation.html", context)
    else:
        return redirect("home")


# ------------------------------------------------------------------------------------


@login_required(login_url="login")
def search(request, name):
    filtered_video = Video.objects.filter(name__icontains=name)
    list_video = list(filtered_video)
    if len(list_video) > 0:
        context = {"movie_list": list_video}
        return render(request, "allfi/search.html", context)
    else:
        context = {"nothing": "No hay nada"}
        return render(request, "allfi/search.html", context)


# ------------------------------------------------------------------------------------


@login_required(login_url="login")
def genre(request, name):
    filtered_video = Video.objects.filter(genres__icontains=name)
    set_video = list(filtered_video)
    i = 0
    list_video = []
    while i < len(set_video):
        six_video = []
        while len(six_video) < 3 and i < len(set_video):
            par_video = [set_video[i]]
            i = i + 1
            if i < len(set_video):
                par_video.append(set_video[i])
                i = i + 1
            six_video.append(par_video)
        list_video.append(six_video)
    if len(list_video) > 0:
        context = {"movie_list": list_video,
                   "ciencia": "Ciencia Ficción",
                   "misterio": "Misterio",
                   "crimen": "Crimen",
                   "suspense": "Suspense",
                   "terror": "Terror",
                   "aventura": "Aventura",
                   "fantasia": "Fantasía",
                   "romance": "Romance",
                   "animacion": "Animación",
                   "drama": "Drama",
                   "comedia": "Comedia",
                   "accion": "Acción",
                   "genero": name}
        return render(request, "allfi/genres.html", context)
    else:
        context = {"sol": "No hay películas del género introducido"}
        return render(request, "allfi/sol_operation.html", context)
