from note_taking_app.views import signup, login, Create, NoteAPIView, share_note, HistoryView
from django.urls import path

urlpatterns = [
    path("login/", login),
    path("notes/create/", Create.as_view()),
    path("signup/", signup),
    path("notes/<int:note_id>/", NoteAPIView.as_view()),
    path("notes/share/", share_note),
    path("notes/version-history/<int:note_id>/", HistoryView.as_view())
]
