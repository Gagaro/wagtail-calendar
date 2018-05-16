def get_page_event_data(page):
    """
    This return the data for the fullcalendar event.
    It should be the same for a given page whatever the context is.
    """
    # This can be customized by type by adding a `get_page_event_data` method on the model
    if hasattr(page, 'get_page_event_data'):
        return page.get_page_event_data()
    return {
        'type': 'page',
        'pk': page.pk,
        'author': str(page.owner),
        'description': page.search_description,  # description can be HTML to allow more customization of the popup
        'status': page.status_string,
    }
