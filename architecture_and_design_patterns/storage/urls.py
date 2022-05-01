from storage.views import Index, About, Watch, Contacts, SeriesList, \
    SeriesSchedule, CreateSeries, CreateCategory, CategoryList, CopySeries


urls = {
    '/': Index(),
    '/about/': About(),
    '/watch/': Watch(),
    '/contacts/': Contacts(),
    '/series-list/': SeriesList(),
    '/series-schedule/': SeriesSchedule(),
    '/create-series/': CreateSeries(),
    '/create-category/': CreateCategory(),
    '/category-list/': CategoryList(),
    '/copy-series/': CopySeries()
}
