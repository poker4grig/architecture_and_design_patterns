from storage.views import Index, About, Watch, Contacts

urls = {
    '/': Index(),
    '/about/': About(),
    '/watch/': Watch(),
    '/contacts/': Contacts()
}
